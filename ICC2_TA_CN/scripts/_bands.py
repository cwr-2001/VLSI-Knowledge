import fitz
from extract_figures import captions, band, norm

d = fitz.open(r"d:\IC Design\VLSI\icc2 timing analysis.pdf")
for pi in (78, 90, 91, 106):
    p = d[pi]
    print("==== page", pi + 1, "h", round(p.rect.height, 1))
    caps = captions(p)
    for k, (rect, text, name) in enumerate(caps):
        nxt = caps[k + 1][0].y0 if k + 1 < len(caps) else p.rect.height - 50
        got = band(p, rect, nxt)
        print(name, "cap", round(rect.y0, 1), round(rect.y1, 1), "band", None if not got else tuple(round(x, 1) for x in got))
    print("-- blocks --")
    for b in p.get_text("blocks"):
        t = norm(b[4])
        if not t:
            continue
        if b[1] > 700:
            continue
        print(f"  y={b[1]:6.1f}-{b[3]:6.1f} {t[:110]}")
