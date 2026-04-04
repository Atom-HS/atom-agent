from pathlib import Path
from datetime import datetime
from atom_agent.core.classifier import classify
from atom_agent.core.namer import generate_name, generate_destination


def test_invoice_naming():
    path = Path("invoice_atlas.pdf")
    c = classify(path)
    name = generate_name(path, c, datetime(2026, 4, 5))
    assert name.startswith("mod-finance_")
    assert "resource" in name
    assert "2026-04-05" in name
    assert name.endswith(".pdf")


def test_trash_keeps_original_name():
    path = Path("setup.exe")
    c = classify(path)
    name = generate_name(path, c)
    assert name == "setup.exe"


def test_destination_vital_doc():
    path = Path("passaporte_scan.pdf")
    c = classify(path)
    dest = generate_destination(c)
    assert dest == "mod-bridge/documents/"


def test_destination_finance():
    path = Path("gastos.xlsx")
    c = classify(path)
    dest = generate_destination(c)
    assert dest.startswith("mod-finance")
