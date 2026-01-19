---
name: library-doc
description: Index and search library documentation locally for offline use. Invoke when user asks to index docs, search library topics, or list indexed libraries.
allowed-tools: WebSearch, Bash, Read
user-invocable: true
---

# Library Documentation Indexer

Index library docs locally for fast, offline search.

## Commands

### List indexed libraries

```bash
python3 ./list.py [--json]
```

### Search docs

```bash
python3 ./search.py "<query>" [--library <name>] [--limit <n>] [--json]
```

Examples:
```bash
# First, check what libraries are indexed
python3 ./list.py

# Search all indexed libraries
python3 ./search.py "authentication"

# Search specific library
python3 ./search.py "hooks lifecycle" --library react

# Get more results as JSON
python3 ./search.py "async await" --limit 20 --json
```

### Delete a library

```bash
python3 ./list.py --delete <name>
```

## Indexing a Library

### Step 1: Clarify what to index

Ask the user if ambiguous. "index X docs" could mean:
- A library/framework (e.g., React, FastAPI)
- A web API or spec (e.g., WebSocket API)
- Different implementations across languages

### Step 2: Find docs source

Search: `"<library> documentation github"` or `"<library> docs site:github.com"`

Look for:
- Official repo with `docs/`, `content/`, or `pages/` folder
- Dedicated docs repo (`<lib>-docs`, `<lib>.dev`)
- README-only projects

### Step 3: Identify structure

Determine:
- **Docs path**: `docs/`, `content/`, `src/content/`, etc.
- **File types**: `.md`, `.mdx`
- **Base URL**: Live docs URL for linking (e.g., `https://docs.example.com`)

### Step 4: Clone and index

```bash
cd /tmp && rm -rf <lib>-docs
git clone --depth 1 --filter=blob:none --sparse <repo-url> <lib>-docs
cd <lib>-docs && git sparse-checkout set <docs-path>

find <docs-path> -type f \( -name "*.md" -o -name "*.mdx" \) | while read -r f; do
  cat "$f" | python3 ./index.py <lib> -f "$f" -u "<base-url>/${f%.md}"
done

rm -rf /tmp/<lib>-docs
```

### Step 5: Verify

```bash
python3 ./list.py
python3 ./search.py "getting started" --library <lib>
```

## Examples

### Index a library with docs folder

```bash
cd /tmp && rm -rf <lib>-docs
git clone --depth 1 --filter=blob:none --sparse <repo-url> <lib>-docs
cd <lib>-docs && git sparse-checkout set docs

find docs -type f -name "*.md" | while read -r f; do
  cat "$f" | python3 ./index.py <lib> -f "$f" -u "<base-url>/${f#docs/}"
done

rm -rf /tmp/<lib>-docs
```

### Index a README-only project

```bash
cd /tmp && rm -rf <lib>-repo
git clone --depth 1 <repo-url> <lib>-repo
cat <lib>-repo/README.md | python3 ./index.py <lib> -f "README.md" -u "<repo-url>#readme"
rm -rf /tmp/<lib>-repo
```
