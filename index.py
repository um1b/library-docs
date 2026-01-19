#!/usr/bin/env python3
"""Index documentation content into SQLite.

Usage:
    echo '<content>' | python3 index.py <library> --file <path> [--url <url>] [--title <title>]
    python3 index.py <library> --file <path> --content "<content>" [--url <url>] [--title <title>]
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
    return path.split('/')[-1].replace('.md', '').replace('.mdx', '').replace('-', ' ').title()


def main():
    parser = argparse.ArgumentParser(description='Index documentation content')
    parser.add_argument('library', help='Library name')
    parser.add_argument('--file', '-f', required=True, help='File path within docs')
    parser.add_argument('--url', '-u', help='Source URL')
    parser.add_argument('--title', '-t', help='Document title (auto-extracted if not provided)')
    parser.add_argument('--content', '-c', help='Content (reads from stdin if not provided)')

    args = parser.parse_args()

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

    print(f"Indexed: {args.file} -> {args.library}")


if __name__ == '__main__':
    main()
