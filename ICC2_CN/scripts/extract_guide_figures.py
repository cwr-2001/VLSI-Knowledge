# -*- coding: utf-8 -*-
"""Crop 'Figure N ...' regions from a Synopsys UG PDF.

Figures sit under the italic caption. The crop runs from the caption baseline
to the next body paragraph or heading, then whitespace is trimmed.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz
from PIL import Image

DPI = 140
ZOOM = DPI / 72.0
CAPTION_RE = re.compile(r"^Figure\s+(\d+)\s+(?!shows\b|compares\b|illustrates\b)(\S.*)$", re.I)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def captions(page: fitz.Page):
    out = []
    for b in page.get_text("blocks"):
        if b[6] != 0:
            continue
        t = norm(b[4])
        m = CAPTION_RE.match(t)
        if m and len(t) < 240 and (b[3] - b[1]) < 48:
            out.append((int(m.group(1)), fitz.Rect(b[:4]), t))
    out.sort(key=lambda x: x[1].y0)
    return out


def _art_rects(page: fitz.Page, y0: float, y_limit: float) -> list[fitz.Rect]:
    """Image and drawing rectangles that belong to the figure band."""
    rects: list[fitz.Rect] = []
    page_area = page.rect.width * page.rect.height
    for info in page.get_image_info():
        r = fitz.Rect(info["bbox"])
        if r.y0 >= y0 - 4 and r.y1 <= y_limit + 2 and r.height > 18 and r.width > 18:
            if r.get_area() < 0.85 * page_area:
                rects.append(r)
    for d in page.get_drawings():
        raw = d.get("rect")
        if not raw:
            continue
        r = fitz.Rect(raw)
        if r.y1 < y0 - 2 or r.y0 > y_limit:
            continue
        if r.height < 2 or r.width < 2:
            continue
        if r.width > page.rect.width * 0.72 and r.height < 5:
            continue
        if r.y0 < 68:
            continue
        if r.get_area() > 0.9 * page_area:
            continue
        rects.append(r)
    return rects


def _is_plate(r: fitz.Rect) -> bool:
    """Page-sized or figure-sized background frame, not a real object."""
    return r.width > 300 and r.height > 140


def _hits_art(b, arts: list[fitz.Rect]) -> bool:
    r = fitz.Rect(b[:4])
    for a in arts:
        if _is_plate(a):
            continue
        if r.intersects(a):
            return True
    return False


def crop_rect(page: fitz.Page, cap: fitz.Rect, next_cap_y: float | None) -> fitz.Rect:
    """Crop from just under the caption through the artwork, stopping before body text."""
    y0 = cap.y1 + 1.5
    y_limit = page.rect.height - 52
    if next_cap_y is not None:
        y_limit = min(y_limit, next_cap_y - 3)
    for b in page.get_text("blocks"):
        if b[6] != 0:
            continue
        t = norm(b[4])
        if b[1] > 680 and "User Guide" in t:
            y_limit = min(y_limit, b[1] - 4)

    arts = _art_rects(page, y0, y_limit)
    union = None
    for r in arts:
        if _is_plate(r):
            continue
        union = r if union is None else (union | r)
    if union is None:
        for r in arts:
            union = r if union is None else (union | r)

    y1 = (min(union.y1 + 8, y_limit) if union is not None else y_limit)
    for b in page.get_text("blocks"):
        if b[6] != 0 or b[1] < y0 + 6 or b[1] >= y1:
            continue
        t = norm(b[4])
        if not t or _hits_art(b, arts):
            continue
        x0, x1 = b[0], b[2]
        w = x1 - x0
        # real paragraph under the figure
        if len(t) > 100 and w > 300 and x0 < 150:
            y1 = min(y1, b[1] - 3)
            continue
        # section heading (diagram labels sit further right, or inside a box)
        if (
            x0 < 140
            and w > 70
            and 8 < len(t) < 110
            and len(t.split()) >= 2
            and not t.lower().startswith("figure ")
        ):
            y1 = min(y1, b[1] - 3)
            continue
        if re.match(r"^\d+\.\s+\S", t) and x0 < 140:
            y1 = min(y1, b[1] - 3)
        if t.lower().startswith("note:") and x0 < 140:
            y1 = min(y1, b[1] - 3)

    if y1 - y0 < 24 and union is not None:
        y1 = min(union.y1 + 8, y_limit)
    y1 = max(y1, y0 + 24)
    return fitz.Rect(60, y0, page.rect.width - 40, min(y1, y_limit))


def trim(im: Image.Image) -> Image.Image:
    bg = im.getpixel((2, 2))
    diff = im.convert("L").point(lambda p: 255 if p < 248 else 0)
    bbox = diff.getbbox()
    if not bbox:
        return im
    l, t, r, b = bbox
    pad = 8
    l = max(0, l - pad)
    t = max(0, t - pad)
    r = min(im.width, r + pad)
    b = min(im.height, b + pad)
    if r - l < 20 or b - t < 20:
        return im
    return im.crop((l, t, r, b))


def extract(pdf: Path, out_dir: Path, manifest: Path, prefix: str, only: set[int] | None = None):
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf)
    rows = []
    seen = set()
    for i, page in enumerate(doc):
        caps = captions(page)
        for idx, (num, rect, title) in enumerate(caps):
            if only and num not in only:
                continue
            if num in seen:
                continue
            nxt = caps[idx + 1][1].y0 if idx + 1 < len(caps) else None
            clip = crop_rect(page, rect, nxt)
            if clip.height < 20 or clip.width < 20:
                print(f"skip tiny fig {num} p{i+1}")
                continue
            pix = page.get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM), clip=clip, alpha=False)
            im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            im = trim(im)
            name = f"{prefix}-fig-{num:03d}.png"
            im.save(out_dir / name, optimize=True)
            seen.add(num)
            rows.append((num, i + 1, title, name, im.width, im.height))
            print(f"fig {num:3d} p{i+1:3d} {im.width}x{im.height} {title[:80]}")
    doc.close()
    lines = [f"{n}\t{p}\t{fn}\t{w}x{h}\t{title}" for n, p, title, fn, w, h in rows]
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {len(rows)} figures -> {manifest}")


if __name__ == "__main__":
    which = sys.argv[1]
    only = set(int(x) for x in sys.argv[2].split(",")) if len(sys.argv) > 2 else None
    if which == "gui":
        extract(
            Path(r"d:\IC Design\VLSI\icc2 gui.pdf"),
            Path(r"d:\IC Design\VLSI\ICC2_GUI_CN\figures"),
            Path(r"d:\IC Design\VLSI\ICC2_GUI_CN\scripts\figures.txt"),
            "gui",
            only,
        )
    elif which == "dp":
        extract(
            Path(r"d:\IC Design\VLSI\icc2 Design Planning.pdf"),
            Path(r"d:\IC Design\VLSI\ICC2_DP_CN\figures"),
            Path(r"d:\IC Design\VLSI\ICC2_DP_CN\scripts\figures.txt"),
            "dp",
            only,
        )
    else:
        raise SystemExit("gui|dp")
