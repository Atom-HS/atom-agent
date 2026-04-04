from pathlib import Path
from atom_agent.core.classifier import classify


def test_pdf_default():
    c = classify(Path("document.pdf"))
    assert c.atom_type == "resource"
    assert c.module == "bridge"
    assert not c.is_trash


def test_exe_is_trash():
    c = classify(Path("setup.exe"))
    assert c.is_trash
    assert c.confidence >= 0.95


def test_tmp_is_trash():
    c = classify(Path("data.tmp"))
    assert c.is_trash


def test_invoice_is_finance():
    c = classify(Path("invoice_atlas_apr.pdf"))
    assert c.module == "finance"
    assert "#domain:finance" in c.tags
    assert c.confidence > 0.70


def test_passport_is_vital():
    c = classify(Path("passaporte_scan.pdf"))
    assert c.module == "bridge"
    assert "#vital-doc" in c.tags
    assert "#domain:documents" in c.tags


def test_photo_is_family():
    c = classify(Path("IMG_20240315.jpg"))
    assert c.module == "family"
    assert "#domain:memories" in c.tags


def test_xlsx_is_finance():
    c = classify(Path("gastos_2024.xlsx"))
    assert c.module == "finance"


def test_unknown_extension():
    c = classify(Path("mystery.xyz"))
    assert c.module == "bridge"
    assert c.confidence < 0.5
    assert "#needs-triage" in c.tags
