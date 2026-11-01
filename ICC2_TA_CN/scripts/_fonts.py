import fitz
d = fitz.open(r"d:\IC Design\VLSI\icc2 timing analysis.pdf")
for pi in (49, 61, 79, 142):
    print("====", pi + 1)
    p = d[pi]
    for b in p.get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        for l in b["lines"]:
            spans = l["spans"]
            if not spans:
                continue
            t = "".join(s["text"] for s in spans).strip()
            if not t:
                continue
            s0 = spans[0]
            if s0["size"] >= 10.5 or t.startswith(("Figure", "Chapter", "To ", "Creating")):
                print(f"{s0['size']:5.1f} f={s0['flags']:3} y={l['bbox'][1]:6.1f} {t[:100]}")
