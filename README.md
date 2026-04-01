# discord-mcp

[![Python](https://img.shields.io/badge/python->=3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/github/license/rexendz/discord-mcp)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-server-blueviolet?logo=anthropic&logoColor=white)](https://modelcontextprotocol.io/)
[![FastMCP](https://img.shields.io/badge/built%20with-FastMCP-orange)](https://github.com/jlowin/fastmcp)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that exposes the Discord REST API as tools for AI assistants such as GitHub Copilot. Built with [FastMCP](https://github.com/jlowin/fastmcp), it lets any MCP-compatible client send messages, manage channels, moderate members, handle roles, and control threads in a Discord server — all through natural language.

> [!IMPORTANT]
> **This project was designed and tested exclusively with [VS Code](https://code.visualstudio.com/) and the [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat).**
> It has **not** been tested with other agentic tools or MCP clients (e.g. Claude Code, Cursor, Continue, or any other third-party tool). Compatibility with those environments is not guaranteed and is entirely untested. Use outside of VS Code + GitHub Copilot is at your own risk.

## Tools

The server exposes **40 tools** grouped into five categories.

### 💬 Messages

| Tool | Description |
|---|---|
| `send_message` | Send a message to a channel |
| `get_messages` | Retrieve recent messages from a channel |
| `get_message` | Retrieve a specific message |
| `edit_message` | Edit an existing bot message |
| `delete_message` | Delete a message |
| `pin_message` | Pin a message in a channel |
| `unpin_message` | Unpin a message from a channel |
| `get_pinned_messages` | List all pinned messages in a channel |
| `add_reaction` | Add an emoji reaction to a message |
| `delete_reaction` | Remove the bot's reaction from a message |

### 📢 Channels

| Tool | Description |
|---|---|
| `get_channel` | Get information about a channel |
| `list_guild_channels` | List all channels in the guild |
| `create_channel` | Create a new channel |
| `edit_channel` | Modify an existing channel |
| `delete_channel` | Delete a channel |
| `get_channel_invites` | List all invites for a channel |
| `create_channel_invite` | Create an invite for a channel |

### 🏰 Guild (Server)

| Tool | Description |
|---|---|
| `get_guild` | Get information about the configured guild |
| `edit_guild` | Modify the guild's settings |
| `list_guild_members` | List members of the guild |
| `get_guild_member` | Get a specific guild member by user ID |
| `kick_guild_member` | Kick a member from the guild |
| `ban_guild_member` | Ban a user from the guild |
| `unban_guild_member` | Unban a previously banned user |
| `get_guild_bans` | List all bans in the guild |
| `get_guild_invites` | List all active guild invites |
| `get_guild_audit_log` | Retrieve the guild's audit log |

### 🎭 Roles

| Tool | Description |
|---|---|
| `list_guild_roles` | List all roles in the guild |
| `create_role` | Create a new guild role |
| `edit_role` | Modify an existing role |
| `delete_role` | Delete a guild role |
| `add_role_to_member` | Assign a role to a member |
| `remove_role_from_member` | Remove a role from a member |

### 🧵 Threads

| Tool | Description |
|---|---|
| `create_thread_from_message` | Create a public thread from an existing message |
| `create_thread` | Create a thread not attached to a message |
| `create_forum_thread` | Create a new post in a forum channel |
| `list_public_archived_threads` | List public archived threads in a channel |
| `list_private_archived_threads` | List private archived threads in a channel |
| `list_active_guild_threads` | List all active threads in the guild |
| `join_thread` | Add the bot to a thread |
| `leave_thread` | Remove the bot from a thread |
| `add_thread_member` | Add a user to a thread |
| `remove_thread_member` | Remove a user from a thread |
| `get_thread_member` | Get a thread member object for a user |
| `list_thread_members` | List all members of a thread |
| `edit_thread` | Modify a thread's settings |

## Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- A Discord bot token with the required permissions
- Your Discord server (guild) ID

## Setup

### 1. Create a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.
2. Navigate to **Bot** and create a bot. Copy the **Token**.
3. Under **OAuth2 → URL Generator**, select the `bot` scope and the permissions your use-case requires (e.g. *Send Messages*, *Manage Channels*, *Manage Roles*, *Ban Members*).
4. Open the generated URL in your browser to invite the bot to your server.

### 2. Install the Server

```bash
# Clone the repository
git clone https://github.com/rexendz/discord-mcp.git
cd discord-mcp

# Install with uv (recommended)
uv sync
```

Or install directly from the source with pip:

```bash
pip install .
```

### 3. Configure Environment Variables

The server requires two environment variables:

| Variable | Description |
|---|---|
| `DISCORD_TOKEN` | Your Discord bot token |
| `DISCORD_GUILD_ID` | The ID of the Discord server to manage |

## VS Code Setup (GitHub Copilot)

You can use this MCP server with [GitHub Copilot in VS Code](https://code.visualstudio.com/docs/copilot/overview).

### Option A — Workspace Configuration (`.vscode/mcp.json`)

Add a `.vscode/mcp.json` file to your project so anyone who opens it can use the server:

```json
{
  "servers": {
    "discord-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "path/to/discord-mcp", "discord-mcp"],
      "env": {
        "DISCORD_TOKEN": "${input:discordToken}",
        "DISCORD_GUILD_ID": "${input:discordGuildId}"
      }
    }
  },
  "inputs": [
    {
      "id": "discordToken",
      "type": "promptString",
      "description": "Discord bot token",
      "password": true
    },
    {
      "id": "discordGuildId",
      "type": "promptString",
      "description": "Discord Guild (server) ID"
    }
  ]
}
```

### Option B — User Configuration (`settings.json`)

To make the server available across all your VS Code workspaces, add the following to your **User `settings.json`** (`Ctrl+Shift+P` → *Preferences: Open User Settings (JSON)*):

```json
{
  "mcp": {
    "servers": {
      "discord-mcp": {
        "type": "stdio",
        "command": "uvx",
        "args": ["--from", "/absolute/path/to/discord-mcp", "discord-mcp"],
        "env": {
          "DISCORD_TOKEN": "<your-bot-token>",
          "DISCORD_GUILD_ID": "<your-guild-id>"
        }
      }
    }
  }
}
```

> **Tip:** Avoid hardcoding sensitive tokens in `settings.json`. Prefer using VS Code's `${input:...}` prompt mechanism (as shown in Option A) or store credentials in your system's secret manager.

### Using the Tools

Once the server is configured, open the **Copilot Chat** panel (`Ctrl+Alt+I` on Windows/Linux, `Cmd+Opt+I` on macOS), switch to **Agent** mode, and simply ask:

```
Send a message to channel 1234567890 saying "Hello from Copilot!"
```

Copilot will automatically invoke the appropriate `send_message` tool.

## License

[MIT](LICENSE)
