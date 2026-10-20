"""Build stats.json for the Denver residential rental licenses brief (2026-10-20).

Primary source: warehouse snapshot
stack/denver/snapshots/2026-10-20/rental_licenses.parquet (Denver DLCP
residential rental property license register, ArcGIS table 52, pulled
2026-10-20T12:32:53Z, 38,970 rows).

CRITICAL GRAIN NOTE (the brief's central semantic fact): one register ROW is
not one license and not reliably one unit. Rows sharing a LICENSE_NUM are the
unit/address filings of a single license (a 697-row license enumerates 697
unit addresses on one parcel); other licenses file a single row for a whole
multi-unit building. This script therefore computes every concentration and
footprint figure on TWO labeled bases and never mixes them:
- LICENSE basis: distinct LICENSE_NUM (26,941 active).
- ROW basis: register rows (38,949 active).
Parcel and neighborhood assignment: PARCEL_NUM is a Double in the source;
the canonical schednum is str(int(PARCEL_NUM)).zfill(13), matched directly
against parcel spine v6. Neighborhood = spine v6 neighborhood of the parcel.
Rates: active ROWS per 1,000 ACS 2020-2024 5-year housing units (warehouse
layer acs_neighborhood_units.parquet; same denominators as the October 17-19
briefs). STR comparison: the published 2026-10-19 STR package panel.
No licensee name, street address, or parcel number is written to any output.
"""
import json
import re
from collections import Counter

import numpy as np
import pandas as pd

PKG = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-rental-licenses-brief-2026-10-20"
STACK = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/stack/denver"
STR_PKG = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-str-licenses-brief-2026-10-19"
ACTIVE = "License Issued - Active"
PULL_DATE = "2026-10-20"

raw = pd.read_parquet(f"{STACK}/snapshots/2026-10-20/rental_licenses.parquet")
spine = pd.read_parquet(f"{STACK}/joins/parcel_spine_v6.parquet")
acs = pd.read_parquet(f"{STACK}/layers/acs_neighborhood_units.parquet")
str_panel = pd.read_csv(f"{STR_PKG}/data/neighborhood_panel.csv")
str_stats = json.load(open(f"{STR_PKG}/stats.json"))

S = {}
S["meta"] = {
    "dataset": "ODC_residential_rental_property_active_licenses (Denver Open Data, ArcGIS FeatureServer table 52)",
    "publisher": "Department of Licensing and Consumer Protection (DLCP), City and County of Denver",
    "snapshot": "warehouse snapshots/2026-10-20/rental_licenses.parquet (pulled 2026-10-20T12:32:53Z)",
    "active_basis": "LICENSE_STATUS == 'License Issued - Active' exactly; Delinquent rows are never counted as active",
    "grain": "one register row is a unit/address filing; rows sharing a LICENSE_NUM belong to one license. Figures are computed on two labeled bases: distinct LICENSE_NUM (license basis) and register rows (row basis)",
    "holder_key": "ENTITY_NAME normalized: uppercase, whitespace collapsed",
    "parcel_key": "schednum = str(int(PARCEL_NUM)).zfill(13) matched against parcel spine v6 (PARCEL_NUM is esriFieldTypeDouble in the source service)",
    "acs_denver_county_units": 359581,
    "acs_units_allocated_to_neighborhoods": float(acs["acs_units_2020_2024"].sum()),
    "product_rule": "aggregates only in every shipped file category (brief and social markdown, stats.json, data/, code/, charts/, hero): no licensee name, street address, or parcel number value in any output; the raw register snapshot lives only in the warehouse",
}

# ---------- register totals (counters BEFORE any filter) ----------
status_counter = {str(k): int(v) for k, v in raw["LICENSE_STATUS"].value_counts(dropna=False).items()}
S["register"] = {
    "rows": int(len(raw)),
    "status_counter": status_counter,
    "status_shares_pct": {k: round(v / len(raw) * 100, 2) for k, v in status_counter.items()},
    "license_type_counter": {str(k): int(v) for k, v in raw["LICENSE_TYPE"].value_counts(dropna=False).items()},
    "distinct_license_nums": int(raw["LICENSE_NUM"].nunique()),
    "distinct_license_nums_active": int(raw.loc[raw["LICENSE_STATUS"] == ACTIVE, "LICENSE_NUM"].nunique()),
    "rows_per_license_distribution": {
        str(k): int(v) for k, v in Counter(
            raw.groupby("LICENSE_NUM").size().tolist()).items() if k in (1, 2, 3, 4, 5)},
    "licenses_with_multiple_rows": int((raw.groupby("LICENSE_NUM").size() >= 2).sum()),
    "rows_in_multi_row_licenses": int(raw.groupby("LICENSE_NUM").size().loc[lambda s: s >= 2].sum()),
    "max_rows_on_one_license": int(raw.groupby("LICENSE_NUM").size().max()),
    "entity_name_null_rows": int(raw["ENTITY_NAME"].isna().sum()),
    "entity_name_null_rows_active": int(raw.loc[raw["LICENSE_STATUS"] == ACTIVE, "ENTITY_NAME"].isna().sum()),
}
assert sum(status_counter.values()) == len(raw)

# ---------- parcel bridge (direct schednum match on spine v6) ----------
def schednum_of(v):
    if pd.isna(v):
        return None
    return str(int(v)).zfill(13)

raw["schednum"] = raw["PARCEL_NUM"].map(schednum_of)
spine_by_sched = spine.set_index("schednum")
raw["neighborhood"] = raw["schednum"].map(spine_by_sched["neighborhood"])
raw["TOT_UNITS"] = raw["schednum"].map(spine_by_sched["TOT_UNITS"])
act = raw[raw["LICENSE_STATUS"] == ACTIVE].copy()
S["parcel_bridge"] = {
    "basis": "all register rows",
    "matched_rows": int(raw["schednum"].isin(set(spine["schednum"])).sum()),
    "unmatched_rows": int((~raw["schednum"].isin(set(spine["schednum"]))).sum()),
    "match_rate_pct": round(float(raw["schednum"].isin(set(spine["schednum"])).mean() * 100), 2),
    "active_matched_rows": int(act["neighborhood"].notna().sum()),
    "active_unmatched_rows": int(act["neighborhood"].isna().sum()),
    "active_match_rate_pct": round(float(act["neighborhood"].notna().mean() * 100), 2),
    "active_unmatched_distinct_parcels": int(act.loc[act["neighborhood"].isna(), "schednum"].nunique()),
    "active_unmatched_distinct_licenses": int(act.loc[act["neighborhood"].isna(), "LICENSE_NUM"].nunique()),
    "active_unmatched_rows_on_two_largest_parcels": int(
        act.loc[act["neighborhood"].isna(), "schednum"].value_counts().head(2).sum()),
    "note": "the active bridge counts a row as matched when the spine assigns it a neighborhood (38,427 matched, 522 unassigned). Of the 522 unassigned active rows, 499 sit on parcels absent from the 2026-10-15 spine snapshot and 23 sit on 22 parcels that are present in spine v6 but carry a null neighborhood value; on pure schednum membership the bridge matches 38,450 active rows. The two largest unassigned parcels hold 157 of the 522 rows. Unmatched licenses are counted in every citywide total and excluded from parcel and neighborhood tables only",
}
assert S["parcel_bridge"]["matched_rows"] + S["parcel_bridge"]["unmatched_rows"] == len(raw)

# ---------- holder normalization + classification (STR token rule) ----------
def norm_name(s):
    if pd.notna(s):
        return re.sub(r"\s+", " ", str(s).upper().strip())
    return np.nan

raw["holder"] = raw["ENTITY_NAME"].map(norm_name)
act = raw[raw["LICENSE_STATUS"] == ACTIVE].copy()

BUSINESS_TOKENS = set(str_stats["classification_rule"]["business_tokens"])

def classify(name):
    if not isinstance(name, str):
        return "not_determined"
    toks = re.findall(r"[A-Z]+(?:'[A-Z]+)?", name)
    if any(t in BUSINESS_TOKENS for t in toks):
        return "business_entity_name"
    if 2 <= len(toks) <= 5 and all(t.replace("'", "").isalpha() for t in toks):
        return "individual_name"
    return "not_determined"

raw["name_class"] = raw["holder"].map(classify)
act = raw[raw["LICENSE_STATUS"] == ACTIVE].copy()

def classification_block(frame, unit_label, dedupe_col=None):
    f = frame.drop_duplicates(dedupe_col) if dedupe_col else frame
    n = len(f)
    c = f["name_class"].value_counts(dropna=False)
    out = {unit_label: int(n)}
    for k in ["individual_name", "business_entity_name", "not_determined"]:
        cnt = int(c.get(k, 0))
        out[k] = {"count": cnt, "share_pct": round(cnt / n * 100, 2) if n else None}
    assert sum(out[k]["count"] for k in ["individual_name", "business_entity_name", "not_determined"]) == n
    return out

S["classification_active_rows"] = classification_block(act, "rows")
S["classification_active_licenses"] = classification_block(act, "licenses", dedupe_col="LICENSE_NUM")
named_holders = act.dropna(subset=["holder"]).drop_duplicates("holder")
S["classification_active_holders"] = classification_block(named_holders, "holders")
S["classification_register_rows"] = classification_block(raw, "rows")
S["classification_rule"] = {
    "business_tokens": sorted(BUSINESS_TOKENS),
    "rule": "business if any name token is a business token (same token set as the 2026-10-19 STR brief); else individual if 2-5 alphabetic tokens; else not determined",
    "scope": "classification of the ENTITY_NAME string as filed, not of beneficial ownership",
}

# ---------- concentration (two labeled bases) ----------
def concentration(frame, unit_col, unit_label, basis_label):
    vc = frame.groupby("holder")[unit_col].nunique() if unit_col == "LICENSE_NUM" else frame.groupby("holder").size()
    vc = vc.dropna()
    n_units = int(vc.sum())
    n_hold = int(len(vc))
    counts = sorted(vc.tolist(), reverse=True)
    bands = {"1": 0, "2": 0, "3-5": 0, "6-10": 0, "11+": 0}
    band_units = {"1": 0, "2": 0, "3-5": 0, "6-10": 0, "11+": 0}
    for c in counts:
        b = "1" if c == 1 else "2" if c == 2 else "3-5" if c <= 5 else "6-10" if c <= 10 else "11+"
        bands[b] += 1
        band_units[b] += c

    def top_share(k):
        return round(sum(counts[:k]) / n_units * 100, 2)
    return {
        "basis": basis_label,
        "units": n_units,
        "distinct_holders": n_hold,
        "max_per_holder": int(max(counts)),
        "holders_by_band": bands,
        "units_by_band": band_units,
        "top_shares_pct": {"top_1": top_share(1), "top_5": top_share(5),
                           "top_10": top_share(10), "top_25": top_share(25)},
        "share_held_by_holders_with_2plus_pct": round(sum(c for c in counts if c >= 2) / n_units * 100, 2),
        "share_held_by_holders_with_11plus_pct": round(sum(c for c in counts if c >= 11) / n_units * 100, 2),
        "units_whose_holder_has_exactly_1": int(sum(c for c in counts if c == 1)),
        "share_whose_holder_has_exactly_1_pct": round(sum(c for c in counts if c == 1) / n_units * 100, 2),
    }

S["concentration_active_licenses"] = concentration(
    act, "LICENSE_NUM", "licenses",
    "active distinct LICENSE_NUM per normalized ENTITY_NAME (license basis)")
S["concentration_active_rows"] = concentration(
    act, None, "rows",
    "active register rows per normalized ENTITY_NAME (row basis; rows enumerate units on some licenses and not on others - see grain note)")
S["concentration_register_licenses"] = concentration(
    raw, "LICENSE_NUM", "licenses", "all register rows, every status, distinct LICENSE_NUM per holder")

# name-merge sensitivities (active, license basis primary)
def first_last(name):
    if not isinstance(name, str):
        return (None,)
    toks = re.findall(r"[A-Z]+", name)
    return (toks[0], toks[-1]) if len(toks) >= 2 else (name,)

def initial_surname(name):
    if not isinstance(name, str):
        return (None,)
    toks = re.findall(r"[A-Z]+", name)
    return (toks[0][0], toks[-1]) if len(toks) >= 2 else (name,)

S["name_merge_sensitivity_active"] = {}
for key, fn in [("first_last_token_merge", first_last), ("initial_surname_overmerge", initial_surname)]:
    grp = act["holder"].map(fn).astype(str)
    lic_groups = act.assign(grp=grp).groupby("grp")["LICENSE_NUM"].nunique()
    row_groups = act.assign(grp=grp).groupby("grp").size()
    S["name_merge_sensitivity_active"][key] = {
        "distinct_groups": int(len(lic_groups)),
        "max_licenses_per_group": int(lic_groups.max()),
        "groups_with_2plus_licenses": int((lic_groups >= 2).sum()),
        "licenses_in_groups_with_2plus": int(lic_groups[lic_groups >= 2].sum()),
        "share_licenses_in_groups_with_2plus_pct": round(float(lic_groups[lic_groups >= 2].sum()) / act["LICENSE_NUM"].nunique() * 100, 2),
        "max_rows_per_group": int(row_groups.max()),
    }

# ---------- parcels (MATCHED basis: active rows assigned a neighborhood via
# the spine. Corrected in the 2026-10-20 Section 11 fix loop: the original
# build grouped over ALL register parcel keys while the block's basis string
# claimed unmatched rows were excluded - adversarial Finding 2.) ----------
matched_parcel_rows = act[act["neighborhood"].notna()]
row_per_parcel = matched_parcel_rows.groupby("schednum").size()
lic_per_parcel = matched_parcel_rows.groupby("schednum")["LICENSE_NUM"].nunique()
_second_sched = row_per_parcel.sort_values(ascending=False).index[1]
S["parcels_active"] = {
    "basis": "active rows matched to the parcel spine and assigned a neighborhood (38,427 of 38,949 active rows); every count in this block is computed over the 26,394 distinct matched parcels only; the 522 unassigned active rows are excluded",
    "rows_with_parcel_match": int(act["neighborhood"].notna().sum()),
    "distinct_parcels": int(row_per_parcel.shape[0]),
    "distinct_parcels_matched_to_spine": int(act.loc[act["neighborhood"].notna(), "schednum"].nunique()),
    "parcels_with_multiple_rows": int((row_per_parcel >= 2).sum()),
    "rows_on_multiple_row_parcels": int(row_per_parcel[row_per_parcel >= 2].sum()),
    "share_of_matched_rows_on_multiple_row_parcels_pct": round(float(
        row_per_parcel[row_per_parcel >= 2].sum() / len(matched_parcel_rows) * 100), 1),
    "max_rows_on_one_parcel": int(row_per_parcel.max()),
    "largest_parcel_neighborhood": str(spine_by_sched.loc[row_per_parcel.idxmax(), "neighborhood"]),
    "largest_parcel_units_on_parcel_record": (
        None if pd.isna(spine_by_sched.loc[row_per_parcel.idxmax(), "TOT_UNITS"])
        else float(spine_by_sched.loc[row_per_parcel.idxmax(), "TOT_UNITS"])),
    "largest_parcel_distinct_licenses": int(lic_per_parcel.loc[row_per_parcel.idxmax()]),
    "second_largest_parcel_rows": int(row_per_parcel.loc[_second_sched]),
    "second_largest_parcel_neighborhood": str(spine_by_sched.loc[_second_sched, "neighborhood"]),
    "second_largest_parcel_units_on_parcel_record": (
        None if pd.isna(spine_by_sched.loc[_second_sched, "TOT_UNITS"])
        else float(spine_by_sched.loc[_second_sched, "TOT_UNITS"])),
    "second_largest_parcel_distinct_licenses": int(lic_per_parcel.loc[_second_sched]),
    "parcels_with_multiple_distinct_licenses": int((lic_per_parcel >= 2).sum()),
    "max_distinct_licenses_on_one_parcel": int(lic_per_parcel.max()),
    "licenses_on_multiple_license_parcels": int(lic_per_parcel[lic_per_parcel >= 2].sum()),
    "parcel_with_max_distinct_licenses_neighborhood": str(
        spine_by_sched.loc[lic_per_parcel.idxmax(), "neighborhood"]) if lic_per_parcel.idxmax() in spine_by_sched.index and pd.notna(spine_by_sched.loc[lic_per_parcel.idxmax(), "neighborhood"]) else None,
    "parcel_with_max_distinct_licenses_units_on_parcel_record": (
        None if lic_per_parcel.idxmax() not in spine_by_sched.index or pd.isna(spine_by_sched.loc[lic_per_parcel.idxmax(), "TOT_UNITS"])
        else float(spine_by_sched.loc[lic_per_parcel.idxmax(), "TOT_UNITS"])),
    "row_count_distribution_parcels_by_row_count_top": {
        str(k): int(v) for k, v in sorted(Counter(row_per_parcel.tolist()).items())[:5]},
}

# ---------- grain check: rows vs assessor TOT_UNITS on licensed parcels ----------
matched_act = act[act["neighborhood"].notna()].copy()
distinct_parc = matched_act.drop_duplicates("schednum")[["schednum", "TOT_UNITS"]].copy()
distinct_parc["rows"] = distinct_parc["schednum"].map(row_per_parcel)
with_tot = distinct_parc.dropna(subset=["TOT_UNITS"])
S["grain_check"] = {
    "distinct_matched_licensed_parcels": int(len(distinct_parc)),
    "of_those_parcels_with_tot_units_recorded": int(len(with_tot)),
    "parcels_with_tot_units_null_on_spine": int(distinct_parc["TOT_UNITS"].isna().sum()),
    "sum_tot_units_over_licensed_parcels_with_tot_recorded": float(with_tot["TOT_UNITS"].sum()),
    "sum_tot_units_all_spine_parcels": float(spine["TOT_UNITS"].sum(skipna=True)),
    "share_of_spine_tot_units_on_licensed_parcels_pct": round(float(with_tot["TOT_UNITS"].sum() / spine["TOT_UNITS"].sum(skipna=True) * 100), 1),
    "active_rows_on_matched_parcels": int(len(matched_act)),
    "parcels_where_rows_equal_tot_units": int((with_tot["rows"] == with_tot["TOT_UNITS"]).sum()),
    "parcels_where_rows_below_tot_units": int((with_tot["rows"] < with_tot["TOT_UNITS"]).sum()),
    "parcels_where_rows_above_tot_units": int((with_tot["rows"] > with_tot["TOT_UNITS"]).sum()),
    "single_row_parcels": int((distinct_parc["rows"] == 1).sum()),
    "single_row_parcels_with_tot_units_10plus": int(((distinct_parc["rows"] == 1) & (distinct_parc["TOT_UNITS"] >= 10)).sum()),
    "tot_units_on_single_row_parcels_with_tot_10plus": float(distinct_parc.loc[(distinct_parc["rows"] == 1) & (distinct_parc["TOT_UNITS"] >= 10), "TOT_UNITS"].sum()),
    "reading": "rows neither equal licenses nor reliably equal units: most single-row parcels carry TOT_UNITS of 1 on the assessor record, but 1,026 single-row parcels carry 10 or more units on their record (a single row filed for a whole building), while unit-enumerated licenses file hundreds of rows on one parcel and can exceed the parcel record's TOT_UNITS. Unit coverage is therefore reported from the assessor TOT_UNITS sum over licensed parcels, never from row counts.",
}

# ---------- neighborhoods + STR comparison ----------
units = dict(zip(acs["neighborhood"], acs["acs_units_2020_2024"]))
row_cnt = act["neighborhood"].value_counts(dropna=True)
lic_cnt = act.dropna(subset=["neighborhood"]).groupby("neighborhood")["LICENSE_NUM"].nunique()
str_map = str_panel.set_index("neighborhood")
panel = pd.DataFrame({"neighborhood": sorted(units.keys())})
panel["acs_units"] = panel["neighborhood"].map(units)
panel["rental_active_rows"] = panel["neighborhood"].map(row_cnt).fillna(0).astype(int)
panel["rental_rows_per_1000_units"] = (panel["rental_active_rows"] / panel["acs_units"] * 1000).round(2)
panel["rental_distinct_licenses"] = panel["neighborhood"].map(lic_cnt).fillna(0).astype(int)
panel["str_active_licenses"] = panel["neighborhood"].map(str_map["active_licenses"]).fillna(0).astype(int)
panel["str_per_1000_units"] = panel["neighborhood"].map(str_map["licenses_per_1000_units"])
panel = panel.sort_values("neighborhood").reset_index(drop=True)
panel.to_csv(f"{PKG}/data/neighborhood_panel.csv", index=False)

assigned_rows = int(row_cnt.sum())
top_count = panel.nlargest(12, "rental_active_rows")[["neighborhood", "rental_active_rows", "acs_units", "rental_rows_per_1000_units", "rental_distinct_licenses", "str_active_licenses", "str_per_1000_units"]]
top_rate = panel.nlargest(12, "rental_rows_per_1000_units")[["neighborhood", "rental_active_rows", "acs_units", "rental_rows_per_1000_units", "rental_distinct_licenses", "str_active_licenses", "str_per_1000_units"]]
def spearman(a, b):
    ra = pd.Series(np.asarray(a, dtype=float)).rank()
    rb = pd.Series(np.asarray(b, dtype=float)).rank()
    return round(float(np.corrcoef(ra, rb)[0, 1]), 3)
S["neighborhoods"] = {
    "active_rows_with_neighborhood": assigned_rows,
    "active_rows_without_neighborhood": int(act["neighborhood"].isna().sum()),
    "neighborhoods_total": int(len(panel)),
    "neighborhoods_with_1plus_active_rows": int((panel["rental_active_rows"] > 0).sum()),
    "neighborhoods_with_zero_active_rows": int((panel["rental_active_rows"] == 0).sum()),
    "zero_active_neighborhoods": sorted(panel.loc[panel["rental_active_rows"] == 0, "neighborhood"].tolist()),
    "citywide_active_rows_per_1000_units_assigned_basis": round(assigned_rows / panel["acs_units"].sum() * 1000, 1),
    "citywide_active_rows_per_1000_units_all_active_rows": round(len(act) / panel["acs_units"].sum() * 1000, 1),
    "top_by_count": top_count.to_dict("records"),
    "top_by_rate_per_1000": top_rate.to_dict("records"),
    "top5_count_share_pct_of_assigned_rows": round(float(panel.nlargest(5, "rental_active_rows")["rental_active_rows"].sum() / assigned_rows * 100), 1),
    "top10_count_share_pct_of_assigned_rows": round(float(panel.nlargest(10, "rental_active_rows")["rental_active_rows"].sum() / assigned_rows * 100), 1),
    "median_neighborhood_rate_per_1000": round(float(panel["rental_rows_per_1000_units"].median()), 1),
    "median_neighborhood_rate_basis": "median across all 78 neighborhoods (no zero-row neighborhoods exist in this register, so the with-rows median is identical)",
}
S["str_comparison"] = {
    "str_brief_date": "2026-10-19",
    "str_active_licenses": int(str_stats["register"]["status_counter"]["License Issued - Active"]),
    "ltr_active_distinct_licenses": int(act["LICENSE_NUM"].nunique()),
    "ltr_active_rows": int(len(act)),
    "ratio_ltr_licenses_to_str_licenses": round(float(act["LICENSE_NUM"].nunique() / str_stats["concentration_active"]["licenses"]), 1),
    "ratio_ltr_rows_to_str_licenses": round(float(len(act) / str_stats["concentration_active"]["licenses"]), 1),
    "str_citywide_per_1000_units": float(str_stats["neighborhoods"]["citywide_active_per_1000_units"]),
    "ltr_citywide_rows_per_1000_units": S["neighborhoods"]["citywide_active_rows_per_1000_units_all_active_rows"],
    "spearman_neighborhood_rates_ltr_rows_vs_str_licenses": spearman(panel["rental_rows_per_1000_units"], panel["str_per_1000_units"]),
    "spearman_neighborhood_counts_ltr_rows_vs_str_licenses": spearman(panel["rental_active_rows"], panel["str_active_licenses"]),
    "neighborhoods_compared": int(len(panel)),
    "str_zero_neighborhoods": str_stats["neighborhoods"]["zero_active_neighborhoods"],
    "note": "the two registers measure different things on different grains: STR counts are licenses (one license per licensee, one unit per license under the primary-residence rules); LTR rows are unit/address filings under licenses that can cover a whole building. Rates are printed side by side with their bases labeled, never added or merged.",
}

# ---------- vintage (license-number prefix year) + expiration ----------
act_lic = act.drop_duplicates("LICENSE_NUM").copy()
act_lic["lic_year"] = act_lic["LICENSE_NUM"].str[:4]
act_rows_y = act.assign(lic_year=act["LICENSE_NUM"].str[:4])
S["vintage_active"] = {
    "basis": "year prefix of LICENSE_NUM (the license number encodes its issue year, e.g. 2023-BFN-...); this service carries no original-issue date field, and RENEWAL_CREATED is a 1900 sentinel on active rows (see field_hygiene), so no date-field vintage is claimed",
    "distinct_licenses_by_prefix_year": {str(k): int(v) for k, v in act_lic["lic_year"].value_counts().sort_index().items()},
    "rows_by_prefix_year": {str(k): int(v) for k, v in act_rows_y["lic_year"].value_counts().sort_index().items()},
    "share_licenses_prefix_2023_pct": round(float((act_lic["lic_year"] == "2023").mean() * 100), 1),
    "share_licenses_prefix_2023_or_later_pct": round(float((act_lic["lic_year"] >= "2023").mean() * 100), 1),
}
exp_all = pd.to_datetime(raw["EXPIRATION_DATE"], format="mixed", errors="coerce")
exp_act = pd.to_datetime(act["EXPIRATION_DATE"], format="mixed", errors="coerce")
S["expiry_hygiene"] = {
    "active_rows_with_expiration_before_pull_date": int((exp_act < PULL_DATE).sum()),
    "share_of_active_rows_pct": round(float((exp_act < PULL_DATE).mean() * 100), 3),
    "all_rows_with_expiration_before_pull_date": int((exp_all < PULL_DATE).sum()),
    "delinquent_rows_with_expiration_before_pull_date": int(((exp_all < PULL_DATE) & (raw["LICENSE_STATUS"] == "Delinquent")).sum()),
    "active_expiration_by_year": {str(int(k)): int(v) for k, v in exp_act.dt.year.value_counts().sort_index().items()},
    "note": "status and expiration fields are recorded as published; a past expiration date on an active-status row is a field disagreement printed without a compliance claim. The DLCP renewal FAQ provides for a 90-day grace period after expiration, which the register alone cannot apply row by row.",
}

# ---------- field hygiene / sentinels ----------
rc = raw["RENEWAL_CREATED"].astype(str)
S["field_hygiene"] = {
    "multiple_licenses_counter": {str(k): int(v) for k, v in raw["MULTIPLE_LICENSES"].value_counts(dropna=False).items()},
    "multiple_licenses_reading": "constant 'Stand Alone' on all rows, including the 697 rows of the largest multi-unit license; not a usable signal - multi-row and multi-license patterns in this brief are computed from LICENSE_NUM and the parcel bridge",
    "relationship_counter_top": {str(k): int(v) for k, v in raw["RELATIONSHIP"].value_counts(dropna=False).head(3).items()},
    "renewal_status_counter_top": {str(k): int(v) for k, v in raw["RENEWAL_STATUS"].value_counts(dropna=False).head(3).items()},
    "renewal_created_sentinel": {
        "value_1_1_1900_rows": int((rc == "1/1/1900 12:00:00 AM").sum()),
        "share_pct": round(float((rc == "1/1/1900 12:00:00 AM").mean() * 100), 2),
        "non_sentinel_rows": int((rc != "1/1/1900 12:00:00 AM").sum()),
        "reading": "RENEWAL_CREATED reads 1/1/1900 on every active row; the only non-sentinel values are the 21 Delinquent rows (2026 dates). The field is a sentinel on this basis and is used for nothing in this brief.",
    },
    "zip_sentinel": {
        "zip_zero_rows": int((raw["ZIP"] == 0).sum()),
        "zip_null_rows": int(raw["ZIP"].isna().sum()),
        "reading": "ZIP is 0 on 3,436 rows and null on 773; ZIP is used for no figure in this brief. 0 and null are treated as unknown, never as a ZIP code.",
    },
    "parcel_num_field": {
        "source_type": "esriFieldTypeDouble",
        "null_rows": int(raw["PARCEL_NUM"].isna().sum()),
        "zero_rows": int((raw["PARCEL_NUM"] == 0).sum()),
        "digit_length_counter": {str(k): int(v) for k, v in Counter(raw["PARCEL_NUM"].map(lambda v: len(str(int(v)))).tolist()).items()},
        "reading": "PARCEL_NUM values are integers of 10 to 12 digits (leading zeros dropped by the Double field in varying numbers); the canonical 13-character schednum restores them by zfill and matches the spine at 98.7 percent of rows. No null, zero, or negative sentinel parcel values exist in this pull.",
    },
    "exact_duplicate_rows": {
        "duplicate_license_parcel_address_groups": int(raw.duplicated(subset=["LICENSE_NUM", "PARCEL_NUM", "ADDRESS"], keep=False).sum() // 2),
        "duplicate_rows_total": int(raw.duplicated(subset=["LICENSE_NUM", "PARCEL_NUM", "ADDRESS"], keep=False).sum()),
        "reading": "6 license/parcel/address combinations appear twice (12 rows, 6 excess rows, 0.02 percent of active rows). They are counted as published; removing them changes no printed figure at its printed precision.",
    },
    "double_filed_license": {
        "licenses": 1,
        "rows": 172,
        "distinct_addresses": 86,
        "parcels": 2,
        "reading": "one license with 100 or more rows files each of its 86 unit addresses twice, once under each of two parcel numbers (one of them the largest unmatched parcel in the bridge). Counted as published; the pattern is disclosed in Findings 1 and 5. The other 11 licenses with 100 or more rows each sit on one parcel with all-distinct addresses.",
    },
    "licenses_spanning_multiple_parcels": int((act.groupby("LICENSE_NUM")["schednum"].nunique() >= 2).sum()),
    "licenses_spanning_multiple_neighborhoods": int((act.dropna(subset=["neighborhood"]).groupby("LICENSE_NUM")["neighborhood"].nunique() >= 2).sum()),
    "holders_per_license_max": int(act.groupby("LICENSE_NUM")["holder"].nunique().max()),
    "licenses_with_multiple_holders": int((act.groupby("LICENSE_NUM")["holder"].nunique() >= 2).sum()),
}

with open(f"{PKG}/stats.json", "w") as fh:
    json.dump(S, fh, indent=1)
print(json.dumps({k: S[k] for k in ["register", "concentration_active_licenses", "classification_active_licenses"]}, indent=1))
print("neighborhoods with rows:", S["neighborhoods"]["neighborhoods_with_1plus_active_rows"])
print("parcels:", S["parcels_active"])
print("grain:", S["grain_check"]["sum_tot_units_over_licensed_parcels_with_tot_recorded"], S["grain_check"]["share_of_spine_tot_units_on_licensed_parcels_pct"])
print("stats.json written")
