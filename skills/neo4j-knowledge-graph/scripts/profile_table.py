#!/usr/bin/env python3
"""Profile CSV or Excel tables before designing a Neo4j graph."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


def clean(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    return str(value).strip()


def read_rows(path: Path, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    elif suffix in {".xls", ".xlsx"}:
        try:
            import pandas as pd
        except ImportError as exc:
            raise SystemExit(
                "Excel profiling requires pandas plus xlrd/openpyxl. "
                "Install them or export the sheet to CSV."
            ) from exc
        rows = pd.read_excel(path, dtype=object).fillna("").to_dict("records")
    else:
        raise SystemExit("Unsupported file type: %s" % path.suffix)
    return rows[:limit] if limit is not None else rows


def infer_likely_id(name: str, values: Iterable[str], row_count: int) -> bool:
    lowered = name.lower()
    if any(token in lowered for token in ["id", "code", "number", "编号", "代码", "号码"]):
        return True
    if any(token in lowered for token in ["amount", "price", "total", "金额", "合计", "价税"]):
        return False
    non_blank = [value for value in values if value]
    if row_count < 20:
        return False
    return bool(non_blank) and len(set(non_blank)) == len(non_blank) and len(non_blank) >= int(row_count * 0.9)


def profile_rows(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    columns = list(rows[0].keys()) if rows else []
    column_profiles = []
    for column in columns:
        values = [clean(row.get(column)) for row in rows]
        non_blank = [value for value in values if value]
        samples = []
        for value in non_blank:
            if value not in samples:
                samples.append(value)
            if len(samples) == 5:
                break
        column_profiles.append(
            {
                "name": column,
                "blank_count": len(values) - len(non_blank),
                "distinct_count": len(set(non_blank)),
                "sample_values": samples,
                "likely_identifier": infer_likely_id(column, values, len(rows)),
            }
        )
    return {
        "row_count": len(rows),
        "column_count": len(columns),
        "columns": column_profiles,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Profile a CSV or Excel file for Neo4j graph modeling")
    parser.add_argument("path", help="CSV, XLS, or XLSX file to profile")
    parser.add_argument("--limit", type=int, default=200, help="Maximum rows to inspect")
    parser.add_argument("--indent", type=int, default=2, help="JSON indentation")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    rows = read_rows(Path(args.path), limit=args.limit)
    print(json.dumps(profile_rows(rows), ensure_ascii=False, indent=args.indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
