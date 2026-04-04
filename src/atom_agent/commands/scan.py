"""Scan command — orchestrates scan -> classify -> propose -> approve -> move -> index."""

from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from rich.console import Console
from rich.table import Table
from atom_agent.config import config
from atom_agent.scanners.filesystem import scan_folder, ScanResult
from atom_agent.core.mover import move_file
from atom_agent.supabase_client import create_item, commit_item

console = Console()


def run_scan(source: str, deep: bool = False, dry_run: bool = False) -> None:
    source_path = Path(source).resolve()
    console.print(f"\n[bold]scanning[/] {source_path}" + (" (deep)" if deep else ""))
    console.print()

    try:
        results = scan_folder(source_path, deep)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]error:[/] {e}")
        return

    if not results:
        console.print("[dim]no files found[/]")
        return

    moves = [r for r in results if r.action == "move"]
    trash = [r for r in results if r.action == "trash"]
    dups = [r for r in results if r.action == "duplicate"]
    manual = [r for r in results if r.action == "manual"]

    console.print(f"[bold]=== resumo ===[/]")
    console.print(f"  mover:      [green]{len(moves)}[/]")
    console.print(f"  lixo:       [yellow]{len(trash)}[/]")
    console.print(f"  duplicata:  [dim]{len(dups)}[/]")
    console.print(f"  manual:     [red]{len(manual)}[/]")
    console.print()

    if moves:
        table = Table(show_header=True, header_style="bold")
        table.add_column("arquivo", style="dim", max_width=30)
        table.add_column("destino", max_width=40)
        table.add_column("conf", justify="right", width=5)
        table.add_column("motivo", style="dim", max_width=25)
        for r in moves:
            color = "green" if r.confidence >= 0.8 else "yellow" if r.confidence >= 0.6 else "red"
            table.add_row(r.proposed_title[:30], f"{r.proposed_destination}{r.proposed_filename}"[:40],
                          f"[{color}]{r.confidence:.0%}[/{color}]", r.reasoning[:25])
        console.print(table)
        console.print()

    if dry_run:
        console.print("[dim]dry run — nada foi movido[/]")
        return

    if not moves and not trash and not dups:
        console.print("[dim]nada pra processar[/]")
        return

    answer = console.input("[bold]aprovar?[/] [A]ll / [N]one: ").strip().lower()
    if answer not in ("a", "all"):
        console.print("[dim]cancelado[/]")
        return

    root = config.atomdrive_root
    processed = 0

    for r in moves:
        try:
            dest = root / r.proposed_destination / r.proposed_filename
            now = datetime.now(timezone.utc).isoformat()
            item_id = create_item(
                title=r.proposed_title, atom_type=r.proposed_type, module=r.proposed_module,
                tags=r.proposed_tags, naming=r.proposed_filename,
                body={"hash": r.file_hash, "mime": r.mime, "size": r.size, "original_path": r.original_path,
                      "locations": [{"service": "local", "root": str(root),
                                     "path": f"{r.proposed_destination}{r.proposed_filename}",
                                     "role": "primary", "synced_at": now}]},
            )
            move_file(Path(r.original_path), dest, r.file_hash)
            commit_item(item_id)
            console.print(f"  [green]v[/] {r.proposed_title[:30]} -> {r.proposed_destination}")
            processed += 1
        except Exception as e:
            console.print(f"  [red]x[/] {r.proposed_title[:30]}: {e}")

    trash_dir = root / "lixo" / "trash"
    dup_dir = root / "lixo" / "duplicatas"

    for r in trash:
        try:
            dest = trash_dir / r.proposed_title
            move_file(Path(r.original_path), dest, r.file_hash)
            console.print(f"  [yellow]trash[/] {r.proposed_title[:30]}")
        except Exception as e:
            console.print(f"  [red]x[/] trash {r.proposed_title[:30]}: {e}")

    for r in dups:
        try:
            dest = dup_dir / r.proposed_title
            move_file(Path(r.original_path), dest, r.file_hash)
            console.print(f"  [dim]dup[/] {r.proposed_title[:30]}")
        except Exception as e:
            console.print(f"  [red]x[/] dup {r.proposed_title[:30]}: {e}")

    console.print(f"\n[bold]o[/] {processed} movidos. {len(trash) + len(dups)} descartados.")
