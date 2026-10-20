# Sources - Denver residential rental licenses brief (2026-10-20)

## Primary dataset
- Denver Open Data Catalog, ODC_residential_rental_property_active_licenses
  (residential rental property licenses), ArcGIS FeatureServer table 52:
  https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/ODC_residential_rental_property_active_licenses/FeatureServer/52
  Publisher: Department of Licensing and Consumer Protection (DLCP), City and County
  of Denver.
  Fresh snapshot: full-service pull 2026-10-20 (2026-10-20T12:32:53Z), 38,970 records;
  service last edit 2026-10-20T09:40:45Z (editingInfo.lastEditDate epoch 1792489245499
  at pull time). Pulled count asserted equal to the live service count (38,970) before
  writing. Archived at warehouse stack/denver/snapshots/2026-10-20/rental_licenses.parquet
  (sha256 8f72f12d69212ede53b0ba43f153255b238e12d81e65620a651fc12574dcc5a5; pull log
  pull_log_rental_2026-10-20.json beside it). The live count recorded on 2026-10-19
  during lead verification was 38,981 rows; the table moved by 11 rows in one day.

## Field semantics (established from the service itself, 2026-10-20)
- LICENSE_STATUS: two values, counted exhaustively before any filter.
  License Issued - Active 38,949; Delinquent 21. This brief's active basis is the
  exact string "License Issued - Active" and nothing else.
- LICENSE_TYPE: "Residential Rental Property" on every record.
- LICENSE_NUM: the license key. 26,962 distinct values for 38,970 rows: rows sharing
  a license number are the unit/address filings of one license (verified row by row
  for every license with 100 or more rows: one holder name throughout; 11 of the 12
  on one parcel with all-distinct addresses, and one documented exception filing
  86 addresses under each of two parcel numbers). No license number mixes statuses. The 4-digit prefix encodes the issue
  year and is the only vintage signal in the service.
- ENTITY_NAME: the holder name as filed; the holder key for this brief after
  normalization (uppercase, whitespace collapsed). Null on 2 rows (both active, 2
  distinct licenses). Used only in aggregate (counts, shares, bands). No holder name
  appears in any published artifact of this package.
- PARCEL_NUM: esriFieldTypeDouble in the service. Values are integers of 10 to 12
  digits (leading zeros dropped in varying numbers); no nulls, zeros, or negatives.
  The canonical schednum is str(int(value)).zfill(13), matched directly against
  parcel spine v6.
- MULTIPLE_LICENSES: constant "Stand Alone" on all 38,970 rows, including all 697
  rows of the largest multi-unit license. Not a usable signal; multi-row and
  multi-license patterns in this brief are computed from LICENSE_NUM and the parcel
  bridge, never from this field.
- RELATIONSHIP: null on all 38,949 active rows; "Renewal" on the 21 Delinquent rows.
  RENEWAL_STATUS: null on active rows; "Pending" on the 21 Delinquent rows.
- RENEWAL_CREATED: reads "1/1/1900 12:00:00 AM" on all 38,949 active rows; the only
  non-sentinel values are the 21 Delinquent rows (2026 dates). A sentinel on this
  basis; used for nothing in this brief.
- EXPIRATION_DATE: a text date. 2 active-status rows carry an expiration date before
  the 2026-10-20 pull date; the remaining 21 past-expiration rows are exactly the
  Delinquent rows. Reported in Finding 5 as a field disagreement only.
- ZIP: integer; 0 on 3,436 rows and null on 773 (0 treated as unknown). Used for no
  figure in this brief.
- No original-issue date field exists in this service (no ORIG_ISSUED analogue), and
  no tax or ID field is present in the service at all.

## Parcel bridge and neighborhood assignment
- Direct key bridge: schednum (zfill-13 normalization of PARCEL_NUM) against parcel
  spine v6 (stack/denver/joins/parcel_spine_v6.parquet, built 2026-10-15).
  Register-wide match 38,471 of 38,970 rows (98.72 percent); active match 38,427 of
  38,949 (98.66 percent). Unmatched active rows: 522 rows on 205 parcels under 213
  licenses, concentrated (the two largest unmatched parcels hold 157 rows), consistent
  with newer parcels absent from the 2026-10-15 spine snapshot.
- Neighborhood: spine v6 neighborhood of the assigned parcel (the city's 78
  statistical neighborhoods, official ODC boundaries). 38,427 of 38,949 active rows
  carry a neighborhood.
- Parcel unit counts (TOT_UNITS) are the spine's assessor parcel record figures
  (assessor parcels layer, 2026-10-15 snapshot), reported as parcel record figures,
  not as counts of licensed or rented units.

## Comparison and denominator layers (warehouse)
- STR comparison: Machine Readable, Denver short-term rental licenses brief,
  2026-10-19 (package denver-str-licenses-brief-2026-10-19: stats.json and
  data/neighborhood_panel.csv). Active STR licenses 2,083; citywide 5.8 per 1,000
  housing units; 75 of 78 neighborhoods; zero neighborhoods Auraria, Kennedy,
  Sun Valley.
- Denominators: US Census Bureau, American Community Survey 2020-2024 5-year
  estimates, table B25001 (housing units), tract level, Denver County, via Census
  Reporter; allocated to the city's 78 statistical neighborhoods by tract area
  share (warehouse layer acs_neighborhood_units.parquet; Denver County total
  359,581 units, 359,351 allocated). Same denominators as the October 17, 18, and
  19 briefs. The warehouse ACS layer carries total housing units only: no
  renter-occupied denominator exists in the warehouse at any geography, which is
  why Finding 5 prints no licensed share of rental stock.

## Program rules context (the city's own documents)
- City and County of Denver, Department of Licensing and Consumer Protection,
  "Frequently asked questions - general," Residential rental property,
  denvergov.org:
  https://www.denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Business-Licensing/Business-licenses/Residential-rental-property/Frequently-asked-questions
  Fetched and read in full 2026-10-20. States, in the city's own words: a license
  is required for anyone offering, providing, or operating a residential rental
  property for 30 days or more; all landlords renting any dwelling unit long term
  must have a license; each single-unit property requires an individual license;
  for multi-unit properties, a single license can be issued for multiple units,
  addresses, or structures on a single or contiguous parcels under the same
  ownership; licenses are valid for four years unless ownership changes and are
  non-transferable. The brief states these rules as program context only; it tests
  no license against them.
- City and County of Denver, Department of Licensing and Consumer Protection,
  "Frequently asked questions - renewal," denvergov.org (same path stem,
  Frequently-asked-questions-renewal). Fetched and read in full 2026-10-20.
  States the license fee schedule by unit count, the four-year term, the renewal
  window (apply 90 days before expiration), and the 90-day grace period after
  expiration (20 percent penalty in the first 30 days, 50 percent in days 31 to
  90, new application after 90 days), cited in Finding 5.
- City and County of Denver news release, "Denver Begins Residential Rental
  Enforcement Efforts," published February 23, 2023, denvergov.org:
  https://denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Business-Licensing/News/EXL/Denver-Begins-Enforcement-Efforts-Aimed-at-Increasing-Residential-Rental-Licensing-Compliance
  Fetched and read in full 2026-10-20. States: the licensing requirement began for
  multi-unit rental properties on January 1, 2023; landlords of single-unit rental
  properties were not required to obtain a license until January 1, 2024; the city
  began accepting applications in March 2022.

## Budget calendar (Who can act)
- City and County of Denver, Denver City Council news release, "Denver City Council
  Makes Budget Recommendations," published October 9, 2026, denvergov.org:
  https://www.denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Denver-City-Council/News/2027-budget-recommendations
  - the 2027 budget dates used in the brief: final proposed budget due October 19,
  2026; public hearing October 26; last amendment vote November 2; final passage
  November 9 (charter deadline). Verified live 2026-10-18 during the traffic
  brief's QA run and carried in the STR package; the same citation is carried here.
