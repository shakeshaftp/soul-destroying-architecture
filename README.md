# Building Beautifully

A project of the Manhattan Institute, by Paul Shakeshaft and John Ketcham,
arguing for beauty in the built environment — for wellbeing, for housing
supply, and for the environment.

This repository holds the public site: the argument, and a catalogue of
building comparisons chosen to show that the case is not about old versus new.

Built from the MI data-site starter. Live at
<https://shakeshaftp.github.io/soul-destroying-architecture>.

## Run it

```bash
pip install -r requirements.txt
python pipeline/run_update.py
start site\index.html
```

## Where things live

```
config.json           title, headline, source, accent, licence list, writing
data/source.csv       THE CATALOGUE — this is what you edit
images/               the photographs, committed, each one cleared
templates/index.html  the page source
site/                 generated — never edit by hand
```

## The catalogue

`data/source.csv` is one row per building. Two rows sharing a `pair_id` make
one comparison:

| column | what goes in it |
| --- | --- |
| `pair_id` | short slug, e.g. `penn-station`. Two rows share it. |
| `role` | `exemplar` (the building we hold up) or `contrast` (the one we argue against) |
| `building` | its name |
| `architect` | may be blank — plenty of good buildings have no single author |
| `year` | completed |
| `city`, `country` | where it is |
| `tradition` | Beaux-Arts, Amsterdam School, Islamic, Nordic modernism… |
| `use` | what it is for. Becomes the comparison's heading. |
| `caption` | one or two sentences under the photograph |
| `image_file` | filename in `images/`, or blank |
| `image_credit` | who took the photograph |
| `image_licence` | must be one of `allowed_licences` in `config.json` |
| `image_source_url` | where you got it — the file's page, not the raw image |
| `pairing_note` | **why this pair is fair.** Fill it on one row of the pair; the pipeline copies it to the other. |

### Adding a comparison

1. Add two rows to `data/source.csv` sharing a new `pair_id`.
2. Write the `pairing_note` before anything else. If you cannot say why the
   two buildings are a fair comparison — same use, similar scale, comparable
   era or budget — the pair does not belong in the set.
3. Drop the photographs in `images/` and fill in the file, credit and licence.
   See [images/README.md](images/README.md) for what is safe to publish.
4. `python pipeline/run_update.py`.

A row with no `image_file` is fine. The page shows a labelled gap and the
footer counts how many are outstanding, which doubles as the to-do list.

## What will stop a build

`pipeline/validate_data.py` refuses to publish, and the live site keeps the
last good version, if:

- a comparison has no pairing note;
- a pair does not have exactly one `exemplar` and one `contrast`;
- a row is missing its building, city, country, tradition, use or caption;
- a named photograph is not in `images/`;
- a photograph has no credit, or no licence, or a licence that is not in
  `allowed_licences`.

The last three are the ones that matter most. This repository is public and on
a personal account, so an uncredited photograph is the easiest possible thing
for an opponent of the project to make a story out of.

Do not relax these checks to get a run through. If validation fails, the
catalogue is wrong.

## Publishing

Settings → Pages → Source: **GitHub Actions**, once. Then push to `main`;
`.github/workflows/update.yml` builds and deploys, and re-runs each morning.

The daily run will be a no-op until there is something that actually changes
day to day — survey results, most likely. That is expected; a quiet Actions
tab does not mean anything is broken.

Run `/publish` before the site is shared, for the favicon, preview image and
metadata pass.

## Still to do

- Source and clear the twelve photographs.
- Confirm the facts flagged in the catalogue (see the project notes).
- Decide the public URL — a custom domain is reimbursable.
