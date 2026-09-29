"""
STEP 4 — render the site from the catalogue.

Reads templates/index.html, fills it in, and writes site/. The site folder is
generated output: edit the template, not the result.

The catalogue is flat — one row per building — because that is what makes a
readable CSV and a readable diff. Assembling the rows into comparisons is a
rendering job, and it happens here.
"""
import json
import shutil

import pandas as pd
from jinja2 import Template

from common import DATA, ENCODING, SITE, TEMPLATES, images_dir, load_config


def to_pairs(df):
    """Two rows sharing a pair_id become one comparison."""
    pairs = []
    for pair_id, g in df.groupby("pair_id", sort=False):
        by_role = {r["role"]: r for r in g.to_dict(orient="records")}
        exemplar, contrast = by_role.get("exemplar"), by_role.get("contrast")
        if not (exemplar and contrast):
            continue          # validate_data has already refused this run
        pairs.append({
            "id": pair_id,
            "use": exemplar.get("use", ""),
            "note": exemplar.get("pairing_note", ""),
            "exemplar": exemplar,
            "contrast": contrast,
        })
    return pairs


def build():
    cfg = load_config()
    df = pd.read_csv(DATA / "site_data.csv", dtype=str,
                     keep_default_na=False, encoding=ENCODING)
    meta = json.loads((DATA / "meta.json").read_text(encoding=ENCODING))

    # One setting drives the custom domain. Filling in "custom_domain" in
    # config.json makes it the canonical address everywhere — the <link
    # rel=canonical>, the Open Graph URLs, and the CNAME file GitHub Pages
    # needs in the artifact. Leave it empty and the site stays on github.io.
    domain = cfg.get("custom_domain", "").strip().lstrip("@").rstrip("/")
    if domain:
        cfg["site_url"] = f"https://{domain}"

    pairs = to_pairs(df)

    html = Template(
        (TEMPLATES / "index.html").read_text(encoding=ENCODING),
        trim_blocks=True, lstrip_blocks=True,
    ).render(
        cfg=cfg,
        meta=meta,
        pairs=pairs,
        rows=df.to_dict(orient="records"),
        columns=list(df.columns),
        label_col=cfg["label_column"],
    )

    SITE.mkdir(exist_ok=True)
    (SITE / "index.html").write_text(html, encoding=ENCODING)

    # GitHub Pages reads CNAME from the uploaded artifact. Without it, a
    # redeploy can drop the custom domain set in the repository settings.
    cname = SITE / "CNAME"
    if domain:
        cname.write_text(domain + "\n", encoding=ENCODING)
    elif cname.exists():
        cname.unlink()

    # The raw catalogue, downloadable from the site.
    shutil.copy(DATA / "site_data.csv", SITE / "data.csv")

    # The photographs. Only the files the catalogue actually references get
    # copied, so an abandoned draft image never reaches the published site.
    src_imgs = images_dir(cfg)
    dest_imgs = SITE / "images"
    if dest_imgs.exists():
        shutil.rmtree(dest_imgs)
    wanted = {f.strip() for f in df["image_file"] if f.strip()}
    if wanted and src_imgs.exists():
        dest_imgs.mkdir(parents=True, exist_ok=True)
        for name in sorted(wanted):
            src = src_imgs / name
            if src.exists():
                shutil.copy(src, dest_imgs / name)

    for asset in ("favicon.svg", "preview.png", "apple-touch-icon.png"):
        src = TEMPLATES / asset
        if src.exists():
            shutil.copy(src, SITE / asset)

    print(f"built site/index.html — {len(pairs)} comparisons, "
          f"{len(wanted)} photograph(s)")


if __name__ == "__main__":
    build()
