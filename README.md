# Library Documentation Indexer

Index and search library documentation locally for fast, offline access in Claude Code.

## Features

- **Full-text search** with FTS5 (title boosting, prefix matching, multi-word queries)
- **Offline access** to indexed docs - no network latency
- **Version support** - index multiple versions of the same library (e.g., `nextjs`, `nextjs-15`)
- **Sparse checkout** - only downloads docs files, not entire repos
- **URL linking** - preserved links to original documentation
- **59 library presets** - pre-configured repos/paths for popular libraries
- **Auto-chunking** - large docs split by headings for better search

## Requirements

- Python 3.9+

## Installation

```bash
git clone https://github.com/um1b/library-docs.git ~/.claude/skills/library-docs
```

## Update

```bash
git -C ~/.claude/skills/library-docs pull
```

## Usage

Use the `/library-doc` skill in Claude Code:

```
/library-doc index bun          # Index Bun documentation
/library-doc search "FFI"       # Search all libraries
/library-doc list               # List indexed libraries
```

Or just ask naturally: "index the React docs", "search for authentication in nextjs".

## Presets

59 popular libraries have pre-configured repo URLs and doc paths:

```bash
python3 ./scripts/presets.py list           # Show all presets
python3 ./scripts/presets.py show nextjs    # Show preset details
```

**Frontend**: react, nextjs, vue, svelte, nuxt, angular, astro, remix, solid
**CSS/UI**: tailwind, shadcn
**Backend**: express, fastapi, django, flask, hono, nestjs, rails, laravel
**Runtimes**: bun, node, deno
**Languages**: typescript, python, rust, go
**Databases**: prisma, drizzle, supabase, mongodb, sqlalchemy
**State**: redux, zustand, tanstack-query, jotai
**Testing**: vitest, playwright, jest, pytest, cypress
**Build**: vite, esbuild, webpack, turbo
**AI/ML**: langchain, openai, anthropic, huggingface
**DevOps**: docker, kubernetes, terraform

## Commands

| Command | Description |
|---------|-------------|
| `python3 ./scripts/list.py` | List all indexed libraries |
| `python3 ./scripts/list.py <library>` | List documents in a library |
| `python3 ./scripts/list.py --delete <name>` | Delete a library |
| `python3 ./scripts/search.py "<query>"` | Search all libraries |
| `python3 ./scripts/search.py "<query>" --library <name>` | Search specific library |
| `python3 ./scripts/read.py <library> <id\|path\|title>` | Read full document |
| `python3 ./scripts/presets.py list` | List all presets |
| `python3 ./scripts/presets.py show <name>` | Show preset details |

## Architecture

```
library-docs/
├── scripts/
│   ├── db.py        # SQLite + FTS5 database layer
│   ├── index.py     # Batch/single file indexer (with auto-chunking)
│   ├── search.py    # Full-text search CLI
│   ├── list.py      # List libraries/documents
│   ├── read.py      # Read full document content
│   └── presets.py   # 59 library presets (repos, paths, URLs)
├── SKILL.md         # Claude Code skill definition
├── README.md
└── data/
    └── library.db   # SQLite database (created on first use)
```

## How It Works

1. **Indexing**: Clones docs from GitHub using sparse checkout (docs folder only), extracts titles from markdown frontmatter/headings, stores content in SQLite with FTS5 indexing
2. **Searching**: Uses BM25 ranking with title boosting (10x weight), supports prefix matching (`auth*`) and multi-word OR queries
3. **Reading**: Retrieves full document by ID, path, or exact title match

## Example Workflow

```bash
# 1. Index a library
/library-doc index bun

# 2. Search for a topic
python3 ./scripts/search.py "websocket" --library bun
# Returns: title, URL, snippet with highlighted matches

# 3. Read the full document
python3 ./scripts/read.py bun "WebSockets"
# Returns: complete markdown content

# 4. Read specific lines (for long docs)
python3 ./scripts/read.py bun "WebSockets" --lines 1-100
```

## CLAUDE.md Configuration

Add to `~/.claude/CLAUDE.md` for automatic doc lookups:

```
When working with a library (writing code, configuring, integrating, or troubleshooting), use the library-doc skill to search indexed documentation first. This helps you:
- Use current APIs instead of outdated patterns
- Find correct configuration options and defaults
- Understand library-specific conventions and best practices
- Debug errors by checking if behavior matches documented expectations
```
