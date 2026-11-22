"""Validate every record in records/ against the missing-links shape.

This checks the same shape described in schema/missing_link.yaml.
It does not need LinkML installed, and it makes no network calls.

Usage:
    python3 scripts/validate_records.py [--records records] [--strict]

Exit code 0 means every record is valid. Exit code 1 lists the
problems, one line per problem, with the file and the field.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PROBLEM_TYPES = {
    "different_namespaces",
    "missing_join",
    "wrong_join",
    "failed_match",
    "other",
}
STATUSES = {"open", "under_review", "accepted", "rejected"}

REQUIRED_TOP = [
    "id",
    "title",
    "problem_type",
    "identifier_type",
    "graphs",
    "proposed_standard_namespace",
    "evidence",
    "status",
]


def check_record(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # yaml.YAMLError and read errors
        return [f"{path}: cannot parse YAML: {exc}"]
    if not isinstance(data, dict):
        return [f"{path}: record must be a mapping, not {type(data).__name__}"]
    for field in REQUIRED_TOP:
        if field not in data or data[field] in (None, ""):
            errors.append(f"{path}: missing required field '{field}'")
    if errors:
        return errors

    if not isinstance(data["id"], str) or not ID_RE.match(data["id"]):
        errors.append(f"{path}: id must be lower-case letters, numbers and hyphens")
    elif data["id"] != path.stem:
        errors.append(
            f"{path}: id '{data['id']}' does not match file name '{path.stem}'"
        )
    if data["problem_type"] not in PROBLEM_TYPES:
        errors.append(
            f"{path}: problem_type must be one of {sorted(PROBLEM_TYPES)}"
        )
    if data["status"] not in STATUSES:
        errors.append(f"{path}: status must be one of {sorted(STATUSES)}")

    graphs = data["graphs"]
    if not isinstance(graphs, list) or len(graphs) < 2:
        errors.append(f"{path}: graphs must be a list of at least 2 graphs")
    else:
        names = []
        for i, g in enumerate(graphs):
            if not isinstance(g, dict):
                errors.append(f"{path}: graphs[{i}] must be a mapping")
                continue
            if not g.get("graph"):
                errors.append(f"{path}: graphs[{i}] is missing 'graph'")
            else:
                names.append(str(g["graph"]))
            if not g.get("namespace"):
                errors.append(f"{path}: graphs[{i}] is missing 'namespace'")
        if len(names) != len(set(names)):
            errors.append(f"{path}: graphs must not repeat a graph name")

    evidence = data["evidence"]
    if not isinstance(evidence, dict):
        errors.append(f"{path}: evidence must be a mapping")
    elif not evidence.get("summary"):
        errors.append(f"{path}: evidence.summary must not be empty")

    for i, fm in enumerate(data.get("failed_matches") or []):
        if not isinstance(fm, dict):
            errors.append(f"{path}: failed_matches[{i}] must be a mapping")
            continue
        for field in ("graphs", "attempted_identifier", "reason"):
            if not fm.get(field):
                errors.append(f"{path}: failed_matches[{i}] is missing '{field}'")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate missing-links records.")
    parser.add_argument("--records", default="records", help="records directory")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    records_dir = root / args.records
    files = sorted(records_dir.rglob("*.yaml")) + sorted(
        records_dir.rglob("*.yml")
    )
    files = sorted(set(files))
    if not files:
        print(f"No records found under {records_dir}")
        return 1
    all_errors: list[str] = []
    for path in files:
        all_errors.extend(check_record(path))
    if all_errors:
        print(f"{len(all_errors)} problem(s) in {len(files)} record(s):")
        for error in all_errors:
            print(f"  - {error}")
        return 1
    print(f"OK: {len(files)} record(s) valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
