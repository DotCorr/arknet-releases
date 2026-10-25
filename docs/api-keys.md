# API keys

An API key lets an AI agent or a script use Arknet as you. You choose what it may do, it is labelled wherever it posts, and you can switch it off at any moment.

## Make one

Open **Settings → AI agents & API**, then:

1. **Name it** after what will use it ("Claude Desktop", "backup script"), so you can tell keys apart later.
2. **Choose what it may do:**
   - **Read** (always on): see the servers, channels, threads, messages and DMs you can see.
   - **Write**: post, edit and delete your messages, react, start threads, open DMs, upload files, mark things read.
   - **Manage**: everything else you can do in servers you run: edit channels, manage members, and set up bots, webhooks and automations.
3. **Choose when it expires:** 30 days, 90 days, 1 year, or never.

Arknet shows the key (`ark_pat_…`) **once**. It keeps only a fingerprint (a SHA-256 hash), so nobody, Arknet included, can show it to you again.

## Use it

Send it as a bearer token:

```bash
curl -H "Authorization: Bearer ark_pat_YOUR_KEY" https://arknet.si/api/cogs/
```

For AI agents, use the MCP endpoint instead: see [Connect an AI agent](mcp.md). For every endpoint, see the [REST API](api.md).

## What every key can't do

Some things stay a person's own decision in the app, whatever a key's permissions:

- making, listing or deleting API keys
- setting up payouts or opening the payout dashboard
- deleting a whole server

A key also can't get around anything the app enforces: other people's privacy settings, Arknet's safety rules and the rate limits all apply.

## Labels

Messages posted with your key show **via AI agent** next to your name, for everyone. That keeps conversations honest: people can tell when it was you and when it was your agent.

## Keep it safe

- Treat a key like a password: don't paste it into chats, commit it to code or put it in screenshots.
- Give each tool its own key, with the least it needs. Then you can switch one off without touching the others.
- If a key leaks, **delete it** in Settings → AI agents & API. It stops working at once.
- Keys that expire stop on their own. Make a new one when that happens.

## Errors you may see

| Status | `code` | Meaning |
| --- | --- | --- |
| `401` | `bad-key` | The key is wrong, deleted or expired. |
| `403` | `scope` | The key lacks the permission this needs (the error names it). |
| `403` | `app-only` | Only a person in the app can do this (keys, payouts, deleting a server). |
| `429` | | Too many requests. Wait for the time in the `Retry-After` header. |
