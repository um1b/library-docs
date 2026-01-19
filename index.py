#!/usr/bin/env python3
"""Index documentation content into SQLite.

Usage:
    echo '<content>' | python3 index.py <library> --file <path> [--url <url>] [--title <title>]
    python3 index.py <library> --file <path> --content "<content>" [--url <url>] [--title <title>]

Batch mode with progress bar:
    find docs -name "*.md" | python3 index.py <library> --batch --base-url "https://example.com/docs"
"""
import argparse
import sys
import re
from db import get_connection, get_or_create_library, upsert_document


def extract_title(content: str, path: str) -> str:
    """Extract title from markdown content or path."""
    # Try to find first h1 heading
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # Try frontmatter title
    if content.startswith('---'):
        fm_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
        if fm_match:
            return fm_match.group(1).strip()

    # Fall back to filename
    return path.split('/')[-1].replace('.md', '').replace('.mdx', '').replace('.rst', '').replace('-', ' ').title()


def print_progress(current: int, total: int, width: int = 40, interval: int = 1):
    """Print a horizontal progress bar at specified intervals."""
    if current != total and current % interval != 0:
        return
    percent = current / total if total > 0 else 1
    filled = int(width * percent)
    bar = '█' * filled + '░' * (width - filled)
    sys.stderr.write(f'[{bar}] {current}/{total}\n')
    sys.stderr.flush()


def batch_index(library: str, base_url: str, strip_prefix: str = ''):
    """Index multiple files from stdin with progress bar."""
    # Read all file paths first to get total count
    files = [line.strip() for line in sys.stdin if line.strip()]
    total = len(files)

    if total == 0:
        print("No files to index.", file=sys.stderr)
        return

    # Calculate progress interval: ~5 updates for small sets, every 200 for large
    interval = 200 if total >= 1000 else max(1, total // 5)

    conn = get_connection()
    library_id = get_or_create_library(conn, library)

    for i, filepath in enumerate(files, 1):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            if not content.strip():
                continue

            # Build URL from filepath
            url_path = filepath
            if strip_prefix and url_path.startswith(strip_prefix):
                url_path = url_path[len(strip_prefix):]
            url_path = url_path.lstrip('/')
            # Remove extension and /index suffix
            url_path = re.sub(r'\.(md|mdx|rst)$', '', url_path)
            url_path = re.sub(r'/index$', '/', url_path)
            url = f"{base_url.rstrip('/')}/{url_path}" if base_url else None

            title = extract_title(content, filepath)

            upsert_document(
                conn,
                library_id=library_id,
                path=filepath,
                content=content,
                title=title,
                url=url
            )
        except Exception as e:
            sys.stderr.write(f'Error indexing {filepath}: {e}\n')

        print_progress(i, total, interval=interval)

    conn.close()
    sys.stderr.write(f'Done! Indexed {total} docs into "{library}"\n')


def main():
    parser = argparse.ArgumentParser(description='Index documentation content')
    parser.add_argument('library', help='Library name')
    parser.add_argument('--file', '-f', help='File path within docs')
    parser.add_argument('--url', '-u', help='Source URL')
    parser.add_argument('--title', '-t', help='Document title (auto-extracted if not provided)')
    parser.add_argument('--content', '-c', help='Content (reads from stdin if not provided)')
    parser.add_argument('--batch', '-b', action='store_true', help='Batch mode: read file paths from stdin')
    parser.add_argument('--base-url', help='Base URL for batch mode (e.g., https://docs.example.com)')
    parser.add_argument('--strip-prefix', default='', help='Prefix to strip from paths for URL generation')

    args = parser.parse_args()

    # Batch mode
    if args.batch:
        batch_index(args.library, args.base_url or '', args.strip_prefix)
        return

    # Single file mode
    if not args.file:
        parser.error('--file is required in single-file mode')

    # Get content from argument or stdin
    if args.content:
        content = args.content
    else:
        content = sys.stdin.read()

    if not content.strip():
        print("Error: No content provided", file=sys.stderr)
        sys.exit(1)

    # Extract or use provided title
    title = args.title or extract_title(content, args.file)

    # Index the document
    conn = get_connection()
    library_id = get_or_create_library(conn, args.library)
    upsert_document(
        conn,
        library_id=library_id,
        path=args.file,
        content=content,
        title=title,
        url=args.url
    )
    conn.close()


if __name__ == '__main__':
    main()
