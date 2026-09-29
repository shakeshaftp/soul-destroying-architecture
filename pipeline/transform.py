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

    out = DATA / "site_data.csv"
    df.to_csv(out, index=False, encoding=ENCODING)

    # Which photographs are actually in place, and which are still to come.
    imgs = images_dir(cfg)
    have = df["image_file"].apply(lambda f: bool(f) and (imgs / f).exists())

    now = datetime.now(timezone.utc)

    # Read the previous count before overwriting meta.json, so validate_data
    # has something real to compare today's run against.
    meta_path = DATA / "meta.json"
    previous = None
    if meta_path.exists():
        previous = json.loads(meta_path.read_text(encoding=ENCODING)).get("rows")

    write_json(meta_path, {
        "rows": int(len(df)),
        "previous_rows": previous,
        "pairs": int(df["pair_id"].nunique()),
        "countries": int(df["country"].nunique()),
        "traditions": int(df["tradition"].nunique()),
        "images_present": int(have.sum()),
        "images_missing": int((~have).sum()),
        "updated": f"{now:%B} {now.day}, {now:%Y}",
        "updated_iso": now.isoformat(timespec="seconds"),
        "source_name": cfg["source_name"],
        "source_url": cfg["source_url"],
    })

    print(f"wrote {len(df)} buildings in {df['pair_id'].nunique()} pairs "
          f"to data/site_data.csv ({int(have.sum())} photographs in place)")
    return df


if __name__ == "__main__":
    transform()
