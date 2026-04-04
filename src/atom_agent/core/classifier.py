"""File classifier — rules by extension + name patterns + confidence bands."""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from pathlib import Path
from atom_agent.config import AUTO_TRASH_EXTENSIONS


@dataclass
class Classification:
    atom_type: str
    module: str
    domain: str
    tags: list[str] = field(default_factory=list)
    is_trash: bool = False
    confidence: float = 0.5
    reasoning: str = ""


_NAME_RULES: list[tuple[str, str, str, list[str], str]] = [
    (r"invoice|fatura|receipt|recibo|nota.?fiscal", "finance", "finance", ["#domain:finance"], "financial document"),
    (r"passport|passaporte|visa|certid[aã]o|birth.?cert", "bridge", "documents", ["#domain:documents", "#vital-doc"], "vital identity document"),
    (r"contract|contrato|lease|acordo", "bridge", "documents", ["#domain:documents", "#vital-doc"], "legal contract"),
    (r"resume|curricul|cv[_\s\-]", "work", "documents", ["#domain:documents"], "resume/CV"),
    (r"IMG_|DSC_|photo|foto", "family", "memories", ["#domain:memories"], "photo (name pattern)"),
    (r"screenshot|Screen.?Shot|Captura|print.?screen", "bridge", "storage", ["#domain:storage"], "screenshot"),
    (r"recipe|receita(?!.*m[eé]dic)", "body", "storage", ["#domain:storage"], "recipe (culinary)"),
    (r"prescri[pç]|receita.?m[eé]dic", "body", "health", ["#domain:health"], "medical prescription"),
]

_EXT_DEFAULTS: dict[str, tuple[str, str, str, float]] = {
    ".pdf": ("resource", "bridge", "documents", 0.70),
    ".jpg": ("resource", "family", "memories", 0.75),
    ".jpeg": ("resource", "family", "memories", 0.75),
    ".png": ("resource", "bridge", "storage", 0.65),
    ".heic": ("resource", "family", "memories", 0.75),
    ".webp": ("resource", "bridge", "storage", 0.65),
    ".mp4": ("resource", "family", "memories", 0.75),
    ".mov": ("resource", "family", "memories", 0.75),
    ".avi": ("resource", "family", "memories", 0.70),
    ".xlsx": ("resource", "finance", "finance", 0.70),
    ".xls": ("resource", "finance", "finance", 0.70),
    ".csv": ("resource", "finance", "finance", 0.65),
    ".docx": ("doc", "work", "documents", 0.65),
    ".doc": ("doc", "work", "documents", 0.65),
    ".pptx": ("doc", "work", "documents", 0.70),
    ".md": ("note", "mind", "storage", 0.60),
    ".txt": ("note", "mind", "storage", 0.55),
    ".zip": ("resource", "bridge", "storage", 0.50),
    ".rar": ("resource", "bridge", "storage", 0.50),
    ".7z": ("resource", "bridge", "storage", 0.50),
}


def classify(path: Path) -> Classification:
    ext = path.suffix.lower()
    name = path.stem.lower()

    if ext in AUTO_TRASH_EXTENSIONS:
        return Classification(atom_type="trash", module="", domain="", is_trash=True, confidence=0.95, reasoning=f"auto-trash: {ext}")

    for pattern, module, domain, extra_tags, reason in _NAME_RULES:
        if re.search(pattern, name, re.IGNORECASE):
            base_type, _, _, base_conf = _EXT_DEFAULTS.get(ext, ("resource", "bridge", "storage", 0.60))
            return Classification(
                atom_type=base_type, module=module, domain=domain,
                tags=["#connector", "#source:atom-agent"] + extra_tags,
                confidence=min(base_conf + 0.20, 0.95), reasoning=reason,
            )

    if ext in _EXT_DEFAULTS:
        typ, mod, dom, conf = _EXT_DEFAULTS[ext]
        return Classification(
            atom_type=typ, module=mod, domain=dom,
            tags=["#connector", "#source:atom-agent", f"#domain:{dom}"],
            confidence=conf, reasoning=f"extension: {ext}",
        )

    return Classification(
        atom_type="resource", module="bridge", domain="storage",
        tags=["#connector", "#source:atom-agent", "#domain:storage", "#needs-triage"],
        confidence=0.30, reasoning=f"unknown: {ext}",
    )
