# Independent Verification Ledger — Denver Long-Term Rental Licenses Brief (2026-10-20)

Section 11 independent verification pass, run 2026-10-20. This ledger was produced by a
verifier who did NOT read or reuse the package's `code/build_stats.py` or
`code/audit_section10.py`. All figures below were recomputed with a fresh, separately
written implementation (scratch script under /tmp) reading only:

- Raw snapshot: `stack/denver/snapshots/2026-10-20/rental_licenses.parquet`
- Parcel spine: `stack/denver/joins/parcel_spine_v6.parquet`
- ACS layer: `stack/denver/layers/acs_neighborhood_units.parquet`
- STR comparison package (2026-10-19): `stats.json` + `data/neighborhood_panel.csv`

"Claimed" is the value in this package's `stats.json` / `brief-draft.md`.
Verdicts: **reproduced** (independent recomputation ties at printed precision) /
**corrected** / **caveated** (figure ties under the package's operative basis, but the
basis or label needs a note) / **refuted**.

## Summary

- Figures checked: 74 (61 in the main ledger, 13 spot checks)
- Reproduced: 66
- Caveated: 8 (rows 29–35 and S13; two root causes — the parcel-bridge "matched"
  definition / parcel-stacking basis, and the name-merge sensitivity tokenization.
  Every caveated count ties exactly under the package's operative basis; no printed
  headline figure changes under either basis)
- Corrected: 0
- Refuted: 0

## Ledger

| # | Figure | Claimed | Recomputed | Verdict | Notes |
|---|--------|---------|------------|---------|-------|
| 1 | Total register rows | 38,970 | 38,970 | reproduced | |
| 2 | Status counter — Active | 38,949 | 38,949 | reproduced | exact string "License Issued - Active" |
| 3 | Status counter — Delinquent | 21 | 21 | reproduced | no license mixes statuses (0 multi-status licenses) |
| 4 | Distinct LICENSE_NUM, all rows | 26,962 | 26,962 | reproduced | |
| 5 | Distinct LICENSE_NUM, active | 26,941 | 26,941 | reproduced | 26,941 + 21 delinquent = 26,962 |
| 6 | Distinct holders (normalized ENTITY_NAME) | 20,780 | 20,780 | reproduced | uppercase, whitespace collapsed |
| 7 | Named active licenses (holder basis denominator) | 26,939 | 26,939 | reproduced | 2 active licenses on 2 rows carry no ENTITY_NAME |
| 8 | Sole-license holders | 18,471 | 18,471 | reproduced | |
| 9 | Sole-license share | 68.6% (68.57%) | 68.57% | reproduced | 18,471 / 26,939 |
| 10 | Largest holder, licenses | 525 | 525 | reproduced | |
| 11 | Largest holder share | 1.95% | 1.95% | reproduced | 525 / 26,939 |
| 12 | Top 5 holders share | 3.89% | 3.89% | reproduced | top-5 count 1,048 licenses |
| 13 | Top 10 holders share | 4.86% | 4.86% | reproduced | top-10 count 1,310 licenses |
| 14 | Top 25 holders share | 6.36% | 6.36% | reproduced | top-25 count 1,712 licenses |
| 15 | Holder band — 1 license | 18,471 holders | 18,471 | reproduced | |
| 16 | Holder band — 2 licenses | 1,430 holders | 1,430 | reproduced | 2,860 licenses |
| 17 | Holder band — 3–5 licenses | 685 holders | 685 | reproduced | 2,431 licenses |
| 18 | Holder band — 6–10 licenses | 129 holders | 129 | reproduced | 918 licenses |
| 19 | Holder band — 11+ licenses | 65 holders | 65 | reproduced | |
| 20 | Licenses held by 11+ band | 2,259 (8.4%) | 2,259 (8.39%) | reproduced | |
| 21 | Max rows on one LICENSE_NUM | 697 | 697 | reproduced | |
| 22 | Licenses with 2+ rows | 2,833 | 2,833 | reproduced | |
| 23 | Rows in multi-row licenses | 14,841 | 14,841 | reproduced | 38.1% of register |
| 24 | Licenses with 100+ rows | 12 | 12 | reproduced | all 12 active |
| 25 | Double-filed license | 172 rows, 86 distinct addresses, 2 parcels | 172 rows, 86 distinct addresses, 2 parcels | reproduced | the other 11 licenses with 100+ rows each sit on 1 parcel; license number withheld per package product rule |
| 26 | Classification, active licenses — individual | 16,012 (59.43%) | 16,012 (59.43%) | reproduced | see Note A on tokenization |
| 27 | Classification, active licenses — business | 9,994 (37.10%) | 9,994 (37.10%) | reproduced | business token set taken from stats.json `classification_rule` |
| 28 | Classification, active licenses — not determined | 935 (3.47%) | 935 (3.47%) | reproduced | see Note A |
| 29 | Parcel bridge — active matched rows | 38,427 (98.66%) | 38,427 (98.66%) on the package's operative basis | caveated | see Note B |
| 30 | Parcel bridge — active unmatched rows | 522 | 522 on the package's operative basis | caveated | see Note B |
| 31 | Unmatched — distinct parcels | 205 | 205 on the package's operative basis | caveated | see Note B |
| 32 | Unmatched — distinct licenses | 213 | 213 on the package's operative basis | caveated | see Note B |
| 33 | Parcels with 2+ rows | 2,911 | 2,911 | caveated | count is over all 26,599 register parcel keys; see Note C |
| 34 | Rows on 2+-row parcels | 15,261 | 15,261 | caveated | see Note C |
| 35 | Parcels with 2+ distinct licenses | 212 | 212 | caveated | all-parcel-keys basis; see Note C |
| 36 | Max distinct licenses on one parcel | 29 | 29 | reproduced | Hampden South; parcel TOT_UNITS 8 |
| 37 | Grain — matched licensed parcels with TOT_UNITS recorded | 26,309 | 26,309 | reproduced | on the package's matched basis (Note B); 85 matched parcels have null TOT_UNITS |
| 38 | Grain — TOT_UNITS sum on licensed parcels | 133,839 | 133,839 | reproduced | |
| 39 | Grain — TOT_UNITS sum, all spine parcels | 445,057 | 445,057 | reproduced | |
| 40 | Grain — licensed share of assessor units | 30.1% | 30.1% | reproduced | identical at printed precision on either bridge basis (133,861 / 445,057 also rounds to 30.1%) |
| 41 | Grain — rows equal TOT_UNITS | 22,107 parcels | 22,107 | reproduced | package matched basis |
| 42 | Grain — rows below TOT_UNITS | 2,745 parcels | 2,745 | reproduced | identical on either basis |
| 43 | Grain — rows above TOT_UNITS | 1,457 parcels | 1,457 | reproduced | package matched basis |
| 44 | Grain — single-row parcels with TOT_UNITS ≥ 10 | 1,026 (73,501 units) | 1,026 (73,501 units) | reproduced | identical on either basis |
| 45 | Neighborhoods with active rows | 78 of 78 | 78 of 78 | reproduced | no zero-row neighborhoods |
| 46 | Citywide rate, all active rows | 108.4 per 1,000 ACS units | 108.4 | reproduced | denominator is the allocated ACS total 359,351.5, per Methods |
| 47 | Citywide rate, assigned rows only | 106.9 per 1,000 | 106.9 | reproduced | 38,427 / 359,351.5 |
| 48 | Median neighborhood rate | 107.1 per 1,000 | 107.1 | reproduced | median across all 78 neighborhoods |
| 49 | Whittier rate | 286.1 per 1,000 (644 rows) | 286.1 (644 rows, 2,251.0 ACS units) | reproduced | 2.6× the citywide all-rows rate |
| 50 | Top-5 neighborhood count share | 19.7% | 19.7% | reproduced | Capitol Hill 1,887; Central Park 1,617; Five Points 1,503; Speer 1,321; Gateway–Green Valley Ranch 1,227; sum 7,555 / 38,427 assigned rows |
| 51 | Vintage — 2022 prefix licenses | 2,233 | 2,233 | reproduced | |
| 52 | Vintage — 2023 prefix licenses | 13,292 (49.3%) | 13,292 (49.3%) | reproduced | |
| 53 | Vintage — 2024 prefix licenses | 6,203 | 6,203 | reproduced | |
| 54 | Vintage — 2025 prefix licenses | 3,088 | 3,088 | reproduced | |
| 55 | Vintage — 2026 prefix licenses | 2,125 | 2,125 | reproduced | |
| 56 | Vintage — 2023-or-later share | 91.7% | 91.7% | reproduced | |
| 57 | RENEWAL_CREATED = 1/1/1900 on active rows | 38,949 (all active rows) | 38,949 | reproduced | the only non-sentinel values are the 21 Delinquent rows |
| 58 | ZIP = 0 rows | 3,436 | 3,436 | reproduced | register-wide |
| 59 | ZIP null rows | 773 | 773 | reproduced | register-wide |
| 60 | Active rows with expiration before 2026-10-20 | 2 | 2 | reproduced | register-wide past-expiration rows 23, of which 21 are the Delinquent rows |
| 61 | Exact duplicate license/parcel/address pairs | 6 groups (12 rows) | 6 groups (12 rows) | reproduced | no group exceeds 2 rows; all 6 groups are active |

## Spot checks — figures in brief-draft.md prose beyond the assigned list

Chosen by the verifier from the brief text (not in the assigned checklist):

| # | Figure (location) | Claimed | Recomputed | Verdict |
|---|-------------------|---------|------------|---------|
| S1 | Row-basis concentration: largest holder's rows (Finding 2) | 850 rows, 2.18% of 38,947 named active rows | 850 rows, 2.18% | reproduced |
| S2 | Row-basis 11+ band (Finding 2) | 260 holders holding 10,322 rows (26.5%) | 260 holders, 10,322 rows, 26.5% | reproduced |
| S3 | Second-largest parcel (Finding 3) | 444 rows, Central Park, 5 licenses, 398 units on assessor record | 444 rows, Central Park, 5 licenses, TOT_UNITS 398 | reproduced |
| S4 | Largest parcel detail (Findings 1/3) | 697 rows, North Capitol Hill, single license, 229 units on record | 697 rows, North Capitol Hill, 1 license, TOT_UNITS 229 | reproduced |
| S5 | Built-in control A (Finding 1) | 89.2% of single-row licenses with a TOT_UNITS record sit on TOT_UNITS = 1 parcels | 89.2% (n = 23,909 single-row licenses with a record) | reproduced |
| S6 | Licenses spanning multiple parcels / neighborhoods (Finding 1) | 19 licenses span 2+ parcels; 8 span 2+ neighborhoods | 19; 8 | reproduced |
| S7 | Expiration cohorts, active rows (Finding 5) | largest cohort 2027 with 18,095 rows; years run 2026–2031 | 2026: 2,921; 2027: 18,095; 2028: 10,576; 2029: 3,885; 2030: 3,470; 2031: 2 (sum 38,949) | reproduced |
| S8 | Classification on other bases (Finding 2) | rows: business 19,230 of 38,949 (49.37%); holders: business 6,469 of 20,780 (31.13%), individual 13,516 (65.04%) | rows: 19,230 (49.37%), individual 18,602, ND 1,117; holders: 6,469 (31.13%), individual 13,516, ND 795 | reproduced |
| S9 | STR comparison (Finding 4) | STR active licenses 2,083; ratios 12.9× (licenses) and 18.7× (rows); STR citywide 5.8 per 1,000; Spearman 0.654 (rates) / 0.698 (counts); STR zero neighborhoods Auraria, Kennedy, Sun Valley; Whittier STR rate 27.1; North Capitol Hill LTR 183.3 vs STR 3.2 (19 licenses) | 2,083 (STR package status counter); 12.9×; 18.7×; 5.8; Spearman 0.654 / 0.698 across the 78 neighborhoods (LTR side recomputed from raw, STR side from the 2026-10-19 panel); zero list matches; Whittier STR 27.1; North Capitol Hill LTR 183.33, STR 3.2 on 19 licenses | reproduced |
| S10 | Top-10 neighborhood count share (Finding 4) | 32.7% of assigned rows | 32.7% | reproduced |
| S11 | Register-wide parcel bridge (Methods) | 38,471 of 38,970 rows matched (98.7%) | 38,471 (98.72%) by pure schednum membership | reproduced |
| S12 | Name-merge sensitivity maxima (Finding 2) | first+last-token merge max 525 licenses; initial+surname over-merge max 1,160 licenses | 525; 1,160 | reproduced |
| S13 | Name-merge sensitivity group counts (Finding 2) | first+last merge: 17,496 groups, 45.4% of licenses in 2+ groups; over-merge: 12,979 groups, 60.8% in 2+ groups | first+last: 17,461 groups, 2,797 groups with 2+, 12,275 licenses in them (45.6%); over-merge: 12,941 groups, 60.9% in 2+ groups | caveated — maxima tie exactly; group counts/shares differ by ≤38 groups and ≤0.2 pp under a straightforward alphabetic-token implementation, indicating a minor undocumented tokenization detail in the builder's merge keys. No other figure depends on these sensitivity bounds. |

## Notes

**Note A — classification tokenization (rows 26–28, S8).** The counts reproduce exactly
(16,012 / 9,994 / 935 on licenses; also exact on rows and holders) when a trailing
parenthetical annotation (e.g. "(COUPLE)", "(MARRIED COUPLE)") is not counted as name
tokens. A naive count of all alphabetic tokens gives 16,008 individual / 939 not
determined — a 4-license difference (4 holders, 4 rows). The documented rule in
stats.json ("tokens are the alphabetic words of the normalized name") does not mention
the parenthetical handling. No brief prose figure changes either way: at the brief's
printed precision the shares are 59.4% / 37.1% / 3.5% under both tokenizations
(stats.json's two-decimal shares 59.43 / 3.47 follow the builder's tokenization).

**Note B — parcel bridge basis (rows 29–32, and the matched basis behind rows 37–43).**
The Methods state the bridge as schednum membership against spine v6. Pure schednum
membership gives: active matched 38,450 rows (98.72%), unmatched 499 rows on 183
parcels / 191 licenses. The package's figures (38,427 / 522 / 205 / 213) reproduce
exactly when "matched" is taken as "assigned a neighborhood through the spine": 23 of
the 522 "unmatched" active rows sit on 22 parcels that ARE present in spine v6 (each
with TOT_UNITS = 1) but whose spine neighborhood value is null, so they receive no
neighborhood. Consequences, all internally consistent within the package: (1) the
stats.json bridge note's phrase "parcels absent from the spine snapshot" is imprecise
for those 22 parcels — they are present but neighborhood-less; (2) the grain-check
block (rows 37–43) is computed on the same operative basis, excluding those 22 parcels
(on a pure-schednum basis the grain block would read: 26,331 parcels with TOT_UNITS
recorded, sum 133,861, equal/below/above 22,128 / 2,745 / 1,458 — the 30.1% coverage
share and the single-row ≥10-unit count are unchanged); (3) the register-wide bridge
figure (S11, 38,471) IS computed by pure schednum membership, so the package uses the
membership basis register-wide and the neighborhood-assignment basis for active rows.
The two largest unmatched parcels hold 157 rows on both bases.

**Note C — parcel stacking basis (rows 33–35).** The counts 2,911 multi-row parcels /
15,261 rows / 212 multi-license parcels (574 licenses on them) are computed over all
26,599 distinct parcel keys in the active register, including the unmatched parcels;
the brief's Finding 3 prose discloses this ("On 23,688 of the register's 26,599 parcel
keys…"), but the stats.json `parcels_active` basis label ("unmatched active rows
excluded") does not match the computation. On the package's matched basis the same
statistics are 2,846 parcels / 14,879 rows / 205 parcels / 559 licenses. The maxima
(697 rows; 29 licenses) are identical on every basis. Finding 3's "39.7 percent of
matched rows" divides the all-keys numerator (15,261) by the matched-row denominator
(38,427) — arithmetically correct as printed, but the numerator and denominator are on
different parcel bases.

## Method note

Holder key: ENTITY_NAME uppercased with whitespace collapsed, applied to active rows;
concentration counts distinct LICENSE_NUM per holder over the 26,939 named active
licenses. Parcel key: `str(int(PARCEL_NUM)).zfill(13)`. Vintage: first four characters
of LICENSE_NUM over distinct active licenses. Neighborhood rates: active rows assigned
via the spine neighborhood, over `acs_neighborhood_units.parquet` (allocated total
359,351.5). Spearman coefficients computed as Pearson correlation of average ranks.
Expiration comparison date: 2026-10-20 (the pull date), strict less-than.
