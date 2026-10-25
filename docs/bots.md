# Bots

A bot is a member of one server with an account of its own. It reads and posts like anyone else, and you drive it from code or from an AI agent. A bot's posts carry a **Bot** badge, and a bot can never step outside its server.

## Make a bot

Owners and moderators open **Server settings → Integrations → Bots**, give it a name, and add it. Arknet then:

- creates the bot's account and adds it to the server as a member,
- shows its **key** (`ark_bot_…`) **once**, and
- shows its **signing secret** (`whsec_…`), used to check the events Arknet sends it.

A server can have up to 10 bots. You can give a bot a new key at any time; the old one stops at once.

## What a bot can do

| A bot can | A bot can't |
| --- | --- |
| Read channels and threads in its server | See or post in any other server |
| Post, reply, react, start threads (**Write**) | Send or read DMs, or make friends |
| Upload files into its server | Make API keys or touch payouts |
| List members, and see who is online | Delete the server |
| Edit channels, with **Manage** turned on | Get around Arknet's safety rules or limits |

Choose **Post and react** (write) and **Manage channels** (manage) under the bot in Integrations. To make a bot a moderator, change its role in the member list.

## Drive it with the API

```bash
# Post as the bot
curl -X POST https://arknet.si/api/cogs/channels/CHANNEL_ID/messages \
  -H "Authorization: Bearer ark_bot_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Good morning! Today is release day."}'
```

The bot uses the same endpoints as people: see the [REST API](api.md). It can also connect to the [realtime socket](api.md#realtime) to hear everything live.

## Drive it with an AI agent

Give an MCP client the bot's key instead of your own, and the agent acts as the bot, in its server only. See [Connect an AI agent](mcp.md#using-a-bot-instead).

## Events: let Arknet tell your bot

Set an **Event URL** under the bot in Integrations, and pick the events you want:

- `message.created`: a new message anywhere in the server
- `message.updated`: an edit, a deletion or a pin
- `member.joined`: someone joined the server

Arknet then sends each event as a `POST` with a JSON body:

```json
{
  "id": "5d7c1a6e-9a0f-4d2e-8b8e-1f3a2c4d5e6f",
  "type": "message.created",
  "createdAt": "2026-10-25T17:02:11.204Z",
  "serverId": "6730f0c2a1b2c3d4e5f60718",
  "channel": { "id": "6730f0c2a1b2c3d4e5f60719", "name": "general", "kind": "text" },
  "message": {
    "id": "6730f1d4a1b2c3d4e5f6071a",
    "authorUserId": "6730f0aaa1b2c3d4e5f60700",
    "authorName": "ada",
    "text": "!ping",
    "createdAt": "2026-10-25T17:02:11.198Z"
  }
}
```

A `member.joined` event carries `member: { userId, name }` instead of `channel` and `message`.

The rules of delivery:

- **Headers:** `Arknet-Event` (the type), `Arknet-Delivery` (the `id`) and `Arknet-Signature`.
- **Answer fast:** reply `2xx` within 5 seconds, and do slow work afterwards.
- **Retries:** if your URL doesn't answer `2xx`, Arknet tries twice more, after 10 seconds and after a minute. Use `id` to ignore repeats. Answer `410` to stop retries for an event.
- **No echoes:** a bot never receives its own messages.
- **Public HTTPS only:** private and internal addresses are refused.
- **History:** the last deliveries, and whether they worked, show under **Recent deliveries** in Integrations.

## Check the signature

`Arknet-Signature` looks like `t=1761411731,v1=5f2b…`. `v1` is an HMAC-SHA256, keyed with the signing secret, of `t`, a dot, and the raw request body. Check it, and reject old timestamps, before you trust an event.

**Node.js**

```js
const crypto = require('crypto');

function fromArknet(rawBody, header, secret, toleranceSeconds = 300) {
  const { t, v1 } = Object.fromEntries(header.split(',').map((part) => part.split('=')));
  const expected = crypto.createHmac('sha256', secret).update(`${t}.${rawBody}`).digest('hex');
  const fresh = Math.abs(Date.now() / 1000 - Number(t)) < toleranceSeconds;
  return fresh && crypto.timingSafeEqual(Buffer.from(v1, 'hex'), Buffer.from(expected, 'hex'));
}
```

**Python**

```python
import hashlib, hmac, time

def from_arknet(raw_body: bytes, header: str, secret: str, tolerance: int = 300) -> bool:
    parts = dict(part.split("=", 1) for part in header.split(","))
    signed = parts["t"].encode() + b"." + raw_body
    expected = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    fresh = abs(time.time() - int(parts["t"])) < tolerance
    return fresh and hmac.compare_digest(expected, parts["v1"])
```

## A tiny bot

A complete bot that answers `!ping`, using Node.js and Express:

```js
const express = require('express');
const crypto = require('crypto');

const KEY = process.env.ARKNET_BOT_KEY; // ark_bot_…
const SECRET = process.env.ARKNET_SIGNING_SECRET; // whsec_…
const ARKNET = 'https://arknet.si/api/cogs';

const app = express();
app.post('/arknet', express.text({ type: 'application/json' }), async (req, res) => {
  const { t, v1 } = Object.fromEntries(
    String(req.get('Arknet-Signature')).split(',').map((p) => p.split('=')),
  );
  const expected = crypto.createHmac('sha256', SECRET).update(`${t}.${req.body}`).digest('hex');
  if (v1 !== expected) return res.sendStatus(401);
  res.sendStatus(200); // answer first, then work

  const event = JSON.parse(req.body);
  if (event.type === 'message.created' && event.message.text.trim() === '!ping') {
    await fetch(`${ARKNET}/channels/${event.channel.id}/messages`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: 'pong', replyTo: event.message.id }),
    });
  }
});
app.listen(8080);
```

Put it on a public HTTPS address, set that address as the bot's Event URL, and say `!ping` in the server.
