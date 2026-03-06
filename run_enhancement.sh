#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  Bank Loan Analysis — Dashboard Enhancement Runner (Linux/Mac)
#  Repository : DragonlordHarsh/MOOC-DSV
# ─────────────────────────────────────────────────────────────
set -e

echo "Installing dependencies..."
pip install -r requirements_enhance.txt

echo "Running enhancement script..."
python3 enhance_dashboard.py

echo ""
echo "Done! Output files:"
echo "  Bank Loan Analysis Project - Enhanced.twb"
echo "  Bank Loan Analysis Project - Enhanced.twbx"
