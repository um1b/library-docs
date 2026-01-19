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

### List documents in a library

```bash
python3 ./list.py <library> [--json]
```

### Search docs

```bash
python3 ./search.py "<query>" [--library <name>] [--limit <n>] [--json]
```

### Delete a library

```bash
python3 ./list.py --delete <name>
```

### Examples

```bash
# List all indexed libraries
python3 ./list.py

# List all documents in a library
python3 ./list.py nextjs

# Search all indexed libraries
python3 ./search.py "authentication"

# Search specific library
python3 ./search.py "server components" --library nextjs

# Get more results as JSON
python3 ./search.py "async await" --limit 20 --json
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

**For specific versions:** Check the repo's releases/tags page. Common tag patterns:
- `v15.0.0`, `v15.1.0` (semantic versioning)
- `15.x`, `v15` (major version branches)
- `docs-v15`, `release-15.0` (alternative patterns)

### Step 3: Identify structure

Determine:
- **Docs path**: `docs/`, `content/`, `src/content/`, etc.
- **File types**: `.md`, `.mdx`
- **Base URL**: Live docs URL for linking (e.g., `https://docs.example.com`)

### Step 4: Clone and index

**Naming convention:**
- `nextjs` - latest/default version
- `nextjs-15` - specific major version
- `python-3.12` - specific minor version (when relevant)

```bash
cd /tmp && rm -rf <lib>-docs

# For latest version:
git clone --depth 1 --filter=blob:none --sparse <repo-url> <lib>-docs

# For specific version (use --branch with tag):
git clone --branch <tag> --depth 1 --filter=blob:none --sparse <repo-url> <lib>-docs

cd <lib>-docs && git sparse-checkout set <docs-path>

# Check if docs exist before indexing
count=$(find <docs-path> -type f \( -name "*.md" -o -name "*.mdx" \) | wc -l)
if [ "$count" -eq 0 ]; then
  echo "Error: No docs found in <docs-path>. Check the path or file types."
  exit 1
fi

find <docs-path> -type f \( -name "*.md" -o -name "*.mdx" \) | \
  python3 ./index.py <lib> --batch --base-url "<base-url>" --strip-prefix "<docs-path>/"

rm -rf /tmp/<lib>-docs
```

### Step 5: Verify

```bash
python3 ./list.py <lib>
```

If the library shows 0 docs or not found, check:
- Docs path is correct
- File extensions match (`.md`, `.mdx`, `.rst`)
- Sparse checkout succeeded

## Examples

### Index a library with docs folder

```bash
cd /tmp && rm -rf <lib>-docs
git clone --depth 1 --filter=blob:none --sparse <repo-url> <lib>-docs
cd <lib>-docs && git sparse-checkout set docs

find docs -type f -name "*.md" | \
  python3 ./index.py <lib> --batch --base-url "<base-url>" --strip-prefix "docs/"

rm -rf /tmp/<lib>-docs

# Verify
python3 ./list.py <lib>
```

### Index a README-only project

```bash
cd /tmp && rm -rf <lib>-repo
git clone --depth 1 <repo-url> <lib>-repo
cat <lib>-repo/README.md | python3 ./index.py <lib> -f "README.md" -u "<repo-url>#readme"
rm -rf /tmp/<lib>-repo

# Verify
python3 ./list.py <lib>
```

### Index a specific version

```bash
cd /tmp && rm -rf nextjs-docs

# Clone Next.js v15 docs
git clone --branch v15.0.0 --depth 1 --filter=blob:none --sparse \
  https://github.com/vercel/next.js.git nextjs-docs
cd nextjs-docs && git sparse-checkout set docs

find docs -type f -name "*.mdx" | \
  python3 ./index.py nextjs-15 --batch --base-url "https://nextjs.org/docs" --strip-prefix "docs/"

rm -rf /tmp/nextjs-docs

# Verify
python3 ./list.py nextjs-15
```
