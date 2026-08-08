param(
  [Parameter(Mandatory = $true)][int]$Start,
  [Parameter(Mandatory = $true)][int]$End,
  [string]$OutFile = "extracted.txt",
  [string]$Pdf = "..\..\RedHawk_UG_2021.pdf",
  [switch]$DocPage
)

# -DocPage: Start/End are printed document page numbers (offset +38)
# Without -DocPage: Start/End are PDF page numbers (1-based)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Resolve-Path (Join-Path $here "..")
$pdfPath = if ([System.IO.Path]::IsPathRooted($Pdf)) { $Pdf } else { Join-Path $root $Pdf }
$outPath = if ([System.IO.Path]::IsPathRooted($OutFile)) { $OutFile } else { Join-Path $root $OutFile }

if (-not (Test-Path $pdfPath)) {
  throw "PDF not found: $pdfPath"
}

$pdfStart = if ($DocPage) { $Start + 38 } else { $Start }
$pdfEnd   = if ($DocPage) { $End + 38 } else { $End }

Write-Host "Extracting PDF pages $pdfStart-$pdfEnd from:"
Write-Host "  $pdfPath"
pdftotext -f $pdfStart -l $pdfEnd -layout $pdfPath $outPath
Write-Host "Wrote: $outPath"
