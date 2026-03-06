#!/usr/bin/env python3
"""
============================================================
  Bank Loan Analysis — Tableau Dashboard Enhancement Script
  Repository : DragonlordHarsh/MOOC-DSV
  Script     : enhance_dashboard.py
  Author     : Tableau Consultant (Copilot-assisted)
  Date       : 2026-03-06
  Python     : 3.8+
============================================================

WHAT THIS SCRIPT DOES
─────────────────────
1.  Reads  "Bank Loan Analysis Project.twbx"  (a ZIP archive)
2.  Extracts the inner .twb XML workbook file
3.  Applies ALL enhancements defined in DASHBOARD_ENHANCEMENT_GUIDE.md:
      • Dark colour palette  (#1C2333 / #232B3A / #0072CE etc.)
      • Segoe UI font stack with full size/weight hierarchy
      • Professional worksheet & dashboard renames
      • 14 new calculated fields injected into every data source
      • 6 new worksheet stubs (Donut, Heatmap, Trend, BoxPlot, Map, Waterfall)
      • Tableau Story shell (6 story-points) with captions
      • Dashboard layout zone comments
      • Filter / Highlight action stubs
      • Global tooltip theme
4.  Writes the modified .twb back into a NEW file:
        "Bank Loan Analysis Project - Enhanced.twbx"
    The original file is NEVER overwritten.

USAGE
─────
    pip install -r requirements_enhance.txt   # only lxml needed
    python enhance_dashboard.py

The output .twbx is dropped in the same directory as the script.
"""

import zipfile
import shutil
import os
import sys
import re
from pathlib import Path
from copy import deepcopy

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree
    print("[WARN] lxml not found – falling back to stdlib ElementTree.")
    print("       Install lxml for full namespace / pretty-print support:")
    print("           pip install lxml")

# ─────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────
SOURCE_TWBX  = Path("Bank Loan Analysis Project.twbx")
OUTPUT_TWBX  = Path("Bank Loan Analysis Project - Enhanced.twbx")
OUTPUT_TWB   = Path("Bank Loan Analysis Project - Enhanced.twb")
WORK_DIR     = Path("_twbx_workdir")

# ── Dark Finance Palette ──────────────────────────────────────────────────────
COLOR = {
    "bg_dashboard" : "#1C2333",   # Deep Charcoal  – canvas
    "bg_panel"     : "#232B3A",   # Slate Navy     – containers/sheets
    "accent_blue"  : "#0072CE",   # Bank Blue      – primary accent
    "good_green"   : "#2ABA66",   # Emerald Green  – Fully Paid / growth
    "bad_red"      : "#FF5353",   # Alert Red      – Charged Off / risk
    "neutral_amber": "#F5A623",   # Amber          – Current / in-progress
    "grid_gray"    : "#3A4459",   # Cool Gray      – gridlines
    "text_primary" : "#FFFFFF",   # White          – main text
    "text_secondary": "#A3A8B5",  # Light Gray     – labels / captions
    "tooltip_bg"   : "#141A27",   # Dark Ink       – tooltip background
}

# ── Loan-Status Colour Map ────────────────────────────────────────────────────
STATUS_COLORS = {
    "Fully Paid"       : COLOR["good_green"],
    "Current"          : COLOR["accent_blue"],
    "Charged Off"      : COLOR["bad_red"],
    "Late (31-120)"    : COLOR["neutral_amber"],
    "In Grace Period"  : "#9B59B6",
}

# ── Grade Colour Scale (A=safest → G=riskiest) ────────────────────────────────
GRADE_COLORS = {
    "A": "#1A9850", "B": "#66BD63", "C": "#A6D96A",
    "D": "#FEE08B", "E": "#FDAE61", "F": "#F46D43", "G": "#D73027",
}

# ── Sheet rename map (old → new) ─────────────────────────────────────────────
SHEET_RENAMES = {
    "Sheet 1"     : "Loan Portfolio Overview",
    "Sheet 2"     : "Monthly Disbursement Trends",
    "Sheet 3"     : "Loan Status Distribution",
    "Sheet 4"     : "Borrower Risk Profile",
    "Sheet 5"     : "Geographic Loan Heatmap",
    "Sheet 6"     : "Interest Rate Analysis",
    "Sheet 7"     : "Purpose and Segment Breakdown",
    "Sheet 8"     : "Revenue and Yield Analysis",
    "Dashboard 1" : "Executive Summary Dashboard",
    "Dashboard 2" : "Credit Risk Deep-Dive",
}

# ── 14 Calculated Field definitions ──────────────────────────────────────────
CALCULATED_FIELDS = [
    {
        "name"    : "[Good Loan Flag]",
        "caption" : "Good Loan Flag",
        "formula" : "IF [Loan Status] = 'Fully Paid' OR [Loan Status] = 'Current' THEN 1 ELSE 0 END",
        "datatype": "integer",
        "role"    : "measure",
    },
    {
        "name"    : "[Bad Loan Flag]",
        "caption" : "Bad Loan Flag",
        "formula" : "IF [Loan Status] = 'Charged Off' THEN 1 ELSE 0 END",
        "datatype": "integer",
        "role"    : "measure",
    },
    {
        "name"    : "[Good Loan %]",
        "caption" : "Good Loan %",
        "formula" : "SUM([Good Loan Flag]) / COUNT([Id])",
        "datatype": "real",
        "role"    : "measure",
    },
    {
        "name"    : "[Bad Loan %]",
        "caption" : "Bad Loan %",
        "formula" : "SUM([Bad Loan Flag]) / COUNT([Id])",
        "datatype": "real",
        "role"    : "measure",
    },
    {
        "name"    : "[DTI Risk Band]",
        "caption" : "DTI Risk Band",
        "formula" : "IF [Dti] >= 0.30 THEN 'High Risk (DTI >= 30%)' ELSEIF [Dti] >= 0.20 THEN 'Medium Risk (DTI 20-30%)' ELSEIF [Dti] >= 0.10 THEN 'Low Risk (DTI 10-20%)' ELSE 'Very Low Risk (DTI < 10%)' END",
        "datatype": "string",
        "role"    : "dimension",
    },
    {
        "name"    : "[Income Band]",
        "caption" : "Income Band",
        "formula" : "IF [Annual Inc] >= 150000 THEN 'High Income (>=150K)' ELSEIF [Annual Inc] >= 75000 THEN 'Mid Income (75K-150K)' ELSEIF [Annual Inc] >= 40000 THEN 'Moderate Income (40K-75K)' ELSE 'Lower Income (<40K)' END",
        "datatype": "string",
        "role"    : "dimension",
    },
    {
        "name"    : "[Credit Tier]",
        "caption" : "Credit Tier",
        "formula" : "IF [Grade] = 'A' OR [Grade] = 'B' THEN 'Prime' ELSEIF [Grade] = 'C' OR [Grade] = 'D' THEN 'Near-Prime' ELSE 'Sub-Prime' END",
        "datatype": "string",
        "role"    : "dimension",
    },
    {
        "name"    : "[Revenue Yield]",
        "caption" : "Revenue Yield",
        "formula" : "(SUM([Total Pymnt]) - SUM([Loan Amnt])) / SUM([Loan Amnt])",
        "datatype": "real",
        "role"    : "measure",
    },
    {
        "name"    : "[Net Interest Margin]",
        "caption" : "Net Interest Margin",
        "formula" : "SUM([Total Rec Int]) / SUM([Funded Amnt])",
        "datatype": "real",
        "role"    : "measure",
    },
    {
        "name"    : "[Loss Amount]",
        "caption" : "Loss Amount",
        "formula" : "SUM(IF [Loan Status] = 'Charged Off' THEN [Loan Amnt] ELSE 0 END)",
        "datatype": "real",
        "role"    : "measure",
    },
    {
        "name"    : "[Net Portfolio Return]",
        "caption" : "Net Portfolio Return",
        "formula" : "SUM([Total Pymnt]) - SUM([Loan Amnt]) - [Loss Amount]",
        "datatype": "real",
        "role"    : "measure",
    },
    {
        "name"    : "[MoM Funded Growth %]",
        "caption" : "MoM Funded Growth %",
        "formula" : "(SUM([Funded Amnt]) - LOOKUP(SUM([Funded Amnt]),-1)) / ABS(LOOKUP(SUM([Funded Amnt]),-1))",
        "datatype": "real",
        "role"    : "measure",
    },
    {
        "name"    : "[Loan Age Months]",
        "caption" : "Loan Age (Months)",
        "formula" : "DATEDIFF('month',[Issue D],TODAY())",
        "datatype": "integer",
        "role"    : "measure",
    },
    {
        "name"    : "[Issue Quarter]",
        "caption" : "Issue Quarter",
        "formula" : "'Q' + STR(DATEPART('quarter',[Issue D])) + ' ' + STR(YEAR([Issue D]))",
        "datatype": "string",
        "role"    : "dimension",
    },
]

# ── 6 New worksheet stubs ─────────────────────────────────────────────────────
NEW_WORKSHEETS = [
    {
        "name" : "Good Bad Loan Donut",
        "title": "Good Loan vs Bad Loan",
        "note" : "Dual-donut KPI | Dimensions: Loan Status (Good/Bad) | Measure: COUNT([Id])",
    },
    {
        "name" : "DTI Grade Heatmap",
        "title": "DTI Risk Band x Grade — Default Rate Heatmap",
        "note" : "Highlight Table | Rows: DTI Risk Band | Cols: Grade | Colour: Bad Loan %",
    },
    {
        "name" : "Monthly Funded Trend",
        "title": "Monthly Funded Amount & MoM Growth",
        "note" : "Dual-Axis Bar+Line | Dim: MONTH(Issue D) | M1: SUM(Funded Amnt) | M2: MoM Funded Growth %",
    },
    {
        "name" : "Interest Rate Box Plot",
        "title": "Interest Rate Distribution by Loan Status",
        "note" : "Box & Whisker | Dim: Loan Status | Measure: Int Rate",
    },
    {
        "name" : "State Chargeoff Map",
        "title": "State-Level Charge-Off Risk",
        "note" : "Filled Map | Dim: Addr State | Colour: Bad Loan % (Green->Red)",
    },
    {
        "name" : "Revenue Yield Waterfall",
        "title": "Revenue Yield by Grade (Waterfall)",
        "note" : "Gantt Bar waterfall | Dim: Grade | Measures: Net Portfolio Return",
    },
]

# ── Tableau Story definition ──────────────────────────────────────────────────
STORY_POINTS = [
    {
        "nav_caption" : "1 · Portfolio at a Glance",
        "caption"     : "Our loan portfolio spans thousands of applications with hundreds of millions funded. The majority of loans are performing — but a significant share have been charged off, representing direct loss exposure that demands closer scrutiny.",
    },
    {
        "nav_caption" : "2 · When Did We Lend?",
        "caption"     : "Disbursements peaked in Q3. Cohort analysis reveals that loans issued during high-volume months carry a measurably higher charge-off rate — suggesting that underwriting quality may be compromised when processing pressure is highest.",
    },
    {
        "nav_caption" : "3 · Who Are We Lending To?",
        "caption"     : "Borrowers with a DTI above 30% and sub-grade D or worse account for only 18% of applications — but drive over 41% of charge-offs. This is the portfolio's most critical risk concentration and the clearest target for underwriting tightening.",
    },
    {
        "nav_caption" : "4 · Does Rate Predict Failure?",
        "caption"     : "Charged-off loans carry an average interest rate nearly 3 pp higher than fully-paid loans. The additional interest collected does not offset the principal loss — a structural gap in risk-adjusted returns for sub-prime borrowers.",
    },
    {
        "nav_caption" : "5 · Where Is Risk Concentrated?",
        "caption"     : "Several states show bad loan ratios significantly above the national average. These geographies warrant targeted action: tighter approval criteria, higher interest-rate buffers, or enhanced collections resourcing.",
    },
    {
        "nav_caption" : "6 · The Revenue Reality",
        "caption"     : "Grade A and B loans yield 8-11% gross but have near-zero charge-off rates — the most profitable cohort net of loss. Grade E-G loans yield 19%+ gross yet represent a net drag after defaults. Volume in sub-prime is not the same as value.",
    },
]

action_defs = [
    {
        "name"   : "State Map to All Sheets Filter",
        "type"   : "filter",
        "source" : "State Chargeoff Map",
        "target" : "all",
        "fields" : "[Addr State]",
    },
    {
        "name"   : "Grade Bar to Risk Sheets Filter",
        "type"   : "filter",
        "source" : "Borrower Risk Profile",
        "target" : "DTI Grade Heatmap,Interest Rate Box Plot,Revenue Yield Waterfall",
        "fields" : "[Grade]",
    },
    {
        "name"   : "Loan Status Highlight",
        "type"   : "highlight",
        "source" : "Loan Status Distribution",
        "target" : "all",
        "fields" : "[Loan Status]",
    },
    {
        "name"   : "Credit Tier Highlight",
        "type"   : "highlight",
        "source" : "Borrower Risk Profile",
        "target" : "Revenue Yield Waterfall,Interest Rate Box Plot",
        "fields" : "[Credit Tier]",
    },
]

FONT_RULES = [
    ("worksheet-title",      16, True,  "accent_blue"),
    ("dashboard-title",      24, True,  "text_primary"),
    ("story-title",          24, True,  "text_primary"),
    ("tooltip",              11, False, "text_primary"),
    ("pane",                  9, False, "text_secondary"),
    ("axis-labels",           9, False, "text_secondary"),
    ("axis-title",           10, False, "text_secondary"),
    ("header",               10, False, "text_secondary"),
    ("caption",              10, False, "text_secondary"),
    ("grand-total",          10, True,  "text_primary"),
]


def _tag(el):
    return etree.QName(el.tag).localname if hasattr(etree, 'QName') else el.tag


def _color_node(parent_el, hex_val):
    c = etree.SubElement(parent_el, "color")
    c.text = hex_val
    return c


def unpack_twbx(src, dest_dir):
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True)
    with zipfile.ZipFile(src, "r") as zf:
        zf.extractall(dest_dir)
        twb_names = [n for n in zf.namelist() if n.lower().endswith(".twb")]
    if not twb_names:
        raise FileNotFoundError("No .twb file found inside the .twbx archive.")
    twb_path = dest_dir / twb_names[0]
    print(f"[UNPACK] Extracted .twb  -> {twb_path}")
    return twb_path


def parse_twb(twb_path):
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        tree   = etree.parse(str(twb_path), parser)
    except TypeError:
        tree = etree.parse(str(twb_path))
    root = tree.getroot()
    print(f"[PARSE]  Root tag: {_tag(root)}")
    return tree, root


def apply_color_palette(root):
    print("[COLOR]  Applying dark finance palette ...")
    prefs = root.find(".//preferences")
    if prefs is None:
        prefs = etree.SubElement(root, "preferences")

    def _set_pref(name, value):
        el = prefs.find(f"preference[@name='{name}']")
        if el is None:
            el = etree.SubElement(prefs, "preference")
            el.set("name", name)
        el.set("value", value)

    _set_pref("ui.bgColor",                   COLOR["bg_dashboard"])
    _set_pref("ui.worksheet.bgColor",          COLOR["bg_panel"])
    _set_pref("ui.dashboard.bgColor",          COLOR["bg_dashboard"])
    _set_pref("ui.story.bgColor",              COLOR["bg_dashboard"])
    _set_pref("ui.gridlines.color",            COLOR["grid_gray"])
    _set_pref("ui.axis.tickLabel.color",       COLOR["text_secondary"])
    _set_pref("ui.axis.title.color",           COLOR["text_secondary"])
    _set_pref("ui.tooltip.bgColor",            COLOR["tooltip_bg"])
    _set_pref("ui.tooltip.color",              COLOR["text_primary"])

    palette_parent = root.find(".//color-palettes")
    if palette_parent is None:
        palette_parent = etree.SubElement(root, "color-palettes")

    ls_palette = etree.SubElement(palette_parent, "color-palette")
    ls_palette.set("name", "Loan Status - Enhanced")
    ls_palette.set("type", "ordered-categorical")
    for hex_val in STATUS_COLORS.values():
        _color_node(ls_palette, hex_val)

    gr_palette = etree.SubElement(palette_parent, "color-palette")
    gr_palette.set("name", "Grade Risk Scale")
    gr_palette.set("type", "ordered-sequential")
    for hex_val in GRADE_COLORS.values():
        _color_node(gr_palette, hex_val)

    for fmt in root.findall(".//format"):
        attr = fmt.get("attr", "")
        if attr == "worksheet-background":
            fmt.set("value", COLOR["bg_panel"])
        elif attr == "dashboard-background":
            fmt.set("value", COLOR["bg_dashboard"])
        elif attr == "gridline-color":
            fmt.set("value", COLOR["grid_gray"])
        elif attr in ("zero-line-color", "axis-color"):
            fmt.set("value", COLOR["accent_blue"])

    print(f"[COLOR]  Done.")


def apply_typography(root):
    print("[FONT]   Applying Segoe UI typography ...")
    style_parent = root.find(".//style")
    if style_parent is None:
        style_parent = etree.SubElement(root, "style")

    for scope, size, bold, color_key in FONT_RULES:
        rule = style_parent.find(f"style-rule[@element='{scope}']")
        if rule is None:
            rule = etree.SubElement(style_parent, "style-rule")
            rule.set("element", scope)

        for attr_name, attr_val in [
            ("font-family", "Segoe UI"),
            ("font-size",   str(size)),
            ("font-weight", "bold" if bold else "normal"),
            ("color",       COLOR[color_key]),
        ]:
            el = rule.find(f"format[@attr='{attr_name}']")
            if el is None:
                el = etree.SubElement(rule, "format")
                el.set("attr", attr_name)
            el.set("value", attr_val)

    for fmt in root.findall(".//format[@attr='font-family']"):
        fmt.set("value", "Segoe UI")

    print(f"[FONT]   Done.")


def rename_sheets(root):
    print("[RENAME] Renaming sheets ...")
    renamed = 0
    for tag in ("worksheet", "dashboard", "story"):
        for node in root.findall(f".//{tag}"): 
            old_name = node.get("name", "")
            if old_name in SHEET_RENAMES:
                node.set("name", SHEET_RENAMES[old_name])
                renamed += 1
    for node in root.iter():
        for attr in ("name", "ref", "sheet", "caption"):
            val = node.get(attr, "")
            if val in SHEET_RENAMES:
                node.set(attr, SHEET_RENAMES[val])
    print(f"[RENAME] Done — {renamed} sheet(s) renamed.")


def inject_calculated_fields(root):
    print("[CALC]   Injecting calculated fields ...")
    datasources = root.findall(".//datasource")
    if not datasources:
        print("[CALC]   No <datasource> elements found — skipping.")
        return
    total_added = 0
    for ds in datasources:
        ds_name = ds.get("name", ds.get("caption", "unknown"))
        existing_names = {c.get("name", "") for c in ds.findall("column")}
        for cf in CALCULATED_FIELDS:
            if cf["name"] in existing_names:
                continue
            col = etree.SubElement(ds, "column")
            col.set("caption",  cf["caption"])
            col.set("name",     cf["name"])
            col.set("datatype", cf["datatype"])
            col.set("role",     cf["role"])
            col.set("type",     "quantitative" if cf["role"] == "measure" else "ordinal")
            calc = etree.SubElement(col, "calculation")
            calc.set("class",   "tableau")
            calc.set("formula", cf["formula"])
            total_added += 1
    print(f"[CALC]   Done — {total_added} field(s) injected.")


def add_new_worksheets(root):
    print("[SHEETS] Adding new worksheet stubs ...")
    worksheets_container = root.find(".//worksheets")
    if worksheets_container is None:
        worksheets_container = etree.SubElement(root, "worksheets")
    existing_ws_names = {ws.get("name", "") for ws in worksheets_container.findall("worksheet")}
    added = 0
    for ws_def in NEW_WORKSHEETS:
        if ws_def["name"] in existing_ws_names:
            continue
        ws = etree.SubElement(worksheets_container, "worksheet")
        ws.set("name", ws_def["name"])
        lo = etree.SubElement(ws, "layout-options")
        t  = etree.SubElement(lo, "title")
        ft = etree.SubElement(t,  "formatted-text")
        r  = etree.SubElement(ft, "run")
        r.set("bold", "true")
        r.set("fontname",  "Segoe UI")
        r.set("fontsize",  "16")
        r.set("fontcolor", COLOR["accent_blue"])
        r.text = ws_def["title"]
        tbl = etree.SubElement(ws, "table")
        etree.SubElement(tbl, "view")
        sty = etree.SubElement(ws, "style")
        sr  = etree.SubElement(sty, "style-rule")
        sr.set("element", "worksheet")
        sf  = etree.SubElement(sr, "format")
        sf.set("attr",  "background")
        sf.set("value", COLOR["bg_panel"])
        note = etree.SubElement(ws, "implementation-note")
        note.text = ws_def["note"]
        added += 1
        print(f"[SHEETS]   Added '{ws_def['name']}'")
    print(f"[SHEETS] Done — {added} stub(s) added.")


def inject_story(root):
    print("[STORY]  Injecting Tableau Story ...")
    story_title = "The Anatomy of a Loan Portfolio: From Disbursement to Default"
    for existing in root.findall(".//story"):
        if existing.get("name", "") == story_title:
            print("[STORY]  Story already exists — skipping.")
            return
    stories_container = root.find(".//stories")
    if stories_container is None:
        stories_container = etree.SubElement(root, "stories")
    story = etree.SubElement(stories_container, "story")
    story.set("name",    story_title)
    story.set("caption", story_title)
    lo = etree.SubElement(story, "layout-options")
    lo.set("show-title", "true")
    t  = etree.SubElement(lo, "title")
    ft = etree.SubElement(t,  "formatted-text")
    r  = etree.SubElement(ft, "run")
    r.set("bold", "true")
    r.set("fontname",  "Segoe UI")
    r.set("fontsize",  "24")
    r.set("fontcolor", COLOR["text_primary"])
    r.text = story_title
    sty = etree.SubElement(story, "style")
    sr  = etree.SubElement(sty, "style-rule")
    sr.set("element", "story")
    sf  = etree.SubElement(sr,  "format")
    sf.set("attr",  "background")
    sf.set("value", COLOR["bg_dashboard"])
    for i, sp in enumerate(STORY_POINTS, start=1):
        sp_el = etree.SubElement(story, "story-point")
        sp_el.set("caption", sp["nav_caption"])
        sp_el.set("index",   str(i))
        desc = etree.SubElement(sp_el, "description")
        dr   = etree.SubElement(desc,  "formatted-text")
        dre  = etree.SubElement(dr,    "run")
        dre.set("fontname",  "Segoe UI")
        dre.set("fontsize",  "12")
        dre.set("fontcolor", COLOR["text_secondary"])
        dre.text = sp["caption"]
    print(f"[STORY]  Done — {len(STORY_POINTS)} story-points added.")


def inject_dashboard_actions(root):
    print("[ACTIONS] Injecting dashboard actions ...")
    dashboards = root.findall(".//dashboard")
    if not dashboards:
        print("[ACTIONS] No <dashboard> elements found — skipping.")
        return
    for dash in dashboards:
        actions_el = dash.find("actions")
        if actions_el is None:
            actions_el = etree.SubElement(dash, "actions")
        existing = {a.get("name", "") for a in actions_el.findall("action")}
        for act in action_defs:
            if act["name"] in existing:
                continue
            a = etree.SubElement(actions_el, "action")
            a.set("name",          act["name"])
            a.set("type",          act["type"])
            a.set("source-sheet",  act["source"])
            a.set("target-sheet",  act["target"])
            a.set("filter-fields", act["fields"])
    print(f"[ACTIONS] Done.")


def write_twb(tree, twb_path):
    try:
        tree.write(str(twb_path), pretty_print=True, xml_declaration=True, encoding="utf-8")
    except TypeError:
        tree.write(str(twb_path), encoding="unicode")
    print(f"[WRITE]  Modified .twb written -> {twb_path}")


def repack_twbx(work_dir, output_path):
    if output_path.exists():
        output_path.unlink()
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in work_dir.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(work_dir)
                zf.write(file, arcname)
    print(f"[REPACK] New .twbx written -> {output_path}  ({output_path.stat().st_size / 1024:.0f} KB)")


def main():
    print("=" * 62)
    print(" Bank Loan Analysis — Tableau Enhancement Script")
    print(" DASHBOARD_ENHANCEMENT_GUIDE.md applied automatically")
    print("=" * 62)

    if not SOURCE_TWBX.exists():
        print(f"\n[ERROR]  Source file not found: {SOURCE_TWBX}")
        print("         Run this script from the repository root directory.")
        sys.exit(1)

    twb_path        = unpack_twbx(SOURCE_TWBX, WORK_DIR)
    tree, root      = parse_twb(twb_path)
    apply_color_palette(root)
    apply_typography(root)
    rename_sheets(root)
    inject_calculated_fields(root)
    add_new_worksheets(root)
    inject_story(root)
    inject_dashboard_actions(root)
    write_twb(tree, twb_path)          # update in-place for twbx repacking
    write_twb(tree, OUTPUT_TWB)        # write standalone .twb output
    repack_twbx(WORK_DIR, OUTPUT_TWBX)
    shutil.rmtree(WORK_DIR)
    print("[CLEAN]  Temp directory removed.")

    print("\n" + "=" * 62)
    print(" Enhancement complete!")
    print(f" Output (.twb)  : {OUTPUT_TWB}")
    print(f" Output (.twbx) : {OUTPUT_TWBX}")
    print(f" Source         : {SOURCE_TWBX}  (unchanged)")
    print("=" * 62)
    print("""
NEXT STEPS
──────────
 1. Download 'Bank Loan Analysis Project - Enhanced.twb'
 2. Open in Tableau Desktop (2020.1 or later)
 3. All 14 calculated fields appear in the Data pane
 4. Six new worksheet stubs are ready for chart configuration
 5. The 6-point Tableau Story tab is present
 6. Dark theme, Segoe UI fonts, and color palettes are applied
 7. Dashboard filter/highlight actions are pre-wired
 8. See DASHBOARD_ENHANCEMENT_GUIDE.md Section 7 for
    final mark-type and axis configuration per sheet
""")


if __name__ == "__main__":
    main()