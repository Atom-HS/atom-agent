"""Configuration loader — reads ~/.atom-agent/config.yaml or env vars."""

import os
from pathlib import Path
from typing import Optional

import yaml
from dotenv import load_dotenv

load_dotenv()

CONFIG_DIR = Path.home() / ".atom-agent"
CONFIG_FILE = CONFIG_DIR / "config.yaml"

AUTO_TRASH_EXTENSIONS = frozenset({
    ".tmp", ".cache", ".crdownload", ".part",
    ".exe", ".msi", ".dmg", ".pkg",
})

IGNORE_FILES = frozenset({".DS_Store", "Thumbs.db", "desktop.ini", ".gitkeep"})


class Config:
    def __init__(self) -> None:
        self._data: dict = {}
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                self._data = yaml.safe_load(f) or {}

    @property
    def supabase_url(self) -> str:
        return self._data.get("supabase", {}).get("url") or os.environ.get("SUPABASE_URL", "")

    @property
    def supabase_key(self) -> str:
        return self._data.get("supabase", {}).get("service_key") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

    @property
    def user_id(self) -> str:
        return self._data.get("supabase", {}).get("user_id") or os.environ.get("USER_ID", "")

    @property
    def atomdrive_root(self) -> Path:
        raw = self._data.get("atomdrive", {}).get("root") or os.environ.get("ATOM_DRIVE_ROOT", "C:/AtomDrive")
        return Path(raw)

    @property
    def auto_approve_threshold(self) -> int:
        return self._data.get("scan", {}).get("auto_approve_threshold", 95)

    def validate(self) -> list[str]:
        errors = []
        if not self.supabase_url: errors.append("SUPABASE_URL not configured")
        if not self.supabase_key: errors.append("SUPABASE_SERVICE_ROLE_KEY not configured")
        if not self.user_id: errors.append("USER_ID not configured")
        return errors

    @staticmethod
    def init(root: str) -> None:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        initial = {
            "supabase": {
                "url": os.environ.get("SUPABASE_URL", "https://avvwjkzkzklloyfugzer.supabase.co"),
                "service_key": os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "REPLACE_ME"),
                "user_id": os.environ.get("USER_ID", "acc24249-ad6d-4378-a382-e1fbbcdec1d2"),
            },
            "atomdrive": {"root": root},
            "scan": {"auto_trash_extensions": list(AUTO_TRASH_EXTENSIONS), "auto_approve_threshold": 95},
        }
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(initial, f, default_flow_style=False)


config = Config()
