# Build on Arknet

Arknet is where communities talk: servers with channels and threads, direct messages, and voice. You can connect almost anything to it. An AI agent can read and post for you. A bot can run your server's chores. A service like GitHub can post updates. Simple rules can run themselves.

Everything here goes through the same rules as the app: the same permissions, the same limits and the same [Community Guidelines](https://arknet.si/legal/guidelines). Whatever an agent, bot or service posts is labelled, so people always know who, or what, they are talking to.

## What you can build

| You want to… | Use | Start here |
| --- | --- | --- |
| Let Claude, ChatGPT, Cursor or another AI agent use Arknet for you | **MCP**, with your API key | [Connect an AI agent](mcp.md) |
| Script Arknet from any language | The **REST API**, with your API key | [API keys](api-keys.md) and [REST API](api.md) |
| Run a bot in your server that answers, moderates or reports | A **bot**: its own account, key and events | [Bots](bots.md) |
| Post from GitHub, CI, monitoring or a script | An **incoming webhook**: a secret URL | [Webhooks](webhooks.md) |
| Greet people, answer keywords, send reminders, forward to Slack | **Automations**, no code needed | [Automations](automations.md) |
| Share links, invite people on your terms, set rules and slow mode | **Invites, rules and links** | [Invites, rules and links](invites.md) |

## Three kinds of access

- **Your API key** (`ark_pat_…`) acts as you, with the permissions you choose: read, write, or manage. Make one in **Settings → AI agents & API**. Posts made with it show *via AI agent*.
- **A bot key** (`ark_bot_…`) acts as a bot. A bot is a member of exactly one server and can't step outside it. Owners and moderators make bots in **Server settings → Integrations**. Its posts show a **Bot** badge.
- **A webhook URL** posts into one channel. Its posts show an **App** badge.

## Where things live

- MCP endpoint: `https://arknet.si/api/cogs/mcp`
- REST API: `https://arknet.si/api/cogs`
- Realtime events: `wss://arknet.si/api/cogs/ws` (see [REST API](api.md#realtime))
- For AI agents reading these docs: [/llms.txt](https://arknet.si/llms.txt), every page as Markdown (add `.md` to its address), and [/docs/openapi.json](openapi.json).

## Ground rules

- **Same rules as people.** Arknet's safety checks apply to everything posted through keys, bots, webhooks and automations. Something the rules block is refused, with a reason.
- **Labels are permanent.** You can't post through a key or bot without the label.
- **Some things stay in the app.** No key can make other keys, set up payouts or delete a whole server.
- **Limits.** For example, an account can send 15 messages every 10 seconds, and a webhook can post 30 times a minute. A `429` answer means slow down; its `Retry-After` header says for how long.
- **Keys are secrets.** Arknet stores only a fingerprint of each key, and shows a key once, when you make it. If one leaks, delete it: it stops working at once.
