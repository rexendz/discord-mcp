"""Smoke tests — no Discord credentials required."""

from __future__ import annotations

import importlib
import os


def test_package_importable() -> None:
    """discord_mcp must be importable without any env vars set."""
    mod = importlib.import_module("discord_mcp")
    assert mod is not None


def test_server_module_importable() -> None:
    """server module must be importable and expose the mcp instance."""
    from discord_mcp.server import mcp

    assert mcp is not None


def test_guild_id_raises_when_unset(monkeypatch: "pytest.MonkeyPatch") -> None:
    """_guild_id() must raise ValueError when DISCORD_GUILD_ID is not set."""
    import pytest

    monkeypatch.delenv("DISCORD_GUILD_ID", raising=False)

    from discord_mcp.server import _guild_id

    with pytest.raises(ValueError, match="DISCORD_GUILD_ID"):
        _guild_id()


def test_headers_use_token(monkeypatch: "pytest.MonkeyPatch") -> None:
    """_headers() must include the bot token from the environment."""
    monkeypatch.setenv("DISCORD_TOKEN", "test-token-123")

    from discord_mcp import server

    # Reload to pick up fresh env
    import importlib
    importlib.reload(server)

    headers = server._headers()
    assert headers["Authorization"] == "Bot test-token-123"
    assert headers["Content-Type"] == "application/json"
