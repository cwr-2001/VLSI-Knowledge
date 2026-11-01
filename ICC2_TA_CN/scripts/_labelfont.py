import fitz
d = fitz.open(r"d:\IC Design\VLSI\icc2 timing analysis.pdf")
for pi in (78, 90):
    print("====", pi + 1)
    p = d[pi]
    for b in p.get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        for ln in b["lines"]:
            spans = ln["spans"]
            if not spans:
                continue
            t = "".join(s["text"] for s in spans).strip()
            if not t or ln["bbox"][1] < 100 or ln["bbox"][1] > 680:
                continue
            s0 = spans[0]
            if s0["size"] < 12:
                print(f"{s0['size']:4.1f} y={ln['bbox'][1]:6.1f} {t[:90]}")
