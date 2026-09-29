"""
STEP 2 — turn the raw catalogue into exactly what the site needs.

The dataset is one row per building. Two rows sharing a pair_id make one
comparison: the `exemplar` (the building we hold up) and the `contrast` (the
building we are arguing against).

This step cleans the catalogue, propagates each pair's pairing note to both of
its rows, orders the set, and records provenance. It must produce:

  data/site_data.csv   the published catalogue, one row per building
  data/meta.json       counts, update date, and provenance for the footer
"""
import hashlib
import json
from datetime import datetime, timezone

import pandas as pd

from common import DATA, ENCODING, images_dir, load_config, write_json
from fetch import RAW

# Order buildings within a pair: the one we are advocating for reads first.
ROLE_ORDER = {"exemplar": 0, "contrast": 1}


def transform():
    cfg = load_config()
    df = pd.read_csv(RAW, dtype=str, keep_default_na=False, encoding=ENCODING)

    # --- clean -----------------------------------------------------------
    df.columns = [c.strip() for c in df.columns]
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    # A row with no building name is an editing accident, not a building.
    df = df[df["building"] != ""]
    df["role"] = df["role"].str.lower()

    # --- the pairing note belongs to the pair, so only one row need carry
    #     it in source.csv. Give it to both rows here. ---------------------
    def first_note(s):
        filled = [n for n in s if n.strip()]
        return filled[0] if filled else ""

    df["pairing_note"] = df.groupby("pair_id")["pairing_note"].transform(first_note)

    # --- order: pairs in the order they appear, exemplar before contrast --
    pair_order = {p: i for i, p in enumerate(df["pair_id"].drop_duplicates())}
    df["_pair"] = df["pair_id"].map(pair_order)
    df["_role"] = df["role"].map(ROLE_ORDER).fillna(9)
    df = df.sort_values(["_pair", "_role"]).drop(columns=["_pair", "_role"])
    # ---------------------------------------------------------------------

    # Serialise before writing, so we can tell whether anything actually
    # changed. "\n" is forced so a run here and a run on the Linux CI runner
    # produce byte-identical output.
    out = DATA / "site_data.csv"
    new_csv = df.to_csv(index=False, lineterminator="\n")
    with open(out, "w", encoding=ENCODING, newline="") as f:
        f.write(new_csv)

    # Which photographs are actually in place, and which are still to come.
    imgs = images_dir(cfg)
    have = df["image_file"].apply(lambda f: bool(f) and (imgs / f).exists())

    # Read the previous run before overwriting it. validate_data needs the old
    # row count to compare against, and the date below needs the old date.
    meta_path = DATA / "meta.json"
    old = {}
    if meta_path.exists():
        old = json.loads(meta_path.read_text(encoding=ENCODING))

    # "Last updated" should mean the day the catalogue changed, not the day a
    # cron job happened to fire. This is a curated set, so most mornings
    # nothing will have changed — advancing the date anyway would put a
    # misleading line in the footer and commit an empty diff every single day.
    fingerprint = hashlib.sha256(
        f"{new_csv}|images:{int(have.sum())}".encode("utf-8")).hexdigest()

    now = datetime.now(timezone.utc)
    if fingerprint == old.get("fingerprint") and old.get("updated"):
        updated, updated_iso = old["updated"], old["updated_iso"]
    else:
        updated = f"{now:%B} {now.day}, {now:%Y}"
        updated_iso = now.isoformat(timespec="seconds")

    write_json(meta_path, {
        "rows": int(len(df)),
        "previous_rows": old.get("rows"),
        "fingerprint": fingerprint,
        "pairs": int(df["pair_id"].nunique()),
        "countries": int(df["country"].nunique()),
        "traditions": int(df["tradition"].nunique()),
        "images_present": int(have.sum()),
        "images_missing": int((~have).sum()),
        "updated": updated,
        "updated_iso": updated_iso,
        "source_name": cfg["source_name"],
        "source_url": cfg["source_url"],
    })

    print(f"wrote {len(df)} buildings in {df['pair_id'].nunique()} pairs "
          f"to data/site_data.csv ({int(have.sum())} photographs in place)")
    return df


if __name__ == "__main__":
    transform()
