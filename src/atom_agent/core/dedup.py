"""Deduplication — check hash against Supabase items."""

from __future__ import annotations
from typing import Optional
from atom_agent.supabase_client import check_duplicate


def is_duplicate(file_hash: str) -> tuple[bool, Optional[str]]:
    existing_id = check_duplicate(file_hash)
    return (existing_id is not None, existing_id)
