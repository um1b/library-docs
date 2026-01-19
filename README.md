# Library Documentation Indexer

A local documentation indexer for Claude Code that allows you to index and search library docs offline.

## Installation

```bash
git clone https://github.com/um1b/library-docs ~/.claude/skills/library-doc
```

## Usage

Use the `/library-doc` skill in Claude Code:

- `/library-doc list` - List indexed libraries
- `/library-doc search <query>` - Search indexed docs
- `/library-doc index <library>` - Index a library's documentation

## CLAUDE.md Configuration

Add the following to your `~/.claude/CLAUDE.md` to have Claude Code automatically search indexed documentation when building applications:

> When generating code for a library, first use the library-doc skill to check if documentation is indexed and search it before writing code. This ensures code follows current APIs and best practices.
