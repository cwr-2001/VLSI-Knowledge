param(
  [Parameter(Mandatory = $true)][int]$Start,
  [Parameter(Mandatory = $true)][int]$End,
  [string]$OutFile = "extracted.txt",
  [string]$Pdf = "..\..\Fusion Compiler User Guide Version V-2023.12-SP3, May 2024.pdf"
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Resolve-Path (Join-Path $here "..")
$pdfPath = if ([System.IO.Path]::IsPathRooted($Pdf)) { $Pdf } else { Join-Path $root $Pdf }
$outPath = if ([System.IO.Path]::IsPathRooted($OutFile)) { $OutFile } else { Join-Path $root $OutFile }

if (-not (Test-Path $pdfPath)) {
  throw "PDF not found: $pdfPath"
}

Write-Host "Extracting pages $Start-$End from:"
Write-Host "  $pdfPath"

# Prefer Python+PyMuPDF (pdftotext may be unavailable on Windows)
$py = Join-Path $here "extract_pages.py"
python $py $Start $End $outPath $pdfPath
Write-Host "Wrote: $outPath"
