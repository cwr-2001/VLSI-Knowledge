# -*- coding: utf-8 -*-
from pathlib import Path

base = Path(r"d:\IC Design\VLSI\ICV_CN\scripts")
frag = base / "_ch8_frags"
frag.mkdir(exist_ok=True)

ids = (base / "_enum_ids.txt").read_text(encoding="utf-8").splitlines()

indesign = """
INCREMENTAL_MILKYWAY_OPTIONS_INCLUDE_VIEW INCREMENTAL_OPTIONS_SELECT_WINDOW
INDESIGN_DO_FLOATING_VIA_FILL_PURGE INDESIGN_DONT_UPDATE_TECHNOLOGY_FILE
INDESIGN_ENABLE_MY_ASSIGN METAL_FILL_BLOCKAGE_LAYERS
METAL_FILL_BLOCKAGE_VIEW METAL_FILL_DATATYPES
METAL_FILL_DENSITY_DEBUG METAL_FILL_DENSITY_CHECK
METAL_FILL_DENSITY_DELTA_WIN_SIZE METAL_FILL_DENSITY_MIN
METAL_FILL_FLATTEN METAL_FILL_INLIB
METAL_FILL_INLIB_CELL METAL_FILL_INLIB_EXCLUDE_FILL
METAL_FILL_INLIB_PATH METAL_FILL_INSTALL_ICV_RH
METAL_FILL_INSTALL_PRIMEYIELD_RH METAL_FILL_LAYER_NUMBERS
METAL_FILL_OUTLIB METAL_FILL_OUTLIB_APPLY_PREFIX
METAL_FILL_OUTLIB_CELL METAL_FILL_OUTLIB_CELL_PREFIX
METAL_FILL_OUTLIB_MODE METAL_FILL_OUTLIB_PATH
METAL_FILL_OUTLIB_TEMP_CELL METAL_FILL_OUTLIB_VIEW
METAL_FILL_OUTLIB_RF_CELL_PREFIX METAL_FILL_RUNSET2LIBRARY_LAYER_MAP
METAL_FILL_SELECT_WINDOW METAL_FILL_USER_RUNSET
_METHODOLOGY_FUNCTIONS_RS_ SAVE_METAL_FILL_INLIB_EXCLUDE_FILL
_SMF_ICV_RH_ SNPSINDESIGN
VIA_FILL_ALLOWED_ONE_SIDE VIA_FILL_ASSOCIATED_METAL
VIA_FILL_DATATYPES VIA_FILL_LAYER_NUMBERS
VIA_FILL_MASK_NAMES VIA_FILL_MET_ENCLOSURE
VIA_FILL_OUTLIB_RF_CELL_PREFIX _WRITE_AREFS
""".split()

sys_kw = (
    "barrier broadcast builtin deprecated intrinsic method obsolete preprocess "
    "primary proxy_out published required shutdown unsafe unique volatile"
).split()

app_ids = (
    "binary boolean break by const constraint constraint_category CONSTRAINT_EQ "
    "CONSTRAINT_GE CONSTRAINT_GELE CONSTRAINT_GELT CONSTRAINT_GT CONSTRAINT_GTLE "
    "CONSTRAINT_GTLT CONSTRAINT_LE CONSTRAINT_LT CONSTRAINT_NE continue DELETE_TEXT "
    "DELETE_AND_REPORT defined double elif else elseif enum false for foreach function "
    "hash if in in_out integer list newtype of on out return returning step string "
    "struct substrate SUBSTRATE thru to true unary undefined violation void while"
).split()


def esc(s: str) -> str:
    return s.replace("_", r"\_") if s else ""


def rows_n(items, n: int) -> str:
    lines = []
    for i in range(0, len(items), n):
        trip = list(items[i : i + n])
        while len(trip) < n:
            trip.append("")
        lines.append(" & ".join(esc(t) for t in trip) + r" \\")
    return "\n".join(lines)


(frag / "sys_kw.tex").write_text(rows_n(sys_kw, 3), encoding="utf-8")
(frag / "indesign.tex").write_text(rows_n(indesign, 2), encoding="utf-8")
(frag / "app_ids.tex").write_text(rows_n(app_ids, 3), encoding="utf-8")
(frag / "enum.tex").write_text(rows_n(ids, 3), encoding="utf-8")

print("sys sample:", repr((frag / "sys_kw.tex").read_text(encoding="utf-8").splitlines()[0]))
print("enum rows:", len((frag / "enum.tex").read_text(encoding="utf-8").splitlines()))

body1 = (base / "_ch8a_body1.tex").read_text(encoding="utf-8")
body2 = (base / "_ch8a_body2.tex").read_text(encoding="utf-8")
body3 = (base / "_ch8a_body3.tex").read_text(encoding="utf-8")
body1 = body1.replace("@@SYS_KW@@", (frag / "sys_kw.tex").read_text(encoding="utf-8"))
body1 = body1.replace("@@INDESIGN@@", (frag / "indesign.tex").read_text(encoding="utf-8"))
body1 = body1.replace("@@APP_IDS@@", (frag / "app_ids.tex").read_text(encoding="utf-8"))
body1 = body1.replace("@@ENUM@@", (frag / "enum.tex").read_text(encoding="utf-8"))
out = body1 + "\n" + body2 + "\n" + body3
dest = Path(r"d:\IC Design\VLSI\ICV_CN\chapters\08_pxl.tex")
dest.write_text(out, encoding="utf-8")
print("wrote", dest, "lines", out.count("\n") + 1)
# sanity
assert r"barrier & broadcast & builtin \\" in out
assert "proxy\\_out" in out
assert "ABORT" in out or r"ABORT" in out
assert "% --- 第8章后半见下方继续" in out
print("sanity ok")
