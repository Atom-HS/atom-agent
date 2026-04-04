"""Atom Agent CLI — braco fisico do Atom HS."""

from __future__ import annotations
import typer
from rich.console import Console
from atom_agent.config import config, Config

app = typer.Typer(name="atom-agent", help="Braco fisico do Atom HS — organiza o mundo digital.", no_args_is_help=True)
console = Console()


@app.command()
def init(root: str = typer.Option("C:/AtomDrive", help="AtomDrive root path")) -> None:
    """Setup inicial — cria config e valida conexao."""
    Config.init(root)
    console.print(f"[green]v[/] Config criado em ~/.atom-agent/config.yaml")
    console.print(f"  AtomDrive root: {root}")
    errors = config.validate()
    if errors:
        for e in errors:
            console.print(f"  [red]x[/] {e}")
        console.print("\n[yellow]Edite ~/.atom-agent/config.yaml com suas credenciais[/]")
    else:
        console.print(f"  [green]v[/] Supabase configurado")


@app.command()
def scan(
    path: str = typer.Argument(help="Pasta pra escanear"),
    deep: bool = typer.Option(False, "--deep", help="Recursivo (subpastas)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="So lista, nao move"),
) -> None:
    """Escaneia pasta, classifica, propoe destinos, move com aprovacao."""
    errors = config.validate()
    if errors and not dry_run:
        for e in errors:
            console.print(f"[red]x[/] {e}")
        raise typer.Exit(1)
    from atom_agent.commands.scan import run_scan
    run_scan(path, deep=deep, dry_run=dry_run)


@app.command()
def status() -> None:
    """Resumo do estado do AtomDrive."""
    root = config.atomdrive_root
    if not root.exists():
        console.print(f"[yellow]AtomDrive nao encontrado em {root}[/]")
        console.print("Rode `atom-agent init` pra configurar")
        return
    total_files = sum(1 for _ in root.rglob("*") if _.is_file())
    total_size = sum(f.stat().st_size for f in root.rglob("*") if f.is_file())
    console.print(f"\n[bold]atomdrive[/] {root}")
    console.print(f"  arquivos: {total_files}")
    console.print(f"  tamanho:  {total_size / (1024 * 1024):.1f} MB")
    for d in sorted(root.iterdir()):
        if d.is_dir() and not d.name.startswith("."):
            count = sum(1 for _ in d.rglob("*") if _.is_file())
            if count > 0:
                console.print(f"  {d.name}/: {count} arquivos")


if __name__ == "__main__":
    app()
