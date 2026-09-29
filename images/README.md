# Photographs

Put the image files for the catalogue in this folder, then name each one in the
`image_file` column of `data/source.csv`.

Only files named by a row ever reach the published site, so a draft or a
rejected crop can sit here harmlessly.

## What the pipeline will not let you publish

`pipeline/validate_data.py` stops the build if a row names an image and any of
the following is true:

- the file is not in this folder;
- `image_credit` is empty — somebody took the photograph, name them;
- `image_licence` is empty, or is not one of the `allowed_licences` listed in
  `config.json`.

A row with an empty `image_file` is fine. The page shows a labelled gap and the
footer counts how many are still outstanding, which is a more useful to-do list
than a spreadsheet.

## Before you add anything

This repository is public and sits on a personal account. Everything in this
folder is being redistributed to the world, so:

- **Note the licence at the moment you download the file**, not later. It is
  much harder to reconstruct afterwards, and an uncredited photograph is the
  easiest possible thing for an opponent of the project to make a story out of.
- **Wikimedia Commons** gives you the photographer and licence on the file page.
  Put the page URL — not the raw image URL — in `image_source_url`.
- **Freedom of panorama differs by country.** Photographing a building from a
  public street and publishing the result is fine in the United States, the
  United Kingdom, Germany and Japan. It is restricted in France, Italy,
  Belgium and Greece, where a recent building's architect may still hold
  rights in its image. Buildings old enough to be out of copyright are not
  affected — which covers most of what this project will want.
- **Your own photographs**: use `Own photograph` as the licence and your name
  as the credit.

If you are not sure a file is clear, leave `image_file` empty and say so. The
site is designed to look deliberate with gaps in it.

## Naming

Name files after the row that uses them, so a missing one is obvious:

```
penn-station-exemplar.jpg
penn-station-contrast.jpg
town-hall-exemplar.jpg
```

Aim for landscape, at least 1600px wide, under about 400KB each. Large images
are the usual reason a GitHub Pages site feels slow.
