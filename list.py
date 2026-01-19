#!/usr/bin/env python3
"""List indexed libraries or documents.

Usage:
    python3 list.py [--json]
    python3 list.py <library> [--json]
    python3 list.py --delete <name>
"""
import argparse
import json
from db import get_connection, list_libraries, list_documents, delete_library


def main():
    parser = argparse.ArgumentParser(description='List indexed libraries or documents')
    parser.add_argument('library', nargs='?', help='Library name to list documents for')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    parser.add_argument('--delete', '-d', help='Delete a library by name')

    args = parser.parse_args()

    conn = get_connection()

    if args.delete:
        if delete_library(conn, args.delete):
            print(f"Deleted library: {args.delete}")
        else:
            print(f"Library not found: {args.delete}")
        conn.close()
        return

    # List documents for a specific library
    if args.library:
        docs = list_documents(conn, args.library)
        conn.close()

        if not docs:
            if args.json:
                print(json.dumps({"error": f"Library '{args.library}' not found or empty", "documents": []}))
            else:
                print(f"Library '{args.library}' not found or has no documents.")
            return

        if args.json:
            output = {
                "library": args.library,
                "documents": [
                    {"title": row["title"], "path": row["path"], "url": row["url"]}
                    for row in docs
                ],
                "count": len(docs)
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"Documents in '{args.library}' ({len(docs)} docs):\n")
            for i, row in enumerate(docs, 1):
                title = row['title'] or row['path']
                print(f"{i:3}. {title}")
                if row["url"]:
                    print(f"     {row['url']}")
        return

    # List all libraries
    libraries = list_libraries(conn)
    conn.close()

    if not libraries:
        if args.json:
            print(json.dumps({"libraries": [], "count": 0}))
        else:
            print("No libraries indexed yet.")
        return

    if args.json:
        output = {
            "libraries": [
                {
                    "name": row["name"],
                    "doc_count": row["doc_count"],
                    "indexed_at": row["indexed_at"]
                }
                for row in libraries
            ],
            "count": len(libraries)
        }
        print(json.dumps(output, indent=2))
    else:
        print("Indexed libraries:\n")
        for row in libraries:
            print(f"  {row['name']}: {row['doc_count']} docs (indexed: {row['indexed_at']})")
        print(f"\nTotal: {len(libraries)} library/libraries")


if __name__ == '__main__':
    main()
