# Test missing-links locally, before creating the repository

Do this on your own computer, in the folder you copied the
skeleton into. Nothing here needs an account, a server, or a
language model. The only requirement is Python 3.10 or later.

## 1. Get into the folder

In Anaconda Prompt, or any terminal:

```bash
cd missing-links
```

Check Python:

```bash
python --version
```

You need 3.10 or later. If `python` does not work, try
`python3 --version` and use `python3` in the commands below.

## 2. Install PyYAML

```bash
pip install pyyaml
```

PyYAML is the only dependency. It reads the YAML record files.
There is no other install step.

## 3. Validate the records

```bash
python scripts/validate_records.py
```

You should see:

```
OK: 3 record(s) valid.
```

That means all three example records pass: the two graphs, the
problem type, the identifier type, the proposed standard (or
`to_be_confirmed`), and the evidence summary are all present.

## 4. Build the views

```bash
python scripts/build_views.py
```

You should see:

```
Wrote 3 record(s) to docs/index.html and docs/matrix.html.
```

## 5. Look at the views

Open these two files in a browser, by double-clicking them:

- `docs/index.html` — the list of the three records.
- `docs/matrix.html` — the cross-graph matrix. GeoConnex,
  RuralKG, and SpatialKG are the rows and columns. Each pair
  with a record shows that record's id and its status, `open`.
  The other cells are empty.

No server is needed. They are plain static pages.

## 6. Check that a bad record fails

This is the test that matters most, because it is what the
GitHub Action will do on a pull request.

1. Make a copy of one record, for example
   `records/state-identifiers/states-geoconnex-ruralkg.yaml`,
   and delete the `evidence:` block from the copy, or change
   `status: open` to `status: finished`.
2. Run the validator again:

```bash
python scripts/validate_records.py
```

It should fail, and name the file and the field that is wrong.
3. Delete the copy you made, and run the validator once more.
   It should pass again.

If the validator passes a record with no evidence, or with a
status that is not one of `open`, `under_review`, `accepted`,
or `rejected`, do not create the repository yet. Tell me what
it did, and I will fix it.

## 7. Check the workflows read correctly

Open these two files and check they look like plain text, with
no error in your editor:

- `.github/workflows/validate.yml`
- `.github/workflows/pages.yml`

You do not need to run them locally. They run on GitHub, after
the repository is created. `validate.yml` runs on every pull
request. `pages.yml` runs only on merge to main, and publishes
the views.

## 8. Only then, create the repository

Do not create the repository in the organisation until steps
3 to 6 pass on your computer.

When you do create it, create an empty repository, then copy
these files into it, add them, commit, and push. Do not copy
the zip file itself, and do not use force push. Enable Pages
once, in Settings > Pages > Source: GitHub Actions, before
the first merge to main. The first `pages.yml` run will fail
until Pages is enabled, in the same way it did for the
connection-map repo.
