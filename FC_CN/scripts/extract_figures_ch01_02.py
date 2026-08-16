# -*- coding: utf-8 -*-
"""Extract ch1–ch2 figures from EN FC UG with tight crops."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "figures"
PDF = Path(
    r"d:\IC Design\VLSI\Fusion Compiler User Guide Version V-2023.12-SP3, May 2024.pdf"
)
DPI = 240  # higher clarity for print/PDF
ZOOM = DPI / 72.0
PAD_PT = 10.0  # keep labels from being clipped
TRIM_MARGIN_PX = 12

FIGURES = [
    ("fig-physyn-flow", 34, "Figure 1 Fusion Compiler Physical Synthesis Flow", "figure"),
    ("fig-formality-flow", 35, "following figure shows an overview of the design flow from the Fusion Compiler", "phrase"),
    ("fig-pnr-flow", 36, "Figure 2 Fusion Compiler Place and Route Flow", "figure"),
    ("fig-upf-flows", 40, "Figure 3 UPF-Prime (Traditional) and Golden UPF Flows", "figure"),
    ("fig-dp-example", 41, "Figure 4 Double-Patterning Example", "figure"),
    ("fig-odd-cycle", 42, "Figure 5 Odd-Cycle Violation", "figure"),
    ("fig-no-odd-cycle", 42, "Figure 6 No Odd-Cycle Violation", "figure"),
    ("fig-lib-config", 77, "as shown in the following figure:", "phrase"),
    ("fig-logic-hier", 79, "Figure 7 Logic Hierarchy of Design", "figure"),
    ("fig-fc-lib-analysis-flow", 84, "Figure 8 Library Analysis Flow", "figure"),
    ("fig-fc-lib-monotonic", 85, "Figure 9 Monotonic Distribution in Library Cell Family", "figure"),
    ("fig-fc-lib-redundant", 86, "Figure 10 Redundant Cell in Library Cell Family", "figure"),
    ("fig-fc-lib-outlier", 87, "Figure 11 Outlier Cell in Library Cell Family", "figure"),
    ("fig-fc-lib-equivalent", 88, "Figure 12 Equivalent Cells in Library Cell Family", "figure"),
    ("fig-fc-lib-gap", 89, "Figure 13 Gap in Library Cell Family", "figure"),
    ("fig-merge-va", 122, "Figure 14 Merging Voltage Area Shapes", "figure"),
    ("fig-nested-va", 123, "Figure 15 Nested Voltage Areas", "figure"),
    ("fig-va-guard", 125, "Figure 16 Voltage Area Guard Band", "figure"),
    ("fig-eff-bound", 126, "Figure 17 Effective Boundaries of Overlapping Voltage Areas", "figure"),
    ("fig-phys-ft", 128, "Figure 18 Physical-Feedthrough Nets of Voltage Areas", "figure"),
    ("fig-phys-ft-off", 128, "Figure 19 Physical-Feedthrough Nets Disabled for a Voltage Area", "figure"),
    ("fig-ft-buf-diff", 130, "Figure 20 Difference in the Logical View After Physical- and Logical-Feedthrough Buffering", "figure"),
    ("fig-clk-lat-cg", 306, "Figure 55 Clock Latency With Clock-Gating Design", "figure"),
    ("fig-cg-stages", 308, "Figure 56 Clock-Gating Stages and Latency Calculations", "figure"),
    ("fig-lat-fanout", 309, "Figure 57 Latency Calculations With Varying Fanout", "figure"),
    ("fig-keepout", 138, "Figure 21 Placement Keepout Margins", "figure"),
    ("fig-ch2b-ir-drop-categories", 160, "Figure 22 Default Cell Categories for IR-Drop-Aware Placement", "figure"),
    ("fig-ch2b-equiv-pin-loc", 165, "Figure 23 Equivalent Cells With Different Pin Locations", "figure"),
    ("fig-ch2b-equiv-pin-color", 166, "Figure 24 Equivalent Cells With Pins of Different Colors", "figure"),
    ("fig-ch2b-drc-disabled", 174, "Figure 25 DRC Disabled Clock and Constant Nets Highlighted", "figure"),
    ("fig-ch2b-port-isolation", 176, "Without port isolation", "port_iso"),
    ("fig-ch2b-multiport-nets", 177, "Feedthrough net Logically equivalent outputs", "art_above_label"),
    ("fig-ch2b-clock-net-types", 203, "Figure 27 Root, Internal, and Sink Clock Net Types", "figure"),
    ("fig-ch2b-root-fanout", 204, "Figure 28 Using a Fanout Limit for Selecting Root Nets", "figure"),
    ("fig-ch2b-level-ndr", 205, "Figure 29 Level-Based Clock Nondefault Routing Rule", "figure"),
]

CAPTION_RE = re.compile(r"^Figure\s+(\d+)\b")
BODY_START = re.compile(
    r"^(by default|to (prevent|specify|restrict|have|explicitly|perform|remove|use|create|define|enable|disable|rerun)|"
    r"when you|if you|for example|note:|an outer|you can|during |restricting |"
    r"formal verification|place and route|fixing multiple|multiple-port nets|"
    r"preserving pin|controlling |enabling |the following commands|"
    r"when calculating|specifying a smaller|fc_shell>)",
    re.I,
)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def page_caption_blocks(page: fitz.Page) -> list[tuple[fitz.Rect, str]]:
    out = []
    for b in page.get_text("blocks"):
        txt = norm(b[4])
        if CAPTION_RE.match(txt) and len(txt) < 200:
            rest = CAPTION_RE.sub("", txt, count=1).strip().lower()
            if rest.startswith(("shows ", "compares ", "illustrates ")):
                continue
            out.append((fitz.Rect(b[:4]), txt))
    out.sort(key=lambda x: x[0].y0)
    return out


def find_block_containing(page: fitz.Page, phrase: str) -> fitz.Rect | None:
    phrase_n = norm(phrase).lower()
    for b in page.get_text("blocks"):
        if phrase_n in norm(b[4]).lower():
            return fitz.Rect(b[:4])
    words = phrase.split()
    for n in range(min(8, len(words)), 2, -1):
        hits = page.search_for(" ".join(words[:n]))
        if hits:
            return hits[0]
    return None


def find_caption(page: fitz.Page, key: str) -> fitz.Rect:
    captions = page_caption_blocks(page)
    key_n = norm(key).lower()
    for r, txt in captions:
        if key_n in norm(txt).lower() or norm(txt).lower().startswith(key_n[:36]):
            return r
    m = re.match(r"Figure\s+(\d+)", key)
    if m:
        n = m.group(1)
        for r, txt in captions:
            if re.match(rf"Figure\s+{n}\b", txt):
                return r
    raise RuntimeError(f"caption not found: {key}")


def stop_y(page: fitz.Page, after_y: float) -> float:
    """End of figure band: next caption / section / long prose."""
    y = page.rect.height - 58
    for r, _ in page_caption_blocks(page):
        if r.y0 > after_y + 8:
            y = min(y, r.y0 - 6)
    for b in page.get_text("blocks"):
        if b[1] <= after_y + 25:
            continue
        t = norm(b[4])
        tl = t.lower()
        h = b[3] - b[1]
        # section-like headers
        if h < 28 and len(t) < 90 and not tl.startswith("figure "):
            if any(
                k in tl
                for k in (
                    "overview",
                    "preserving",
                    "fixing",
                    "controlling",
                    "enabling",
                    "defining",
                    "restricting",
                )
            ):
                y = min(y, b[1] - 6)
                continue
        if BODY_START.match(tl) or (len(t) > 90 and h > 28):
            # skip short in-figure labels
            if len(t) < 55 and h < 22:
                continue
            y = min(y, b[1] - 6)
    return y


def images_in_band(page: fitz.Page, y0: float, y1: float) -> fitz.Rect | None:
    rects = []
    for info in page.get_image_info(xrefs=True):
        r = fitz.Rect(info["bbox"])
        mid = 0.5 * (r.y0 + r.y1)
        if y0 - 2 <= mid <= y1 + 2 and r.height > 20:
            rects.append(r)
    if not rects:
        return None
    u = rects[0]
    for r in rects[1:]:
        u |= r
    return u


def drawings_in_band(page: fitz.Page, y0: float, y1: float) -> fitz.Rect | None:
    """Union drawing paths in band; drop page frames / chrome that span the column."""
    page_area = page.rect.width * page.rect.height
    band_h = max(1.0, y1 - y0)
    rects = []
    for d in page.get_drawings():
        rr = d.get("rect")
        if not rr:
            continue
        r = fitz.Rect(rr)
        if r.height < 1.2 or r.width < 1.2:
            continue
        if r.y1 < 55 or r.y0 > page.rect.height - 52:
            continue
        if r.width > page.rect.width * 0.70 and r.height < 6:
            continue
        if r.width > page.rect.width * 0.70 and r.height > max(220, 0.45 * band_h):
            continue
        if r.get_area() > 0.28 * page_area:
            continue
        mid = 0.5 * (r.y0 + r.y1)
        if y0 - 4 <= mid <= y1 + 4:
            rects.append(r)
    if not rects:
        return None
    u = rects[0]
    for r in rects[1:]:
        u |= r
    # soft clamp — keep a little room for strokes/labels near band edge
    u.y0 = max(u.y0, y0 - 6)
    u.y1 = min(u.y1, y1 + 6)
    return u


def is_figure_label(t: str) -> bool:
    """True for in-figure labels; False for body/commands/captions."""
    if not t:
        return False
    if CAPTION_RE.match(t) or BODY_START.match(t.lower()):
        return False
    if "fc_shell>" in t.lower():
        return False
    # long prose / notes
    if len(t) > 90:
        return False
    if t.count(" ") > 12 and len(t) > 60:
        return False
    return True


def labels_in_band(page: fitz.Page, y0: float, y1: float) -> list[fitz.Rect]:
    """All short labels fully inside the figure vertical band."""
    out = []
    for b in page.get_text("blocks"):
        t = norm(b[4])
        if not is_figure_label(t):
            continue
        br = fitz.Rect(b[:4])
        # require label center in band (avoids grabbing nearby body)
        mid = 0.5 * (br.y0 + br.y1)
        if y0 - 2 <= mid <= y1 + 2:
            out.append(br)
    return out


def pad(page: fitz.Page, r: fitz.Rect, p: float = PAD_PT) -> fitz.Rect:
    return fitz.Rect(
        max(55, r.x0 - p),
        max(50, r.y0 - p),
        min(page.rect.width - 40, r.x1 + p),
        min(page.rect.height - 50, r.y1 + p),
    )


def figure_clip(page: fitz.Page, y0: float, y1: float) -> fitz.Rect:
    """Prefer embedded image (+ nearby labels); else drawings + nearby labels."""
    img = images_in_band(page, y0, y1)
    labels = labels_in_band(page, y0, y1)

    if img is not None:
        u = fitz.Rect(img)
        # labels that touch a padded image box (captions under/over art)
        near = fitz.Rect(img.x0 - 36, img.y0 - 28, img.x1 + 36, img.y1 + 36)
        for br in labels:
            if near.intersects(br):
                u |= br
        u.y0 = max(u.y0, y0 - 2)
        u.y1 = min(u.y1, y1 + 2)
        return pad(page, u, PAD_PT)

    art = drawings_in_band(page, y0, y1)
    if art is None:
        # fall back: labels only, or full band
        if labels:
            u = labels[0]
            for br in labels[1:]:
                u |= br
            return pad(page, u, PAD_PT)
        return fitz.Rect(70, y0, page.rect.width - 45, y1)

    u = fitz.Rect(art)
    # keep labels above/within art and a little below (view titles etc.)
    near = fitz.Rect(art.x0 - 48, min(y0, art.y0) - 8, art.x1 + 48, art.y1 + 40)
    for br in labels:
        if near.intersects(br):
            u |= br
    u.y0 = max(u.y0, y0 - 2)
    u.y1 = min(u.y1, y1 + 2)
    return pad(page, u, PAD_PT)


def trim_ink(img: Image.Image, bg: int = 250, margin: int = TRIM_MARGIN_PX) -> Image.Image:
    """Light whitespace trim — keep a comfortable margin around ink."""
    g = img.convert("L")
    w, h = g.size
    px = g.load()
    step_x = max(1, w // 500)
    step_y = max(1, h // 500)
    ys = [y for y in range(h) if any(px[x, y] < bg for x in range(0, w, step_x))]
    xs = [x for x in range(w) if any(px[x, y] < bg for y in range(0, h, step_y))]
    if not xs or not ys:
        return img
    left, right = xs[0], xs[-1]
    top, bottom = ys[0], ys[-1]
    while top <= bottom and all(px[x, top] >= bg for x in range(left, right + 1)):
        top += 1
    while bottom >= top and all(px[x, bottom] >= bg for x in range(left, right + 1)):
        bottom -= 1
    while left <= right and all(px[left, y] >= bg for y in range(top, bottom + 1)):
        left += 1
    while right >= left and all(px[right, y] >= bg for y in range(top, bottom + 1)):
        right -= 1
    left = max(0, left - margin)
    top = max(0, top - margin)
    right = min(w - 1, right + margin)
    bottom = min(h - 1, bottom + margin)
    if right - left < 20 or bottom - top < 20:
        return img
    return img.crop((left, top, right + 1, bottom + 1))


def render_clip(page: fitz.Page, clip: fitz.Rect, out_path: Path) -> None:
    if clip.width < 10 or clip.height < 10:
        raise RuntimeError(f"degenerate clip {clip}")
    # annots=0 avoids chrome; alpha=False keeps opaque white bg
    pix = page.get_pixmap(
        matrix=fitz.Matrix(ZOOM, ZOOM),
        clip=clip,
        alpha=False,
        annots=False,
    )
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    img = trim_ink(img)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # compress_level keeps sharpness; avoid palette quantization
    img.save(out_path, "PNG", optimize=True, compress_level=6)


def extract_one(doc: fitz.Document, stem: str, page_no: int, key: str, mode: str) -> Path:
    page = doc[page_no - 1]
    out = OUT_DIR / f"{stem}.png"

    if mode == "figure":
        cap = find_caption(page, key)
        y0 = cap.y1 + 1
        y1 = stop_y(page, y0)
        render_clip(page, figure_clip(page, y0, y1), out)
        return out

    if mode == "phrase":
        r = find_block_containing(page, key)
        if r is None:
            raise RuntimeError(f"phrase not found: {key}")
        y0 = r.y1 + 1
        y1 = stop_y(page, y0)
        render_clip(page, figure_clip(page, y0, y1), out)
        return out

    if mode == "port_iso":
        r1 = find_block_containing(page, "Without port isolation")
        if r1 is None:
            raise RuntimeError("port isolation label missing")
        y0 = r1.y0 - 2
        y1 = stop_y(page, y0)
        for b in page.get_text("blocks"):
            if norm(b[4]).lower().startswith("fixing multiple-port") and b[1] > y0:
                y1 = min(y1, b[1] - 8)
        render_clip(page, figure_clip(page, y0, y1), out)
        return out

    if mode == "art_above_label":
        r = find_block_containing(page, key)
        if r is None:
            raise RuntimeError(f"label not found: {key}")
        y1 = r.y1 + 4
        y0 = 95
        render_clip(page, figure_clip(page, y0, y1), out)
        return out

    raise ValueError(mode)


def main() -> int:
    doc = fitz.open(PDF)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ok = fail = 0
    for stem, page_no, key, mode in FIGURES:
        try:
            path = extract_one(doc, stem, page_no, key, mode)
            im = Image.open(path)
            print(f"OK  {stem:40s} p{page_no:<4d} {im.size[0]:4d}x{im.size[1]:<4d} {path.stat().st_size:7d}B")
            ok += 1
        except Exception as e:
            print(f"FAIL {stem:40s} p{page_no:<4d} {e}")
            fail += 1
    print(f"Done: {ok} ok, {fail} fail")
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
