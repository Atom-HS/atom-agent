"""Supabase client — CRUD for items with body.locations."""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Optional
from supabase import create_client, Client
from atom_agent.config import config

_client: Optional[Client] = None


def get_client() -> Client:
    global _client
    if _client is None:
        url = config.supabase_url
        key = config.supabase_key
        if not url or not key:
            raise RuntimeError("Supabase not configured. Run `atom-agent init` or set env vars.")
        _client = create_client(url, key)
    return _client


def check_duplicate(file_hash: str) -> Optional[str]:
    client = get_client()
    result = client.table("items").select("id, body").eq("user_id", config.user_id).execute()
    for row in result.data or []:
        body = row.get("body") or {}
        if isinstance(body, dict) and body.get("hash") == file_hash:
            return row["id"]
    return None


def create_item(title: str, atom_type: str, module: str, tags: list[str], naming: str, body: dict[str, Any]) -> str:
    client = get_client()
    now = datetime.now(timezone.utc).isoformat()
    row = {
        "user_id": config.user_id, "title": title, "type": atom_type, "module": module,
        "tags": tags, "status": "inbox", "state": "inbox", "genesis_stage": 1,
        "source": "atom-agent", "naming_convention": naming, "body": body,
        "created_at": now, "updated_at": now,
    }
    result = client.table("items").insert(row).execute()
    if not result.data:
        raise RuntimeError(f"Insert failed: {result}")
    return result.data[0]["id"]


def commit_item(item_id: str) -> None:
    client = get_client()
    now = datetime.now(timezone.utc).isoformat()
    client.table("items").update({
        "state": "committed", "genesis_stage": 7, "status": "completed", "updated_at": now,
    }).eq("id", item_id).execute()
