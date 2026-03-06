@echo off
REM ─────────────────────────────────────────────────────────────
REM  Bank Loan Analysis — Dashboard Enhancement Runner (Windows)
REM  Repository : DragonlordHarsh/MOOC-DSV
REM ─────────────────────────────────────────────────────────────

echo Installing dependencies...
pip install -r requirements_enhance.txt

echo Running enhancement script...
python enhance_dashboard.py

echo.
echo Done! Output files:
echo   Bank Loan Analysis Project - Enhanced.twb
echo   Bank Loan Analysis Project - Enhanced.twbx
