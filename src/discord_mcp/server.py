"""Discord MCP server using FastMCP.

Exposes tools for interacting with the Discord API covering:
- Message management
- Channel management
- Server (guild) management
- Role management
- Thread management
"""

from __future__ import annotations

import os
from typing import Any

import httpx
from fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DISCORD_API_BASE = "https://discord.com/api/v10"

# ---------------------------------------------------------------------------
# MCP server instance
# ---------------------------------------------------------------------------

mcp = FastMCP(
    name="discord-mcp",
    instructions=(
        "A Discord MCP server that exposes tools for managing messages, channels, "
        "guilds, roles, and threads via the Discord REST API. "
        "Requires DISCORD_TOKEN (Bot token) and DISCORD_GUILD_ID environment variables."
    ),
)

# ---------------------------------------------------------------------------
# Shared HTTP helpers
# ---------------------------------------------------------------------------


def _headers() -> dict[str, str]:
    token = os.environ.get("DISCORD_TOKEN", "")
    return {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
    }


def _guild_id() -> str:
    guild_id = os.environ.get("DISCORD_GUILD_ID", "")
    if not guild_id:
        raise ValueError("DISCORD_GUILD_ID environment variable is not set.")
    return guild_id


async def _request(
    method: str,
    path: str,
    *,
    json: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
) -> Any:
    """Execute an authenticated Discord API request and return parsed JSON."""
    url = f"{DISCORD_API_BASE}{path}"
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            url,
            headers=_headers(),
            json=json,
            params=params,
            timeout=30,
        )
    response.raise_for_status()
    if response.status_code == 204:
        return {"success": True}
    return response.json()


# ===========================================================================
# MESSAGE TOOLS
# ===========================================================================


@mcp.tool()
async def send_message(
    channel_id: str,
    content: str,
    tts: bool = False,
) -> dict[str, Any]:
    """Send a message to a Discord channel.

    Args:
        channel_id: The ID of the channel to send the message in.
        content: The text content of the message.
        tts: Whether the message should be sent as text-to-speech.

    Returns:
        The created message object.
    """
    return await _request(
        "POST",
        f"/channels/{channel_id}/messages",
        json={"content": content, "tts": tts},
    )


@mcp.tool()
async def get_messages(
    channel_id: str,
    limit: int = 50,
    before: str | None = None,
    after: str | None = None,
    around: str | None = None,
) -> list[dict[str, Any]]:
    """Retrieve messages from a Discord channel.

    Args:
        channel_id: The ID of the channel.
        limit: Max number of messages to return (1–100, default 50).
        before: Return messages before this message ID.
        after: Return messages after this message ID.
        around: Return messages around this message ID.

    Returns:
        A list of message objects.
    """
    params: dict[str, Any] = {"limit": min(max(limit, 1), 100)}
    if before:
        params["before"] = before
    if after:
        params["after"] = after
    if around:
        params["around"] = around
    return await _request("GET", f"/channels/{channel_id}/messages", params=params)


@mcp.tool()
async def get_message(channel_id: str, message_id: str) -> dict[str, Any]:
    """Retrieve a specific message from a channel.

    Args:
        channel_id: The ID of the channel.
        message_id: The ID of the message to retrieve.

    Returns:
        The message object.
    """
    return await _request("GET", f"/channels/{channel_id}/messages/{message_id}")


@mcp.tool()
async def edit_message(
    channel_id: str,
    message_id: str,
    content: str,
) -> dict[str, Any]:
    """Edit an existing message sent by the bot.

    Args:
        channel_id: The ID of the channel.
        message_id: The ID of the message to edit.
        content: The new text content for the message.

    Returns:
        The updated message object.
    """
    return await _request(
        "PATCH",
        f"/channels/{channel_id}/messages/{message_id}",
        json={"content": content},
    )


@mcp.tool()
async def delete_message(channel_id: str, message_id: str) -> dict[str, Any]:
    """Delete a message from a channel.

    Args:
        channel_id: The ID of the channel.
        message_id: The ID of the message to delete.

    Returns:
        A success indicator.
    """
    return await _request("DELETE", f"/channels/{channel_id}/messages/{message_id}")


@mcp.tool()
async def pin_message(channel_id: str, message_id: str) -> dict[str, Any]:
    """Pin a message in a channel.

    Args:
        channel_id: The ID of the channel.
        message_id: The ID of the message to pin.

    Returns:
        A success indicator.
    """
    return await _request("PUT", f"/channels/{channel_id}/pins/{message_id}")


@mcp.tool()
async def unpin_message(channel_id: str, message_id: str) -> dict[str, Any]:
    """Unpin a message from a channel.

    Args:
        channel_id: The ID of the channel.
        message_id: The ID of the message to unpin.

    Returns:
        A success indicator.
    """
    return await _request("DELETE", f"/channels/{channel_id}/pins/{message_id}")


@mcp.tool()
async def get_pinned_messages(channel_id: str) -> list[dict[str, Any]]:
    """Retrieve all pinned messages in a channel.

    Args:
        channel_id: The ID of the channel.

    Returns:
        A list of pinned message objects.
    """
    return await _request("GET", f"/channels/{channel_id}/pins")


@mcp.tool()
async def add_reaction(
    channel_id: str,
    message_id: str,
    emoji: str,
) -> dict[str, Any]:
    """Add a reaction to a message.

    Args:
        channel_id: The ID of the channel.
        message_id: The ID of the message.
        emoji: The emoji to react with (e.g. "👍" or "name:id" for custom emojis).

    Returns:
        A success indicator.
    """
    return await _request(
        "PUT",
        f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me",
    )


@mcp.tool()
async def delete_reaction(
    channel_id: str,
    message_id: str,
    emoji: str,
) -> dict[str, Any]:
    """Remove the bot's reaction from a message.

    Args:
        channel_id: The ID of the channel.
        message_id: The ID of the message.
        emoji: The emoji reaction to remove.

    Returns:
        A success indicator.
    """
    return await _request(
        "DELETE",
        f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me",
    )


# ===========================================================================
# CHANNEL TOOLS
# ===========================================================================


@mcp.tool()
async def get_channel(channel_id: str) -> dict[str, Any]:
    """Retrieve information about a channel.

    Args:
        channel_id: The ID of the channel.

    Returns:
        The channel object.
    """
    return await _request("GET", f"/channels/{channel_id}")


@mcp.tool()
async def list_guild_channels() -> list[dict[str, Any]]:
    """List all channels in the configured guild.

    Returns:
        A list of channel objects for the guild.
    """
    return await _request("GET", f"/guilds/{_guild_id()}/channels")


@mcp.tool()
async def create_channel(
    name: str,
    type: int = 0,
    topic: str | None = None,
    parent_id: str | None = None,
    position: int | None = None,
    nsfw: bool = False,
) -> dict[str, Any]:
    """Create a new channel in the guild.

    Args:
        name: The name for the new channel.
        type: Channel type integer (0=text, 2=voice, 4=category, 5=announcement,
              15=forum, 16=media). Defaults to 0 (text).
        topic: The channel topic (text channels only).
        parent_id: The category channel ID to place this channel in.
        position: The sort position of the channel.
        nsfw: Whether the channel is age-restricted.

    Returns:
        The newly created channel object.
    """
    body: dict[str, Any] = {"name": name, "type": type, "nsfw": nsfw}
    if topic is not None:
        body["topic"] = topic
    if parent_id is not None:
        body["parent_id"] = parent_id
    if position is not None:
        body["position"] = position
    return await _request("POST", f"/guilds/{_guild_id()}/channels", json=body)


@mcp.tool()
async def edit_channel(
    channel_id: str,
    name: str | None = None,
    topic: str | None = None,
    position: int | None = None,
    nsfw: bool | None = None,
    parent_id: str | None = None,
    rate_limit_per_user: int | None = None,
) -> dict[str, Any]:
    """Modify an existing channel.

    Args:
        channel_id: The ID of the channel to modify.
        name: New name for the channel.
        topic: New topic for the channel.
        position: New sort position.
        nsfw: Whether the channel should be age-restricted.
        parent_id: New parent category ID.
        rate_limit_per_user: Slowmode delay in seconds (0–21600).

    Returns:
        The updated channel object.
    """
    body: dict[str, Any] = {}
    if name is not None:
        body["name"] = name
    if topic is not None:
        body["topic"] = topic
    if position is not None:
        body["position"] = position
    if nsfw is not None:
        body["nsfw"] = nsfw
    if parent_id is not None:
        body["parent_id"] = parent_id
    if rate_limit_per_user is not None:
        body["rate_limit_per_user"] = rate_limit_per_user
    return await _request("PATCH", f"/channels/{channel_id}", json=body)


@mcp.tool()
async def delete_channel(channel_id: str) -> dict[str, Any]:
    """Delete a channel (or close a DM).

    Args:
        channel_id: The ID of the channel to delete.

    Returns:
        The deleted channel object.
    """
    return await _request("DELETE", f"/channels/{channel_id}")


@mcp.tool()
async def get_channel_invites(channel_id: str) -> list[dict[str, Any]]:
    """List all invites for a channel.

    Args:
        channel_id: The ID of the channel.

    Returns:
        A list of invite objects.
    """
    return await _request("GET", f"/channels/{channel_id}/invites")


@mcp.tool()
async def create_channel_invite(
    channel_id: str,
    max_age: int = 86400,
    max_uses: int = 0,
    temporary: bool = False,
    unique: bool = False,
) -> dict[str, Any]:
    """Create an invite for a channel.

    Args:
        channel_id: The ID of the channel.
        max_age: Duration of the invite in seconds (0 = never expires, default 86400).
        max_uses: Maximum number of uses (0 = unlimited).
        temporary: Whether this invite grants temporary membership.
        unique: If True, always creates a new unique invite instead of reusing.

    Returns:
        The created invite object.
    """
    return await _request(
        "POST",
        f"/channels/{channel_id}/invites",
        json={
            "max_age": max_age,
            "max_uses": max_uses,
            "temporary": temporary,
            "unique": unique,
        },
    )


# ===========================================================================
# SERVER (GUILD) TOOLS
# ===========================================================================


@mcp.tool()
async def get_guild() -> dict[str, Any]:
    """Retrieve information about the configured guild.

    Returns:
        The guild object with full metadata.
    """
    return await _request("GET", f"/guilds/{_guild_id()}", params={"with_counts": True})


@mcp.tool()
async def edit_guild(
    name: str | None = None,
    description: str | None = None,
    afk_timeout: int | None = None,
    verification_level: int | None = None,
    default_message_notifications: int | None = None,
    explicit_content_filter: int | None = None,
) -> dict[str, Any]:
    """Modify the configured guild's settings.

    Args:
        name: New name for the guild.
        description: New description (Community guilds only).
        afk_timeout: AFK timeout in seconds (60, 300, 900, 1800, 3600).
        verification_level: Verification level (0–4).
        default_message_notifications: Notification level (0=all, 1=mentions).
        explicit_content_filter: Explicit content filter level (0–2).

    Returns:
        The updated guild object.
    """
    body: dict[str, Any] = {}
    if name is not None:
        body["name"] = name
    if description is not None:
        body["description"] = description
    if afk_timeout is not None:
        body["afk_timeout"] = afk_timeout
    if verification_level is not None:
        body["verification_level"] = verification_level
    if default_message_notifications is not None:
        body["default_message_notifications"] = default_message_notifications
    if explicit_content_filter is not None:
        body["explicit_content_filter"] = explicit_content_filter
    return await _request("PATCH", f"/guilds/{_guild_id()}", json=body)


@mcp.tool()
async def list_guild_members(
    limit: int = 100,
    after: str | None = None,
) -> list[dict[str, Any]]:
    """List members of the configured guild.

    Args:
        limit: Maximum number of members to return (1–1000, default 100).
        after: Return members whose ID is greater than this value (for pagination).

    Returns:
        A list of guild member objects.
    """
    params: dict[str, Any] = {"limit": min(max(limit, 1), 1000)}
    if after:
        params["after"] = after
    return await _request("GET", f"/guilds/{_guild_id()}/members", params=params)


@mcp.tool()
async def get_guild_member(user_id: str) -> dict[str, Any]:
    """Retrieve a guild member by user ID.

    Args:
        user_id: The Discord user ID of the member.

    Returns:
        The guild member object.
    """
    return await _request("GET", f"/guilds/{_guild_id()}/members/{user_id}")


@mcp.tool()
async def kick_guild_member(user_id: str) -> dict[str, Any]:
    """Remove (kick) a member from the guild.

    Args:
        user_id: The Discord user ID of the member to kick.

    Returns:
        A success indicator.
    """
    return await _request("DELETE", f"/guilds/{_guild_id()}/members/{user_id}")


@mcp.tool()
async def ban_guild_member(
    user_id: str,
    delete_message_seconds: int = 0,
) -> dict[str, Any]:
    """Ban a user from the guild.

    Args:
        user_id: The Discord user ID to ban.
        delete_message_seconds: Number of seconds of messages to delete (0–604800).

    Returns:
        A success indicator.
    """
    return await _request(
        "PUT",
        f"/guilds/{_guild_id()}/bans/{user_id}",
        json={"delete_message_seconds": delete_message_seconds},
    )


@mcp.tool()
async def unban_guild_member(user_id: str) -> dict[str, Any]:
    """Unban a previously banned user.

    Args:
        user_id: The Discord user ID to unban.

    Returns:
        A success indicator.
    """
    return await _request("DELETE", f"/guilds/{_guild_id()}/bans/{user_id}")


@mcp.tool()
async def get_guild_bans(
    limit: int = 100,
    before: str | None = None,
    after: str | None = None,
) -> list[dict[str, Any]]:
    """List all bans in the configured guild.

    Args:
        limit: Maximum number of bans to return (1–1000, default 100).
        before: Return bans for users before this user ID.
        after: Return bans for users after this user ID.

    Returns:
        A list of ban objects.
    """
    params: dict[str, Any] = {"limit": min(max(limit, 1), 1000)}
    if before:
        params["before"] = before
    if after:
        params["after"] = after
    return await _request("GET", f"/guilds/{_guild_id()}/bans", params=params)


@mcp.tool()
async def get_guild_invites() -> list[dict[str, Any]]:
    """Retrieve all active invites for the configured guild.

    Returns:
        A list of invite objects.
    """
    return await _request("GET", f"/guilds/{_guild_id()}/invites")


@mcp.tool()
async def get_guild_audit_log(
    limit: int = 50,
    action_type: int | None = None,
    user_id: str | None = None,
    before: str | None = None,
) -> dict[str, Any]:
    """Retrieve the guild's audit log.

    Args:
        limit: Maximum entries to return (1–100, default 50).
        action_type: Filter by audit log action type integer.
        user_id: Filter by the user who performed the action.
        before: Return entries before this audit log entry ID.

    Returns:
        An audit log object containing entries.
    """
    params: dict[str, Any] = {"limit": min(max(limit, 1), 100)}
    if action_type is not None:
        params["action_type"] = action_type
    if user_id:
        params["user_id"] = user_id
    if before:
        params["before"] = before
    return await _request("GET", f"/guilds/{_guild_id()}/audit-logs", params=params)


# ===========================================================================
# ROLE TOOLS
# ===========================================================================


@mcp.tool()
async def list_guild_roles() -> list[dict[str, Any]]:
    """List all roles in the configured guild.

    Returns:
        A list of role objects.
    """
    return await _request("GET", f"/guilds/{_guild_id()}/roles")


@mcp.tool()
async def create_role(
    name: str,
    permissions: str | None = None,
    color: int = 0,
    hoist: bool = False,
    mentionable: bool = False,
) -> dict[str, Any]:
    """Create a new role in the guild.

    Args:
        name: The name for the new role.
        permissions: Bitwise permission string (e.g. "8" for administrator).
        color: RGB color value as an integer (e.g. 0xFF5733).
        hoist: Whether the role should be displayed separately in the member list.
        mentionable: Whether the role should be mentionable by all members.

    Returns:
        The created role object.
    """
    body: dict[str, Any] = {
        "name": name,
        "color": color,
        "hoist": hoist,
        "mentionable": mentionable,
    }
    if permissions is not None:
        body["permissions"] = permissions
    return await _request("POST", f"/guilds/{_guild_id()}/roles", json=body)


@mcp.tool()
async def edit_role(
    role_id: str,
    name: str | None = None,
    permissions: str | None = None,
    color: int | None = None,
    hoist: bool | None = None,
    mentionable: bool | None = None,
) -> dict[str, Any]:
    """Modify an existing guild role.

    Args:
        role_id: The ID of the role to modify.
        name: New name for the role.
        permissions: New bitwise permission string.
        color: New RGB color integer.
        hoist: Whether the role should be displayed separately.
        mentionable: Whether the role should be mentionable.

    Returns:
        The updated role object.
    """
    body: dict[str, Any] = {}
    if name is not None:
        body["name"] = name
    if permissions is not None:
        body["permissions"] = permissions
    if color is not None:
        body["color"] = color
    if hoist is not None:
        body["hoist"] = hoist
    if mentionable is not None:
        body["mentionable"] = mentionable
    return await _request(
        "PATCH", f"/guilds/{_guild_id()}/roles/{role_id}", json=body
    )


@mcp.tool()
async def delete_role(role_id: str) -> dict[str, Any]:
    """Delete a guild role.

    Args:
        role_id: The ID of the role to delete.

    Returns:
        A success indicator.
    """
    return await _request("DELETE", f"/guilds/{_guild_id()}/roles/{role_id}")


@mcp.tool()
async def add_role_to_member(user_id: str, role_id: str) -> dict[str, Any]:
    """Assign a role to a guild member.

    Args:
        user_id: The Discord user ID of the member.
        role_id: The ID of the role to assign.

    Returns:
        A success indicator.
    """
    return await _request(
        "PUT", f"/guilds/{_guild_id()}/members/{user_id}/roles/{role_id}"
    )


@mcp.tool()
async def remove_role_from_member(user_id: str, role_id: str) -> dict[str, Any]:
    """Remove a role from a guild member.

    Args:
        user_id: The Discord user ID of the member.
        role_id: The ID of the role to remove.

    Returns:
        A success indicator.
    """
    return await _request(
        "DELETE", f"/guilds/{_guild_id()}/members/{user_id}/roles/{role_id}"
    )


# ===========================================================================
# THREAD TOOLS
# ===========================================================================


@mcp.tool()
async def create_thread_from_message(
    channel_id: str,
    message_id: str,
    name: str,
    auto_archive_duration: int = 1440,
) -> dict[str, Any]:
    """Create a public thread from an existing message.

    Args:
        channel_id: The ID of the channel containing the message.
        message_id: The ID of the message to create the thread from.
        name: The name of the new thread.
        auto_archive_duration: Minutes until the thread auto-archives
            (60, 1440, 4320, or 10080). Defaults to 1440 (1 day).

    Returns:
        The created thread channel object.
    """
    return await _request(
        "POST",
        f"/channels/{channel_id}/messages/{message_id}/threads",
        json={"name": name, "auto_archive_duration": auto_archive_duration},
    )


@mcp.tool()
async def create_thread(
    channel_id: str,
    name: str,
    auto_archive_duration: int = 1440,
    type: int = 11,
    invitable: bool = True,
) -> dict[str, Any]:
    """Create a thread not attached to an existing message (private or public).

    Args:
        channel_id: The ID of the channel to create the thread in.
        name: The name of the new thread.
        auto_archive_duration: Minutes until auto-archive (60, 1440, 4320, 10080).
            Defaults to 1440 (1 day).
        type: Thread type (10=announcement thread, 11=public thread,
              12=private thread). Defaults to 11.
        invitable: Whether non-moderators can add other users to a private thread.

    Returns:
        The created thread channel object.
    """
    return await _request(
        "POST",
        f"/channels/{channel_id}/threads",
        json={
            "name": name,
            "auto_archive_duration": auto_archive_duration,
            "type": type,
            "invitable": invitable,
        },
    )


@mcp.tool()
async def create_forum_thread(
    channel_id: str,
    name: str,
    content: str,
    auto_archive_duration: int = 1440,
    applied_tags: list[str] | None = None,
) -> dict[str, Any]:
    """Create a new post (thread) in a forum or media channel.

    Args:
        channel_id: The ID of the forum/media channel.
        name: The title of the new forum post.
        content: The content for the initial message in the thread.
        auto_archive_duration: Minutes until auto-archive (60, 1440, 4320, 10080).
            Defaults to 1440 (1 day).
        applied_tags: A list of tag IDs to apply to the forum post.

    Returns:
        The created thread channel object (with an embedded first message).
    """
    body: dict[str, Any] = {
        "name": name,
        "auto_archive_duration": auto_archive_duration,
        "message": {"content": content},
    }
    if applied_tags:
        body["applied_tags"] = applied_tags
    return await _request("POST", f"/channels/{channel_id}/threads", json=body)


@mcp.tool()
async def list_public_archived_threads(
    channel_id: str,
    limit: int = 50,
    before: str | None = None,
) -> dict[str, Any]:
    """List public archived threads in a channel.

    Args:
        channel_id: The ID of the channel.
        limit: Maximum number of threads to return.
        before: Return threads before this ISO8601 timestamp.

    Returns:
        An object containing threads, members, and a has_more boolean.
    """
    params: dict[str, Any] = {"limit": limit}
    if before:
        params["before"] = before
    return await _request(
        "GET", f"/channels/{channel_id}/threads/archived/public", params=params
    )


@mcp.tool()
async def list_private_archived_threads(
    channel_id: str,
    limit: int = 50,
    before: str | None = None,
) -> dict[str, Any]:
    """List private archived threads in a channel (requires MANAGE_THREADS).

    Args:
        channel_id: The ID of the channel.
        limit: Maximum number of threads to return.
        before: Return threads before this ISO8601 timestamp.

    Returns:
        An object containing threads, members, and a has_more boolean.
    """
    params: dict[str, Any] = {"limit": limit}
    if before:
        params["before"] = before
    return await _request(
        "GET", f"/channels/{channel_id}/threads/archived/private", params=params
    )


@mcp.tool()
async def list_active_guild_threads() -> dict[str, Any]:
    """List all active threads in the configured guild.

    Returns:
        An object containing active threads and the current user's thread member objects.
    """
    return await _request("GET", f"/guilds/{_guild_id()}/threads/active")


@mcp.tool()
async def join_thread(thread_id: str) -> dict[str, Any]:
    """Add the bot to a thread.

    Args:
        thread_id: The ID of the thread to join.

    Returns:
        A success indicator.
    """
    return await _request("PUT", f"/channels/{thread_id}/thread-members/@me")


@mcp.tool()
async def leave_thread(thread_id: str) -> dict[str, Any]:
    """Remove the bot from a thread.

    Args:
        thread_id: The ID of the thread to leave.

    Returns:
        A success indicator.
    """
    return await _request("DELETE", f"/channels/{thread_id}/thread-members/@me")


@mcp.tool()
async def add_thread_member(thread_id: str, user_id: str) -> dict[str, Any]:
    """Add a user to a thread.

    Args:
        thread_id: The ID of the thread.
        user_id: The Discord user ID to add to the thread.

    Returns:
        A success indicator.
    """
    return await _request("PUT", f"/channels/{thread_id}/thread-members/{user_id}")


@mcp.tool()
async def remove_thread_member(thread_id: str, user_id: str) -> dict[str, Any]:
    """Remove a user from a thread.

    Args:
        thread_id: The ID of the thread.
        user_id: The Discord user ID to remove from the thread.

    Returns:
        A success indicator.
    """
    return await _request("DELETE", f"/channels/{thread_id}/thread-members/{user_id}")


@mcp.tool()
async def get_thread_member(
    thread_id: str,
    user_id: str,
    with_member: bool = False,
) -> dict[str, Any]:
    """Get a thread member object for a user.

    Args:
        thread_id: The ID of the thread.
        user_id: The Discord user ID.
        with_member: Whether to include guild member data in the response.

    Returns:
        A thread member object.
    """
    return await _request(
        "GET",
        f"/channels/{thread_id}/thread-members/{user_id}",
        params={"with_member": with_member},
    )


@mcp.tool()
async def list_thread_members(
    thread_id: str,
    with_member: bool = False,
    limit: int = 100,
    after: str | None = None,
) -> list[dict[str, Any]]:
    """List all members of a thread.

    Args:
        thread_id: The ID of the thread.
        with_member: Whether to include guild member data in the response.
        limit: Maximum number of thread members to return (1–100).
        after: Return members after this user ID (for pagination).

    Returns:
        A list of thread member objects.
    """
    params: dict[str, Any] = {
        "with_member": with_member,
        "limit": min(max(limit, 1), 100),
    }
    if after:
        params["after"] = after
    return await _request(
        "GET", f"/channels/{thread_id}/thread-members", params=params
    )


@mcp.tool()
async def edit_thread(
    thread_id: str,
    name: str | None = None,
    archived: bool | None = None,
    auto_archive_duration: int | None = None,
    locked: bool | None = None,
    invitable: bool | None = None,
    rate_limit_per_user: int | None = None,
    applied_tags: list[str] | None = None,
) -> dict[str, Any]:
    """Modify a thread channel's settings.

    Args:
        thread_id: The ID of the thread to modify.
        name: New name for the thread.
        archived: Whether the thread should be archived.
        auto_archive_duration: New auto-archive duration in minutes.
        locked: Whether the thread is locked (only moderators can unarchive).
        invitable: Whether non-moderators can add members (private threads only).
        rate_limit_per_user: Slowmode delay in seconds (0–21600).
        applied_tags: Updated list of tag IDs (forum threads only).

    Returns:
        The updated thread channel object.
    """
    body: dict[str, Any] = {}
    if name is not None:
        body["name"] = name
    if archived is not None:
        body["archived"] = archived
    if auto_archive_duration is not None:
        body["auto_archive_duration"] = auto_archive_duration
    if locked is not None:
        body["locked"] = locked
    if invitable is not None:
        body["invitable"] = invitable
    if rate_limit_per_user is not None:
        body["rate_limit_per_user"] = rate_limit_per_user
    if applied_tags is not None:
        body["applied_tags"] = applied_tags
    return await _request("PATCH", f"/channels/{thread_id}", json=body)


# ===========================================================================
# Entry point
# ===========================================================================


def main() -> None:
    """Run the Discord MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
