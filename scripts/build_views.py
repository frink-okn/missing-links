"""Build the views in docs/ from the records in records/.

Reads every record, then writes two static pages:

- docs/index.html — a list of every record, with its status.
- docs/matrix.html — a cross-graph matrix: one row and one column
  per graph, each cell naming the records for that pair, or empty
  when no record exists for that pair.

Usage:
    python3 scripts/build_views.py [--records records] [--out docs]

No network calls. Python standard library plus PyYAML.
"""

from __future__ import annotations

import argparse
import html
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    import sys

    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

STATUS_LABEL = {
    "open": "open",
    "under_review": "under review",
    "accepted": "accepted",
    "rejected": "rejected",
}


def load_records(records_dir: Path) -> list[dict]:
    files = sorted(set(records_dir.rglob("*.yaml")) | set(records_dir.rglob("*.yml")))
    records = []
    for path in files:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data["_file"] = str(path.relative_to(records_dir.parent))
            records.append(data)
    return sorted(records, key=lambda r: str(r.get("id", "")))


def page(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — missing-links</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ccc; padding: 0.4rem 0.6rem; text-align: left; vertical-align: top; }}
th {{ background: #f2f2f2; }}
code {{ background: #f2f2f2; padding: 0.1rem 0.3rem; }}
</style>
</head>
<body>
<h1>missing-links</h1>
<p><a href="index.html">Records</a> · <a href="matrix.html">Cross-graph matrix</a></p>
<h2>{html.escape(title)}</h2>
{body}
</body>
</html>
"""


def build_index(records: list[dict]) -> str:
    rows = []
    for r in records:
        graphs = ", ".join(str(g.get("graph", "")) for g in r.get("graphs") or [])
        status = STATUS_LABEL.get(str(r.get("status", "")), str(r.get("status", "")))
        rows.append(
            "<tr><td><code>{}</code></td><td>{}</td><td>{}</td>"
            "<td>{}</td><td>{}</td><td>{}</td></tr>".format(
                html.escape(str(r.get("id", ""))),
                html.escape(str(r.get("title", ""))),
                html.escape(str(r.get("identifier_type", ""))),
                html.escape(graphs),
                html.escape(str(r.get("proposed_standard_namespace", ""))),
                html.escape(status),
            )
        )
    body = (
        f"<p>{len(records)} record(s). A record is a draft until a reviewer "
        "accepts it. Status shows where each one stands.</p>"
        "<table><tr><th>Id</th><th>Title</th><th>Identifier</th>"
        "<th>Graphs</th><th>Proposed standard</th><th>Status</th></tr>"
        + "".join(rows)
        + "</table>"
    )
    return page("Records", body)


def build_matrix(records: list[dict]) -> str:
    graphs = sorted(
        {str(g.get("graph", "")) for r in records for g in (r.get("graphs") or [])}
    )
    by_pair: dict[tuple[str, str], list[dict]] = {}
    for r in records:
        names = sorted(str(g.get("graph", "")) for g in (r.get("graphs") or []))
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                by_pair.setdefault((a, b), []).append(r)
    header = "<tr><th></th>" + "".join(
        f"<th>{html.escape(g)}</th>" for g in graphs
    ) + "</tr>"
    rows = []
    for a in graphs:
        cells = [f"<th>{html.escape(a)}</th>"]
        for b in graphs:
            if a == b:
                cells.append("<td>—</td>")
                continue
            key = tuple(sorted((a, b)))
            pair_records = by_pair.get(key, [])
            if not pair_records:
                cells.append("<td></td>")
            else:
                cell = "<br>".join(
                    "<code>{}</code> ({})".format(
                        html.escape(str(r.get("id", ""))),
                        html.escape(
                            STATUS_LABEL.get(
                                str(r.get("status", "")), str(r.get("status", ""))
                            )
                        ),
                    )
                    for r in pair_records
                )
                cells.append(f"<td>{cell}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    body = (
        "<p>One cell per pair of graphs. A cell names the records for "
        "that pair, with their status. An empty cell means no record "
        "exists for that pair yet.</p>"
        "<table>" + header + "".join(rows) + "</table>"
    )
    return page("Cross-graph matrix", body)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build missing-links views.")
    parser.add_argument("--records", default="records")
    parser.add_argument("--out", default="docs")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    records = load_records(root / args.records)
    out = root / args.out
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(build_index(records), encoding="utf-8")
    (out / "matrix.html").write_text(build_matrix(records), encoding="utf-8")
    print(f"Wrote {len(records)} record(s) to {out / 'index.html'} and {out / 'matrix.html'}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
