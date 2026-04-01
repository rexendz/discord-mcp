# Contributing to discord-mcp

Thank you for taking the time to contribute! This document covers everything you need to get started.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Commit Messages](#commit-messages)
- [Pull Requests](#pull-requests)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

---

## Code of Conduct

Be respectful and constructive. Harassment or hostile behaviour of any kind will not be tolerated.

---

## Getting Started

1. **Fork** the repository and clone your fork.
2. Create a new branch off `main` for your work (see [Making Changes](#making-changes)).
3. Open a pull request when you are ready for review.

---

## Development Setup

**Requirements:** Python ≥ 3.11 and [uv](https://docs.astral.sh/uv/).

```bash
# Install all dependencies (including dev extras)
uv sync --all-groups

# Activate the virtual environment (optional — uv run handles this automatically)
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\Activate.ps1  # Windows PowerShell
```

### Environment variables

Copy the example below into a `.env` file (never commit this file):

```env
DISCORD_TOKEN=your_bot_token_here
DISCORD_GUILD_ID=your_guild_id_here
```

### Running the server locally

```bash
uv run discord-mcp
```

---

## Making Changes

| Branch naming | When to use |
|---|---|
| `feat/<short-description>` | New feature |
| `fix/<short-description>` | Bug fix |
| `chore/<short-description>` | Maintenance, dependencies, tooling |
| `docs/<short-description>` | Documentation only |

Keep branches focused — one logical change per PR.

### Linting & formatting

This project uses [Ruff](https://docs.astral.sh/ruff/) for both linting and formatting.

```bash
uv run ruff check .          # lint
uv run ruff check . --fix    # lint + auto-fix
uv run ruff format .         # format
```

CI will fail if either check reports errors.

### Tests

```bash
uv run pytest
```

Add or update tests for every behaviour change. Tests live alongside the source in `tests/`.

---

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) spec:

```
<type>(<scope>): <short summary>

[optional body]

[optional footer(s)]
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`

Examples:
- `feat(tools): add get_guild_member tool`
- `fix(http): handle 429 rate-limit responses`
- `chore(deps): bump fastmcp to 2.1.0`

---

## Pull Requests

- Fill in the PR template completely.
- Link to any related issue with `Closes #<issue>` or `Relates to #<issue>`.
- Keep PRs small and focused — large PRs are hard to review.
- All CI checks must pass before merge.
- At least **one approving review** is required.
- Squash merging is preferred to keep the history clean.

---

## Reporting Bugs

Use the **Bug Report** issue template. Include:

- Steps to reproduce (minimal and complete)
- Expected vs. actual behaviour
- Python version, OS, and relevant dependency versions
- Any relevant log output

---

## Suggesting Features

Use the **Feature Request** issue template. Explain:

- The problem you are trying to solve
- Your proposed solution
- Alternatives you have considered
