@echo off
REM Build PrimeTime UG Chinese translation with XeLaTeX (run twice for TOC)
cd /d "%~dp0"
for %%I in (.) do set "JOBNAME=%%~nxI"
where xelatex >nul 2>&1
if errorlevel 1 (
  echo [ERROR] xelatex not found. Install TeX Live or MiKTeX first.
  exit /b 1
)
echo === Pass 1/2 ===
xelatex -interaction=nonstopmode -jobname="%JOBNAME%" main.tex
if errorlevel 1 exit /b 1
echo === Pass 2/2 ===
xelatex -interaction=nonstopmode -jobname="%JOBNAME%" main.tex
echo.
echo Done. Output: %JOBNAME%.pdf
