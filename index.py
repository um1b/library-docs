#!/usr/bin/env python3
"""Index documentation content into SQLite.

Usage:
    echo '<content>' | python3 index.py <library> --file <path> [--url <url>] [--title <title>]
    python3 index.py <library> --file <path> --content "<content>" [--url <url>] [--title <title>]

Batch mode:
    find docs -name "*.md" | python3 index.py <library> --batch --base-url "https://example.com/docs"
"""
from __future__ import annotations
import argparse
import sys
import re
from db import get_connection, get_or_create_library, upsert_document

# Chunk files larger than this (in characters)
CHUNK_THRESHOLD = 8000


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


def chunk_document(content: str, path: str, base_url: str = None) -> list[dict]:
    """Split large documents into chunks by ## headings.

    Returns list of dicts with: path, content, title, url
    Only chunks if content exceeds CHUNK_THRESHOLD.
    """
    # Don't chunk small documents
    if len(content) < CHUNK_THRESHOLD:
        return [{
            'path': path,
            'content': content,
            'title': extract_title(content, path),
            'url': base_url
        }]

    # Extract frontmatter if present
    frontmatter = ''
    doc_content = content
    if content.startswith('---'):
        fm_end = content.find('---', 3)
        if fm_end != -1:
            frontmatter = content[:fm_end + 3]
            doc_content = content[fm_end + 3:].strip()

    # Split by ## headings (keep the heading with its content)
    sections = re.split(r'^(## .+)$', doc_content, flags=re.MULTILINE)

    chunks = []
    doc_title = extract_title(content, path)

    # First section (before any ##) - intro/overview
    if sections[0].strip():
        intro = sections[0].strip()
        if frontmatter:
            intro = frontmatter + '\n\n' + intro
        chunks.append({
            'path': path,
            'content': intro,
            'title': doc_title,
            'url': base_url
        })

    # Process heading + content pairs
    for i in range(1, len(sections), 2):
        if i + 1 < len(sections):
            heading = sections[i].strip()
            section_content = sections[i + 1].strip()

            # Skip empty sections
            if not section_content:
                continue

            # Extract section title from heading
            section_title = heading.replace('## ', '').strip()
            full_title = f"{doc_title} > {section_title}"

            # Build section URL with anchor
            section_url = base_url
            if base_url:
                anchor = re.sub(r'[^a-z0-9\s-]', '', section_title.lower())
                anchor = re.sub(r'\s+', '-', anchor)
                section_url = f"{base_url}#{anchor}"

            chunks.append({
                'path': f"{path}##{section_title}",
                'content': f"{heading}\n\n{section_content}",
                'title': full_title,
                'url': section_url
            })

    # If no chunks created (no ## headings), return whole document
    if not chunks:
        return [{
            'path': path,
            'content': content,
            'title': doc_title,
            'url': base_url
        }]

    return chunks


def batch_index(library: str, base_url: str, strip_prefix: str = '', chunk: bool = True):
    """Index multiple files from stdin."""
    files = [line.strip() for line in sys.stdin if line.strip()]
    total = len(files)

    if total == 0:
        return

    conn = get_connection()
    library_id = get_or_create_library(conn, library)

    for filepath in files:
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

            # Chunk large documents or index as single doc
            if chunk:
                chunks = chunk_document(content, filepath, url)
            else:
                chunks = [{
                    'path': filepath,
                    'content': content,
                    'title': extract_title(content, filepath),
                    'url': url
                }]

            for doc in chunks:
                upsert_document(
                    conn,
                    library_id=library_id,
                    path=doc['path'],
                    content=doc['content'],
                    title=doc['title'],
                    url=doc['url']
                )

        except Exception:
            pass  # Silent errors

    conn.close()


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
    parser.add_argument('--no-chunk', action='store_true', help='Disable automatic chunking of large documents')

    args = parser.parse_args()

    # Batch mode
    if args.batch:
        batch_index(args.library, args.base_url or '', args.strip_prefix, chunk=not args.no_chunk)
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
