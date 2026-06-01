import unittest
from pathlib import Path

from examples.modern_invoice_graphrag.app import build_parser, read_rows


class AppTests(unittest.TestCase):
    def test_read_rows_loads_csv_sample_with_limit(self):
        rows = read_rows(
            Path("examples/modern_invoice_graphrag/sample_invoice_rows.csv"),
            limit=2,
        )

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["发票名称"], "山东增值税电子普通发票")
        self.assertEqual(rows[1]["发票号码"], "13208805")

    def test_parser_accepts_dry_run_command(self):
        args = build_parser().parse_args(
            [
                "--input",
                "examples/modern_invoice_graphrag/sample_invoice_rows.csv",
                "dry-run",
            ]
        )

        self.assertEqual(args.command, "dry-run")
        self.assertEqual(args.input, "examples/modern_invoice_graphrag/sample_invoice_rows.csv")


if __name__ == "__main__":
    unittest.main()
