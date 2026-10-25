# Connect an AI agent (MCP)

The [Model Context Protocol](https://modelcontextprotocol.io) lets AI agents use tools. Arknet speaks it, so Claude, ChatGPT, Cursor, VS Code and any other MCP client can read your servers and post for you. You choose what an agent may do, and everything it posts is labelled *via AI agent*.

## 1. Make a key

In Arknet, open **Settings → AI agents & API** and make a key:

- **Read** lets the agent see what you can see.
- **Write** lets it post, reply, react, start threads and send DMs as you.
- **Manage** lets it edit servers and channels you run, and their bots and automations.

Copy the key (`ark_pat_…`) right away; Arknet shows it once. After you make it, the page also gives you ready-made setup for the tools below, with your key filled in.

## 2. Connect your tool

The endpoint is `https://arknet.si/api/cogs/mcp`, and the key goes in an `Authorization: Bearer` header.

### Claude Code

```bash
claude mcp add --transport http arknet https://arknet.si/api/cogs/mcp \
  --header "Authorization: Bearer ark_pat_YOUR_KEY"
```

### Claude Desktop

Add this to `claude_desktop_config.json` (Settings → Developer → Edit config), then restart Claude. It uses [mcp-remote](https://www.npmjs.com/package/mcp-remote) to carry the header:

```json
{
  "mcpServers": {
    "arknet": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://arknet.si/api/cogs/mcp", "--header", "Authorization:${ARKNET_AUTH}"],
      "env": { "ARKNET_AUTH": "Bearer ark_pat_YOUR_KEY" }
    }
  }
}
```

### Cursor

In `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "arknet": {
      "url": "https://arknet.si/api/cogs/mcp",
      "headers": { "Authorization": "Bearer ark_pat_YOUR_KEY" }
    }
  }
}
```

### VS Code

In `.vscode/mcp.json`:

```json
{
  "servers": {
    "arknet": {
      "type": "http",
      "url": "https://arknet.si/api/cogs/mcp",
      "headers": { "Authorization": "Bearer ark_pat_YOUR_KEY" }
    }
  }
}
```

### Anything else

Any client that speaks MCP over Streamable HTTP and can send a header works. If yours can't send headers, use `mcp-remote` as in the Claude Desktop example.

## 3. Ask away

Try: *"What did people say in #general today?"*, *"Reply to Ada's question in the planning thread"*, or *"Start a thread in #ideas called launch-party"*.

## Tools

| Tool | What it does | Needs |
| --- | --- | --- |
| `whoami` | Who the key acts as, its permissions, and a bot's server | Read |
| `list_servers` | Your servers, with ids and your role | Read |
| `list_channels` | Channels and threads in a server, as a tree | Read |
| `read_messages` | Recent messages in a channel, thread or DM, oldest first | Read |
| `list_members` | Who is in a server, their role, and whether they're online | Read |
| `send_message` | Post in a channel, thread or DM, or reply to a message | Write |
| `start_thread` | Start a thread in a channel or inside another thread | Write |
| `react` | Add or take back an emoji reaction | Write |
| `list_dms` | Your direct messages *(personal keys only)* | Read |
| `open_dm` | Open a DM with someone, if their settings allow it *(personal keys only)* | Write |
| `find_people` | Look someone up by username *(personal keys only)* | Read |
| `get_notifications` | Your latest notifications *(personal keys only)* | Read |

An agent only sees the tools its key allows. A read-only key gets no writing tools, and a bot key gets no personal ones.

## What agents can't do

Agents use Arknet's own API, so they meet the same rules as you:

- **Your privacy settings and other people's still apply.** An agent can't DM someone who doesn't take DMs from you.
- **Arknet's safety rules still apply.** Posts the rules block come back as a tool error with the reason, so the agent can tell you.
- **App-only actions stay in the app.** No agent can make keys, set up payouts or delete a server.
- **Limits apply.** For example, 15 messages every 10 seconds.

## Using a bot instead

A bot's key (`ark_bot_…`, from **Server settings → Integrations**) works the same way. The agent then acts as the bot, inside that bot's server only, and its posts carry a **Bot** badge. See [Bots](bots.md).

## Protocol details

- **Transport:** Streamable HTTP, `POST` only. `GET` and `DELETE` answer `405`. Responses are single JSON objects; there are no SSE streams or sessions.
- **Versions:** `2026-07-28`, with per-request `_meta`, `server/discover`, and the `MCP-Protocol-Version`, `Mcp-Method` and `Mcp-Name` headers checked against the body. Clients that open with `initialize` can use `2025-11-25`, `2025-06-18` or `2025-03-26`.
- **Errors:** `401` for a missing or invalid key (with `WWW-Authenticate`), `400` with `-32020` for headers that don't match the body, `400` with `-32022` for an unsupported version (listing the supported ones), and `404` with `-32601` for an unknown method. A failed tool comes back as a result with `isError: true`.
- **Browsers:** requests with an `Origin` header from another site are refused.

## Troubleshooting

- **401:** the key is wrong, deleted or expired. Make a new one.
- **"this key needs the … permission":** give the key more permissions, or make a new one.
- **"bots work inside their own server":** the bot was asked about a server it isn't in.
- **Nothing happens in Claude Desktop:** check that `npx` works in a terminal, then restart Claude.
