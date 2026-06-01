import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path("skills/neo4j-knowledge-graph/scripts/profile_table.py")


def load_profile_module():
    spec = importlib.util.spec_from_file_location("profile_table", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ProfileTableTests(unittest.TestCase):
    def test_profile_rows_detects_likely_identifiers_and_samples(self):
        module = load_profile_module()
        rows = [
            {"invoice_code": "A001", "payee": "Alice", "amount": "10"},
            {"invoice_code": "A002", "payee": "Bob", "amount": "20"},
            {"invoice_code": "A003", "payee": "Alice", "amount": ""},
        ]

        profile = module.profile_rows(rows)

        self.assertEqual(profile["row_count"], 3)
        self.assertEqual(profile["column_count"], 3)
        invoice_code = next(column for column in profile["columns"] if column["name"] == "invoice_code")
        payee = next(column for column in profile["columns"] if column["name"] == "payee")
        amount = next(column for column in profile["columns"] if column["name"] == "amount")
        self.assertTrue(invoice_code["likely_identifier"])
        self.assertFalse(payee["likely_identifier"])
        self.assertFalse(amount["likely_identifier"])
        self.assertEqual(amount["blank_count"], 1)
        self.assertEqual(invoice_code["sample_values"], ["A001", "A002", "A003"])

    def test_profile_script_outputs_json_for_csv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "invoices.csv"
            csv_path.write_text("发票代码,收款人\n37001700112,束曼\n42001700112,戴宗鸿\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), str(csv_path), "--limit", "1"],
                check=True,
                text=True,
                capture_output=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(payload["row_count"], 1)
        self.assertEqual(payload["columns"][0]["name"], "发票代码")
        self.assertTrue(payload["columns"][0]["likely_identifier"])


if __name__ == "__main__":
    unittest.main()
