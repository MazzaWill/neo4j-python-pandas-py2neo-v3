import unittest

from examples.modern_invoice_graphrag.model import InvoiceRecord, records_from_rows


def sample_row():
    return {
        "发票名称": "山东增值税电子普通发票",
        "机器编号": 499099649091,
        "发票代码": 37001700112,
        "发票号码": 476941,
        "价税合计（小写）": "￥2617.05",
        "收款人": "束曼",
        "复核": "束曼",
        "开票人": "王敏",
    }


class InvoiceRecordTests(unittest.TestCase):
    def test_invoice_record_normalizes_legacy_excel_row(self):
        record = InvoiceRecord.from_row(sample_row(), source_row=2)

        self.assertEqual(record.invoice_name, "山东增值税电子普通发票")
        self.assertEqual(record.invoice_code, "37001700112")
        self.assertEqual(record.invoice_number, "476941")
        self.assertEqual(record.amount, "￥2617.05")
        self.assertEqual(record.payee, "束曼")
        self.assertEqual(record.reviewer, "束曼")
        self.assertEqual(record.drawer, "王敏")
        self.assertEqual(record.source_row, 2)
        self.assertTrue(record.invoice_id.startswith("invoice-"))

    def test_invoice_id_is_stable_for_the_same_business_fields(self):
        first = InvoiceRecord.from_row(sample_row(), source_row=2)
        second = InvoiceRecord.from_row(sample_row(), source_row=99)

        self.assertEqual(first.invoice_id, second.invoice_id)

    def test_search_text_contains_invoice_and_people_context(self):
        record = InvoiceRecord.from_row(sample_row(), source_row=2)

        search_text = record.search_text()

        self.assertIn("山东增值税电子普通发票", search_text)
        self.assertIn("37001700112", search_text)
        self.assertIn("476941", search_text)
        self.assertIn("束曼", search_text)
        self.assertIn("王敏", search_text)

    def test_graph_payload_includes_invoice_properties_people_and_embedding(self):
        record = InvoiceRecord.from_row(sample_row(), source_row=2)

        payload = record.to_graph_payload([0.1, 0.2, 0.3])

        self.assertEqual(payload["invoice"]["invoice_id"], record.invoice_id)
        self.assertEqual(payload["invoice"]["embedding"], [0.1, 0.2, 0.3])
        self.assertEqual(payload["invoice"]["search_text"], record.search_text())
        self.assertIn({"role": "payee", "name": "束曼"}, payload["people"])
        self.assertIn({"role": "reviewer", "name": "束曼"}, payload["people"])
        self.assertIn({"role": "drawer", "name": "王敏"}, payload["people"])

    def test_records_from_rows_preserves_input_order_and_source_rows(self):
        rows = [sample_row(), dict(sample_row(), **{"发票号码": 476942})]

        records = records_from_rows(rows, first_source_row=2)

        self.assertEqual([record.source_row for record in records], [2, 3])
        self.assertEqual(records[0].invoice_number, "476941")
        self.assertEqual(records[1].invoice_number, "476942")


if __name__ == "__main__":
    unittest.main()
