"""Fresh pull of the Denver residential rental property license register, 2026-10-20.

Source: Denver Open Data Catalog, ODC_residential_rental_property_active_licenses
(ArcGIS FeatureServer table 52), Department of Licensing and Consumer Protection.

Writes ONLY to the warehouse:
- stack/denver/snapshots/2026-10-20/rental_licenses.parquet
- pull log next to it: pull_log_rental_2026-10-20.json

The raw register is NEVER copied into the brief package. The package ships
aggregates only.
Paginated at maxRecordCount=2000 ordered by OBJECTID; pulled count asserted
equal to live service count before writing.
"""
import hashlib
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

import pandas as pd

BASE = ("https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/"
        "ODC_residential_rental_property_active_licenses/FeatureServer/52/query")
ROOT = ("https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/"
        "ODC_residential_rental_property_active_licenses/FeatureServer/52")
STACK_SNAP_DIR = ("/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/"
                  "stack/denver/snapshots/2026-10-20")
STACK_SNAP = f"{STACK_SNAP_DIR}/rental_licenses.parquet"
PAGE = 2000


def get_json(url):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return json.load(r)
        except Exception:
            if attempt == 3:
                raise
            time.sleep(3 * (attempt + 1))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


if os.path.exists(STACK_SNAP):
    raise RuntimeError(f"snapshot already exists, refusing to overwrite: {STACK_SNAP}")

meta = get_json(ROOT + "?f=json")
last_edit_ms = (meta.get("editingInfo") or {}).get("lastEditDate")

count_url = BASE + "?" + urllib.parse.urlencode(
    {"where": "1=1", "returnCountOnly": "true", "f": "json"})
expected = get_json(count_url)["count"]
print("live service count:", expected)

rows = []
offset = 0
while True:
    params = {
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "false",
        "orderByFields": "OBJECTID",
        "resultOffset": offset,
        "resultRecordCount": PAGE,
        "f": "json",
    }
    resp = get_json(BASE + "?" + urllib.parse.urlencode(params))
    feats = resp.get("features", [])
    rows.extend(f["attributes"] for f in feats)
    print(f"offset {offset}: +{len(feats)} (total {len(rows)})", flush=True)
    if not resp.get("exceededTransferLimit") or not feats:
        break
    offset += PAGE

assert len(rows) == expected, f"pulled {len(rows)}, expected {expected}"
df = pd.DataFrame(rows)
print("rows:", len(df), "cols:", len(df.columns))
print("status counter:", df["LICENSE_STATUS"].value_counts(dropna=False).to_dict())

os.makedirs(STACK_SNAP_DIR, exist_ok=True)
df.to_parquet(STACK_SNAP, index=False)

log = {
    "dataset": "ODC_residential_rental_property_active_licenses (ArcGIS FeatureServer table 52)",
    "publisher": "Department of Licensing and Consumer Protection (DLCP), City and County of Denver, via Denver Open Data Catalog",
    "service_url": ROOT,
    "pulled_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "service_last_edit_ms": last_edit_ms,
    "service_last_edit_utc": (
        datetime.fromtimestamp(last_edit_ms / 1000, timezone.utc).isoformat() if last_edit_ms else None),
    "rows": int(len(df)),
    "status_counter": {str(k): int(v) for k, v in df["LICENSE_STATUS"].value_counts(dropna=False).items()},
    "snapshot_path": STACK_SNAP,
    "size_bytes": os.path.getsize(STACK_SNAP),
    "sha256": sha256(STACK_SNAP),
}
with open(f"{STACK_SNAP_DIR}/pull_log_rental_2026-10-20.json", "w") as fh:
    json.dump(log, fh, indent=1)
print(json.dumps(log, indent=1))
