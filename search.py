#!/usr/bin/env python3
"""Search indexed documentation.

Usage:
    python3 search.py "<query>" [--library name] [--limit n]

Examples:
    python3 search.py "authentication"
    python3 search.py "hooks lifecycle" --library react
    python3 search.py "auth*" --limit 20
"""
import argparse
import json
from db import get_connection, search_documents, list_libraries


def main():
    parser = argparse.ArgumentParser(description='Search indexed documentation')
    parser.add_argument('query', help='Search query (supports multiple words, prefix with *)')
    parser.add_argument('--library', '-l', help='Filter by library name')
    parser.add_argument('--limit', '-n', type=int, default=10, help='Max results (default: 10)')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    conn = get_connection()

    # Validate library exists if specified
    if args.library:
        libraries = [row["name"] for row in list_libraries(conn)]
        if args.library not in libraries:
            if args.json:
                print(json.dumps({"error": f"Library '{args.library}' not found", "available": libraries}))
            else:
                print(f"Library '{args.library}' not found.")
                if libraries:
                    print(f"Available libraries: {', '.join(libraries)}")
                else:
                    print("No libraries indexed yet.")
            conn.close()
            return

    results = search_documents(conn, args.query, args.library, args.limit)
    conn.close()

    if not results:
        if args.json:
            print(json.dumps({"results": [], "count": 0, "query": args.query}))
        else:
            print(f"No results found for '{args.query}'.")
        return

    if args.json:
        output = {
            "query": args.query,
            "results": [
                {
                    "library": row["library"],
                    "path": row["path"],
                    "title": row["title"],
                    "url": row["url"],
                    "snippet": row["snippet"]
                }
                for row in results
            ],
            "count": len(results)
        }
        print(json.dumps(output, indent=2))
    else:
        lib_filter = f" in '{args.library}'" if args.library else ""
        print(f"Found {len(results)} result(s) for '{args.query}'{lib_filter}:\n")
        for i, row in enumerate(results, 1):
            title = row['title'] or row['path']
            print(f"{i}. [{row['library']}] {title}")
            if row["url"]:
                print(f"   {row['url']}")
            snippet = row["snippet"].replace(">>>", "\033[1m").replace("<<<", "\033[0m")
            # Clean up snippet for display
            snippet = ' '.join(snippet.split())
            print(f"   {snippet}")
            print()


if __name__ == '__main__':
    main()
