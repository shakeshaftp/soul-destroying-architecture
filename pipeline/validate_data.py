"""
STEP 3 — refuse to publish something broken.

This runs before every commit. If it raises, the workflow stops and the live
site keeps yesterday's good data instead of getting today's bad data.

Two of the checks here are not about tidiness, they are the point of the
project:

  * a comparison cannot be published without a pairing note, because an
    unexplained pair is the thing critics of this argument look for; and
  * a photograph cannot be published without a named credit and a licence
    from the list in config.json, because this repository is public and
    everything in it is being redistributed.

Add your own checks as you learn what "wrong" looks like for this catalogue.
"""
import json
import sys

import pandas as pd

from common import DATA, ENCODING, images_dir, load_config

REQUIRED_COLUMNS = [
    "pair_id", "role", "building", "year", "city", "country",
    "tradition", "use", "caption", "image_file", "image_credit",
    "image_licence", "image_source_url", "pairing_note",
]

# Every row needs these filled in. `architect` is deliberately not here:
# plenty of good buildings have no single named architect.
REQUIRED_PER_ROW = ["building", "city", "country", "tradition", "use", "caption"]

ROLES = {"exemplar", "contrast"}


def validate():
    cfg = load_config()
    path = DATA / "site_data.csv"

    if not path.exists():
        raise SystemExit("FAIL: data/site_data.csv does not exist")

    df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding=ENCODING)
    problems = []

    if df.empty:
        problems.append("the catalogue is empty")

    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        # Nothing below can run without the columns, so stop here.
        print("VALIDATION FAILED:", file=sys.stderr)
        print(f"  - missing required columns: {', '.join(missing_cols)}", file=sys.stderr)
        raise SystemExit(1)

    # --- every row is a complete building -------------------------------
    for col in REQUIRED_PER_ROW:
        blank = df[df[col].str.strip() == ""]
        for _, r in blank.iterrows():
            problems.append(f"{r['pair_id']}/{r['role']}: no {col}")

    bad_roles = sorted(set(df["role"]) - ROLES)
    if bad_roles:
        problems.append(
            f"role must be 'exemplar' or 'contrast', found: {', '.join(bad_roles)}")

    # --- every pair is a real pair ---------------------------------------
    for pair_id, g in df.groupby("pair_id", sort=False):
        roles = sorted(g["role"])
        if len(g) != 2 or roles != ["contrast", "exemplar"]:
            problems.append(
                f"{pair_id}: a comparison needs exactly one exemplar and one "
                f"contrast, found {len(g)} row(s): {', '.join(roles) or 'none'}")

        # The discipline the whole argument rests on.
        if not g["pairing_note"].str.strip().any():
            problems.append(
                f"{pair_id}: no pairing note — say why these two buildings are "
                "a fair comparison before publishing them side by side")

    # --- every published photograph is cleared and credited --------------
    allowed = set(cfg.get("allowed_licences", []))
    imgs = images_dir(cfg)

    for _, r in df.iterrows():
        f = r["image_file"].strip()
        if not f:
            continue          # no photograph yet is a fine state; the page says so
        where = f"{r['pair_id']}/{r['role']} ({r['building']})"
        if not (imgs / f).exists():
            problems.append(f"{where}: image_file '{f}' is not in {imgs.name}/")
        if not r["image_credit"].strip():
            problems.append(f"{where}: photograph has no credit")
        licence = r["image_licence"].strip()
        if not licence:
            problems.append(f"{where}: photograph has no licence recorded")
        elif allowed and licence not in allowed:
            problems.append(
                f"{where}: licence '{licence}' is not in allowed_licences in "
                "config.json — add it there if it is genuinely redistributable")

    # --- guard against a broken edit silently gutting the site -----------
    meta_path = DATA / "meta.json"
    if meta_path.exists():
        previous = json.loads(meta_path.read_text(encoding=ENCODING)).get("previous_rows")
        if previous and len(df) < previous * 0.5:
            problems.append(
                f"row count fell from {previous} to {len(df)} — that looks "
                "like a broken edit, not a deliberate one")

    if problems:
        print("VALIDATION FAILED:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        raise SystemExit(1)

    # Not a failure, just worth knowing about.
    if imgs.exists():
        used = {f.strip() for f in df["image_file"] if f.strip()}
        spare = sorted(p.name for p in imgs.iterdir()
                       if p.is_file() and p.suffix.lower() in
                       {".jpg", ".jpeg", ".png", ".webp", ".avif"}
                       and p.name not in used)
        if spare:
            print(f"note: {len(spare)} image(s) in {imgs.name}/ not used by any "
                  f"row: {', '.join(spare[:5])}{' ...' if len(spare) > 5 else ''}")

    print(f"validation passed: {len(df)} buildings, "
          f"{df['pair_id'].nunique()} comparisons")
    return df


if __name__ == "__main__":
    validate()
