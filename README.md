<p align="center">
  <code>·  —  △  □  ⬠  ⬡  ○</code>
  <br/><br/>
  <strong>Atom Agent</strong>
  <br/>
  <sub>The physical arm of Atom HS — filesystem scanner, classifier, organizer.</sub>
</p>

---

## What is this

A Python CLI that scans your local filesystem, classifies files by extension and name patterns, renames them following the Genesis naming convention, and moves them to an organized folder structure (AtomDrive). Every processed file becomes an indexed item in Supabase — visible in MindRoot.

Part of the [Atom](https://github.com/rsmramalho) ecosystem.

## Install

```bash
pip install -e .
```

## Setup

```bash
atom-agent init --root C:/AtomDrive
# Edit ~/.atom-agent/config.yaml with your Supabase credentials
```

## Usage

```bash
atom-agent scan ~/Downloads          # Scan folder, propose moves
atom-agent scan ~/Downloads --deep   # Recursive scan
atom-agent scan ~/Downloads --dry-run  # List only, don't move
atom-agent status                    # AtomDrive summary
```

## How it works

```
scan folder → hash (SHA-256) → dedup check → classify → rename → propose
                                                                    ↓
                                                           human approves
                                                                    ↓
                                                    move → index in Supabase → commit
```

Files enter the Genesis pipeline at stage 1 (inbox) and are committed at stage 7 after physical move.

## Classification

| Extension | Type | Module | Confidence |
|-----------|------|--------|------------|
| .pdf | resource | bridge | 70% |
| .jpg/.jpeg/.heic | resource | family | 75% |
| .xlsx/.csv | resource | finance | 70% |
| .docx | doc | work | 65% |
| .exe/.tmp/.cache | trash | — | 95% |

Name patterns boost confidence: `invoice` → finance, `passport` → bridge+vital-doc, `IMG_` → family.

## Architecture

```
src/atom_agent/
├── cli.py              Entry point (Typer)
├── config.py            ~/.atom-agent/config.yaml
├── supabase_client.py   CRUD items + body.locations
├── core/
│   ├── hasher.py        SHA-256 streaming
│   ├── classifier.py    Extension + name rules
│   ├── namer.py         Genesis §8.4 naming
│   ├── mover.py         Physical move + integrity
│   └── dedup.py         Hash duplicate check
├── scanners/
│   └── filesystem.py    Local folder scanner
└── commands/
    └── scan.py          Scan orchestration
```

## Related

| Repo | Role |
|------|------|
| [mindroot-v2](https://github.com/rsmramalho/mindroot-v2) | Web/mobile interface |
| [atom-hs/atom-engine](https://github.com/atom-hs/atom-engine) | Protocol, schema, specs |
| Supabase | Shared data layer |

---

<sub>Part of the <a href="https://github.com/rsmramalho">Atom</a> ecosystem — Human Systems.</sub>
