param(
  [Parameter(Mandatory = $true)][int]$Start,
  [Parameter(Mandatory = $true)][int]$End,
  [string]$OutFile = "extracted.txt",
  [string]$Pdf = "..\..\PrimeTime_Workshop_Lab Guide-2018.06.pdf"
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Resolve-Path (Join-Path $here "..")
$pdfPath = if ([System.IO.Path]::IsPathRooted($Pdf)) { $Pdf } else { Join-Path $root $Pdf }
$outPath = if ([System.IO.Path]::IsPathRooted($OutFile)) { $OutFile } else { Join-Path $root $OutFile }

if (-not (Test-Path $pdfPath)) {
  throw "PDF not found: $pdfPath"
}

# 扫描件无文字层时，用渲染 + Tesseract OCR
$tess = "C:\Program Files\Tesseract-OCR\tesseract.exe"
if (-not (Test-Path $tess)) {
  throw "Tesseract not found: $tess"
}

$tmp = Join-Path $env:TEMP ("pt_lab_ocr_" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $tmp | Out-Null
try {
  python -c @"
import fitz, os, subprocess
pdf = r'''$pdfPath'''
tmp = r'''$tmp'''
tess = r'''$tess'''
start, end = $Start, $End
doc = fitz.open(pdf)
chunks = []
for i in range(start-1, end):
    png = os.path.join(tmp, f'p{i+1:04d}.png')
    doc[i].get_pixmap(matrix=fitz.Matrix(2,2)).save(png)
    r = subprocess.run([tess, png, 'stdout', '-l', 'eng', '--psm', '6'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    chunks.append(f'===== PAGE {i+1} =====\n{r.stdout}\n')
open(r'''$outPath''', 'w', encoding='utf-8').write('\n'.join(chunks))
print('Wrote', r'''$outPath''')
"@
} finally {
  Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
}
