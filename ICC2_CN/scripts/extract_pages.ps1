param(
  [Parameter(Mandatory = $true)][int]$Start,
  [Parameter(Mandatory = $true)][int]$End,
  [string]$OutFile = "extracted.txt",
  [string]$Pdf = "..\ICC2 Implementation User Guide Version V-2023.12, December 2023.pdf"
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
pdftotext -f $Start -l $End -layout $pdfPath $outPath
Write-Host "Wrote: $outPath"
