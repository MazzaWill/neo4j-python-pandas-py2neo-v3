"""Invoice row normalization for the modern Neo4j example."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from typing import Any, Dict, Iterable, List, Mapping


def _clean(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value):
            return ""
        if value.is_integer():
            return str(int(value))
    return str(value).strip()


def _pick(row: Mapping[str, Any], *names: str) -> str:
    for name in names:
        if name in row:
            cleaned = _clean(row[name])
            if cleaned:
                return cleaned
    return ""


def _stable_invoice_id(invoice_name: str, invoice_code: str, invoice_number: str, source_row: int) -> str:
    identity = "|".join(
        part for part in [invoice_code, invoice_number, invoice_name] if part
    )
    if not identity:
        identity = "row:%s" % source_row
    digest = hashlib.sha1(identity.encode("utf-8")).hexdigest()[:16]
    return "invoice-%s" % digest


@dataclass(frozen=True)
class InvoiceRecord:
    invoice_id: str
    invoice_name: str
    machine_code: str
    invoice_code: str
    invoice_number: str
    amount: str
    payee: str
    reviewer: str
    drawer: str
    source_row: int
    raw: Dict[str, str]

    @classmethod
    def from_row(cls, row: Mapping[str, Any], source_row: int) -> "InvoiceRecord":
        normalized = {str(key): _clean(value) for key, value in row.items()}
        invoice_name = _pick(normalized, "发票名称", "invoice_name", "Invoice Name")
        invoice_code = _pick(normalized, "发票代码", "invoice_code", "Invoice Code")
        invoice_number = _pick(normalized, "发票号码", "invoice_number", "Invoice Number")
        return cls(
            invoice_id=_stable_invoice_id(invoice_name, invoice_code, invoice_number, source_row),
            invoice_name=invoice_name,
            machine_code=_pick(normalized, "机器编号", "machine_code", "Machine Code"),
            invoice_code=invoice_code,
            invoice_number=invoice_number,
            amount=_pick(normalized, "价税合计（小写）", "价税合计(小写)", "amount", "Amount"),
            payee=_pick(normalized, "收款人", "payee", "Payee"),
            reviewer=_pick(normalized, "复核", "reviewer", "Reviewer"),
            drawer=_pick(normalized, "开票人", "drawer", "Drawer"),
            source_row=source_row,
            raw=normalized,
        )

    def search_text(self) -> str:
        parts = [
            "invoice name: %s" % self.invoice_name,
            "invoice code: %s" % self.invoice_code,
            "invoice number: %s" % self.invoice_number,
            "machine code: %s" % self.machine_code,
            "amount: %s" % self.amount,
            "payee: %s" % self.payee,
            "reviewer: %s" % self.reviewer,
            "drawer: %s" % self.drawer,
            "source row: %s" % self.source_row,
        ]
        return " | ".join(part for part in parts if not part.endswith(": "))

    def people(self) -> List[Dict[str, str]]:
        people = []
        for role, name in [
            ("payee", self.payee),
            ("reviewer", self.reviewer),
            ("drawer", self.drawer),
        ]:
            if name:
                people.append({"role": role, "name": name})
        return people

    def to_graph_payload(self, embedding: List[float]) -> Dict[str, Any]:
        return {
            "invoice": {
                "invoice_id": self.invoice_id,
                "invoice_name": self.invoice_name,
                "machine_code": self.machine_code,
                "invoice_code": self.invoice_code,
                "invoice_number": self.invoice_number,
                "amount": self.amount,
                "source_row": self.source_row,
                "search_text": self.search_text(),
                "embedding": embedding,
            },
            "people": self.people(),
        }


def records_from_rows(rows: Iterable[Mapping[str, Any]], first_source_row: int = 2) -> List[InvoiceRecord]:
    return [
        InvoiceRecord.from_row(row, source_row=first_source_row + index)
        for index, row in enumerate(rows)
    ]
