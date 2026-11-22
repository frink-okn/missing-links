# AGENTS.md — triage agent instructions for missing-links

These instructions are for an agent working in a local session.
They are not run by GitHub Actions. Nothing in this file gives
an agent the power to accept a record. Acceptance happens only
when a human reviewer approves a pull request.

## Your job

Research one federation connection problem and draft one record
for it, as a YAML file under `records/`, following
`schema/missing_link.yaml` and the example records.

## How to triage

1. Read the issue. Name the graphs involved and the identifier
   type before you write anything.
2. Check what each graph actually uses. Look at the graph's data,
   a live query, or a saved run. Do not guess a namespace from a
   graph's name.
3. Decide which kind of problem it is: different namespaces,
   missing join, wrong join, failed match, or other.
4. Write the evidence first, then the proposal. If the evidence
   does not support a standard, leave the proposed standard as
   `to_be_confirmed` and say what is missing.

## Rules

- Never invent a namespace, an identifier, a count, or a
  reference. If you could not verify a value, write
  `to_be_confirmed` and add a note saying what still needs
  checking.
- Every record needs at least two graphs, a problem type, an
  identifier type, a proposed standard or `to_be_confirmed`,
  and an evidence summary.
- Keep the record minimal. Add a field only if a reviewer needs
  it to check the problem.
- Run `python3 scripts/validate_records.py` before you finish,
  and fix every error it reports.
- Do not open a pull request on your own, do not merge anything,
  and do not change any file outside the record you were asked
  to draft, unless the user asks you to.

## What you must not do

- Do not approve, accept, or reject a record.
- Do not change the schema, the validator, the view builder, or
  any workflow file without being asked.
- Do not add a language-model call, an API key, or any network
  call to a workflow file.
- Do not claim a record is verified when it is only drafted.
  Its status is `open` until a reviewer changes it.
