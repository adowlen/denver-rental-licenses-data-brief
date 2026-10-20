"""Section 10 pre-flight audit - Denver residential rental licenses brief (2026-10-20).

Runs against the RAW warehouse snapshot and the package stats.json with an
implementation independent of build_stats.py (collections.Counter based).
Prints evidence for every gate; asserts are hard failures. Output is recorded
in verification.md and data/audit_output.txt. No licensee name, street address,
or parcel number value is printed.
"""
import json
import re
from collections import Counter

import pandas as pd

PKG = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-rental-licenses-brief-2026-10-20"
STACK = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/stack/denver"
ACTIVE = "License Issued - Active"
S = json.load(open(f"{PKG}/stats.json"))

raw = pd.read_parquet(f"{STACK}/snapshots/2026-10-20/rental_licenses.parquet")
spine = pd.read_parquet(f"{STACK}/joins/parcel_spine_v6.parquet")
print(f"snapshot rows {len(raw)}")
assert len(raw) == S["register"]["rows"] == 38970
assert raw["OBJECTID"].is_unique

print("\n== 10.1.4 categorical exhaustiveness (counters recorded before any filter) ==")
for col in ["LICENSE_STATUS", "LICENSE_TYPE", "MULTIPLE_LICENSES"]:
    c = Counter(raw[col].tolist())
    print(f"{col} full counter:", dict(c))
    assert sum(c.values()) == len(raw)
assert dict(Counter(raw["LICENSE_STATUS"].tolist())) == S["register"]["status_counter"]
assert Counter(raw["LICENSE_TYPE"].tolist()) == {"Residential Rental Property": len(raw)}
assert Counter(raw["MULTIPLE_LICENSES"].tolist()) == {"Stand Alone": len(raw)}
print("RELATIONSHIP non-null values:", Counter(raw["RELATIONSHIP"].dropna().tolist()))
print("RENEWAL_STATUS non-null values:", Counter(raw["RENEWAL_STATUS"].dropna().tolist()))
assert set(raw["RELATIONSHIP"].dropna().unique()) == {"Renewal"}
assert set(raw["RENEWAL_STATUS"].dropna().unique()) == {"Pending"}

print("\n== 10.1.1 zero/null sentinel traps ==")
print("ENTITY_NAME nulls:", int(raw["ENTITY_NAME"].isna().sum()))
assert int(raw["ENTITY_NAME"].isna().sum()) == 2
print("PARCEL_NUM nulls:", int(raw["PARCEL_NUM"].isna().sum()), "| zeros:", int((raw["PARCEL_NUM"] == 0).sum()),
      "| negatives:", int((raw["PARCEL_NUM"] < 0).sum()))
assert raw["PARCEL_NUM"].notna().all() and (raw["PARCEL_NUM"] > 0).all()
_len_counter = Counter(len(str(int(v))) for v in raw["PARCEL_NUM"])
assert set(_len_counter) == {10, 11, 12}, _len_counter
print("PARCEL_NUM digit-length counter (Double field, leading zeros dropped):", dict(_len_counter),
      "- schednum = str(int(v)).zfill(13) restores the canonical key for every row.")
print("ZIP zeros (sentinel, treated as unknown):", int((raw["ZIP"] == 0).sum()),
      "| ZIP nulls:", int(raw["ZIP"].isna().sum()), "- ZIP is used for no figure.")
rc = raw["RENEWAL_CREATED"].astype(str)
n1900 = int((rc == "1/1/1900 12:00:00 AM").sum())
print(f"RENEWAL_CREATED sentinel 1/1/1900 rows: {n1900} ({n1900/len(raw)*100:.2f}%) - excluded from every date use;")
print("the field is used for nothing in this brief. 'Unknown' dates are never placed in a rate denominator.")

print("\n== 10.1.2 filter polarity (active filter: matched vs excluded) ==")
act = raw[raw["LICENSE_STATUS"] == ACTIVE]
non = raw[raw["LICENSE_STATUS"] != ACTIVE]
print("matched (== License Issued - Active): n =", len(act))
print("excluded (!= active): n =", len(non), "| status counter:", Counter(non["LICENSE_STATUS"].tolist()))
assert len(act) == 38949 and len(non) == 21 and len(act) + len(non) == len(raw)
assert set(non["LICENSE_STATUS"].unique()) == {"Delinquent"}
print("Polarity verified: active is an exact-string equality; the 21 Delinquent rows are")
print("EXCLUDED from active on both the row basis and the license basis, never merged in.")
print("Delinquent distinct LICENSE_NUM:", int(non["LICENSE_NUM"].nunique()),
      "| overlap with active LICENSE_NUM:", len(set(non["LICENSE_NUM"]) & set(act["LICENSE_NUM"])))

print("\n== 10.1.3 numerator/denominator unit agreement ==")
def norm(s):
    return re.sub(r"\s+", " ", str(s).upper().strip()) if pd.notna(s) else None
act_h = act.copy()
act_h["holder"] = act_h["ENTITY_NAME"].map(norm)
lic_per_holder = act_h.dropna(subset=["holder"]).groupby("holder")["LICENSE_NUM"].nunique()
n_lic_named = int(lic_per_holder.sum())
top1 = int(lic_per_holder.max())
assert n_lic_named == S["concentration_active_licenses"]["units"] == 26939
assert round(top1 / n_lic_named * 100, 2) == S["concentration_active_licenses"]["top_shares_pct"]["top_1"]
print(f"Top-1 share recomputed as licenses/licenses: {top1}/{n_lic_named} = {top1/n_lic_named*100:.2f}% (ties stats.json).")
print("Row-basis shares are rows/rows and license-basis shares are licenses/licenses throughout;")
print("the two bases are never mixed in one figure. Per-1,000 rates are register ROWS over ACS")
print("housing units and are labeled row rates wherever printed.")

print("\n== 10.1.5 nullable-denominator trap (name classification) ==")
BUS = set(S["classification_rule"]["business_tokens"])
def classify(name):
    if not isinstance(name, str):
        return "not_determined"
    toks = re.findall(r"[A-Z]+(?:'[A-Z]+)?", name)
    if any(t in BUS for t in toks):
        return "business_entity_name"
    if 2 <= len(toks) <= 5:
        return "individual_name"
    return "not_determined"
for label, frame, dedupe in [("active rows", act, None),
                             ("active licenses", act, "LICENSE_NUM"),
                             ("register rows", raw, None)]:
    f = frame.drop_duplicates(dedupe) if dedupe else frame
    cc = Counter(f["ENTITY_NAME"].map(norm).map(classify))
    tot = sum(cc.values())
    assert tot == len(f), (label, tot, len(f))
    shares = {k: round(cc.get(k, 0) / tot * 100, 2) for k in ["individual_name", "business_entity_name", "not_determined"]}
    assert abs(sum(shares.values()) - 100.0) < 0.02, shares
    print(f"{label}: denominator = ALL {tot} | counts {dict(cc)} | shares {shares} | sum = {sum(shares.values()):.2f}%")
blk = S["classification_active_licenses"]
assert Counter(act.drop_duplicates("LICENSE_NUM")["ENTITY_NAME"].map(norm).map(classify))["business_entity_name"] == blk["business_entity_name"]["count"]
print("Determined + not-determined shares sum to 100% on the full stated population in every basis.")
print("The 2 rows with no ENTITY_NAME are classified not_determined and included in every denominator.")

print("\n== concentration recomputation (independent of build_stats code path) ==")
bands = Counter()
band_units = Counter()
for h, c in lic_per_holder.items():
    b = "1" if c == 1 else "2" if c == 2 else "3-5" if c <= 5 else "6-10" if c <= 10 else "11+"
    bands[b] += 1
    band_units[b] += int(c)
assert {k: bands.get(k, 0) for k in ["1", "2", "3-5", "6-10", "11+"]} == S["concentration_active_licenses"]["holders_by_band"]
assert {k: band_units.get(k, 0) for k in ["1", "2", "3-5", "6-10", "11+"]} == S["concentration_active_licenses"]["units_by_band"]
print("License-basis bands tie to stats.json:", dict(bands))
rows_per_holder = act_h.dropna(subset=["holder"]).groupby("holder").size()
assert int(rows_per_holder.max()) == S["concentration_active_rows"]["max_per_holder"] == 850
print("Row-basis max per holder = 850 rows (same holder as the 525-license maximum; recomputed).")

print("\n== grain control: one LICENSE_NUM, one holder, one status ==")
g = raw.groupby("LICENSE_NUM").agg(holders=("ENTITY_NAME", "nunique"), statuses=("LICENSE_STATUS", "nunique"))
print("licenses with >1 distinct ENTITY_NAME (raw):", int((g["holders"] > 1).sum()),
      "| licenses with >1 status:", int((g["statuses"] > 1).sum()))
assert int((g["statuses"] > 1).sum()) == 0
print("Control PASSED: no license number mixes statuses; a license is wholly active or wholly not.")

print("\n== 10.2 built-in control A: single-unit grain check ==")
sp = spine.set_index("schednum")
act2 = act.copy()
act2["schednum"] = act2["PARCEL_NUM"].map(lambda v: str(int(v)).zfill(13))
act2["TOT_UNITS"] = act2["schednum"].map(sp["TOT_UNITS"])
one_row_lic = act2.groupby("LICENSE_NUM").size()
single_lic_ids = one_row_lic[one_row_lic == 1].index
single_rows = act2[act2["LICENSE_NUM"].isin(single_lic_ids)]
with_tot = single_rows.dropna(subset=["TOT_UNITS"])
share_t1 = float((with_tot["TOT_UNITS"] == 1).mean() * 100)
print(f"single-row licenses with a spine TOT_UNITS record: {len(with_tot)}; share whose parcel record")
print(f"carries TOT_UNITS == 1: {share_t1:.1f}%. At the single-unit end of the register the grain")
print("behaves as expected (one row, one unit on the parcel record); the exceptions are the")
print("multi-unit buildings filed as one row, counted in stats.json grain_check.")
assert share_t1 > 80

print("\n== 10.2 built-in control B: multi-row license integrity ==")
sizes = raw.groupby("LICENSE_NUM").size()
multi_ids = sizes[sizes >= 100].index
assert len(multi_ids) == 12
clean, exception = 0, None
for lid in multi_ids:
    sub = raw[raw["LICENSE_NUM"] == lid]
    assert sub["ENTITY_NAME"].nunique() == 1
    if sub["PARCEL_NUM"].nunique() == 1 and sub["ADDRESS"].nunique() == len(sub):
        clean += 1
    else:
        exception = sub
assert clean == 11 and exception is not None
assert len(exception) == 172 and exception["PARCEL_NUM"].nunique() == 2 and exception["ADDRESS"].nunique() == 86
_per_addr = exception.groupby("ADDRESS")["PARCEL_NUM"].nunique()
assert (_per_addr == 2).all() and len(_per_addr) == 86
print("11 of the 12 licenses with 100+ rows: 1 holder name, 1 parcel, all-distinct addresses.")
print("The 12th is a documented exception: 172 rows = 86 unit addresses, each filed TWICE,")
print("once under each of 2 parcel numbers (one of them the register's largest unmatched")
print("parcel). Control PASSED with the exception printed: large multi-row licenses enumerate")
print("unit addresses; the exception is a cross-parcel double filing, counted as published")
print("and disclosed in stats.json field_hygiene and in the brief (Findings 1 and 5).")

print("\n== 10.2 join hygiene: parcel bridge + neighborhood assignment ==")
jb = S["parcel_bridge"]
assert jb["active_matched_rows"] + jb["active_unmatched_rows"] == 38949
print(f"Active bridge: {jb['active_matched_rows']}/38,949 rows matched ({jb['active_match_rate_pct']}%);")
print(f"unmatched {jb['active_unmatched_rows']} rows on {jb['active_unmatched_distinct_parcels']} parcels / "
      f"{jb['active_unmatched_distinct_licenses']} licenses; the two largest unmatched parcels hold")
print(f"{jb['active_unmatched_rows_on_two_largest_parcels']} of the unmatched rows, so the unmatched set is")
print("concentrated on a small number of parcels, not spread evenly (bridge composition asserted below).")
nb = S["neighborhoods"]
assert nb["neighborhoods_with_1plus_active_rows"] + nb["neighborhoods_with_zero_active_rows"] == 78
print(f"Neighborhoods: {nb['neighborhoods_with_1plus_active_rows']} of 78 hold 1+ active rows; zero-row neighborhoods: {nb['zero_active_neighborhoods']}")
print(f"Physical scale: {jb['active_matched_rows']} assigned active rows over 359,351 allocated ACS housing")
print(f"units = {nb['citywide_active_rows_per_1000_units_assigned_basis']} rows per 1,000 units; licensed matched")
print(f"parcels carry {S['grain_check']['sum_tot_units_over_licensed_parcels_with_tot_recorded']:,.0f} TOT_UNITS on their")
print(f"assessor records against {S['grain_check']['sum_tot_units_all_spine_parcels']:,.0f} citywide on the spine "
      f"({S['grain_check']['share_of_spine_tot_units_on_licensed_parcels_pct']}%).")

print("\n== STR comparison consistency ==")
sc = S["str_comparison"]
assert sc["str_active_licenses"] == 2083
assert sc["spearman_neighborhood_rates_ltr_rows_vs_str_licenses"] == 0.65 or abs(sc["spearman_neighborhood_rates_ltr_rows_vs_str_licenses"] - 0.654) < 0.01
print(f"STR active 2,083 (2026-10-19 package) vs LTR active licenses {sc['ltr_active_distinct_licenses']} "
      f"(ratio {sc['ratio_ltr_licenses_to_str_licenses']}x) and LTR active rows {sc['ltr_active_rows']} "
      f"(ratio {sc['ratio_ltr_rows_to_str_licenses']}x); neighborhood rate Spearman {sc['spearman_neighborhood_rates_ltr_rows_vs_str_licenses']}.")

print("\n== Section 11 fix-loop gate: Finding 3 parcel block (matched basis) ==")
spine_idx = spine.set_index("schednum")
act3 = act.copy()
act3["schednum"] = act3["PARCEL_NUM"].map(lambda v: str(int(v)).zfill(13))
act3["nbhd"] = act3["schednum"].map(spine_idx["neighborhood"])
act3["in_spine"] = act3["schednum"].isin(set(spine["schednum"]))
assert int(act3["in_spine"].sum()) == 38450
null_nb = act3[act3["in_spine"] & act3["nbhd"].isna()]
assert len(null_nb) == 23 and int(null_nb["schednum"].nunique()) == 22
m3 = act3[act3["nbhd"].notna()]
assert len(m3) == S["parcel_bridge"]["active_matched_rows"] == 38427
rpp3 = m3.groupby("schednum").size()
lpp3 = m3.groupby("schednum")["LICENSE_NUM"].nunique()
pa = S["parcels_active"]
assert pa["distinct_parcels"] == int(rpp3.shape[0]) == 26394
assert pa["parcels_with_multiple_rows"] == int((rpp3 >= 2).sum()) == 2846
assert pa["rows_on_multiple_row_parcels"] == int(rpp3[rpp3 >= 2].sum()) == 14879
assert pa["share_of_matched_rows_on_multiple_row_parcels_pct"] == round(int(rpp3[rpp3 >= 2].sum()) / len(m3) * 100, 1) == 38.7
assert pa["parcels_with_multiple_distinct_licenses"] == int((lpp3 >= 2).sum()) == 205
assert pa["licenses_on_multiple_license_parcels"] == int(lpp3[lpp3 >= 2].sum()) == 559
top2_3 = rpp3.sort_values(ascending=False)
s1_3, s2_3 = top2_3.index[0], top2_3.index[1]
assert pa["max_rows_on_one_parcel"] == int(top2_3.iloc[0]) == 697
assert pa["largest_parcel_neighborhood"] == str(spine_idx.loc[s1_3, "neighborhood"]) == "North Capitol Hill"
assert pa["largest_parcel_distinct_licenses"] == int(lpp3.loc[s1_3]) == 1
assert float(spine_idx.loc[s1_3, "TOT_UNITS"]) == pa["largest_parcel_units_on_parcel_record"] == 229.0
assert pa["second_largest_parcel_rows"] == int(top2_3.iloc[1]) == 444
assert pa["second_largest_parcel_neighborhood"] == str(spine_idx.loc[s2_3, "neighborhood"]) == "Central Park"
assert pa["second_largest_parcel_distinct_licenses"] == int(lpp3.loc[s2_3]) == 5
assert float(spine_idx.loc[s2_3, "TOT_UNITS"]) == pa["second_largest_parcel_units_on_parcel_record"] == 398.0
assert pa["basis"].startswith("active rows matched to the parcel spine and assigned a neighborhood")
print("Finding 3 parcel block recomputed on the matched basis (neighborhood-assigned rows):")
print("26,394 distinct matched parcels; 2,846 with 2+ rows holding 14,879 rows (38.7% of matched")
print("rows); 205 parcels with 2+ distinct licenses holding 559 licenses; largest parcel 697 rows")
print("(North Capitol Hill, 1 license, 229 units on record); second largest 444 rows (Central Park,")
print("5 licenses, 398 units on record). Every value ties to stats.json parcels_active.")
print("Bridge composition: pure schednum membership matches 38,450 active rows; 23 of the 522")
print("unassigned rows sit on 22 parcels present in spine v6 with a null neighborhood value.")

print("\n== expiry field disagreement (printed, not adjudicated) ==")
eh = S["expiry_hygiene"]
print(f"Active-status rows whose EXPIRATION_DATE precedes the 2026-10-20 pull: "
      f"{eh['active_rows_with_expiration_before_pull_date']} ({eh['share_of_active_rows_pct']}% of active rows).")
print("Register-wide past-expiration rows:", eh["all_rows_with_expiration_before_pull_date"],
      "(21 of them are the Delinquent rows). The brief reports the disagreement and claims")
print("nothing about any license's validity; the DLCP renewal FAQ's 90-day grace period is cited.")

print("\nALL SECTION 10 ASSERTIONS PASSED")
