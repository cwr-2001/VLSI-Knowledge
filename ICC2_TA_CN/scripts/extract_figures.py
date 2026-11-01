# -*- coding: utf-8 -*-
"""Crop vector figures from IC Compiler II Timing Analysis UG."""
from __future__ import annotations

import re
from pathlib import Path

import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
PDF = Path(r"d:\IC Design\VLSI\icc2 timing analysis.pdf")
DPI = 220
ZOOM = DPI / 72.0
CAPTION_RE = re.compile(r"^Figure\s+(\d+)-(\d+)\b")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def captions(page: fitz.Page):
    out = []
    for b in page.get_text("blocks"):
        txt = norm(b[4])
        m = CAPTION_RE.match(txt)
        if m and len(txt) < 220:
            out.append((fitz.Rect(b[:4]), txt, f"fig-{m.group(1)}-{m.group(2)}"))
    out.sort(key=lambda x: x[0].y0)
    # de-dup same figure number (running header repeats)
    seen = set()
    uniq = []
    for r, t, name in out:
        if name in seen:
            continue
        # skip header-like tiny repeats near top/bottom chrome
        if r.y0 < 60 or r.y0 > page.rect.height - 55:
            continue
        seen.add(name)
        uniq.append((r, t, name))
    return uniq


STOP_RE = re.compile(
    r"^(To |The |You |For |When |If |This |These |Use |By |During |Note|Important|"
    r"See |A |An |In |Each |After |Before |However|Because |Although |Specify |"
    r"Create |Remove |Report |During|With |Without |Both |All |Any |On |At )",
    re.I,
)


def is_body(t: str, h: float) -> bool:
    if not t or CAPTION_RE.match(t):
        return False
    tl = t.lower()
    if tl.startswith(("icc2_shell>", "dc_shell>", "pt_shell>", "prompt>", "#")):
        return True
    if t.startswith("Table "):
        return True
    words = t.split()
    if len(t) > 85 or len(words) >= 8:
        return True
    if STOP_RE.match(t) and len(words) >= 5:
        return True
    if h > 32 and len(words) >= 6:
        return True
    return False


def band(page, cap: fitz.Rect, next_cap_y: float):
    """Figure sits under the caption until the next body paragraph or section head."""
    y0 = cap.y1 + 6
    y1 = min(next_cap_y - 6, 705)
    # Body copy is 11 pt; figure labels and in-figure commands are <= 10 pt.
    # Section headings are ~15 pt.
    d = page.get_text("dict")
    for b in d["blocks"]:
        if b.get("type") != 0:
            continue
        for ln in b.get("lines", []):
            spans = ln.get("spans") or []
            if not spans:
                continue
            if ln["bbox"][1] <= cap.y1 + 4:
                continue
            size = spans[0]["size"]
            t = norm("".join(s["text"] for s in spans))
            if not t or CAPTION_RE.match(t):
                continue
            if size >= 13.5 or (size >= 10.8 and is_body(t, ln["bbox"][3] - ln["bbox"][1])):
                y1 = min(y1, ln["bbox"][1] - 6)
    if y1 - y0 < 28:
        # caption may sit below the art: look upward to previous body
        y1 = cap.y0 - 2
        y0 = 78
        for b in page.get_text("blocks"):
            if b[3] >= cap.y0 - 2:
                continue
            t = norm(b[4])
            h = b[3] - b[1]
            if is_body(t, h):
                y0 = max(y0, b[3] + 3)
        if y1 - y0 < 28:
            return None
    return y0, y1


def drawings_union(page, y0, y1):
    page_area = page.rect.width * page.rect.height
    rects = []
    for d in page.get_drawings():
        rr = d.get("rect")
        if not rr:
            continue
        r = fitz.Rect(rr)
        if r.height < 0.8 or r.width < 0.8:
            continue
        if r.width > page.rect.width * 0.72 and r.height < 5:
            continue
        if r.get_area() > 0.35 * page_area:
            continue
        if r.y0 > y1 + 2 or r.y1 < y0 - 2:
            continue
        # drop page-tall frames
        if r.height > (y1 - y0) + 80 and r.width > page.rect.width * 0.6:
            continue
        rects.append(r)
    if not rects:
        return fitz.Rect(72, y0, page.rect.width - 48, y1)
    u = rects[0]
    for r in rects[1:]:
        u |= r
    # include short labels in the band
    for b in page.get_text("blocks"):
        t = norm(b[4])
        if len(t) > 42 or len(t.split()) > 5 or CAPTION_RE.match(t) or is_body(t, b[3] - b[1]):
            continue
        br = fitz.Rect(b[:4])
        mid = 0.5 * (br.y0 + br.y1)
        if y0 - 2 <= mid <= y1 + 2:
            u |= br
    u.x0 = max(36, u.x0 - 8)
    u.y0 = max(48, u.y0 - 4)
    u.x1 = min(page.rect.width - 28, u.x1 + 8)
    u.y1 = min(y1 + 2, u.y1 + 4)
    return u


def trim(img: Image.Image, bg=248, margin=14) -> Image.Image:
    g = img.convert("L")
    w, h = g.size
    px = g.load()
    sx = max(1, w // 400)
    sy = max(1, h // 400)
    ys = [y for y in range(h) if any(px[x, y] < bg for x in range(0, w, sx))]
    xs = [x for x in range(w) if any(px[x, y] < bg for y in range(0, h, sy))]
    if not xs or not ys:
        return img
    l, r, t, b = xs[0], xs[-1], ys[0], ys[-1]
    l = max(0, l - margin)
    t = max(0, t - margin)
    r = min(w - 1, r + margin)
    b = min(h - 1, b + margin)
    if r - l < 30 or b - t < 30:
        return img
    return img.crop((l, t, r + 1, b + 1))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    saved = []
    for i, page in enumerate(doc):
        caps = captions(page)
        if not caps:
            continue
        for k, (rect, text, name) in enumerate(caps):
            nxt = caps[k + 1][0].y0 if k + 1 < len(caps) else page.rect.height - 50
            got = band(page, rect, nxt)
            if not got:
                print("SKIP", name, "page", i + 1)
                continue
            y0, y1 = got
            clip = drawings_union(page, y0, y1)
            if clip.height < 20 or clip.width < 20:
                print("SMALL", name, clip)
                continue
            pix = page.get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM), clip=clip, alpha=False)
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            img = trim(img)
            path = OUT / f"{name}.png"
            img.save(path, optimize=True)
            saved.append((name, i + 1, text, img.size))
            print(f"{name:12} p{i+1:3} {img.size[0]}x{img.size[1]}  {text[:70]}")
    print("TOTAL", len(saved))


if __name__ == "__main__":
    main()
