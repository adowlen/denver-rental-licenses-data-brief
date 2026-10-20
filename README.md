# Denver residential rental licenses brief - package README

Topic (Alex's pick, 2026-10-19, for the 2026-10-20 brief): how much of Denver's
long-term rental stock sits in the licensed register, how concentrated are
long-term rental licenses by holder and parcel, and how does the licensed
long-term footprint compare neighborhood by neighborhood with the STR footprint
published 2026-10-19. Dataset: residential rental property license register of
the Department of Licensing and Consumer Protection (DLCP)
(ODC_residential_rental_property_active_licenses, table 52), fresh pull
2026-10-20. Completes the rental layer of the locality stack: the STR brief
(2026-10-19) is the short-term side, this is the long-term side, same parcel
spine.

Status: BUILT, NOT PUBLISHED. Nothing pushed, posted, or sent. The Section 10
pre-flight audit passed with evidence recorded in verification.md. The
Section 11 passes have since run: the independent verifier reproduced every
headline figure (74 checked, 66 reproduced, 8 caveated, 0 refuted;
verification-ledger-independent.md), and the adversarial review
(adversarial-review.md) returned 3 BLOCKING findings. A fix loop on
2026-10-20 resolved all three blocking items plus the tasked should-fix
wording items, re-ran the audit (with a new gate section covering the
corrected figures) and the leakage scan, and passed a focused adversarial
re-check of the changed passages; the full record is the fix log at the end
of verification.md. The package is CLEARED for publication under Alex's
2026-10-20 standing rule; publication itself is a separate step.

## Headline result

26,941 active licenses under 20,780 holder names: 18,471 holders hold one
license (68.6 percent of licenses are their holder's only license), the largest
holder holds 525, and holders of 11 or more licenses hold 8.4 percent. The
register's 38,970 rows are filing rows, not licenses: one license carries 697
rows, and whole buildings also file as one row, so unit coverage is reported
from assessor records (licensed parcels carry 30.1 percent of assessor-record
units) and no licensed share of rental stock is computed (no renter-occupied
denominator exists in the warehouse).

## Contents
- brief-draft.md - the brief (publishable text)
- stats.json - every figure used in the brief and social copy, produced by code/build_stats.py
- verification.md - Section 10 pre-flight audit output, methods checklist, controls, warehouse deposit record
- reviewer-notes.md - claims most likely challenged, checks not completed, Section 11.3 flags
- sources.md - dataset citations, field semantics, access notes
- social-drafts.md - LinkedIn page post and personal repost comment (drafts only; no X draft, per Alex's 2026-10-19 rule)
- hero.png - hero graphic (generated illustration + composited verified figure; code/hero_composite.py)
- charts/ - chart_bands.png, chart_neighborhood_rates.png, chart_ltr_vs_str.png, chart_vintage.png
- data/ - neighborhood_panel.csv (aggregate neighborhood panel), audit_output.txt (Section 10 audit output). No raw register file ships in the package: the raw snapshot lives only in the warehouse
- code/ - pull_data.py, build_stats.py, audit_section10.py, leakage_scan.py, charts.py, hero_composite.py
- hero_source/ - the raw generated illustration before compositing

## Dependencies (match code imports)
python 3.12; pandas, numpy, pyarrow (parquet), matplotlib, Pillow (hero composite).
No other third-party imports. Working venv: the crime brief package's ./.venv
(denver-crime-brief-2026-10-17/.venv).

## Rebuild order
1. code/pull_data.py (fresh register pull to the warehouse snapshot 2026-10-20 only;
   refuses to overwrite an existing snapshot; never writes a copy into the package)
2. code/build_stats.py (writes stats.json + data/neighborhood_panel.csv)
3. code/audit_section10.py (Section 10 gates; output to data/audit_output.txt)
4. code/charts.py, code/hero_composite.py
5. code/leakage_scan.py (scans every package file for register values;
   must pass before the package is presented as ready)

## Data provenance
Rental register: warehouse stack/denver/snapshots/2026-10-20/rental_licenses.parquet
(fresh pull, 38,970 rows; pull log pull_log_rental_2026-10-20.json beside it).
Neighborhoods, parcel unit counts: joins/parcel_spine_v6.parquet. Denominators:
ACS 2024 5-year B25001 via layers/acs_neighborhood_units.parquet (same basis as
the crime, traffic, and STR briefs). STR comparison: the 2026-10-19 STR package's
stats.json and data/neighborhood_panel.csv. Warehouse deposit from this study:
the 2026-10-20 snapshot and its pull log only (manifest registration not done;
see reviewer-notes.md).

## Product rules applied
Aggregates only, in every shipped file category: no licensee name, street
address, or parcel number value appears in the brief, the social drafts,
stats.json, the data/ files (aggregate neighborhood panel and audit output
only), the code/ files, the charts, or the hero. The raw register snapshot is
archived only in the warehouse and is never copied into the package.
code/leakage_scan.py scans every package file for register values (holder
names, street addresses, parcel numbers from the warehouse snapshot, in raw
and normalized forms). Licensee names are used transiently inside code to
compute concentration; the audit prints anonymized evidence only.
