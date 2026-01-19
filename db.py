"""SQLite utilities for library documentation indexer."""
import re
import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).parent / "data" / "library.db"


def get_connection() -> sqlite3.Connection:
    """Get a database connection, creating tables if needed."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    init_db(conn)
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Initialize database schema with FTS5."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS libraries (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            doc_count INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            library_id INTEGER NOT NULL,
            path TEXT NOT NULL,
            url TEXT,
            title TEXT,
            content TEXT NOT NULL,
            indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (library_id) REFERENCES libraries(id),
            UNIQUE(library_id, path)
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
            title,
            content,
            path,
            content='documents',
            content_rowid='id'
        );

        CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
            INSERT INTO documents_fts(rowid, title, content, path)
            VALUES (new.id, new.title, new.content, new.path);
        END;

        CREATE TRIGGER IF NOT EXISTS documents_ad AFTER DELETE ON documents BEGIN
            INSERT INTO documents_fts(documents_fts, rowid, title, content, path)
            VALUES('delete', old.id, old.title, old.content, old.path);
        END;

        CREATE TRIGGER IF NOT EXISTS documents_au AFTER UPDATE ON documents BEGIN
            INSERT INTO documents_fts(documents_fts, rowid, title, content, path)
            VALUES('delete', old.id, old.title, old.content, old.path);
            INSERT INTO documents_fts(rowid, title, content, path)
            VALUES (new.id, new.title, new.content, new.path);
        END;
    """)
    conn.commit()


def get_or_create_library(conn: sqlite3.Connection, name: str) -> int:
    """Get or create a library entry, returning its ID."""
    cursor = conn.execute(
        "INSERT OR IGNORE INTO libraries (name) VALUES (?)",
        (name,)
    )
    conn.commit()

    row = conn.execute(
        "SELECT id FROM libraries WHERE name = ?",
        (name,)
    ).fetchone()
    return row["id"]


def upsert_document(
    conn: sqlite3.Connection,
    library_id: int,
    path: str,
    content: str,
    title: str = None,
    url: str = None
) -> None:
    """Insert or update a document."""
    # Delete existing to trigger FTS update
    conn.execute(
        "DELETE FROM documents WHERE library_id = ? AND path = ?",
        (library_id, path)
    )

    conn.execute("""
        INSERT INTO documents (library_id, path, content, title, url)
        VALUES (?, ?, ?, ?, ?)
    """, (library_id, path, content, title, url))

    # Update doc count
    conn.execute("""
        UPDATE libraries
        SET doc_count = (SELECT COUNT(*) FROM documents WHERE library_id = ?),
            indexed_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (library_id, library_id))

    conn.commit()


def build_fts_query(query: str) -> str:
    """Build FTS5 query with support for multi-word and prefix searches.

    - Multiple words are combined with OR for broader matching
    - Words ending with * are treated as prefix searches
    - Title matches are boosted with higher weight
    """
    # Split on whitespace, filter empty
    terms = [t.strip() for t in query.split() if t.strip()]

    if not terms:
        return '""'

    fts_terms = []
    for term in terms:
        # Escape special FTS5 characters except *
        escaped = re.sub(r'(["\^\$\(\)\[\]\{\}\|\+])', r'\\\1', term)

        if escaped.endswith('*'):
            # Prefix search
            fts_terms.append(f'{escaped}')
        else:
            # Exact term with prefix matching for better recall
            fts_terms.append(f'"{escaped}"*')

    # Combine terms with OR, boost title matches
    term_query = ' OR '.join(fts_terms)
    return f'({term_query})'


def search_documents(
    conn: sqlite3.Connection,
    query: str,
    library_name: str = None,
    limit: int = 10
) -> list:
    """Search documents using FTS5 with improved ranking.

    - Multi-word queries match any term (OR)
    - Title matches are boosted
    - Supports prefix matching (e.g., "auth*")
    """
    fts_query = build_fts_query(query)

    sql = """
        SELECT
            d.id,
            d.path,
            d.title,
            d.url,
            snippet(documents_fts, 1, '>>>', '<<<', '...', 64) as snippet,
            l.name as library,
            bm25(documents_fts, 10.0, 1.0, 5.0) as rank
        FROM documents_fts fts
        JOIN documents d ON fts.rowid = d.id
        JOIN libraries l ON d.library_id = l.id
        WHERE documents_fts MATCH ?
    """
    params = [fts_query]

    if library_name:
        sql += " AND l.name = ?"
        params.append(library_name)

    sql += " ORDER BY rank LIMIT ?"
    params.append(limit)

    return conn.execute(sql, params).fetchall()


def list_libraries(conn: sqlite3.Connection) -> list:
    """List all indexed libraries."""
    return conn.execute("""
        SELECT name, doc_count, indexed_at
        FROM libraries
        ORDER BY name
    """).fetchall()


def list_documents(conn: sqlite3.Connection, library_name: str) -> list:
    """List all documents for a library."""
    return conn.execute("""
        SELECT d.title, d.path, d.url
        FROM documents d
        JOIN libraries l ON d.library_id = l.id
        WHERE l.name = ?
        ORDER BY d.path
    """, (library_name,)).fetchall()


def get_document(
    conn: sqlite3.Connection,
    library_name: str,
    identifier: str
) -> Optional[dict]:
    """Get full document content by ID, path, or title (exact match).

    Matching order:
    1. If identifier is numeric → match by document ID
    2. Else → exact match on path
    3. Else → exact match on title (case-insensitive)
    """
    # Try by ID first if numeric
    if identifier.isdigit():
        row = conn.execute("""
            SELECT d.id, d.path, d.title, d.url, d.content, l.name as library
            FROM documents d
            JOIN libraries l ON d.library_id = l.id
            WHERE d.id = ? AND l.name = ?
        """, (int(identifier), library_name)).fetchone()
        if row:
            return dict(row)

    # Try exact path match
    row = conn.execute("""
        SELECT d.id, d.path, d.title, d.url, d.content, l.name as library
        FROM documents d
        JOIN libraries l ON d.library_id = l.id
        WHERE d.path = ? AND l.name = ?
    """, (identifier, library_name)).fetchone()
    if row:
        return dict(row)

    # Try exact title match (case-insensitive)
    row = conn.execute("""
        SELECT d.id, d.path, d.title, d.url, d.content, l.name as library
        FROM documents d
        JOIN libraries l ON d.library_id = l.id
        WHERE LOWER(d.title) = LOWER(?) AND l.name = ?
    """, (identifier, library_name)).fetchone()
    if row:
        return dict(row)

    return None


def delete_library(conn: sqlite3.Connection, name: str) -> bool:
    """Delete a library and all its documents."""
    row = conn.execute(
        "SELECT id FROM libraries WHERE name = ?",
        (name,)
    ).fetchone()

    if not row:
        return False

    library_id = row["id"]
    conn.execute("DELETE FROM documents WHERE library_id = ?", (library_id,))
    conn.execute("DELETE FROM libraries WHERE id = ?", (library_id,))
    conn.commit()
    return True
