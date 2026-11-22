# missing-links

[![Validate records](https://github.com/frink-okn/missing-links/actions/workflows/validate.yml/badge.svg)](https://github.com/frink-okn/missing-links/actions/workflows/validate.yml)
[![Publish views](https://github.com/frink-okn/missing-links/actions/workflows/pages.yml/badge.svg)](https://github.com/frink-okn/missing-links/actions/workflows/pages.yml)
[![License: BSD-3-Clause](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](scripts/validate_records.py)

A collection of structured records of federation connection problems.

A record is one problem where two or more knowledge graphs in the
federation should connect, but do not, or where they connect on the
wrong thing. Each record says which graphs are involved, what
identifier each one uses, what standard is proposed, and what evidence
was checked. Records for joins that were tried and failed are kept
here too, so nobody retries them blindly.

## How it works

An agent researches a problem and drafts a record. Automated checks
verify the record. A human reviewer approves it in a pull request.
Nothing is accepted without that review.

The agent helps in a local session only. It does not run in GitHub
Actions, and no Action calls a language model, merges a record, or
approves a standard. Actions only validate records and rebuild the
views. The human reviewer is the only gate that accepts a record.

## The first records

The first records are about state identifiers: which graphs represent
US states, what IRI namespace each one uses, and what standard
namespace is proposed. Those three records are drafts. Their
namespaces are marked to be confirmed, because that research is not
done yet. They show the shape of a record, not a finished answer.

## Repository layout

- `schema/missing_link.yaml` — the LinkML schema for one record.
- `records/` — one YAML file per problem, grouped by topic.
- `records/state-identifiers/` — the first records, about US states.
- `scripts/validate_records.py` — checks every record against the
  shape the schema requires. Python standard library plus PyYAML.
- `scripts/build_views.py` — rebuilds the index and the cross-graph
  matrix from the records. Python standard library plus PyYAML.
- `docs/` — the built views, published to GitHub Pages.
- `.github/workflows/validate.yml` — validates records on pull
  requests.
- `.github/workflows/pages.yml` — rebuilds the views and publishes
  them on merge to main.
- `AGENTS.md` — instructions for the triage agent, for local use.
- `CONTRIBUTING.md` — how to propose and review a record.

## Try it locally

No account, server, or language model is needed. Python 3.10 or
later and PyYAML are enough.

```bash
pip install pyyaml
python3 scripts/validate_records.py
python3 scripts/build_views.py
```

Then open `docs/index.html` and `docs/matrix.html` in a browser.

See `docs/LOCAL_TEST.md` for the full local test, including how to
check that a bad record fails validation.

## Propose a record

1. Open an issue describing the connection problem.
2. Research it and draft one YAML file under `records/`, following
   the schema and the example records.
3. Run the validator locally and fix any errors.
4. Open a pull request. A reviewer checks the evidence and the
   proposed standard, and merges it if it holds up.

See `CONTRIBUTING.md` for the full workflow.

## Status of a record

- `open` — drafted, not yet reviewed.
- `under_review` — a reviewer is checking it.
- `accepted` — reviewed and accepted.
- `rejected` — reviewed and not accepted, with the reason kept in
  the record.

## License

BSD 3-Clause. See `LICENSE`.
