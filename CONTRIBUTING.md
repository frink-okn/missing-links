# Contributing to missing-links

## The workflow

1. **Open an issue.** Describe the connection problem in plain
   words: which graphs, which identifier, and what goes wrong.
   One issue per problem.
2. **Research it locally.** Check what each graph actually uses.
   Do not invent a namespace, an identifier, or a count. If a
   value is not known yet, write `to_be_confirmed` and say what
   still needs checking.
3. **Draft one record.** Add one YAML file under `records/`,
   in the folder for its topic. Copy the closest example record
   and change it. Follow `schema/missing_link.yaml`.
4. **Validate locally.** Run `python3 scripts/validate_records.py`
   and fix every error it reports.
5. **Open a pull request.** The pull request is the review. A
   reviewer checks the evidence, the namespaces, and the proposed
   standard. The reviewer may ask for more evidence, or reject
   the record with a reason. The reason is kept in the record.
6. **Merge.** Once a reviewer approves, the record is merged.
   GitHub Actions rebuild the index and the cross-graph matrix
   automatically.

## What a reviewer checks

- Every graph named in the record is a real graph in the
  federation, and the namespace listed for it is the one it
  actually uses, or is honestly marked to be confirmed.
- The evidence is enough to repeat the check: a query, a count
  with a date, or a pointer to where it came from.
- The proposed standard is one namespace, not several, and the
  record says why that one was chosen.
- A failed match says what was tried and why it did not work.

## The agent's part

An agent may help in a local session: researching a problem and
drafting a record. It must not invent evidence, and it must mark
anything it could not verify as `to_be_confirmed`. It does not
decide whether a record is accepted. That decision belongs to
the human reviewer, in the pull request.

No language model runs in GitHub Actions in this repository.
Actions only validate records and rebuild views.

## Naming a record

The file name is the record id, for example
`states-geoconnex-ruralkg.yaml`. Use lower-case letters, numbers,
and hyphens only.
