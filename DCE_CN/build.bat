@echo off
REM Build DC Explorer UG Chinese translation with XeLaTeX (run twice for TOC)
cd /d "%~dp0"
where xelatex >nul 2>&1
if errorlevel 1 (
  echo [ERROR] xelatex not found. Install TeX Live or MiKTeX first.
  exit /b 1
)
echo === Pass 1/2 ===
xelatex -interaction=nonstopmode main.tex
if errorlevel 1 exit /b 1
echo === Pass 2/2 ===
xelatex -interaction=nonstopmode main.tex
echo.
echo Done. Output: main.pdf
