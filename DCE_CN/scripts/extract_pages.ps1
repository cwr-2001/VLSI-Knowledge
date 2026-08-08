param(
  [Parameter(Mandatory = $true)][int]$Start,
  [Parameter(Mandatory = $true)][int]$End,
  [string]$OutFile = "extracted.txt",
  [string]$Pdf = "..\DC Explorer User Guide, version S-2021.06.pdf"
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Resolve-Path (Join-Path $here "..")
$pdfPath = if ([System.IO.Path]::IsPathRooted($Pdf)) { $Pdf } else { Join-Path (Resolve-Path (Join-Path $root "..")) (Split-Path $Pdf -Leaf) }
if (-not (Test-Path $pdfPath)) {
  $pdfPath = Join-Path (Resolve-Path (Join-Path $root "..")) "DC Explorer User Guide, version S-2021.06.pdf"
}
$outPath = if ([System.IO.Path]::IsPathRooted($OutFile)) { $OutFile } else { Join-Path $root $OutFile }

if (-not (Test-Path $pdfPath)) {
  throw "PDF not found: $pdfPath"
}

Write-Host "Extracting pages $Start-$End from:"
Write-Host "  $pdfPath"
pdftotext -f $Start -l $End -layout $pdfPath $outPath
Write-Host "Wrote: $outPath"
