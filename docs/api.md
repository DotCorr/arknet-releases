# REST API

Everything the Arknet app does goes through this API, and your [API key](api-keys.md) or a [bot's key](bots.md) can use it too. A machine-readable description is at [/docs/openapi.json](openapi.json).

## Basics

- **Base URL:** `https://arknet.si/api/cogs`
- **Auth:** `Authorization: Bearer ark_pat_…` (you) or `ark_bot_…` (a bot)
- **Format:** JSON in and out. Uploads use `multipart/form-data`.
- **Ids:** 24-character hex strings.
- **Times:** ISO 8601, in UTC.
- **Errors:** a status code and `{ "error": "a sentence a person can read", "code": "…" }`, where `code` appears when there is one: `bad-key`, `scope`, `app-only`, `bot-scope`, `blocked`…

### Limits

Limits apply per account, in a sliding window. Too many requests get `429` and a `Retry-After` header.

| What | Limit |
| --- | --- |
| Sending messages | 15 every 10 seconds |
| Reactions | 30 every 10 seconds |
| Uploads | 30 a minute; 25 MB per file |
| Opening DMs, friend requests | 20 a minute each |
| Incoming webhook posts | 30 a minute per webhook |

## Servers

| Method and path | What it does |
| --- | --- |
| `GET /` | Your servers. *(Not for bots: use `GET /{serverId}`.)* |
| `GET /{serverId}` | A server and its channels and threads: `{ server, channels }` |
| `GET /{serverId}/members` | Members: `userId`, `username`, `role`, `presence`, and `bot: true` for bots |
| `POST /{serverId}/channels` | Make a channel: `{ name, kind: "text" or "voice", category, topic }`. Needs **manage**. |

Invite links, approval, server rules, AutoMod and channel controls (who can post, slow mode) have their own page: [Invites, rules and links](invites.md).

## Channels, threads and messages

| Method and path | What it does |
| --- | --- |
| `GET /channels/{channelId}/messages?before=ISO` | The newest 50 messages, oldest first: `{ messages, hasMore }`. Page back with `before`. |
| `POST /channels/{channelId}/messages` | Post: `{ text, replyTo?, attachments? }`. Returns `{ userMessage }`. |
| `PATCH /channels/{channelId}/messages/{messageId}` | Edit your message: `{ text }` |
| `DELETE /channels/{channelId}/messages/{messageId}` | Delete your message (or any, as a moderator) |
| `POST /channels/{channelId}/messages/{messageId}/reactions` | Add or take back a reaction: `{ emoji }` |
| `POST /channels/{channelId}/messages/{messageId}/pin` | Pin or unpin (moderators; anyone in a DM) |
| `GET /channels/{channelId}/pins` | Pinned messages |
| `POST /channels/{channelId}/threads` | Start a thread: `{ name, rootMessageId? }`. Works in a channel or inside a thread, up to five deep. |
| `PATCH /channels/{channelId}` | Rename or describe: `{ name, topic }`. A channel needs **manage**; a thread's starter may edit theirs. Moderators can also set `category`, `organismMode` and `icon`. |
| `DELETE /channels/{channelId}` | Delete a channel, or a thread with every thread inside it |
| `POST /channels/{channelId}/typing` | Show "typing…" for a moment |
| `POST /channels/{channelId}/read` | Mark read up to now |

A channel's `threadOf` is `null` for a channel, and `{ channelId, rootMessageId? }` for a thread, naming the channel or thread it sits in.

### Attach files

Upload first, then pass what comes back as `attachments`:

```bash
curl -X POST https://arknet.si/api/cogs/uploads \
  -H "Authorization: Bearer ark_pat_YOUR_KEY" \
  -F channelId=CHANNEL_ID -F files=@report.pdf
# → [{ "url": "/api/cogs/files/…", "name": "report.pdf", "mime": "application/pdf", "size": 52311 }]
```

### The message object

```json
{
  "id": "6731…",
  "channelId": "6730…",
  "authorUserId": "6730…",
  "authorName": "ada",
  "role": "user",
  "via": "agent",
  "text": "Sounds good, see you Saturday",
  "attachments": [],
  "replyTo": { "messageId": "6731…", "authorName": "bo", "excerpt": "Saturday at ten?" },
  "mentions": [],
  "editedAt": null,
  "deleted": false,
  "pinned": false,
  "createdAt": "2026-10-25T17:02:11.198Z",
  "reactions": [{ "emoji": "👍", "count": 2, "mine": false }]
}
```

`role` is `user`, `organism` (Cog-S), `activity` or `system` (call logs). `via` says how a `user` message was posted:

- `""`: in the app
- `agent`: with someone's API key
- `bot`: by a bot
- `webhook`: by an incoming webhook
- `automation`: by an automation

## Direct messages, people and notifications

| Method and path | What it does |
| --- | --- |
| `GET /dms` | Your DMs, most recent first |
| `POST /dms` | Open (or reuse) a DM: `{ userIds: [...] }`. Their privacy settings decide whether you may. |
| `GET /users/search?q=` | People whose username starts with `q` (who allow being found) |
| `GET /users/{userId}` | A profile card, as their privacy settings allow |
| `GET /friends` | Your friends and requests |
| `POST /friends` | Send a friend request: `{ username }` |
| `GET /notifications` | Your latest notifications: `{ notifications, unread }` |
| `POST /notifications/read` | Mark read: `{ ids? }` (none means all) |

## Integrations

These all need **manage**, in a server you run. Your own keys are managed only in the app.

| Method and path | What it does |
| --- | --- |
| `GET /integrations/servers/{serverId}` | Bots, incoming webhooks, automations and recent deliveries |
| `POST /integrations/servers/{serverId}/bots` | Add a bot: `{ name, description }`. Returns its key and signing secret, once. |
| `PATCH /integrations/bots/{botId}` | `{ name, description, callbackUrl, events, scopes }` |
| `POST /integrations/bots/{botId}/key` | A new key; the old one stops |
| `DELETE /integrations/bots/{botId}` | Remove a bot |
| `POST /integrations/servers/{serverId}/webhooks` | Add an incoming webhook: `{ channelId, name }`. Returns its path, once. |
| `DELETE /integrations/webhooks/{webhookId}` | Remove it; its URL stops |
| `POST /integrations/servers/{serverId}/automations` | Add an automation: `{ name, trigger, action }` |
| `PATCH /integrations/automations/{id}` | Change it, or switch it off: `{ enabled: false }` |
| `POST /integrations/automations/{id}/run` | Try it once |
| `DELETE /integrations/automations/{id}` | Remove it |

An automation looks like this:

```json
{
  "name": "Welcome",
  "trigger": { "type": "member.joined" },
  "action": { "type": "send_message", "channelId": "6730…", "text": "Welcome, {user}!" }
}
```

Other triggers are `{ "type": "message", "channelId": null, "keyword": "bug" }` and `{ "type": "schedule", "every": "day", "at": "09:00" }`. Schedules also take `"every": "hour"`, or `"week"` with a `weekday` from `0` (Sunday) to `6`, all in UTC. The other action is `{ "type": "webhook", "url": "https://…" }`.

## Realtime

To hear things as they happen (new messages, edits, reactions, typing, presence, joins), open a websocket:

1. `POST /realtime/ticket` returns `{ ticket, path }`. A ticket lasts 30 seconds and works once.
2. Connect to `wss://arknet.si/api/cogs/ws`.
3. Send `{ "type": "auth", "ticket": "…" }` first. Arknet answers `{ "type": "ready" }`.

Then events arrive as JSON. The main ones:

| Event | Payload |
| --- | --- |
| `message.created` | `{ channelId, serverId, message }` |
| `message.updated` | `{ channelId, serverId, message }` |
| `message.reactions` | `{ channelId, messageId, userId, reactions }` |
| `typing` | `{ channelId, userId, name }` |
| `channel.created`, `channel.updated` | `{ serverId, channel }` |
| `channel.deleted` | `{ serverId, channelIds }` |
| `member.joined` | `{ serverId, userId, name }` |
| `presence` | `{ userId, status }` |

Send `{ "type": "ping" }` now and then to keep it open. Bots can use the socket too, for their own server.
