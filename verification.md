# Verification - Denver residential rental licenses brief (2026-10-20)

Dataset: ODC_residential_rental_property_active_licenses, Denver Open Data
Catalog, ArcGIS FeatureServer table 52 (Department of Licensing and Consumer
Protection). Fresh full-service pull 2026-10-20 (2026-10-20T12:32:53Z), 38,970
records, service last edit 2026-10-20T09:40:45Z. Pulled count asserted equal to
the live service count before writing. Snapshot + pull log + sha256:
stack/denver/snapshots/2026-10-20/rental_licenses.parquet and
pull_log_rental_2026-10-20.json (sha256
8f72f12d69212ede53b0ba43f153255b238e12d81e65620a651fc12574dcc5a5).
Denominators: ACS 2020-2024 5-year B25001 housing units (warehouse layer
acs_neighborhood_units.parquet; same basis as the October 17, 18, and 19
briefs). Parcel bridge: direct schednum match on parcel spine v6.
STR comparison: the published 2026-10-19 STR package (stats.json + panel).

## Field semantics, established from the service (2026-10-20)

- LICENSE_STATUS is the only status field and the brief's active basis is the
  exact string "License Issued - Active". Full counter, recorded before any
  filter: Active 38,949 rows; Delinquent 21 rows. No license number mixes
  statuses (asserted in the audit's grain control).
- GRAIN (the brief's central fact): LICENSE_NUM has 26,962 distinct values for
  38,970 rows. Rows sharing a license number are the unit/address filings of
  one license. 24,129 licenses carry 1 row; 2,833 carry 2 or more (14,841
  rows); the maximum is 697 rows on one license, one holder, one parcel,
  all-distinct addresses. Row-level check of the 12 licenses with 100 or more
  rows found one documented exception: a license filing each of its 86 unit
  addresses twice, once under each of two parcel numbers (172 rows). The FAQ's
  own structure (single-unit properties license individually; a multi-unit
  property can hold one license covering multiple units, addresses, or
  structures on single or contiguous parcels under one ownership) matches
  this grain. Only 19 active licenses span more than one parcel and only 8
  span more than one neighborhood.
- ENTITY_NAME is null on 2 rows (both active, 2 distinct licenses). Holder
  counts run over the 26,939 named active licenses and 38,947 named active
  rows; the 2 unnamed licenses are reported wherever holder counts appear.
- MULTIPLE_LICENSES is constant "Stand Alone" on all 38,970 rows, including
  the 697 rows of the largest license. It is not a multi-license signal.
- RELATIONSHIP is null on all active rows and "Renewal" on the 21 Delinquent
  rows. RENEWAL_STATUS is null on active rows and "Pending" on the Delinquent
  rows. No figure rests on either.
- RENEWAL_CREATED reads 1/1/1900 on all 38,949 active rows (99.95 percent of
  the table); the only real dates are the 21 Delinquent rows. Sentinel; unused.
- PARCEL_NUM (Double): integers of 10 to 12 digits {12: 37,169; 11: 1,742;
  10: 59}; no nulls, zeros, or negatives. schednum = zfill(13).
- ZIP: 0 on 3,436 rows, null on 773; treated as unknown; used for nothing.
- EXPIRATION_DATE disagrees with status on a small dated set: 2 active rows
  carry a past expiration at pull; the other 21 past-expiration rows are
  exactly the Delinquent rows. Reported in Finding 5 without a compliance claim.
- Exact duplicates: 6 license/parcel/address combinations appear twice
  (12 rows). Counted as published; no printed figure changes if removed.
- There is no original-issue date field and no tax/ID field in this service.
  Vintage uses the LICENSE_NUM year prefix, labeled as such.

## Methods checklist (brief-writing standards Section 3)

- Base rates and exposure: neighborhood footprint is reported as counts AND
  as rows per 1,000 ACS housing units, labeled row rates; the citywide rate
  (108.4 per 1,000 on all active rows; 106.9 on assigned rows) and the median
  neighborhood rate (107.1 per 1,000, over all 78 neighborhoods; this register
  has no zero-row neighborhoods) are printed next to every ranking. No raw
  share is presented as a density, and no rate is called a coverage rate.
- Direction of causality: Finding 4 (LTR row rates vs STR license rates,
  Spearman 0.654 on rates, 0.698 on counts) is stated as geographic
  co-location only; no causal direction is claimed in either register
  comparison, and the housing-form divergence (North Capitol Hill) is printed
  beside the correlation.
- Category and definition changes: LICENSE_STATUS has two values in this
  pull; the program's phase-in (multi-unit from 2023-01-01, single-unit from
  2024-01-01, per the city's own documents) is a coverage change over time,
  not a category rename, and is treated as such: the brief makes no
  time-series claim from this single snapshot beyond the prefix-year survivor
  stock, which is labeled a survivor stock, not an issuance series.
- Time windows: the register snapshot is a point in time (2026-10-20); the
  program rules cited were in effect for the whole post-phase-in period; the
  STR comparison figures are dated 2026-10-19 and cited as such.
- Joins: parcel bridge 38,471 of 38,970 rows register-wide (98.72 percent)
  and 38,427 of 38,949 active rows (98.66 percent). Unmatched active rows
  (522, 1.34 percent) concentrate on 205 parcels, two of which hold 157 rows,
  so the unmatched set is concentrated in a few parcels absent from the
  2026-10-15 spine rather than spread evenly; unmatched licenses are counted
  in every citywide total and excluded from parcel and neighborhood tables
  only. The unmatched share is below the 5 percent flag threshold, and its
  concentration is printed in the brief.
- Small numbers: the concentration findings rest on the full register
  (26,941 active licenses); the smallest printed neighborhood count in the
  rate top-5 is 374 rows (Clayton) with its denominator printed in the panel.
  The 2 unnamed licenses and the 21 Delinquent rows are always printed with
  their counts adjacent to any share that excludes them.
- Official definitions: "active" is the publisher's own status string;
  "residential rental property" and the license structure are the program's
  own definitions, cited in sources.md and used as context only.
- Layering admission test: ACS housing layer - enables exposure rates
  (Finding 4 cannot rank neighborhoods without it) - ADMITTED. Parcel spine -
  assigns parcels and neighborhoods, supplies the TOT_UNITS records behind
  the Finding 1 grain test and the Finding 5 coverage figure, and exposes the
  Finding 3 parcel patterns (none can be stated from the register alone) -
  ADMITTED. STR panel - enables the labeled two-register comparison in
  Finding 4, which no single source contains - ADMITTED. No further layer was
  used; in particular no renter-tenure layer exists in the warehouse, and its
  absence is reported in Finding 5 rather than worked around.

## Pre-flight audit (Section 10)

Script: code/audit_section10.py (ships in this package). Full output:
data/audit_output.txt. Result: ALL SECTION 10 ASSERTIONS PASSED (37 asserts,
exit code 0, run in the foreground and read back from the output file).
Full output:

```
snapshot rows 38970

== 10.1.4 categorical exhaustiveness (counters recorded before any filter) ==
LICENSE_STATUS full counter: {'Delinquent': 21, 'License Issued - Active': 38949}
LICENSE_TYPE full counter: {'Residential Rental Property': 38970}
MULTIPLE_LICENSES full counter: {'Stand Alone': 38970}
RELATIONSHIP non-null values: Counter({'Renewal': 21})
RENEWAL_STATUS non-null values: Counter({'Pending': 21})

== 10.1.1 zero/null sentinel traps ==
ENTITY_NAME nulls: 2
PARCEL_NUM nulls: 0 | zeros: 0 | negatives: 0
PARCEL_NUM digit-length counter (Double field, leading zeros dropped): {12: 37169, 11: 1742, 10: 59} - schednum = str(int(v)).zfill(13) restores the canonical key for every row.
ZIP zeros (sentinel, treated as unknown): 3436 | ZIP nulls: 773 - ZIP is used for no figure.
RENEWAL_CREATED sentinel 1/1/1900 rows: 38949 (99.95%) - excluded from every date use;
the field is used for nothing in this brief. 'Unknown' dates are never placed in a rate denominator.

== 10.1.2 filter polarity (active filter: matched vs excluded) ==
matched (== License Issued - Active): n = 38949
excluded (!= active): n = 21 | status counter: Counter({'Delinquent': 21})
Polarity verified: active is an exact-string equality; the 21 Delinquent rows are
EXCLUDED from active on both the row basis and the license basis, never merged in.
Delinquent distinct LICENSE_NUM: 21 | overlap with active LICENSE_NUM: 0

== 10.1.3 numerator/denominator unit agreement ==
Top-1 share recomputed as licenses/licenses: 525/26939 = 1.95% (ties stats.json).
Row-basis shares are rows/rows and license-basis shares are licenses/licenses throughout;
the two bases are never mixed in one figure. Per-1,000 rates are register ROWS over ACS
housing units and are labeled row rates wherever printed.

== 10.1.5 nullable-denominator trap (name classification) ==
active rows: denominator = ALL 38949 | counts {'individual_name': 18602, 'business_entity_name': 19230, 'not_determined': 1117} | shares {'individual_name': 47.76, 'business_entity_name': 49.37, 'not_determined': 2.87} | sum = 100.00%
active licenses: denominator = ALL 26941 | counts {'individual_name': 16012, 'business_entity_name': 9994, 'not_determined': 935} | shares {'individual_name': 59.43, 'business_entity_name': 37.1, 'not_determined': 3.47} | sum = 100.00%
register rows: denominator = ALL 38970 | counts {'individual_name': 18614, 'business_entity_name': 19239, 'not_determined': 1117} | shares {'individual_name': 47.76, 'business_entity_name': 49.37, 'not_determined': 2.87} | sum = 100.00%
Determined + not-determined shares sum to 100% on the full stated population in every basis.
The 2 rows with no ENTITY_NAME are classified not_determined and included in every denominator.

== concentration recomputation (independent of build_stats code path) ==
License-basis bands tie to stats.json: {'1': 18471, '3-5': 685, '2': 1430, '11+': 65, '6-10': 129}
Row-basis max per holder = 850 rows (same holder as the 525-license maximum; recomputed).

== grain control: one LICENSE_NUM, one holder, one status ==
licenses with >1 distinct ENTITY_NAME (raw): 0 | licenses with >1 status: 0
Control PASSED: no license number mixes statuses; a license is wholly active or wholly not.

== 10.2 built-in control A: single-unit grain check ==
single-row licenses with a spine TOT_UNITS record: 23909; share whose parcel record
carries TOT_UNITS == 1: 89.2%. At the single-unit end of the register the grain
behaves as expected (one row, one unit on the parcel record); the exceptions are the
multi-unit buildings filed as one row, counted in stats.json grain_check.

== 10.2 built-in control B: multi-row license integrity ==
11 of the 12 licenses with 100+ rows: 1 holder name, 1 parcel, all-distinct addresses.
The 12th is a documented exception: 172 rows = 86 unit addresses, each filed TWICE,
once under each of 2 parcel numbers (one of them the register's largest unmatched
parcel). Control PASSED with the exception printed: large multi-row licenses enumerate
unit addresses; the exception is a cross-parcel double filing, counted as published
and disclosed in stats.json field_hygiene and in the brief (Findings 1 and 5).

== 10.2 join hygiene: parcel bridge + neighborhood assignment ==
Active bridge: 38427/38,949 rows matched (98.66%);
unmatched 522 rows on 205 parcels / 213 licenses; the two largest unmatched parcels hold
157 of the unmatched rows, so the unmatched set is
concentrated in a few parcels absent from the 2026-10-15 spine, not spread evenly.
Neighborhoods: 78 of 78 hold 1+ active rows; zero-row neighborhoods: []
Physical scale: 38427 assigned active rows over 359,351 allocated ACS housing
units = 106.9 rows per 1,000 units; licensed matched
parcels carry 133,839 TOT_UNITS on their
assessor records against 445,057 citywide on the spine (30.1%).

== STR comparison consistency ==
STR active 2,083 (2026-10-19 package) vs LTR active licenses 26941 (ratio 12.9x) and LTR active rows 38949 (ratio 18.7x); neighborhood rate Spearman 0.654.

== expiry field disagreement (printed, not adjudicated) ==
Active-status rows whose EXPIRATION_DATE precedes the 2026-10-20 pull: 2 (0.005% of active rows).
Register-wide past-expiration rows: 23 (21 of them are the Delinquent rows). The brief reports the disagreement and claims
nothing about any license's validity; the DLCP renewal FAQ's 90-day grace period is cited.

ALL SECTION 10 ASSERTIONS PASSED
```

Gate summary:
- 10.1.1 sentinels: ENTITY_NAME nulls enumerated (2); PARCEL_NUM digit lengths
  enumerated with zfill normalization and no sentinel values; ZIP 0 (3,436) and
  null (773) treated as unknown and unused; RENEWAL_CREATED 1/1/1900 on 38,949
  rows treated as a sentinel and used for nothing. "Unknown" values are
  excluded from no denominator silently: classification denominators include
  the not-determined share, and holder counts state the 2 unnamed licenses.
- 10.1.2 polarity: the active filter is an exact-string equality; matched
  38,949 rows vs excluded 21 (all Delinquent). Delinquent is never merged
  into active on either basis; the Delinquent license numbers do not overlap
  the active set.
- 10.1.3 unit agreement: top-1 share recomputed as licenses over licenses
  (525/26,939 = 1.95 percent) and ties to stats.json; row-basis and
  license-basis shares are computed within their own basis throughout, and
  the audit asserts the two bases are never mixed in one figure.
- 10.1.4 exhaustiveness: LICENSE_STATUS (2 values), LICENSE_TYPE (1 value),
  and MULTIPLE_LICENSES (1 constant value) counters recorded before filtering
  and summing to the pulled total; RELATIONSHIP and RENEWAL_STATUS non-null
  values enumerated (Renewal 21; Pending 21).
- 10.1.5 nullable denominators: the name classification is computed on ALL
  active rows (38,949), ALL active licenses (26,941), and ALL register rows
  (38,970); determined plus not-determined shares sum to 100.00 percent in
  every basis. No NaN-skipping aggregation is used anywhere.
- 10.2 controls: grain control (no license mixes holder or status), Control A
  (single-unit grain check, 89.2 percent), and Control B (multi-row license
  integrity, 11 of 12 clean with the double-filed exception printed) all
  pass; see the next section.
- 10.3 documentation sync: README dependency list was checked against actual
  code imports (pandas, numpy, pyarrow, matplotlib, Pillow; standard library
  otherwise). Every number in brief-draft.md and social-drafts.md was
  cross-checked against the final stats.json after the last build_stats.py
  run (Section 12.5 assertion: the hero composite asserts its figures against
  stats.json at build time and the audit asserts the register, concentration,
  classification, bridge, neighborhood, grain, and STR-comparison blocks).

## Built-in controls (Section 10.2.2)

- Grain control: grouped by LICENSE_NUM over the raw snapshot, no license
  number carries more than one distinct ENTITY_NAME (raw) and none carries
  more than one LICENSE_STATUS. A license is a single holder's single-status
  instrument in this table, which is what makes the license basis well-defined.
- Control A, single-unit grain check: among the 23,909 single-row licenses
  with a spine TOT_UNITS record, 89.2 percent sit on parcels whose record
  carries TOT_UNITS of exactly 1. At the single-unit end the register's grain
  behaves as one row for one unit; the exceptions are the multi-unit buildings
  filed as one row, counted in stats.json grain_check (1,026 single-row
  parcels with TOT_UNITS of 10 or more, 73,501 units on their records).
- Control B, multi-row license integrity: the 12 licenses with 100 or more
  rows were inspected row by row. 11 sit under one holder name on one parcel
  with all-distinct addresses. The 12th files 86 addresses twice, once under
  each of two parcel numbers (172 rows); one of its parcel numbers is the
  largest unmatched parcel in the bridge, and its twin is matched, so half
  its rows carry a neighborhood and half do not. The exception is disclosed
  in stats.json (field_hygiene.double_filed_license) and in the brief.
- Sensitivity (not a control): name-variant merging. First-and-last-token
  merging leaves the maximum unchanged (525 licenses) but reduces groups to
  17,496 and puts 45.4 percent of licenses in groups of two or more, because
  business names collide on first and last tokens. First-initial over-merging
  (known to combine different holders) gives a maximum group of 1,160
  licenses and 60.8 percent of licenses in groups of two or more: token
  grouping alone could move the distribution substantially for entity names,
  which is why the exact-name basis is primary and the merges are printed
  as bounds, not measurements.

## Cross-document figure assertion (Section 12.5)

Figures asserted equal across stats.json, brief-draft.md, social-drafts.md,
charts, and hero.png at build time: register 38,970 rows; active 38,949 rows
and 26,941 licenses; delinquent 21; holders 20,780; named licenses 26,939;
bands (license basis) 18,471 / 1,430 / 685 / 129 / 65 holders and 18,471 /
2,860 / 2,431 / 918 / 2,259 licenses; top shares 1.95 / 3.89 / 4.86 / 6.36
percent; exactly-one share 68.57 percent (hero prints 68.6 percent);
classification (license basis) individual 59.43, business 37.10, not
determined 3.47 percent; parcels (matched basis) 26,394 matched distinct,
2,846 with 2 or more rows, 14,879 rows on them (38.7 percent of matched
rows), max 697 rows (North Capitol Hill, 229 units on the record, 1
license), second largest 444 rows (Central Park, 398 units on the record,
5 licenses), 205 parcels with 2 or more licenses holding 559 licenses,
max 29 licenses (Hampden South, 8 units on the record); grain 22,107 rows-equal /
2,745 rows-below / 1,457 rows-above, 1,026 single-row parcels with 10 or
more units (73,501 units); coverage 133,839 of 445,057 assessor-record units
(30.1 percent); neighborhoods 78 of 78 with rows, citywide 108.4 rows per
1,000 (all rows) and 106.9 (assigned), median 107.1, Whittier 286.1, top-5
count share 19.7 percent, top-10 32.7 percent; STR comparison 2,083 active
STR licenses, ratios 12.9x (licenses) and 18.7x (rows), Spearman 0.654
(rates) and 0.698 (counts); vintage prefix 2023 share 49.3 percent, 2023 or
later 91.7 percent; field hygiene (MULTIPLE_LICENSES constant; RENEWAL_CREATED
sentinel 38,949 rows; ZIP 0 on 3,436; past-expiration active rows 2;
duplicates 6 pairs; double-filed license 86 addresses by 2 parcels). The
hero composite asserts its figure against stats.json at build time.
One basis per number (Section 12.4): every count in the prose is labeled
row basis, license basis, or assessor-record basis where the bases differ,
and the register composition (38,949 active rows + 21 delinquent rows =
38,970; 26,941 active licenses + 21 delinquent licenses = 26,962) is
printed in the brief's opening and Finding 1.

## Independent verification and adversarial review (Section 11)

This package was built on brief day (the pick arrived 2026-10-19 for
2026-10-20) in a single builder pass. The Section 10 audit above is the
builder's own gate and is NOT independent verification: its concentration
and classification recomputations use separate code (collections.Counter)
against the raw snapshot, but no separate verifier or adversarial agent pass
has run on this package yet. That is an open item, recorded here and in
reviewer-notes.md: the package should not be presented as having passed
Section 11 until those passes run. The builder-side evidence that does
exist: the audit's Control B caught a real pattern the first drafting pass
had misstated (the cross-parcel double-filed license; the draft's "13
licenses with 100 or more rows, each on one parcel" was corrected to 12
licenses, 11 clean plus the documented exception, in the brief, sources,
stats, and audit before this file was written).

## Warehouse deposit

- Raw snapshot: stack/denver/snapshots/2026-10-20/rental_licenses.parquet
  (38,970 rows) with pull log pull_log_rental_2026-10-20.json (sha256
  8f72f12d69212ede53b0ba43f153255b238e12d81e65620a651fc12574dcc5a5).
- The snapshot was deposited by code/pull_data.py, which writes only to the
  warehouse and refuses to overwrite an existing snapshot. No manifest or
  stack verification entry was added by this build (the STR package's
  deposit script pattern was not repeated here; flagged in reviewer notes).
- Package data files: data/neighborhood_panel.csv (aggregate neighborhood
  panel: LTR rows, LTR row rates, LTR distinct licenses, STR active licenses
  and STR rates, ACS units) and data/audit_output.txt only. No raw register
  file exists anywhere in the package; the warehouse snapshot is the only
  raw copy. A programmatic leakage scan (code/leakage_scan.py; value sets
  taken from the warehouse snapshot: holder names, addresses, parcel numbers
  in raw and normalized forms) is run over the whole package before the
  package is presented as ready; its result is recorded in reviewer-notes.md
  and in the build report.

## Section 11 adversarial pass and publication HOLD (2026-10-20)

The adversarial reviewer pass ran 2026-10-20 (full report:
adversarial-review.md in this package; read in full before this note was
written, per Section 10.3.3). Result: 17 findings - 3 BLOCKING, 6
SHOULD-FIX, 8 FLAG. Under Alex's 2026-10-20 standing rule, publication
proceeds only when QA and the audit gates pass; a BLOCKING Section 11
finding is a failed gate, so THIS PACKAGE IS HELD and was not published.
The package is otherwise untouched by this note.

The three BLOCKING findings, as reported:

1. Finding 1 (cross-package premise): the brief and social draft called
   the October 19 STR brief "published" while that package's own record
   said BUILT, NOT PUBLISHED. Record of partial remediation: earlier in
   this same 2026-10-20 run, under the parent tasking's explicit
   defect-fix instruction, the wording instances were corrected in place
   ("published yesterday" in social-drafts.md became "the companion
   short-term rental brief (October 19, 2026)"; "published October 19,
   2026" in the introduction, Finding 4, and Methods became companion
   brief references with the date as a label, not a publication claim),
   and the STR brief was published to GitHub in the same operation, so
   the premise is resolved prospectively. This finding alone would not
   have held the package after those corrections; Findings 2 and 3 do.
2. Finding 2 (basis mixing, Section 12.4): Finding 3's parcel block
   computes row_per_parcel and lic_per_parcel over ALL active rows
   (matched and unmatched parcel keys) while the text labels 15,261 rows
   as "39.7 percent of matched rows" (the matched denominator is
   38,427). The all-active share is 39.2 percent. Affected: brief
   introduction (2,911 unlabeled), Finding 3 (2,911 / 15,261 / 39.7
   percent; 212 parcels / 574 licenses on the same all-keys basis), and
   the stats.json parcels_active basis string, which states "unmatched
   active rows excluded" and is false for five fields in that block.
   Related residue: Finding 9 (single-row parcel counts 23,548 matched
   vs 23,688 all-keys printed in Findings 1 and 3 with no reconciling
   label).
3. Finding 3 (unverifiable figure, Sections 10.3.2 / 12.5): Finding 3's
   second-largest-parcel sentence (444 rows, Central Park, 5 licenses,
   398 units on its record) appears in no other package artifact -
   stats.json records only the largest parcel - so the figure is not
   reproducible from the package and the recorded cross-check gate does
   not cover it.

What is NOT in dispute: the reviewer recomputed and tied every other
figure in stats.json at printed precision (concentration, classification,
merge sensitivities, vintage, expiry, grain check, neighborhood tables,
STR ratios and correlations), confirmed every named semantic trap is
disclosed in the brief body, and found no leakage (independent greps; no
licensee name, street address, or parcel value anywhere in the package).
SHOULD-FIX items recorded for the fix loop: Finding 4 (hero and
introduction print "18,471 of 26,941" where the 68.6 percent was computed
on 26,939 named licenses), Finding 5 ("at least 22 months" should be 33
months from the January 1, 2024 single-unit date), Finding 6 (North
Capitol Hill is 51st of 78 on the STR rate, not "near the bottom"),
Finding 7 (social 30.1 percent drops the counts-non-rental-units limit;
the brief's Finding 5 treatment stands), Finding 8 (Hampden South
"condominium pattern" gloss), Finding 9 (above). FLAG items 10-17 are
recorded in adversarial-review.md, including Finding 17 (title, hero, and
social print "20,780 holders" without the "names as filed" qualifier
Finding 2 itself requires).

Required before this package can publish: a fix loop that (a) recomputes
the Finding 3 parcel block on one stated basis and corrects the stats.json
basis string, (b) recomputes the second-largest-parcel triple from the
warehouse snapshot into stats.json and the assertion list, or cuts the
sentence, (c) applies the SHOULD-FIX wording items, and (d) is
re-verified by the adversarial pass that raised the findings, with the
independent verifier's ledger (separate pass, running 2026-10-20)
adjudicated alongside. Status records (README, reviewer-notes) update
when the loop closes, per Finding 16.

## Addendum (2026-10-20): independent verifier ledger received

The independent verifier pass completed after the hold above was recorded
(verification-ledger-independent.md in this package; fresh implementation
from the raw snapshot, builder code not used). 74 figures checked: 66
reproduced, 8 caveated, 0 corrected, 0 refuted. Adjudication notes for
the fix loop:

- Adversarial Finding 3: the second-largest-parcel triple (444 rows,
  Central Park, 5 licenses, 398 units) REPRODUCES exactly from the raw
  snapshot. The figure is correct; the defect is documentary only (it
  sits in no package artifact and outside the recorded cross-check).
  Fix: add the triple to stats.json parcels_active and to the Section
  12.5 assertion list; the sentence stays.
- Adversarial Finding 2: the verifier isolates the basis precisely. The
  package's "matched" means "assigned a neighborhood via the spine"
  (38,427 rows), not pure schednum membership (38,450 rows); 23 of the
  522 "unmatched" rows sit on 22 parcels that ARE in spine v6 with a
  null neighborhood value, so the stats.json note calling all unmatched
  parcels "absent from the spine snapshot" is imprecise for those 22.
  Matched-basis stacking values, recomputed: 2,846 parcels with 2+ rows,
  14,879 rows on them, 205 parcels with 2+ licenses. Both maxima (697
  rows; 29 licenses) hold on every basis, and the 30.1 percent coverage
  share is unchanged on the pure-schednum basis (133,861 units).
- Remaining caveats are documentation-grade: the name-merge sensitivity
  group counts move slightly under a straightforward alphabetic-token
  implementation (17,461 / 45.6 percent and 12,941 / 60.9 percent vs the
  printed 17,496 / 45.4 and 12,979 / 60.8; both printed maxima, 525 and
  1,160, reproduce), and the classification counts tie exactly only when
  a trailing parenthetical is not counted as name tokens (4 licenses
  shift between individual and not-determined under a naive count; no
  printed percentage changes).

The HOLD stands: Findings 2 (basis labeling) and the gate-coverage half
of Finding 3 still require the fix loop and adversarial re-verification
recorded above. But every headline figure in the package is now
independently reproduced, and the fix loop's recomputations are already
in hand in the verifier's ledger.

## Section 11 fix loop (2026-10-20) - fixes applied and re-verification

This loop applied the tasked fixes for the three BLOCKING adversarial
findings and the three tasked SHOULD-FIX wording items, then re-verified.
Before any edit, the loop recomputed the parcel figures with a fresh
implementation from the raw snapshot and spine v6 (builder code not
reused for the check) and reproduced the verifier's matched-basis values
exactly: 2,846 parcels with 2+ rows, 14,879 rows on them (38.72 percent
of matched rows, printed 38.7), 205 parcels with 2+ distinct licenses,
559 licenses on them, single-row matched parcels 23,548, and the
second-largest parcel at 444 rows, Central Park, 5 licenses, TOT_UNITS
398. Pure schednum membership matched 38,450 active rows, with 23 rows
on 22 in-spine parcels whose neighborhood value is null - all as the
ledger's Notes B and C record.

Fix 1 (adversarial Finding 2, basis mixing) - APPLIED.
- code/build_stats.py: the parcels block now groups MATCHED rows only
  (neighborhood assigned via the spine); the parcel_bridge note is
  corrected (text below). stats.json was regenerated by the patched
  build; a field-by-field diff against the pre-fix stats.json shows ONLY
  the parcel_bridge note, the parcels_active block, and the new Fix 3
  fields changed - no other figure moved, and
  data/neighborhood_panel.csv is byte-identical.
- stats.json parcels_active now stands on the matched basis under a true
  basis string ("active rows matched to the parcel spine and assigned a
  neighborhood (38,427 of 38,949 active rows); every count in this block
  is computed over the 26,394 distinct matched parcels only; the 522
  unassigned active rows are excluded"): distinct_parcels 26,394,
  parcels_with_multiple_rows 2,846, rows_on_multiple_row_parcels 14,879,
  new field share_of_matched_rows_on_multiple_row_parcels_pct 38.7,
  parcels_with_multiple_distinct_licenses 205,
  licenses_on_multiple_license_parcels 559, and the row-count
  distribution on the matched basis {1: 23,548, 2: 1,357, 3: 625,
  4: 277, 5: 173}. This is also Fix 2: the five fields the old basis
  string was false for now carry matched-basis values.
- brief-draft.md: introduction "2,911 parcels" corrected to 2,846;
  Finding 3's heading and body restated on the one matched basis
  (23,548 single-row matched parcels; 2,846 parcels with two or more
  rows holding 14,879 rows, 38.7 percent of matched rows; 205 parcels
  with two or more licenses holding 559). Finding 3's single-row count
  now equals Finding 1's 23,548 on the same basis, which also closes
  adversarial Finding 9's unreconciled pair.
- The imprecise 522-row note is corrected everywhere it appeared:
  brief-draft.md Finding 4 ("499 of them sit on parcels absent from the
  parcel spine, and 23 sit on 22 parcels that are present in the spine
  but carry no neighborhood value (counted by parcel number alone, the
  bridge matches 38,450 active rows)"), the Data notes bullet, the
  Methods bridge paragraph, the stats.json parcel_bridge note, and the
  neighborhood chart footnote in code/charts.py (charts regenerated).

Fix 3 (gate coverage, second-largest parcel) - APPLIED.
stats.json parcels_active gains second_largest_parcel_rows 444,
second_largest_parcel_neighborhood "Central Park",
second_largest_parcel_distinct_licenses 5, and
second_largest_parcel_units_on_parcel_record 398.0. The triple is added
to the Section 12.5 assertion list above (updated in place), and
code/audit_section10.py gained a fix-loop gate section that recomputes
the whole corrected parcel block - including both parcel triples and
the bridge composition (38,450 membership; 23 rows on 22 null-
neighborhood parcels) - from the raw snapshot and asserts every value
against stats.json. The Finding 3 sentence stays, now reproducible
from package artifacts.

Should-fix wording - APPLIED.
- Finding 4: the introduction now prints "(18,471 of 26,939 named
  active licenses)"; the hero subline reads "18,471 of 26,939 named
  active licenses, held by 20,780 holder names". code/hero_composite.py
  asserts the full printed composition at build time (not just the
  percentage); hero.png was regenerated and read visually - the new
  composition is composited correctly and legibly.
- Finding 5: Finding 1's "at least 22 months" now reads "at least 33
  months" (January 1, 2024 single-unit date to October 2026).
- Finding 6: Finding 4's "near the bottom on the short-term rate" now
  reads "51st of 78 on the short-term rate".

Re-verification.
- Audit re-run: code/audit_section10.py exits 0, "ALL SECTION 10
  ASSERTIONS PASSED", including the new fix-loop gate section; the new
  output is saved to data/audit_output.txt. It supersedes the pre-flight
  output quoted earlier in this file in exactly two respects: the
  join-hygiene wording line (corrected per Fix 1) and the added gate
  section. Every other quoted line is unchanged.
- Leakage scan re-run over the final package (26 files, including
  adversarial-review.md, verification-ledger-independent.md, and this
  fix log): PASSED, TOTAL VALUE HITS: 0, against the same snapshot value
  sets (40,322 holder-name forms, 50,086 address forms, 53,240
  parcel-number forms). The result is also recorded in
  reviewer-notes.md.
- Focused adversarial re-check of the changed passages only: a
  stale-token sweep over brief-draft.md, stats.json, social-drafts.md,
  README.md, reviewer-notes.md, code/charts.py, code/hero_composite.py,
  and code/build_stats.py for the superseded figures and phrases
  (2,911, 15,261, 39.7, 26,599, 23,688, 212 parcels, 574 licenses,
  "near the bottom", "22 months", "18,471 of 26,941", "could not be
  parcel-matched") returns zero hits. Finding 3 now states one labeled
  basis in its heading, body, and stats.json; the hero composition was
  verified visually; no figure outside the tasked set changed (stats
  diff above).

Dispositions.
- Adversarial Finding 1 (BLOCKING): resolved earlier in this run by the
  wording remediation and the STR brief's GitHub publication, as
  recorded in the adjudication addendum above; not reopened.
- Adversarial Findings 2 and 3 (BLOCKING): RESOLVED by this loop.
- Should-fix Findings 4, 5, 6: RESOLVED. Finding 9: resolved as a
  consequence of the Fix 1 restatement.
- Should-fix Findings 7 and 8 and FLAG Findings 10-17 were outside
  this loop's tasking and stand as recorded in adversarial-review.md;
  none is a blocking gate. Status records were updated per Finding 16:
  README.md status paragraph, reviewer-notes.md (checks list, Section
  11 pipeline record, open items), and the Section 12.5 assertion list
  in this file.

Verdict: every blocking item is resolved and the re-verification
passes. This package is CLEARED for publication. Publication was NOT
performed by this loop; it is a separate step.
