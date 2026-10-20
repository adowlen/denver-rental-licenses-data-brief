"""Charts for the Denver residential rental licenses brief. Dark brand style.
All figures from stats.json / neighborhood_panel.csv (never hand-typed).
Every chart labels its basis ON the graphic; footnotes sit fully inside the frame.
"""
import json

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

PKG = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-rental-licenses-brief-2026-10-20"
BG, AMBER, TEAL, FG, MUT = "#101417", "#f5a800", "#19b8a6", "#e8e6e1", "#9aa3ab"
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": FG, "axes.edgecolor": "#2a2f33", "axes.labelcolor": FG,
    "xtick.color": MUT, "ytick.color": MUT, "font.family": "DejaVu Sans",
    "axes.grid": True, "grid.color": "#23282c", "grid.linewidth": 0.6,
})
S = json.load(open(f"{PKG}/stats.json"))
OUT = f"{PKG}/charts"

# --- 1. Holder concentration on the LICENSE basis ---
bands = ["1", "2", "3-5", "6-10", "11+"]
holders = [S["concentration_active_licenses"]["holders_by_band"][b] for b in bands]
licenses = [S["concentration_active_licenses"]["units_by_band"][b] for b in bands]
fig, ax = plt.subplots(figsize=(9.2, 5.2))
ax.bar(bands, holders, color=TEAL, width=0.58)
ax.bar(["1"], [holders[0]], color=AMBER, width=0.58)
for b, h, lic in zip(bands, holders, licenses):
    ax.annotate(f"{h:,} holders\n{lic:,} licenses", (b, h + 700), ha="center", fontsize=10, color=FG,
                fontweight="bold")
ax.set_ylim(0, 22500)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:,.0f}"))
ax.set_xlabel("Active licenses held per holder (band) - LICENSE basis: distinct LICENSE_NUM per ENTITY_NAME", fontsize=10)
ax.set_title("Denver long-term rental license holders by licenses held\n(26,939 named active licenses, 20,780 holders)",
             fontsize=11.5, color=FG, pad=12, loc="left")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout(rect=[0, 0.09, 1, 1])
fig.text(0.012, 0.035, "Basis: active licenses only (LICENSE_STATUS = License Issued - Active), holder = ENTITY_NAME as filed,",
         fontsize=8.5, color=MUT)
fig.text(0.012, 0.008, "normalized for case and spacing. Name-as-filed classification, not beneficial ownership.",
         fontsize=8.5, color=MUT)
fig.savefig(f"{OUT}/chart_bands.png", dpi=200)
plt.close(fig)

# --- 2. Neighborhood density: LTR rows per 1,000 units, top 12 (row basis, labeled) ---
panel = pd.read_csv(f"{PKG}/data/neighborhood_panel.csv")
rate = panel.nlargest(12, "rental_rows_per_1000_units").iloc[::-1]
fig, ax = plt.subplots(figsize=(9.2, 5.6))
ax.barh(rate["neighborhood"], rate["rental_rows_per_1000_units"], color=TEAL, height=0.62)
for i, (v, n) in enumerate(zip(rate["rental_rows_per_1000_units"], rate["rental_active_rows"])):
    ax.annotate(f"{v:.0f}  ({n:,} rows)", (v + 6, i), va="center", fontsize=9.5, color=FG)
ax.set_xlim(0, 340)
ax.set_title("Active long-term rental register ROWS per 1,000 housing units, top 12 neighborhoods\n(citywide: 108.4 rows per 1,000 units, all active rows)",
             fontsize=11.5, color=FG, pad=12, loc="left")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout(rect=[0, 0.11, 1, 1])
fig.text(0.012, 0.055, "ROW basis: one row is a unit/address filing under a license; rows are not licenses and not a unit count.",
         fontsize=8.5, color=MUT)
fig.text(0.012, 0.028, "Denominators: ACS 2020-2024 5-year housing units allocated to statistical neighborhoods.",
         fontsize=8.5, color=MUT)
fig.text(0.012, 0.002, "All 78 neighborhoods hold at least one active row; 522 active rows (1.3%) carry no neighborhood assignment.",
         fontsize=8.5, color=MUT)
fig.savefig(f"{OUT}/chart_neighborhood_rates.png", dpi=200)
plt.close(fig)

# --- 3. Side-by-side: LTR rows vs STR licenses per 1,000 units (labeled scopes) ---
top_ltr = panel.nlargest(10, "rental_rows_per_1000_units").iloc[::-1]
fig, axes = plt.subplots(1, 2, figsize=(9.6, 5.6), sharex=False)
ax = axes[0]
ax.barh(top_ltr["neighborhood"], top_ltr["rental_rows_per_1000_units"], color=AMBER, height=0.62)
for i, v in enumerate(top_ltr["rental_rows_per_1000_units"]):
    ax.annotate(f"{v:.0f}", (v + 6, i), va="center", fontsize=9, color=FG)
ax.set_xlim(0, 340)
ax.set_title("LONG-TERM: register rows\nper 1,000 units", fontsize=10.5, color=FG, loc="left")
ax2 = axes[1]
# STR values for the SAME neighborhoods, in the same order as the left panel
str_vals = top_ltr["str_per_1000_units"].tolist()
ax2.barh(top_ltr["neighborhood"], str_vals, color=TEAL, height=0.62)
for i, v in enumerate(str_vals):
    ax2.annotate(f"{v:.1f}", (v + 0.8, i), va="center", fontsize=9, color=FG)
ax2.set_xlim(0, 32)
ax2.set_title("SHORT-TERM: active licenses\nper 1,000 units (2026-10-19)", fontsize=10.5, color=FG, loc="left")
for a in axes:
    for s in ["top", "right"]:
        a.spines[s].set_visible(False)
fig.suptitle("Same neighborhoods, two registers - different measures, labeled (do not add)", fontsize=11.5, color=FG, x=0.012, ha="left")
fig.tight_layout(rect=[0, 0.11, 1, 0.94])
fig.text(0.012, 0.055, "Left: long-term rental register ROWS per 1,000 ACS housing units (2026-10-20 pull, active rows).",
         fontsize=8.5, color=MUT)
fig.text(0.012, 0.028, "Right: short-term rental active LICENSES per 1,000 units for the same 10 neighborhoods (2026-10-19 brief).",
         fontsize=8.5, color=MUT)
fig.text(0.012, 0.002, "Neighborhoods ordered by the long-term row rate. Citywide: 108.4 LTR rows vs 5.8 STR licenses per 1,000 units.",
         fontsize=8.5, color=MUT)
fig.savefig(f"{OUT}/chart_ltr_vs_str.png", dpi=200)
plt.close(fig)

# --- 4. Vintage: distinct active licenses by license-number prefix year ---
vint = S["vintage_active"]["distinct_licenses_by_prefix_year"]
years = sorted(vint.keys(), key=int)
vals = [vint[y] for y in years]
fig, ax = plt.subplots(figsize=(9.2, 5.0))
ax.bar([int(y) for y in years], vals, color=AMBER, width=0.62)
for x, v in zip(years, vals):
    ax.annotate(f"{v:,}", (int(x), v + 400), ha="center", fontsize=9.5, color=FG, fontweight="bold")
ax.set_ylim(0, 15500)
ax.set_xticks([int(y) for y in years])
ax.set_title("Active long-term rental licenses by license-number prefix year\n(49.3% carry a 2023 prefix - the multi-unit requirement year)",
             fontsize=11.5, color=FG, pad=12, loc="left")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout(rect=[0, 0.10, 1, 1])
fig.text(0.012, 0.045, "Basis: distinct active LICENSE_NUM values, grouped by the 4-digit year prefix of the license number.",
         fontsize=8.5, color=MUT)
fig.text(0.012, 0.012, "This service carries no original-issue date field; the prefix year is the license number's own encoding.",
         fontsize=8.5, color=MUT)
fig.savefig(f"{OUT}/chart_vintage.png", dpi=200)
plt.close(fig)

print("charts written")
