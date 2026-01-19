"""Library presets registry mapping common libraries to their doc sources.

Each preset contains:
- repo: GitHub repository (owner/repo)
- docs_path: Path to docs folder in the repo
- base_url: Live documentation URL
- branch: Optional branch/tag (defaults to main)
- extensions: Optional file extensions (defaults to .md, .mdx)
"""
from __future__ import annotations

PRESETS = {
    # Frontend Frameworks
    "react": {
        "repo": "reactjs/react.dev",
        "docs_path": "src/content",
        "base_url": "https://react.dev",
    },
    "nextjs": {
        "repo": "vercel/next.js",
        "docs_path": "docs",
        "base_url": "https://nextjs.org/docs",
    },
    "vue": {
        "repo": "vuejs/docs",
        "docs_path": "src",
        "base_url": "https://vuejs.org",
    },
    "svelte": {
        "repo": "sveltejs/svelte.dev",
        "docs_path": "apps/svelte.dev/content/docs",
        "base_url": "https://svelte.dev/docs",
    },
    "nuxt": {
        "repo": "nuxt/nuxt",
        "docs_path": "docs",
        "base_url": "https://nuxt.com/docs",
    },
    "angular": {
        "repo": "angular/angular",
        "docs_path": "adev/src/content",
        "base_url": "https://angular.dev",
    },
    "solid": {
        "repo": "solidjs/solid-docs",
        "docs_path": "src/routes",
        "base_url": "https://docs.solidjs.com",
    },
    "astro": {
        "repo": "withastro/docs",
        "docs_path": "src/content/docs",
        "base_url": "https://docs.astro.build",
    },
    "remix": {
        "repo": "remix-run/react-router",
        "docs_path": "docs",
        "base_url": "https://remix.run/docs",
    },

    # CSS/UI
    "tailwind": {
        "repo": "tailwindlabs/tailwindcss.com",
        "docs_path": "src/docs",
        "base_url": "https://tailwindcss.com/docs",
    },
    "shadcn": {
        "repo": "shadcn-ui/ui",
        "docs_path": "apps/v4/content/docs",
        "base_url": "https://ui.shadcn.com/docs",
    },

    # Backend Frameworks
    "express": {
        "repo": "expressjs/expressjs.com",
        "docs_path": "en",
        "base_url": "https://expressjs.com",
    },
    "fastapi": {
        "repo": "fastapi/fastapi",
        "docs_path": "docs/en/docs",
        "base_url": "https://fastapi.tiangolo.com",
        "branch": "master",
    },
    "django": {
        "repo": "django/django",
        "docs_path": "docs",
        "base_url": "https://docs.djangoproject.com",
        "extensions": [".txt"],
    },
    "flask": {
        "repo": "pallets/flask",
        "docs_path": "docs",
        "base_url": "https://flask.palletsprojects.com",
        "extensions": [".rst"],
    },
    "hono": {
        "repo": "honojs/website",
        "docs_path": "docs",
        "base_url": "https://hono.dev",
    },
    "nestjs": {
        "repo": "nestjs/docs.nestjs.com",
        "docs_path": "content",
        "base_url": "https://docs.nestjs.com",
        "branch": "master",
    },
    "rails": {
        "repo": "rails/rails",
        "docs_path": "guides/source",
        "base_url": "https://guides.rubyonrails.org",
    },
    "laravel": {
        "repo": "laravel/docs",
        "docs_path": ".",
        "base_url": "https://laravel.com/docs",
        "branch": "11.x",
    },

    # Runtimes
    "bun": {
        "repo": "oven-sh/bun",
        "docs_path": "docs",
        "base_url": "https://bun.sh/docs",
    },
    "node": {
        "repo": "nodejs/nodejs.org",
        "docs_path": "apps/site/pages/en",
        "base_url": "https://nodejs.org/docs",
    },
    "deno": {
        "repo": "denoland/docs",
        "docs_path": ".",
        "base_url": "https://docs.deno.com",
    },

    # Languages/Type Systems
    "typescript": {
        "repo": "microsoft/TypeScript-Website",
        "docs_path": "packages/documentation/copy/en",
        "base_url": "https://www.typescriptlang.org/docs",
        "branch": "v2",
    },
    "python": {
        "repo": "python/cpython",
        "docs_path": "Doc",
        "base_url": "https://docs.python.org/3",
        "extensions": [".rst"],
    },
    "rust": {
        "repo": "rust-lang/book",
        "docs_path": "src",
        "base_url": "https://doc.rust-lang.org/book",
    },
    "go": {
        "repo": "golang/go",
        "docs_path": "doc",
        "base_url": "https://go.dev/doc",
    },

    # Databases/ORMs
    "prisma": {
        "repo": "prisma/docs",
        "docs_path": "content",
        "base_url": "https://www.prisma.io/docs",
    },
    "drizzle": {
        "repo": "drizzle-team/drizzle-orm",
        "docs_path": "docs",
        "base_url": "https://orm.drizzle.team",
    },
    "sqlalchemy": {
        "repo": "sqlalchemy/sqlalchemy",
        "docs_path": "doc/build",
        "base_url": "https://docs.sqlalchemy.org",
        "extensions": [".rst"],
    },
    "supabase": {
        "repo": "supabase/supabase",
        "docs_path": "apps/docs",
        "base_url": "https://supabase.com/docs",
        "branch": "master",
    },
    "mongodb": {
        "repo": "mongodb/docs",
        "docs_path": "source",
        "base_url": "https://www.mongodb.com/docs",
        "extensions": [".txt", ".rst"],
        "branch": "master",
    },

    # State Management
    "redux": {
        "repo": "reduxjs/redux",
        "docs_path": "docs",
        "base_url": "https://redux.js.org",
    },
    "zustand": {
        "repo": "pmndrs/zustand",
        "docs_path": "docs",
        "base_url": "https://zustand-demo.pmnd.rs",
    },
    "tanstack-query": {
        "repo": "TanStack/query",
        "docs_path": "docs",
        "base_url": "https://tanstack.com/query",
    },
    "jotai": {
        "repo": "pmndrs/jotai",
        "docs_path": "docs",
        "base_url": "https://jotai.org",
    },

    # Testing
    "vitest": {
        "repo": "vitest-dev/vitest",
        "docs_path": "docs",
        "base_url": "https://vitest.dev",
    },
    "playwright": {
        "repo": "microsoft/playwright",
        "docs_path": "docs/src",
        "base_url": "https://playwright.dev/docs",
    },
    "jest": {
        "repo": "jestjs/jest",
        "docs_path": "docs",
        "base_url": "https://jestjs.io/docs",
    },
    "pytest": {
        "repo": "pytest-dev/pytest",
        "docs_path": "doc/en",
        "base_url": "https://docs.pytest.org",
        "extensions": [".rst"],
    },
    "cypress": {
        "repo": "cypress-io/cypress-documentation",
        "docs_path": "docs",
        "base_url": "https://docs.cypress.io",
    },

    # Build Tools
    "vite": {
        "repo": "vitejs/vite",
        "docs_path": "docs",
        "base_url": "https://vitejs.dev",
    },
    "esbuild": {
        "repo": "evanw/esbuild",
        "docs_path": ".",
        "base_url": "https://esbuild.github.io",
        "extensions": [".md"],
    },
    "webpack": {
        "repo": "webpack/webpack.js.org",
        "docs_path": "src/content",
        "base_url": "https://webpack.js.org",
    },
    "turbo": {
        "repo": "vercel/turborepo",
        "docs_path": "docs/site/content",
        "base_url": "https://turbo.build/repo/docs",
    },

    # AI/ML
    "langchain": {
        "repo": "langchain-ai/langchainjs",
        "docs_path": "docs/core_docs",
        "base_url": "https://js.langchain.com/docs",
    },
    "openai": {
        "repo": "openai/openai-python",
        "docs_path": ".",
        "base_url": "https://platform.openai.com/docs",
        "extensions": [".md"],
    },
    "anthropic": {
        "repo": "anthropics/anthropic-sdk-python",
        "docs_path": ".",
        "base_url": "https://docs.anthropic.com",
        "extensions": [".md"],
    },
    "huggingface": {
        "repo": "huggingface/transformers",
        "docs_path": "docs/source/en",
        "base_url": "https://huggingface.co/docs/transformers",
    },

    # GraphQL
    "graphql": {
        "repo": "graphql/graphql.github.io",
        "docs_path": "src/pages",
        "base_url": "https://graphql.org",
        "branch": "source",
    },
    "apollo": {
        "repo": "apollographql/apollo-client",
        "docs_path": "docs/source",
        "base_url": "https://www.apollographql.com/docs/react",
    },

    # Validation
    "zod": {
        "repo": "colinhacks/zod",
        "docs_path": ".",
        "base_url": "https://zod.dev",
        "extensions": [".md"],
    },

    # HTTP/API
    "axios": {
        "repo": "axios/axios",
        "docs_path": ".",
        "base_url": "https://axios-http.com/docs",
        "extensions": [".md"],
    },
    "trpc": {
        "repo": "trpc/trpc",
        "docs_path": "www/docs",
        "base_url": "https://trpc.io/docs",
    },

    # Mobile
    "react-native": {
        "repo": "facebook/react-native-website",
        "docs_path": "docs",
        "base_url": "https://reactnative.dev/docs",
    },
    "expo": {
        "repo": "expo/expo",
        "docs_path": "docs",
        "base_url": "https://docs.expo.dev",
    },
    "flutter": {
        "repo": "flutter/website",
        "docs_path": "src/content",
        "base_url": "https://docs.flutter.dev",
    },

    # CLI/DevOps
    "docker": {
        "repo": "docker/docs",
        "docs_path": "content",
        "base_url": "https://docs.docker.com",
    },
    "kubernetes": {
        "repo": "kubernetes/website",
        "docs_path": "content/en/docs",
        "base_url": "https://kubernetes.io/docs",
    },
    "terraform": {
        "repo": "hashicorp/terraform",
        "docs_path": "docs",
        "base_url": "https://developer.hashicorp.com/terraform/docs",
    },
}


def get_preset(name: str) -> dict | None:
    """Get a library preset by name (case-insensitive)."""
    return PRESETS.get(name.lower())


def list_presets() -> list[str]:
    """List all available preset names."""
    return sorted(PRESETS.keys())


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 presets.py <command> [args]")
        print("Commands: list, show <library>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == 'list':
        presets = list_presets()
        print(f"Available presets ({len(presets)}):\n")
        # Print in columns
        cols = 4
        for i in range(0, len(presets), cols):
            row = presets[i:i + cols]
            print("  " + "  ".join(f"{p:<18}" for p in row))

    elif cmd == 'show':
        if len(sys.argv) < 3:
            print("Usage: python3 presets.py show <library>")
            sys.exit(1)
        name = sys.argv[2]
        preset = get_preset(name)
        if not preset:
            print(f"No preset found for '{name}'")
            print(f"Available: {', '.join(list_presets()[:10])}...")
            sys.exit(1)
        print(f"Preset: {name}")
        print(f"  repo:      https://github.com/{preset['repo']}")
        print(f"  docs_path: {preset['docs_path']}")
        print(f"  base_url:  {preset['base_url']}")
        if 'branch' in preset:
            print(f"  branch:    {preset['branch']}")
        if 'extensions' in preset:
            print(f"  extensions: {', '.join(preset['extensions'])}")
        else:
            print(f"  extensions: .md, .mdx")

    else:
        print(f"Unknown command: {cmd}")
        print("Commands: list, show <library>")
        sys.exit(1)
