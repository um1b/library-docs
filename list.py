#!/usr/bin/env python3
"""List indexed libraries.

Usage:
    python3 list.py [--json]
"""
import argparse
import json
from db import get_connection, list_libraries, delete_library


def main():
    parser = argparse.ArgumentParser(description='List indexed libraries')
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
