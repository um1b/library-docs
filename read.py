#!/usr/bin/env python3
"""Read full document content from indexed library documentation."""
import argparse
import json
import sys

from db import get_connection, get_document


def parse_lines(lines_arg: str) -> tuple[int, int]:
    """Parse --lines argument like '1-50' into (start, end)."""
    if '-' not in lines_arg:
        raise ValueError("Lines must be in format START-END (e.g., 1-50)")
    parts = lines_arg.split('-', 1)
    start = int(parts[0])
    end = int(parts[1])
    if start < 1:
        raise ValueError("Start line must be >= 1")
    if end < start:
        raise ValueError("End line must be >= start line")
    return start, end


def main():
    parser = argparse.ArgumentParser(
        description="Read full document content by ID, path, or title"
    )
    parser.add_argument("library", help="Library name")
    parser.add_argument("identifier", help="Document ID (number), path, or title (exact match)")
    parser.add_argument("--lines", help="Line range to return (e.g., 1-50)")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="Output as JSON with metadata")
    args = parser.parse_args()

    conn = get_connection()
    doc = get_document(conn, args.library, args.identifier)

    if not doc:
        print(f"Document not found: '{args.identifier}' in library '{args.library}'", file=sys.stderr)
        print("\nTip: Use search.py to find documents, then use the ID, path, or exact title.", file=sys.stderr)
        sys.exit(1)

    content = doc["content"]

    # Apply line filtering if requested
    if args.lines:
        try:
            start, end = parse_lines(args.lines)
            lines = content.split('\n')
            # Convert to 0-indexed, slice, rejoin
            content = '\n'.join(lines[start - 1:end])
        except ValueError as e:
            print(f"Invalid --lines argument: {e}", file=sys.stderr)
            sys.exit(1)

    if args.as_json:
        output = {
            "id": doc["id"],
            "library": doc["library"],
            "title": doc["title"],
            "path": doc["path"],
            "url": doc["url"],
            "content": content,
        }
        if args.lines:
            output["lines"] = args.lines
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        print(f"# {doc['title'] or doc['path']}")
        if doc["url"]:
            print(f"URL: {doc['url']}")
        print(f"ID: {doc['id']} | Path: {doc['path']}")
        if args.lines:
            print(f"Lines: {args.lines}")
        print("-" * 60)
        print(content)


if __name__ == "__main__":
    main()
