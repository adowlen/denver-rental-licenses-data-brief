# Reviewer notes - Denver residential rental licenses brief (2026-10-20)

## Claims most likely to be challenged, and where the defense lives

1. "One row is not one license" (Finding 1, the lede, the hero's companion copy).
   Basis: LICENSE_NUM distinct count 26,962 on 38,970 rows; row-level inspection
   of all 12 licenses with 100 or more rows (11 with one holder, one parcel,
   all-distinct addresses; 1 double-filed across two parcels, disclosed). The
   DLCP FAQ's own license structure (single-unit properties license individually;
   a multi-unit property can hold one license for multiple units, addresses, or
   structures on single or contiguous parcels under one ownership) is cited in
   sources.md. The likely challenge runs the other way: a reader may argue the
   rows are the licensing system's own unit records and should be read as
   licensed units. Finding 1's grain test is the defense and the limit at once:
   rows equal the parcel record's unit count on 22,107 of 26,309 parcels, but
   1,026 single-row parcels carry 10 or more units on their records, so rows
   cannot be read as units in aggregate without an error the data itself sizes.

2. "68.6 percent of active licenses are their holder's only license" (headline,
   hero, social). Basis: distinct LICENSE_NUM per normalized ENTITY_NAME on the
   fresh 2026-10-20 snapshot, 18,471 of 26,939 named active licenses
   (stats.json concentration_active_licenses); the 2 unnamed active licenses
   are excluded from the holder basis and stated wherever the count appears.
   The honest limit is printed in Finding 2: the first-and-last-token merge
   leaves the top holder at 525 but moves the groups-of-two-or-more share to
   45.4 percent, because entity names collide on tokens; the initial-token
   over-merge (a deliberate over-count) reaches a 1,160-license maximum group.
   Unlike the STR register, where merging barely moved anything, this register's
   business names make the exact-name basis a floor on grouping, and the brief
   says so. Common control behind distinct filed names remains invisible, as
   with every register in this series.

3. "Licensed parcels carry 30.1 percent of assessor-record units" (Finding 5).
   This is the claim with the largest semantic risk in the package, because it
   sits closest to the coverage question the pick asked. It is a ratio of two
   sums from the same assessor source (133,839 TOT_UNITS on licensed matched
   parcels with a unit record, over 445,057 TOT_UNITS on all spine parcels),
   printed with three scope limits in the same paragraph: it counts every unit
   on a licensed parcel including any non-rental units, it omits unmatched and
   no-record parcels, and it is not a share of rental stock. The pick's literal
   coverage question (licensed share of long-term rental stock) could NOT be
   answered: the warehouse ACS layer carries total housing units only, no
   renter-occupied denominator exists at any geography in the warehouse, and
   the brief prints that absence rather than a substitute rate. Alex should
   weigh whether the 30.1 percent figure, even scoped, invites the misreading
   it warns against; the fallback is to cut it to the panel rates and the
   printed absence.

4. The STR comparison (Finding 4, chart_ltr_vs_str.png). Two registers, two
   grains: STR counts are single-unit licenses; LTR numerators in the rate
   comparison are rows. The chart prints the two measures in separate panels
   with separate scales and labels, the brief never adds them, and the text
   states the units differ before quoting the ratios (12.9x on licenses, 18.7x
   on rows). The rank correlation (0.654 on rates) compares rankings, not
   magnitudes, and is labeled geographic. A challenger could still object that
   any side-by-side invites magnitude comparison; the mitigation is the
   on-graphic labeling, and Alex's framing call governs at QA.

5. The double-filed license (Findings 1 and 5). One license files 86 addresses
   under each of two parcel numbers. The brief counts it as published and
   prints both readings (a two-parcel property filed per parcel, or a clerical
   duplication worth 86 rows, 0.2 percent of active rows). It was caught by
   the audit's Control B after the first drafting pass had described all 12
   large licenses as single-parcel; the correction is recorded in
   verification.md. If DLCP confirms the duplication reading, the row totals
   in a future refresh would drop by 86; no printed figure here changes at its
   printed precision.

## Checks that could not be completed

- Renter-occupied denominator: not available in the warehouse (ACS layer is
  B25001 total units only). The licensed share of rental stock is therefore
  NOT computed; Finding 5 prints the assessor-record ratio with its scope and
  the absence itself. Completing this check needs an ACS tenure table
  (B25003) pull or a Census Reporter tract pull, neither of which was in
  scope for this build.
- Section 11 passes: RAN 2026-10-20 after this note was first written. The
  independent verifier reproduced every headline figure (74 checked, 66
  reproduced, 8 caveated, 0 refuted; verification-ledger-independent.md).
  The adversarial review (adversarial-review.md) returned 3 BLOCKING, 6
  SHOULD-FIX, and 8 FLAG findings. The 2026-10-20 fix loop resolved all
  three blocking items (Finding 1's wording remediation was already on
  record; Findings 2 and 3 were fixed in the loop) and the tasked
  should-fix wording items (Findings 4, 5, 6), re-ran the audit and the
  leakage scan, and passed a focused adversarial re-check of the changed
  passages. Full record: the fix log at the end of verification.md. The
  remaining SHOULD-FIX and FLAG items (Findings 7-17 not listed above)
  were outside the loop's tasking and stand as recorded in
  adversarial-review.md for Alex's awareness; none is a blocking gate.
- Warehouse manifest: the STR package registered its snapshot in
  stack/denver/manifest.json and appended a stack verification entry via a
  deposit script; this build deposited the snapshot and pull log only. If
  Alex wants manifest parity, a deposit step remains to be run.
- The denvergov.org dataset landing page for this table was not text-fetched
  during the build; the live ArcGIS service itself was queried directly for
  every figure, and the program pages cited were fetched and read in full.

## Surprises

- The register's grain is the opposite of the STR register's in both
  directions at once: licenses that enumerate every unit (697 rows for one
  license) and whole buildings filed as one row (1,026 single-row parcels
  with 10 or more units on their assessor records, 73,501 units). Any
  single-number summary of this register ("38,970 licenses") is wrong by
  construction; the live count itself is quoted that way in the lead log's
  verification note from 2026-10-19.
- MULTIPLE_LICENSES reads "Stand Alone" on all 38,970 rows, including the
  697 rows of one license - the same constant-field pattern as the STR
  register, on a register where multi-row licenses are 10.5 percent of all
  licenses and 38.1 percent of all rows.
- RENEWAL_CREATED is a 1900 sentinel on every active row; the register's only
  honest date field is EXPIRATION_DATE, and the only honest vintage is the
  license number's own year prefix.
- Holder concentration exists here in a way it does not in the STR register:
  a 525-license maximum holder (a filer of many single-unit licenses), 65
  holders at 11 or more licenses, and a business-entity license share of
  37.1 percent against the STR register's 0.0 percent - the two programs'
  intake rules produce the difference, and the brief prints that context
  rather than a verdict on either.
- Every one of the 78 neighborhoods carries long-term rows, including the
  three with no STR licenses; the long-term register's floor is set by the
  ordinance's universality, not by market presence.

## Section 11 pipeline record

- Builder: package assembled 2026-10-20 (brief-day build; the pick arrived
  2026-10-19 for 2026-10-20). Fresh pull taken 2026-10-20T12:32:53Z; Section
  10 audit passed before drafting was finalized (data/audit_output.txt), and
  its Control B finding was adjudicated during the build (see claim 5).
- Independent verifier: RAN 2026-10-20 (verification-ledger-independent.md).
  74 figures checked: 66 reproduced, 8 caveated, 0 corrected, 0 refuted.
- Adversarial reviewer: RAN 2026-10-20 (adversarial-review.md). 17 findings:
  3 BLOCKING, 6 SHOULD-FIX, 8 FLAG. Fix loop closed 2026-10-20: all three
  blocking items resolved, tasked should-fix wording items (Findings 4, 5,
  6) applied, audit and leakage scan re-run, focused adversarial re-check
  of the changed passages passed. Record: verification.md fix log.
- Product rules: aggregates only, in every shipped file category: no licensee
  name, street address, or parcel number value appears in the brief, the
  social drafts, stats.json, the data/ files (aggregate neighborhood panel
  and audit output only), the code/ files, the charts, or the hero. The raw
  register snapshot is archived only in the warehouse
  (stack/denver/snapshots/2026-10-20/) and was never copied into the package;
  code/pull_data.py writes only to the warehouse. A programmatic leakage scan
  (code/leakage_scan.py) checks the whole package against the snapshot's value
  sets; its result is recorded in the build report and below once run.
- Leakage scan result: PASSED (run 2026-10-20 after all files were final;
  value sets from the warehouse snapshot: 40,322 holder-name forms, 50,086
  address forms, 53,240 parcel-number forms; TOTAL VALUE HITS: 0 across all
  24 package files, including the hero, charts, code, and data files).
  Re-run after the 2026-10-20 Section 11 fix loop over the final 26-file
  set (now including adversarial-review.md,
  verification-ledger-independent.md, and the verification.md fix log):
  PASSED, TOTAL VALUE HITS: 0.

## Section 11.3 flags for Alex

- First use: the residential rental property register is the primary dataset
  of a brief for the first time (it entered the lead bank 2026-10-19; it has
  no prior warehouse layer). Its name understates its structure: the table
  named "active licenses" counts filing rows, not licenses - flagged in the
  brief's Finding 1 and Data notes.
- Naming an agency: the Who can act section names the Department of Licensing
  and Consumer Protection (DLCP) with two documentation items (publish a
  grain note with distinct-license counts beside row counts; document the
  RENEWAL_CREATED sentinel). This is the standing agency flag. No other
  agency or official is named.
- Surprising result: the grain finding itself, and the 525-license maximum
  holder with 850 rows - the same holder tops both bases, verified by two
  independent code paths (build_stats and the audit's Counter recomputation).
- Definition call for Alex: the brief's headline basis is distinct license
  numbers. The service and the lead log both quote the row count (38,970) as
  the register's size; if Alex prefers the row count as the public headline
  with the license count as the correction inside, Finding 1 is where it
  would change. The package's position, for the reasons in claim 1, is that
  the license basis is the defensible headline.
- Open items: warehouse manifest registration not done; renter-tenure
  denominator not pulled (Finding 5's coverage boundary would move if Alex
  wants B25003 added). Section 11 is complete (see pipeline record above).
- Repo name follows the series pattern (adowlen/denver-rental-licenses-data-brief);
  checked 2026-10-20, it does not exist yet (HTTP 404). Nothing has been
  created, pushed, posted, or sent.
