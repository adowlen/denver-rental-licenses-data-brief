# Adversarial review (Section 11) - Denver residential rental licenses brief (2026-10-20)

Reviewer role: attack, not approve. Standards applied: brief-writing-standards.md
Sections 2 (voice), 3 (methods), 11 (adversarial review), 12 (pilot lessons,
esp. 12.4 one basis per number, 12.5 cross-document assertion, 12.8 physical
falsifiability, 12.9 summaries from the artifact).

Materials read in full: brief-draft.md, stats.json, sources.md,
reviewer-notes.md, verification.md, social-drafts.md, README.md. Also read:
code/build_stats.py and code/charts.py (to establish the true basis of the
parcel figures and the comparison chart's labels), hero.png (visually), the
package data/neighborhood_panel.csv (STR rate rankings), and the 2026-10-19
STR package's README.md and stats.json (to test this package's claims about
that brief). Independent spot recomputations from stats.json are noted per
finding. The independent verifier pass (a separate Section 11 pass) has still
not run; nothing in this report substitutes for it.

Headline verdict: the arithmetic that IS in stats.json ties out everywhere I
recomputed it (concentration bands and shares, classification on all three
bases, merge sensitivities, vintage distribution, expiry cohorts, grain
check, neighborhood tops, STR ratios and correlations). The semantic traps
the task named (LICENSE_NUM as key, MULTIPLE_LICENSES constant,
RENEWAL_CREATED sentinel, expiration/status disagreement, the double-filed
license, exact duplicates) are all disclosed in the brief body (Findings 1
and 5, Data notes), not buried. The defects below are about basis labels
that do not match the code, one figure that exists in no artifact, and one
cross-package factual premise that the repository itself contradicts.

---

## BLOCKING findings

### Finding 1 (BLOCKING) - The package repeatedly calls the October 19 STR brief "published"; the STR package's own record says it is not

At issue (brief-draft.md, Finding 4): "Against the short-term rental
footprint published October 19, 2026..." and "the short-term register holds
2,083 active licenses..."; (Methods): "STR comparison: figures are taken
from the published October 19, 2026 STR package"; (introduction): "...the
short-term rental register's 5.8 active licenses per 1,000 units published
October 19, 2026". At issue (social-drafts.md, LinkedIn page post): "37.1%
of licenses sit under a business-entity name, against 0% in the short-term
register published yesterday."

The STR package's own README.md states: "Status: BUILT, NOT PUBLISHED.
Nothing pushed, posted, or sent... Awaiting Alex's review." The
follow_up_log.md (the log of published briefs) carries no Denver STR entry.
Under the standards (Section 4), nothing publishes without Alex's explicit
approval, and under Section 12.9 a description is checked against the
artifact, not the plan. As the repository stands, this package's central
comparison rests on, and publicly cites, a brief whose publication is not
evidenced anywhere in the record - and the social draft converts that into
the time-sensitive claim "published yesterday," which will be wrong on its
face if the STR brief has not in fact gone out.

Recommended fix: before this package ships, establish the STR brief's
actual status from Alex. If it was published on 2026-10-19 after its README
was written, update the STR README status line and the follow_up_log so the
record supports the word "published." If it was not published, remove
"published" from every reference in brief-draft.md (introduction, Finding 4,
Methods) and rewrite the social sentence so it does not claim a publication
event ("against 0% in the short-term register analyzed October 19, 2026"
only works if that brief is public; otherwise the comparison itself needs
Alex's sequencing call).

### Finding 2 (BLOCKING) - Finding 3's parcel figures mix bases: the numerator is computed over all parcel keys, the percentage is labeled "of matched rows," and stats.json's basis string for the block is false

At issue (brief-draft.md, Finding 3): "Bridged to the assessor parcel file,
the 38,427 matched active rows sit on 26,394 distinct parcels... On 2,911
parcels there are two or more rows, holding 15,261 rows between them (39.7
percent of matched rows)." The same 2,911 figure appears unlabeled in the
introduction: "On parcels, rows stack where one license enumerates a
building's units: 2,911 parcels carry two or more rows."

The build code (code/build_stats.py) computes row_per_parcel =
act.groupby("schednum").size() over ALL active rows - matched and unmatched
alike. So 2,911 multi-row parcels and their 15,261 rows include the 205
parcels the bridge could not match, among them the register's largest
unmatched parcels (157 rows on two parcels, per stats.json parcel_bridge)
and the double-filed license's unmatched parcel (86 of its rows). 15,261 is
therefore not a subset of the 38,427 matched rows, and "39.7 percent of
matched rows" divides an all-keys numerator by a matched-only denominator -
exactly the composition defect Section 12.4 names. The correct all-active
share is 15,261 / 38,949 = 39.2 percent; the matched-only numerator is
smaller than 15,261 by the rows on unmatched multi-row parcels (at least
157). The multi-license parcel counts in the same finding (212 parcels,
574 licenses) come from the same all-keys grouping (lic_per_parcel), while
the paragraph frames them inside the bridged analysis; only the maximum
(29 licenses, Hampden South) is verifiably a matched parcel, because it has
a neighborhood.

Compounding it, stats.json parcels_active carries the basis string "active
rows bridged to parcels (schednum); unmatched active rows excluded" - which
is false for distinct_parcels (26,599 = 26,394 matched + 205 unmatched),
parcels_with_multiple_rows, rows_on_multiple_row_parcels,
parcels_with_multiple_distinct_licenses, and
licenses_on_multiple_license_parcels. The brief's own parenthetical ("the
parcel countywide figure includes 205 parcels the bridge could not match to
the spine") discloses the inclusion for the 23,688 single-row count but the
39.7 percent label and the stats.json basis string still assert the
opposite basis.

Recommended fix: recompute the Finding 3 parcel block on one stated basis.
Either (a) restrict row_per_parcel and lic_per_parcel to matched rows and
reprint 2,911 / 15,261 / 212 / 574 with their matched-only values and the
39.7 percent (recomputed), or (b) keep the all-keys counts and relabel
everywhere, including the introduction, as counts over all 26,599 register
parcel keys with the share taken over all 38,949 active rows. Correct the
stats.json basis string to match the code either way, and re-run the
Section 12.5 assertion after the fix.

### Finding 3 (BLOCKING) - Finding 3's second-largest-parcel figure (444 rows, Central Park, 5 licenses, 398 units) exists in no other package artifact, contradicting the package's recorded cross-check gate

At issue (brief-draft.md, Finding 3): "the second largest is 444 rows on
one parcel in Central Park under 5 licenses, against 398 units on its
record."

A full-text search of the package (stats.json, code/, data/,
verification.md, reviewer-notes.md, sources.md, README.md, social-drafts.md)
finds no occurrence of 444, of a second-largest parcel, or of 398 units
outside that one sentence. stats.json parcels_active records only the
largest parcel (697 rows, North Capitol Hill, 229 units, 1 license). The
figure is therefore not reproducible from any artifact in the package,
while brief-draft.md Methods states "Every figure in this brief is
cross-checked against the package stats file" and verification.md records
the Section 10.3.2 / 12.5 cross-check as passed, with an assertion list
that does not include this figure. The gate evidence as recorded is false
for this figure whether or not 444 is numerically right - and this
reviewer cannot recompute it from the package, because the raw snapshot
lives only in the warehouse and the independent verifier pass has not run.

Recommended fix: recompute the second-largest parcel from the warehouse
snapshot, add the full triple (rows, neighborhood, distinct licenses,
TOT_UNITS) to stats.json parcels_active, add it to the verification.md
assertion list, and re-run the cross-document assertion. If it cannot be
reproduced exactly as printed, cut the sentence; the largest-parcel example
already carries the finding.

---

## SHOULD-FIX findings

### Finding 4 (SHOULD-FIX) - The headline composition "18,471 of 26,941" misstates the cohort the 68.6 percent was computed on; it appears in the introduction and on the hero

At issue (brief-draft.md, introduction): "68.6 percent of active licenses
are their holder's only license (18,471 of 26,941)". At issue (hero.png,
composited text): "68.6% of active long-term rental licenses are their
holder's only license: 18,471 of 26,941 active licenses, held by 20,780
holders."

The share is computed on the 26,939 active licenses that carry a holder
name (stats.json concentration_active_licenses: units 26,939; share
68.57). The 2 unnamed active licenses sit inside the printed denominator
26,941 but cannot be in the numerator's population - a license with no
holder cannot be "their holder's only license." Finding 2 states the basis
correctly ("the 26,939 active licenses that carry a holder name"); the
introduction and the hero do not. The percentage survives rounding either
way (18,471 / 26,941 = 68.56), so this is a Section 12.4 cohort-printing
defect, not a wrong number - but it sits in the two most-read surfaces of
the package, and verification.md's claim that "the hero composite asserts
its figure against stats.json at build time" evidently covered the
percentage, not the printed composition. The hero's "held by 20,780
holders" also prints name strings as holders (see Finding 17).

Recommended fix: print "(18,471 of 26,939 named active licenses)" in the
introduction, fix the hero composite text the same way (and "20,780 holder
names"), and extend the hero build assertion to the full printed
composition, not just the percentage.

### Finding 5 (SHOULD-FIX) - "inside the requirement for at least 22 months" understates the phase-in arithmetic by about a year

At issue (brief-draft.md, Finding 1): "by October 2026 every long-term
rental property in Denver has been inside the requirement for at least 22
months."

The binding date for the last cohort is the single-unit requirement,
January 1, 2024 (cited in the same paragraph and in sources.md). January 1,
2024 to October 20, 2026 is 33 months. "At least 22 months" is literally
true as a lower bound but reads as the computed figure, and a knowledgeable
Denver reader who checks it finds 33 - the kind of loose arithmetic
Section 12.8 exists to catch before a reader does.

Recommended fix: "at least 33 months" (or "more than two and a half
years").

### Finding 6 (SHOULD-FIX) - "near the bottom on the short-term rate" overstates North Capitol Hill's STR rank; the package's own panel puts it 51st of 78

At issue (brief-draft.md, Finding 4): "North Capitol Hill ranks seventh on
the long-term row rate (183.3, driven by large multi-unit buildings) and
near the bottom on the short-term rate (3.2 per 1,000, 19 licenses)."

From this package's own data/neighborhood_panel.csv, 50 neighborhoods have
a higher STR rate than North Capitol Hill's 3.2 and 27 have a lower one:
it ranks 51st of 78 - the lower half, not near the bottom. The sentence's
contrast (7th vs "near the bottom") is doing rhetorical work the panel does
not support.

Recommended fix: "and 51st of 78 on the short-term rate (3.2 per 1,000, 19
licenses)" - the precise rank makes the divergence point without the
overstatement. (The companion claims check out: Whittier is 1st on both
rate tables, 286.1 and 27.1; Cole is top five on both, 2nd on STR at
24.75.)

### Finding 7 (SHOULD-FIX) - Keep the 30.1 percent assessor figure in the brief; fix its compression in the social draft, where the scope limits fall away

At issue (social-drafts.md, LinkedIn page post): "The brief also prints
what the register cannot say: licensed parcels carry 30.1% of the city's
assessor-record units, and no licensed share of rental stock can be
computed from the published data, because no renter-occupied denominator
exists in it."

Finding 5 itself is the model treatment: the figure (133,839 of 445,057
assessor-record units, recomputed and tied) is printed with three scope
limits in the same paragraph, including the decisive one - it counts every
unit on a licensed parcel, rented or not. The LinkedIn compression keeps
"assessor-record units" but drops that limit, and social copy is where the
figure will be quoted from. A reader can still walk away with "30.1% of
Denver's units are licensed rentals," the exact misreading Finding 5 warns
against. This answers the review question directly: the printed scope in
the brief prevents the misreading; the social rendering does not. Do not
cut the figure from the brief - cut is not warranted where the scope is
printed with it - but the reviewer-notes fallback (cut entirely) should
apply to the social copy if the qualifier cannot fit.

Recommended fix: in the social draft, write "parcels holding at least one
active license carry 30.1% of the city's assessor-record units, counting
every unit on those parcels, rented or not" - or drop the figure from the
post and keep only the "no licensed share of rental stock can be computed"
sentence.

### Finding 8 (SHOULD-FIX) - The Hampden South "condominium pattern" gloss asserts a tenure pattern its own cited record cuts against

At issue (brief-draft.md, Finding 3): "the maximum is 29 distinct licenses
on one parcel in the Hampden South neighborhood, whose assessor record
carries 8 units - the condominium pattern, in which separately owned units
on a shared parcel license individually."

29 separately licensed units on a parcel whose assessor record carries 8
units is not, on its face, the condominium pattern; it is at least as
consistent with a stale assessor unit count or a multi-structure parcel.
The gloss presents one interpretation as the explanation, and a local
reader who knows that parcel can falsify it by looking (Section 12.8).

Recommended fix: drop the gloss, or hedge it to what the data shows:
"separately licensed units on a shared parcel, against 8 units on the
parcel's assessor record - the register and the record disagree on the
parcel's unit count, and neither says why."

### Finding 9 (SHOULD-FIX) - Two different "single-row parcel" counts (23,548 and 23,688) are printed in Findings 1 and 3 with no reconciling label

At issue: Finding 1: "23,548 licensed parcels carry a single row" (the
grain check, over the 26,394 matched parcels). Finding 3: "On 23,688 of the
register's 26,599 parcel keys there is exactly one active row" (over all
parcel keys, matched and unmatched). Both numbers are correct on their
bases (difference: 140 single-row unmatched parcel keys), and Finding 3's
sentence does flag that its population includes unmatched parcels - but
nothing tells the reader comparing the two findings that they are looking
at the same quantity on two different populations, and the two counts sit
140 apart with no bridge. This is the reader-facing residue of Finding 2's
basis mixing.

Recommended fix: after the Finding 2 fix, add the reconciling clause where
the second count appears ("23,688 of all 26,599 register parcel keys; on
the matched parcels alone the count is 23,548, as in Finding 1") or print
one basis throughout.

---

## FLAG findings

### Finding 10 (FLAG) - "moderate" is a characterization word inside the interpretation section

At issue (brief-draft.md, "What this might mean"): "concentration on the
license basis is moderate and measurable - most licenses are single-license
holdings, the largest holder holds about one license in fifty, and holders
of 11 or more licenses hold about one license in twelve."

The section is labeled interpretation and the strongest alternative
explanation (the name field understates common control) is printed
alongside, as Section 2 requires - so this is not a Section 2 breach. But
"moderate" is a verdict adjective doing work the three numbers next to it
already do. Consider deleting "moderate and" and letting the fractions
stand.

### Finding 11 (FLAG) - "force into one license per person" is contradicted, mildly, by the figures in the same sentence

At issue ("What this might mean"): "a short-term market the program's
primary-residence rules force into one license per person (2,083 licenses,
2,080 holders, no business names, per the October 19, 2026 brief)."

2,083 licenses under 2,080 holders means three holders hold two licenses
each (STR package stats.json: 2,077 holders with one, 3 with two). The
rules evidently do not force one license per person without exception.
Rephrase to "structured as one license per person" or note the three
exceptions. Also "no business names" should be "no business-entity names"
to match the classification's actual scope (verified against the STR
package: business_entity_name count 0 of 2,083 active licenses - the
underlying figure is correct).

### Finding 12 (FLAG) - The social draft's "0% in the short-term register" drops the classification scope

At issue (social-drafts.md): "against 0% in the short-term register
published yesterday."

The number is verified (STR stats.json: 0 business-entity names of 2,083
active licenses, share 0.0). But as written, the clause's antecedent
("licenses sit under a business-entity name") has to be carried across the
comma, and the as-filed classification limit is absent. On a fast social
read it can land as "0% business involvement in STR," which the STR brief
itself does not claim. Tighten to "against 0% under a business-entity name
in the short-term register" (in addition to the Finding 1 fix to
"published yesterday").

### Finding 13 (FLAG) - The LICENSE_NUM year-prefix semantics are asserted from format, with no program document cited

At issue (sources.md): "The 4-digit prefix encodes the issue year and is
the only vintage signal in the service," listed under "Field semantics
(established from the service itself, 2026-10-20)."

The brief handles the resulting figures carefully (labeled prefix basis,
survivor stock, not an issuance series - all correct and properly
caveated). But "established from the service itself" overstates the
evidence: the service shows a 4-digit prefix shaped like a year; that it
encodes the ISSUE year (rather than, say, the application or account year)
is an inference from format and from the distribution's fit to the
phase-in, with no DLCP document cited for the numbering scheme. A renewal
or reissue that minted a new number would silently move a license's
vintage. Keep the analysis; soften sources.md to "inferred from the
license number format and consistent with the phase-in distribution; no
DLCP document in this package defines the numbering scheme."

### Finding 14 (FLAG) - Process language and an editorial aside in publishable text

At issue (Finding 5): "The pick for this brief asked how much of Denver's
long-term rental stock sits in the licensed register." At issue (Finding
5): "The register's vintage, such as it is, matches the phase-in in
Finding 1."

"The pick" is internal workflow vocabulary a public reader cannot parse,
and "such as it is" is an editorial aside of the kind Section 2 asks the
brief to avoid. Both are one-line rewrites ("This brief set out to measure
..."; delete "such as it is").

### Finding 15 (FLAG) - Social copy pairs the assigned-rows claim with the all-rows citywide rate

At issue (social-drafts.md): "active rows appear in all 78 neighborhoods,
at 108.4 rows per 1,000 housing units citywide."

Rows "appear in" neighborhoods on the assigned basis, whose citywide rate
is 106.9 per 1,000; 108.4 is the all-active-rows basis. The brief prints
both, labeled ("108.4... on all active rows; on assigned rows only,
106.9"). The social sentence fuses the two bases in one breath. Minor, but
it is the same habit as Finding 2 in miniature. Use 106.9 next to the
neighborhood claim or label 108.4 as the all-rows rate.

### Finding 16 (FLAG) - Status lines that this pass makes stale, and the still-open verifier

README.md, reviewer-notes.md ("Independent verifier: NOT RUN. Adversarial
reviewer: NOT RUN."), and verification.md ("no separate verifier or
adversarial agent pass has run on this package yet") were accurate when
written. As of this report the adversarial pass HAS run; the independent
verifier has NOT. Per the tasking, the not-yet-run language is expected
and is not itself a defect - but the fix loop must update all three
records when it closes, and the package remains not Section 11 complete
until the verifier pass runs and every finding here has a recorded
disposition (Section 10.3.3: a loop closed against a partial read is an
open gate). No other stale claims were found: the leakage-scan result,
repo-existence check, snapshot counts, and "nothing pushed, posted, or
sent" statements are consistent across README, reviewer-notes, and
verification.

### Finding 17 (FLAG) - The license-basis headline is defensible; the unqualified "holders" framing in title, hero, and social is the maximum-dispersion reading of a name field

At issue: title "Denver Has 26,941 Active Long-Term Rental Licenses, Held
by 20,780 Holders"; Finding 2's own sensitivity (verified against
stats.json): first-and-last-token merging cuts the group count to 17,496
and puts 45.4 percent of licenses in groups of two or more; the deliberate
over-merge reaches a 1,160-license maximum group.

On the review question: the license basis for the headline is defensible
and is defended the right way - Finding 1 leads the brief, the row count
is never hidden (38,970 is in the second sentence), and the register's own
name ("active licenses" for a table of filing rows) is called out in Data
notes. Counting distinct LICENSE_NUM is the only basis on which "active
licenses" is a true sentence. What the headline surfaces do not carry is
the qualifier the body is careful to print: 20,780 is a count of distinct
holder NAME STRINGS as filed, which Finding 2 itself shows is a floor on
grouping (common control through distinct LLCs, and managers filing for
owners, are invisible in ENTITY_NAME - both stated plainly in Finding 2).
The title, hero, and both social drafts say "holders" without "names as
filed." No sentence in the package overclaims beneficial ownership - the
body disclaims it three times - so this is a framing flag, not a factual
defect, and reviewer-notes already puts the headline-basis call to Alex.
Recommendation: title and hero to "20,780 holder names as filed" (with
Finding 4's composition fix), and one clause in the LinkedIn post's first
paragraph carrying the floor caveat that Finding 2 prints.

---

## Leakage check (task item 8)

Method: my own greps over the package (all .md, .json, .csv, .txt, .py
files), independent of the builder's code/leakage_scan.py, plus a visual
read of hero.png and a read of code/charts.py.

- 13-digit sequences: exactly one hit in the text files - sources.md line
  10, the ArcGIS editingInfo epoch "1792489245499" (a millisecond timestamp
  for the service's last edit). It is not a parcel number. No 13-digit
  parcel value appears anywhere.
- Street-address patterns (number + name + St/Ave/Blvd/Rd/Dr/Ln/Ct/Way/Pl):
  zero hits.
- Holder-name values: no uppercase multi-token name strings with entity
  suffixes (LLC/INC/LLP/LTD/CORP) appear in any markdown file; the only
  such tokens anywhere are the classification token list in stats.json and
  the business-token set in code - field/rule vocabulary, not values.
- hero.png (read visually): contains only the aggregate figures (68.6%,
  18,471, 26,941, 20,780) and a generic illustration - no name, address, or
  parcel value. Charts are built from stats.json and the aggregate
  neighborhood panel only (code/charts.py).
- Corroboration: the builder's leakage_scan.py result recorded in
  reviewer-notes.md (PASSED, 0 value hits across 24 package files, against
  snapshot value sets of 40,322 holder-name forms, 50,086 address forms,
  53,240 parcel-number forms) is consistent with my independent greps.

Verdict: no licensee name, street address, or parcel number value found
anywhere in the package. (Note: this adversarial-review.md becomes a 25th
package file after the recorded scan; it contains no register values
either, but the scan should be re-run over the final file set in the fix
loop for the record.)

## What survived the attack (for the fix loop's calibration)

- Every figure I recomputed from stats.json ties to the brief at printed
  precision, except the items in Findings 2, 3, and 4: concentration bands
  and top shares (1.95 / 3.89 / 4.86 / 6.36; 8.39 for the 11+ band),
  classification on licenses / rows / holders (37.1 / 49.4 / 31.1 business),
  both merge sensitivities, vintage (49.3 percent 2023 prefix; 91.7 percent
  2023-or-later), expiry cohorts, duplicates, the double-filed license
  arithmetic, neighborhood counts and rates, both Spearman coefficients,
  and the 12.9x / 18.7x STR ratios.
- STR comparison labeling in the brief body and in code/charts.py is
  thorough: separate panels, separate scales, panel titles naming the
  measure ("register rows" vs "active licenses"), a suptitle reading
  "different measures, labeled (do not add)," and a brief that never adds
  the two rates. The lapses are in the social compression (Findings 7, 12,
  15) and the publication premise (Finding 1), not in Finding 4 itself.
- The Finding 5 coverage boundary (no renter-occupied denominator, no
  licensed share of rental stock printed) is stated exactly where a reader
  would go looking for the number. Keep it.
- No en or em dashes in brief-draft.md or social-drafts.md (grep count 0);
  LinkedIn tag line complete with city tag; no X draft, per the standing
  rule; budget dates in Who can act match the cited October 9, 2026 council
  release as carried in sources.md.
