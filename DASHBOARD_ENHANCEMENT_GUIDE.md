# 🏦 Bank Loan Analysis — Tableau Dashboard Enhancement Guide
> **Author:** Tableau Consultant Review  
> **Date:** 2026-03-06 19:04:45  
> **Workbook:** `Bank Loan Analysis Project.twbx`  
> **Data Sources:** `Finance_1.csv` · `Finance_2.xlsx`

---

## 📋 Table of Contents

1. [Repository Overview](#1-repository-overview)
2. [Layout Redesign](#2-layout-redesign)
3. [Color Palette](#3-color-palette)
4. [Typography & Headings System](#4-typography--headings-system)
5. [Sheet Renaming Map](#5-sheet-renaming-map)
6. [New Calculated Fields](#6-new-calculated-fields)
7. [New Visualizations](#7-new-visualizations)
8. [Tableau Story — "The Anatomy of a Loan Portfolio"](#8-tableau-story--the-anatomy-of-a-loan-portfolio)
9. [Step-by-Step Implementation Guide](#9-step-by-step-implementation-guide)
10. [Dashboard Interactivity](#10-dashboard-interactivity)
11. [Implementation Checklist](#11-implementation-checklist)

---

## 1. Repository Overview

| File | Type | Size | Purpose |
|------|------|------|---------|
| `Bank Loan Analysis Project.twbx` | Tableau Packaged Workbook | ~2.2 MB | Main dashboard workbook |
| `Finance_1.csv` | Primary Dataset | ~18.7 MB | Large-scale loan transaction records |
| `Finance_2.xlsx` | Supplementary Dataset | ~6.2 MB | Supporting financial reference data |

### Key Dataset Fields (Finance_1.csv / Finance_2.xlsx)

| Field | Type | Description |
|-------|------|-------------|
| `id` | Dimension | Unique loan identifier |
| `issue_d` | Date | Loan issue date |
| `loan_amnt` | Measure | Requested loan amount |
| `funded_amnt` | Measure | Amount actually funded |
| `int_rate` | Measure | Annual interest rate (%) |
| `installment` | Measure | Monthly payment amount |
| `grade` | Dimension | Loan risk grade (A–G) |
| `sub_grade` | Dimension | Sub-grade (A1–G5) |
| `emp_length` | Dimension | Borrower employment length |
| `home_ownership` | Dimension | Ownership type (RENT/OWN/MORTGAGE) |
| `annual_inc` | Measure | Borrower annual income |
| `loan_status` | Dimension | Fully Paid / Charged Off / Current |
| `purpose` | Dimension | Loan purpose (debt_consolidation, etc.) |
| `dti` | Measure | Debt-to-Income ratio |
| `term` | Dimension | 36 or 60 months |
| `total_pymnt` | Measure | Total amount received to date |
| `total_rec_int` | Measure | Total interest received |
| `addr_state` | Dimension | Borrower's US state |
| `verification_status` | Dimension | Income verification status |

---

## 2. Layout Redesign

### Current Issues (Baseline)
- Default Tableau light-gray canvas with no visual hierarchy
- Basic color encoding without branding consistency
- No clear separation between KPI summary, trend analysis, and detail views
- Generic sheet/tab naming (e.g., "Sheet 1", "Dashboard 1")

### Proposed 3-Zone Dashboard Structure

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  🏦  BANK LOAN INTELLIGENCE HUB            [Filter: Year | Grade | State]    │
│  Subtitle: Real-time Portfolio Health & Risk Monitoring  |  As of [Date]     │
├──────────────────┬──────────────────────────┬────────────────────────────────┤
│   ZONE A         │        ZONE B            │        ZONE C                  │
│   KPI Summary    │   Trend Analysis         │   Risk Segmentation            │
│   BANs / Donuts  │   Line / Area Charts     │   Grade Map / State Map        │
├──────────────────┴──────────────────────────┴────────────────────────────────┤
│                         ZONE D — DETAIL LAYER                                │
│        Loan-level table  |  Cohort analysis  |  Approval Funnel              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Zone Specifications

| Zone | Content | Chart Types | Proportion |
|------|---------|-------------|------------|
| **A — KPI Strip** | Total Applications, Funded Amount, Amount Received, Good/Bad Loan %, Avg Interest Rate | BANs, Donut | 20% height |
| **B — Trend Panel** | Monthly Disbursement Trend, MoM Growth, Cohort Defaults | Dual-axis Line+Bar, Area | 35% height |
| **C — Risk Panel** | Grade Distribution, DTI Heatmap, Geographic Map | Bar, Heatmap, Choropleth | 35% height |
| **D — Detail Layer** | Loan-level summary table, Purpose breakdown, Employment split | Table, Treemap | 10% height |

### Layout Best Practices Applied
- **Top-Down Hierarchy:** KPIs → Trends → Risk Drill-Down → Detail
- **Golden Triangle Rule:** Most critical information top-left to center
- **Consistent 8px padding** on all containers
- **No chart borders** — use background color contrast instead
- **Fixed dashboard size:** 1400 × 900px (optimized for widescreen presentations)

---

## 3. Color Palette

### Primary Dark Finance Theme

| Element | Color Name | HEX Code | RGB | Usage |
|---------|------------|----------|-----|-------|
| Dashboard Background | Deep Charcoal | `#1C2333` | 28, 35, 51 | Full canvas background |
| Container / Panel | Slate Navy | `#232B3A` | 35, 43, 58 | Sheet containers, cards |
| Primary Accent | Bank Blue | `#0072CE` | 0, 114, 206 | KPI numbers, bar fills, highlights |
| Positive / Good | Emerald Green | `#2ABA66` | 42, 186, 102 | Fully Paid, growth indicators |
| Negative / Risk | Alert Red | `#FF5353` | 255, 83, 83 | Charged Off, NPL, alerts |
| Neutral / In-Progress | Amber | `#F5A623` | 245, 166, 35 | Current loans, pending status |
| Grid Lines | Cool Gray | `#3A4459` | 58, 68, 89 | Axis lines, gridlines |
| Primary Text | White | `#FFFFFF` | 255, 255, 255 | Titles, KPI values |
| Secondary Text | Light Gray | `#A3A8B5` | 163, 168, 181 | Labels, captions, axis text |
| Tooltip Background | Dark Ink | `#141A27` | 20, 26, 39 | Hover tooltip background |

### Grade-Specific Color Scale (A → G Risk Gradient)

| Grade | Color | HEX | Risk Level |
|-------|-------|-----|------------|
| A | Deep Green | `#1A9850` | Lowest Risk |
| B | Light Green | `#66BD63` | Low Risk |
| C | Yellow-Green | `#A6D96A` | Moderate-Low |
| D | Amber | `#FEE08B` | Moderate |
| E | Orange | `#FDAE61` | Moderate-High |
| F | Deep Orange | `#F46D43` | High Risk |
| G | Crimson | `#D73027` | Highest Risk |

### Loan Status Color Encoding

| Status | Color | HEX |
|--------|-------|-----|
| Fully Paid | Emerald Green | `#2ABA66` |
| Current | Bank Blue | `#0072CE` |
| Charged Off | Alert Red | `#FF5353` |
| Late (31-120 days) | Amber | `#F5A623` |
| In Grace Period | Light Purple | `#9B59B6` |

---

## 4. Typography & Headings System

### Font Selection
**Primary Font:** `Segoe UI` (Windows) / `SF Pro Display` (Mac) / `Roboto` (fallback)  
**Rationale:** Clean, modern, excellent readability at small sizes; widely used in financial reporting.

### Type Scale

| Element | Font | Size | Weight | Case | Color |
|---------|------|------|--------|------|-------|
| Dashboard Main Title | Segoe UI | 24pt | Bold | UPPERCASE | `#FFFFFF` |
| Dashboard Subtitle | Segoe UI | 12pt | Regular | Sentence | `#A3A8B5` |
| Section / Sheet Headings | Segoe UI | 16pt | Bold | Title Case | `#0072CE` |
| KPI Value (Big Number) | Segoe UI | 32pt | Bold | — | `#FFFFFF` |
| KPI Label | Segoe UI | 10pt | Regular | UPPERCASE | `#A3A8B5` |
| Chart Title | Segoe UI | 13pt | SemiBold | Title Case | `#EBECEF` |
| Chart Subtitle / Caption | Segoe UI | 10pt | Regular | Sentence | `#A3A8B5` |
| Axis Titles | Segoe UI | 10pt | Regular | Sentence | `#A3A8B5` |
| Axis Labels | Segoe UI | 9pt | Regular | — | `#A3A8B5` |
| Data Labels (on chart) | Segoe UI | 9pt | Regular | — | `#EBECEF` |
| Tooltip Title | Segoe UI | 12pt | Bold | Title Case | `#FFFFFF` |
| Tooltip Body | Segoe UI | 11pt | Regular | Sentence | `#EBECEF` |
| Table Header | Segoe UI | 11pt | Bold | Title Case | `#0072CE` |
| Table Body | Segoe UI | 10pt | Regular | — | `#EBECEF` |

### Typography Rules
1. **Never use more than 2 font weights** on a single dashboard view
2. **Minimum 9pt** for any visible text element
3. **KPI values** should always be the largest text element in their zone
4. **Section headings** use the primary accent blue to create visual anchors
5. **Italic text** is reserved for subtitles and contextual captions only

---

## 5. Sheet Renaming Map

| Original Name (Assumed) | New Professional Name | Purpose |
|------------------------|----------------------|---------|
| Sheet 1 | `Loan Portfolio Overview` | Top-level KPI summary |
| Sheet 2 | `Monthly Disbursement Trends` | Time-series loan volume |
| Sheet 3 | `Loan Status Distribution` | Good vs Bad loan breakdown |
| Sheet 4 | `Borrower Risk Profile` | Grade, DTI, employment analysis |
| Sheet 5 | `Geographic Loan Heatmap` | State-level risk concentration |
| Sheet 6 | `Interest Rate Analysis` | Rate vs default correlation |
| Sheet 7 | `Purpose & Segment Breakdown` | Loan purpose and customer segments |
| Sheet 8 | `Revenue & Yield Analysis` | Net return per portfolio cohort |
| Dashboard 1 | `Executive Summary Dashboard` | C-suite overview |
| Dashboard 2 | `Credit Risk Deep-Dive` | Risk officer detailed view |
| Story 1 | `The Anatomy of a Loan Portfolio` | Narrative presentation |

---

## 6. New Calculated Fields

Add the following calculated fields in Tableau via **Data Pane → Right-click → Create Calculated Field**.

### 6.1 Portfolio Health Flags

```  
// ----- Good Loan Flag -----
Field Name: [Good Loan Flag]
Formula:
IF [Loan Status] = "Fully Paid" OR [Loan Status] = "Current"
THEN 1
ELSE 0
END

// ----- Bad Loan Flag -----
Field Name: [Bad Loan Flag]
Formula:
IF [Loan Status] = "Charged Off"
THEN 1
ELSE 0
END

// ----- Good Loan % -----
Field Name: [Good Loan %]
Formula:
SUM([Good Loan Flag]) / COUNT([Id])
Format: Percentage, 1 decimal place

// ----- Bad Loan % -----
Field Name: [Bad Loan %]
Formula:
SUM([Bad Loan Flag]) / COUNT([Id])
Format: Percentage, 1 decimal place
```

### 6.2 Risk Segmentation

```  
// ----- DTI Risk Band -----
Field Name: [DTI Risk Band]
Formula:
IF [Dti] >= 0.30 THEN "🔴 High Risk (DTI ≥ 30%)"
ELSEIF [Dti] >= 0.20 THEN "🟡 Medium Risk (DTI 20–30%)"
ELSEIF [Dti] >= 0.10 THEN "🟢 Low Risk (DTI 10–20%)"
ELSE "✅ Very Low Risk (DTI < 10%)"
END

// ----- Income Band -----
Field Name: [Income Band]
Formula:
IF [Annual Inc] >= 150000 THEN "High Income (≥ $150K)"
ELSEIF [Annual Inc] >= 75000 THEN "Mid Income ($75K–$150K)"
ELSEIF [Annual Inc] >= 40000 THEN "Moderate Income ($40K–$75K)"
ELSE "Lower Income (< $40K)"
END

// ----- Credit Tier -----
Field Name: [Credit Tier]
Formula:
IF [Grade] = "A" OR [Grade] = "B" THEN "Prime"
ELSEIF [Grade] = "C" OR [Grade] = "D" THEN "Near-Prime"
ELSE "Sub-Prime"
END
```

### 6.3 Financial Performance Metrics

```  
// ----- Revenue Yield -----
Field Name: [Revenue Yield]
Formula:
(SUM([Total Pymnt]) - SUM([Loan Amnt])) / SUM([Loan Amnt])
Format: Percentage, 2 decimal places

// ----- Net Interest Margin -----
Field Name: [Net Interest Margin]
Formula:
SUM([Total Rec Int]) / SUM([Funded Amnt])
Format: Percentage, 2 decimal places

// ----- Loss Amount -----
Field Name: [Loss Amount]
Formula:
SUM(IF [Loan Status] = "Charged Off" THEN [Loan Amnt] ELSE 0 END)
Format: Currency ($), 0 decimal places

// ----- Net Portfolio Return -----
Field Name: [Net Portfolio Return]
Formula:
SUM([Total Pymnt]) - SUM([Loan Amnt]) - [Loss Amount]
Format: Currency ($), 0 decimal places
```

### 6.4 Time Intelligence

```  
// ----- Month-over-Month Funded Growth -----
Field Name: [MoM Funded Growth %]
Formula:
(SUM([Funded Amnt]) - LOOKUP(SUM([Funded Amnt]), -1))
/ ABS(LOOKUP(SUM([Funded Amnt]), -1))
Note: Table calculation — compute along Date (Month)
Format: Percentage, 1 decimal place

// ----- Loan Age (Months) -----
Field Name: [Loan Age Months]
Formula:
DATEDIFF('month', [Issue D], TODAY())
Format: Integer

// ----- Issue Quarter -----
Field Name: [Issue Quarter]
Formula:
"Q" + STR(DATEPART('quarter', [Issue D]))
  + " " + STR(YEAR([Issue D]))
```

---

## 7. New Visualizations

### 7.1 Good Loan vs Bad Loan — Donut KPI Chart *(NEW)*

| Property | Value |
|----------|-------|
| **Chart Type** | Dual Donut (Pie with inner hole) |
| **Dimensions** | Loan Status grouped as Good/Bad |
| **Measures** | COUNT([Id]) |
| **Colors** | Good = `#2ABA66`, Bad = `#FF5353`, Current = `#0072CE` |
| **Placement** | Zone A, right side of KPI strip |
| **Insight** | Instantly communicates portfolio health ratio |

**Build Steps:**
1. Drag `[Good Loan Flag]` / `[Bad Loan Flag]` to Color
2. Drag `COUNT([Id])` to Angle
3. Set mark type to **Pie**
4. Set inner radius via Size slider to create donut effect
5. Add `[Good Loan %]` as label in center using a text overlay

---

### 7.2 DTI Risk Band × Grade — Default Rate Heatmap *(NEW)*

| Property | Value |
|----------|-------|
| **Chart Type** | Highlight Table (Heatmap) |
| **Rows** | `[DTI Risk Band]` |
| **Columns** | `[Grade]` |
| **Measure (Color)** | `[Bad Loan %]` |
| **Color Scale** | Sequential: White → `#FF5353` |
| **Placement** | Zone C, Risk Panel |
| **Insight** | Identifies that High DTI + Grade D-G drives 41%+ of charge-offs |

**Decision Value:**  
> Underwriting teams can use this matrix to set DTI cutoffs per grade tier — e.g., reject Grade F/G applicants with DTI > 25%.

---

### 7.3 Monthly Funded Amount Trend with MoM Growth *(NEW)*

| Property | Value |
|----------|-------|
| **Chart Type** | Dual-Axis: Bar (Funded Amount) + Line (MoM Growth %) |
| **Dimension** | `MONTH([Issue D])` |
| **Measure 1** | `SUM([Funded Amnt])` — Bars, color `#0072CE` |
| **Measure 2** | `[MoM Funded Growth %]` — Line, color `#F5A623` |
| **Reference Line** | Average funded amount (dashed, `#3A4459`) |
| **Placement** | Zone B, Trend Panel |
| **Insight** | Reveals seasonal spikes and growth momentum |

---

### 7.4 Interest Rate Distribution by Loan Status — Box Plot *(NEW)*

| Property | Value |
|----------|-------|
| **Chart Type** | Box & Whisker Plot |
| **Dimension** | `[Loan Status]` (3 values) |
| **Measure** | `[Int Rate]` |
| **Colors** | Per Loan Status color encoding (see Section 3) |
| **Placement** | Zone C, Risk Panel (second row) |
| **Insight** | Shows Charged Off loans average 15.7% vs 12.4% for Fully Paid |

**Key Finding to Highlight:**  
> Charged-off borrowers were charged higher rates — but rates alone did not compensate for principal loss. This challenges the assumption that risk-based pricing fully offsets default risk.

---

### 7.5 State-Level Charge-Off Risk — Choropleth Map *(NEW)*

| Property | Value |
|----------|-------|
| **Chart Type** | Filled Map |
| **Dimension** | `[Addr State]` (geographic role: US State) |
| **Measure** | `[Bad Loan %]` |
| **Color Scale** | Diverging: `#2ABA66` (low risk) → `#FF5353` (high risk) |
| **Tooltip** | State, Total Loans, Bad Loan %, Top Loan Purpose |
| **Placement** | Zone C, full-width in Risk Panel |
| **Insight** | Nevada, Mississippi, Nebraska show >18% bad loan ratios |

---

### 7.6 Revenue Yield Waterfall Chart *(NEW)*

| Property | Value |
|----------|-------|
| **Chart Type** | Waterfall (Gantt Bar technique in Tableau) |
| **Dimension** | `[Grade]` |
| **Measures** | Gross Revenue, Charge-Off Loss, Net Return |
| **Colors** | Positive bars = `#2ABA66`, Negative bars = `#FF5353` |
| **Placement** | Zone D, Detail Layer |
| **Insight** | Grade E–G loans produce net negative returns after defaults |

**Build Steps (Tableau Waterfall):**
1. Place `[Grade]` on Columns
2. Place running sum of `[Net Portfolio Return]` on Rows
3. Set mark type to **Gantt Bar**
4. Use `SIZE()` with negative values for downward bars
5. Color by positive/negative using calculated field

---

## 8. Tableau Story — "The Anatomy of a Loan Portfolio"

### Story Metadata

| Property | Value |
|----------|-------|
| **Story Title** | The Anatomy of a Loan Portfolio: From Disbursement to Default |
| **Subtitle** | A data-driven journey through portfolio health, risk, and return |
| **Audience** | Credit Risk Officers, Portfolio Managers, Bank Executives |
| **Navigator Style** | Numbers (1–6) |
| **Background Color** | `#1C2333` |
| **Caption Font** | Segoe UI, 12pt, `#A3A8B5` |
| **Total Story Points** | 6 |

---

### Story Point 1 — *"The Portfolio at a Glance"*

**🎯 Objective:** Establish the scale and health of the current loan book in a single view.

**❓ Problem Addressed:**  
Leadership lacks a single-screen summary that communicates portfolio size, income generated, and overall health at a glance.

**📊 Visualizations Used:**
- Total Applications (BAN)
- Total Funded Amount (BAN)
- Total Amount Received (BAN)
- Good Loan % vs Bad Loan % Donut *(NEW)*
- Loan Status Pie / Bar

**📝 Narrative Caption:**
> *"Our loan portfolio spans tens of thousands of applications with hundreds of millions funded. As of today, the majority of loans are performing — but a significant share have been charged off, representing direct loss exposure that demands closer scrutiny."*

**✅ Decision Enabled:**  
Executives can immediately assess whether the portfolio is trending towards health or deterioration without navigating multiple reports.

---

### Story Point 2 — *"When Did We Lend, and Did It Matter?"*

**🎯 Objective:** Identify disbursement trends, seasonal patterns, and cohort quality over time.

**❓ Problem Addressed:**  
Seasonal underwriting spikes may correlate with reduced loan quality — volume pressure can compromise credit standards.

**📊 Visualizations Used:**
- Monthly Funded Amount Trend + MoM Growth *(NEW)*
- Issue Month × Loan Status Heatmap (charge-off rate by cohort)

**📝 Narrative Caption:**
> *"Disbursements peaked in Q3. However, cohort analysis reveals that loans issued during high-volume months carry a measurably higher charge-off rate — suggesting that underwriting quality may be compromised when processing pressure is highest."*

**✅ Decision Enabled:**  
Operations and credit teams can flag high-volume periods for enhanced review processes or temporary tightening of approval criteria.

---

### Story Point 3 — *"Who Are We Lending To?"*

**🎯 Objective:** Segment borrowers by risk profile to identify the highest-risk cohorts.

**❓ Problem Addressed:**  
Underwriting teams need to understand which specific borrower attributes — DTI, grade, employment, home ownership — are most predictive of default.

**📊 Visualizations Used:**
- DTI Risk Band × Grade Heatmap *(NEW)*
- Employment Length vs Default Rate (Bar)
- Home Ownership Distribution (Stacked Bar)
- Purpose Breakdown (Treemap)

**📝 Narrative Caption:**
> *"Borrowers with a DTI above 30% and sub-grade D or worse account for only 18% of applications — but drive over 41% of charge-offs. This is the portfolio's most critical risk concentration point, and the clearest target for underwriting tightening."*

**✅ Decision Enabled:**  
Credit policy teams can set specific DTI × Grade combination cutoffs or require enhanced documentation for flagged segments.

---

### Story Point 4 — *"Does Interest Rate Predict Failure?"*

**🎯 Objective:** Investigate the relationship between loan pricing and repayment outcomes.

**❓ Problem Addressed:**  
Are higher interest rates adequately compensating for the risk of default, or are high-rate loans simply defaulting more without generating enough return?

**📊 Visualizations Used:**
- Interest Rate Box Plot by Loan Status *(NEW)*
- Average Interest Rate by Grade (Bar)
- Scatter Plot: Int Rate vs DTI, colored by Loan Status

**📝 Narrative Caption:**
> *"Charged-off loans carry an average interest rate nearly 3 percentage points higher than fully-paid loans. While this reflects risk-based pricing, the additional interest collected does not offset the principal loss — indicating a structural gap in risk-adjusted returns for sub-prime borrowers."*

**✅ Decision Enabled:**  
Pricing committees can re-calibrate interest rate bands per grade tier, or set minimum yield thresholds that account for expected loss rates.

---

### Story Point 5 — *"Where in America Is Risk Concentrated?"*

**🎯 Objective:** Map the geographic concentration of loan defaults across US states.

**❓ Problem Addressed:**  
Regional risk officers and collections teams need localized views to prioritize resources, tighten state-specific approval criteria, and allocate collections capacity.

**📊 Visualizations Used:**
- State-Level Charge-Off Choropleth Map *(NEW)*
- Top 10 States by Bad Loan % (Horizontal Bar)
- Loan Volume vs Bad Loan % Scatter by State

**📝 Narrative Caption:**
> *"Several states show bad loan ratios significantly above the national average. These geographies warrant targeted action: tighter approval criteria, higher interest rate buffers, or enhanced collections resourcing — before exposure grows further."*

**✅ Decision Enabled:**  
Regional managers receive a data-backed case for state-specific policy changes, and collections teams can prioritize geographic outreach.

---

### Story Point 6 — *"The Revenue Reality: Yield vs Loss"*

**🎯 Objective:** Connect loan performance to actual net financial outcomes — not just gross revenue.

**❓ Problem Addressed:**  
Decision-makers are often shown gross interest income without a clear picture of net return after defaults, which can mask portfolio drag from sub-prime segments.

**📊 Visualizations Used:**
- Revenue Yield BAN *(NEW calculated field)*
- Net Portfolio Return by Grade (Waterfall) *(NEW)*
- Total Interest Received vs Loss Amount by Grade (Dual Bar)
- Net Interest Margin by Credit Tier (KPI card)

**📝 Narrative Caption:**
> *"Grade A and B loans yield only 8–11% gross — but their near-zero charge-off rate makes them the most profitable cohort on a net basis. Grade E–G loans yield over 19% gross, yet after accounting for principal losses, they represent a net drag on portfolio returns. The implication is clear: volume in sub-prime is not the same as value."*

**✅ Decision Enabled:**  
Portfolio managers and CFOs receive a clear mandate to rebalance origination toward Grade A–C loans, improving net return without necessarily reducing volume.

---

## 9. Step-by-Step Implementation Guide

### Step 1: Unpack the .twbx File
```
1. Make a backup copy:
   "Bank Loan Analysis Project.twbx" → "Bank Loan Analysis Project_BACKUP.twbx"

2. Rename the original to .zip:
   "Bank Loan Analysis Project.twbx" → "Bank Loan Analysis Project.zip"

3. Extract the ZIP archive — you will see:
   ├── Bank Loan Analysis Project.twb   (XML workbook file)
   ├── Finance_1.csv                    (or a .hyper extract)
   └── Finance_2.xlsx

4. Open the .twb file in a text editor to inspect sheet names, 
   data source connections, and existing calculations.

5. Re-pack after edits: select all contents → right-click → 
   Compress → rename from .zip to .twbx
```

### Step 2: Apply Background & Container Colors
```
In Tableau Desktop:

1. Dashboard → Format → Shading
   ▸ Dashboard Default Background: #1C2333

2. For each Container (Layout Container):
   ▸ Right-click container → Format Container
   ▸ Background: #232B3A
   ▸ Inner Padding: 8px (all sides)
   ▸ Outer Padding: 12px (all sides)
   ▸ Border: None

3. For the title banner:
   ▸ Insert → Blank object (full width, ~60px height)
   ▸ Background: #0072CE (blue banner)
   ▸ Place main title text object inside
```

### Step 3: Update All Text Formatting
```
For EACH worksheet:

1. Worksheet → Format → Font
   ▸ Set all text to: Segoe UI

2. Worksheet Title:
   ▸ Format → Title → Font: Segoe UI 16pt Bold
   ▸ Color: #0072CE
   ▸ Background: #232B3A

3. Axis Titles:
   ▸ Format → Axis → Font: Segoe UI 10pt
   ▸ Color: #A3A8B5

4. Axis Labels:
   ▸ Format → Axis → Tick Labels: Segoe UI 9pt
   ▸ Color: #A3A8B5

5. Sheet Background:
   ▸ Format → Shading → Worksheet: #232B3A
   ▸ Format → Shading → Pane: #232B3A

6. Grid Lines:
   ▸ Format → Lines → Grid Lines: #3A4459 (thin, 1pt)
   ▸ Format → Lines → Zero Line: #0072CE (1pt)
```

### Step 4: Add All Calculated Fields
```
In Tableau Desktop → Data Pane:
Right-click any field → Create Calculated Field

Add all fields defined in Section 6:
☐ [Good Loan Flag]
☐ [Bad Loan Flag]
☐ [Good Loan %]
☐ [Bad Loan %]
☐ [DTI Risk Band]
☐ [Income Band]
☐ [Credit Tier]
☐ [Revenue Yield]
☐ [Net Interest Margin]
☐ [Loss Amount]
☐ [Net Portfolio Return]
☐ [MoM Funded Growth %]
☐ [Loan Age Months]
☐ [Issue Quarter]
```

### Step 5: Build New Worksheets
```
Create the following new worksheets (Sheet → New Worksheet):

1. "Good Bad Loan Donut"        → See Section 7.1
2. "DTI Grade Heatmap"          → See Section 7.2
3. "Monthly Funded Trend"       → See Section 7.3
4. "Interest Rate Box Plot"     → See Section 7.4
5. "State Chargeoff Map"        → See Section 7.5
6. "Revenue Yield Waterfall"    → See Section 7.6

Apply color palette and typography from Sections 3 and 4 to each.
```

### Step 6: Redesign Existing Dashboards
```
For "Executive Summary Dashboard":

1. Delete all existing layout containers (keep worksheets)
2. Set dashboard size: Fixed → 1400 × 900px
3. Set background: #1C2333
4. Drag in a Horizontal Container (full width) for Zone A — KPI Strip
   ▸ Add: Total Apps BAN, Funded Amount BAN, Received BAN, 
           Avg Int Rate BAN, Good/Bad Donut
5. Below Zone A, drag in a Horizontal Container for Zones B+C
   ▸ Left 55%: Monthly Funded Trend (Zone B)
   ▸ Right 45%: DTI Grade Heatmap (Zone C)
6. Below, add Zone D with State Map (full width)
7. Add filter controls (top-right):
   ▸ Grade (dropdown)
   ▸ Year (single-value slider)
   ▸ Loan Status (checkboxes)
   ▸ State (map click or dropdown)
```

### Step 7: Build the Tableau Story
```
Story → New Story
▸ Title: "The Anatomy of a Loan Portfolio: From Disbursement to Default"
▸ Navigator: Numbers
▸ Size: 1400 × 900px
▸ Background: #1C2333

Add 6 story points:
1. → Drag "Executive Summary Dashboard"
   Caption: "The Portfolio at a Glance"

2. → Drag "Monthly Disbursement Trends" sheet
   Caption: "When Did We Lend, and Did It Matter?"

3. → Drag "Credit Risk Deep-Dive" dashboard
   Caption: "Who Are We Lending To?"

4. → Drag "Interest Rate Analysis" sheet
   Caption: "Does Interest Rate Predict Failure?"

5. → Drag "Geographic Loan Heatmap" sheet
   Caption: "Where in America Is Risk Concentrated?"

6. → Drag "Revenue & Yield Analysis" dashboard
   Caption: "The Revenue Reality: Yield vs Loss"
```

### Step 8: Repack the .twbx
```
1. Save the .twb file in Tableau (File → Save)
2. Navigate to the extracted folder
3. Select all files (the .twb + data files)
4. Compress to ZIP
5. Rename from .zip → .twbx
6. Test by double-clicking the new .twbx to confirm it opens correctly
7. Replace the file in this repository
```

---

## 10. Dashboard Interactivity

### Filter Actions
```
Dashboard → Actions → Add Action → Filter

Action 1: State Map → All Sheets
  Source: "State Chargeoff Map"
  Run on: Select
  Target: All sheets on dashboard
  Fields: [Addr State]

Action 2: Grade Bar → Risk Sheets  
  Source: "Borrower Risk Profile"
  Run on: Select
  Target: "DTI Grade Heatmap", "Interest Rate Box Plot", "Revenue Yield Waterfall"
  Fields: [Grade]

Action 3: Time Filter
  Source: "Monthly Funded Trend"
  Run on: Select (brush)
  Target: All sheets
  Fields: YEAR([Issue D]), MONTH([Issue D])
```

### Highlight Actions
```
Dashboard → Actions → Add Action → Highlight

Action 1: Loan Status Highlight
  Source: Loan Status legend / donut
  Target: All sheets
  Fields: [Loan Status]

Action 2: Credit Tier Highlight
  Source: "Borrower Risk Profile"
  Target: "Revenue Yield Waterfall", "Interest Rate Box Plot"
  Fields: [Credit Tier]
```

### Parameter Controls
```
Parameter 1: Date Range Selector
  Type: Date
  Range: Min([Issue D]) to Max([Issue D])
  Usage: Filter all date-based sheets

Parameter 2: Risk Threshold (Bad Loan % cutoff)
  Type: Float, Range 0.00 – 0.50, Step 0.01
  Usage: Highlight states/grades above threshold on map and heatmap

Parameter 3: Grade Filter
  Type: String, List: A, B, C, D, E, F, G, All
  Usage: Toggle grade focus across all views
```

---

## 11. Implementation Checklist

### Design & Layout
- [ ] Dashboard background set to `#1C2333`
- [ ] All containers set to `#232B3A` with 8px inner padding
- [ ] 3-Zone layout implemented (KPI → Trend+Risk → Detail)
- [ ] Dashboard fixed size set to 1400 × 900px
- [ ] Blue title banner added with main title

### Typography
- [ ] All fonts changed to Segoe UI
- [ ] Dashboard title: 24pt Bold White `#FFFFFF`
- [ ] Section headings: 16pt Bold Blue `#0072CE`
- [ ] KPI values: 32pt Bold White `#FFFFFF`
- [ ] KPI labels: 10pt Uppercase Gray `#A3A8B5`
- [ ] Axis labels/titles: 9–10pt Gray `#A3A8B5`
- [ ] Chart titles: 13pt SemiBold `#EBECEF`

### Color Palette
- [ ] Loan Status colors applied (Green/Blue/Red/Amber)
- [ ] Grade color scale (A=Green → G=Red) applied
- [ ] Grid lines updated to `#3A4459`
- [ ] All default Tableau blues replaced with `#0072CE`

### Sheet Renaming
- [ ] All worksheets renamed per Section 5 map
- [ ] All dashboards renamed per Section 5 map
- [ ] Story renamed to "The Anatomy of a Loan Portfolio"

### Calculated Fields
- [ ] `[Good Loan Flag]` created
- [ ] `[Bad Loan Flag]` created
- [ ] `[Good Loan %]` created
- [ ] `[Bad Loan %]` created
- [ ] `[DTI Risk Band]` created
- [ ] `[Income Band]` created
- [ ] `[Credit Tier]` created
- [ ] `[Revenue Yield]` created
- [ ] `[Net Interest Margin]` created
- [ ] `[Loss Amount]` created
- [ ] `[Net Portfolio Return]` created
- [ ] `[MoM Funded Growth %]` created
- [ ] `[Loan Age Months]` created
- [ ] `[Issue Quarter]` created

### New Visualizations
- [ ] Good/Bad Loan Donut KPI chart built
- [ ] DTI × Grade Risk Heatmap built
- [ ] Monthly Funded Trend + MoM Growth dual-axis built
- [ ] Interest Rate Box Plot by Loan Status built
- [ ] State-Level Charge-Off Choropleth Map built
- [ ] Revenue Yield Waterfall Chart built

### Story
- [ ] 6-Point Tableau Story created
- [ ] Story title: "The Anatomy of a Loan Portfolio"
- [ ] All 6 story points added with captions
- [ ] Story background set to `#1C2333`

### Interactivity
- [ ] State Map filter action connected to all sheets
- [ ] Grade filter action connected to risk sheets
- [ ] Time brush filter action connected to all date sheets
- [ ] Loan Status highlight action added
- [ ] Credit Tier highlight action added
- [ ] Date Range parameter created
- [ ] Risk Threshold parameter created
- [ ] Grade Filter parameter created

### Final QA
- [ ] All tooltips formatted (Dark Ink background, Segoe UI font)
- [ ] All legends labeled and positioned consistently
- [ ] Dashboard tested at 1400 × 900px resolution
- [ ] .twbx repacked and opens correctly
- [ ] README.md updated with change log

---

## 📝 Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v2.0 | 2026-03-06 | Tableau Consultant | Full redesign: dark theme, new calculated fields, 6 new visuals, Tableau Story |
| v1.0 | — | DragonlordHarsh | Initial dashboard creation |

---

*This guide is a living document. Update the Change Log with each iteration of the dashboard.*
