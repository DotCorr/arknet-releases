# Arknet

Arknet is where communities talk: servers with channels and threads, direct messages, voice and video calls. It's made by [Dotcorr](https://github.com/DotCorr), and it's where Cog-S, Dotcorr's AI organism, is cultivated.

This repository is Arknet's public home for **releases**, the **changelog** and the **developer docs**. Arknet's own source code is private.

- **Use Arknet:** [arknet.si](https://arknet.si)
- **What's new:** [CHANGELOG.md](CHANGELOG.md) and [Releases](https://github.com/DotCorr/arknet-releases/releases). Every release is also posted in the `#changelog` channel of the Arknet server.
- **Build on Arknet:** [docs/](docs/index.md)

## Developer docs

| | |
| --- | --- |
| [Build on Arknet](docs/index.md) | What you can build, and where to start |
| [Connect an AI agent (MCP)](docs/mcp.md) | Claude, ChatGPT, Cursor, VS Code and any MCP client |
| [API keys](docs/api-keys.md) | Keys that act as you, with the permissions you choose |
| [Bots](docs/bots.md) | A server's bot: its own account, key and signed events |
| [Webhooks](docs/webhooks.md) | Post into a channel from anything, and receive events |
| [Automations](docs/automations.md) | When-this-then-that rules for a server, no code needed |
| [Invites, rules and links](docs/invites.md) | Channel and message links, invite links and approval, rules, slow mode, AutoMod |
| [REST API](docs/api.md) | Endpoints, limits and the realtime socket ([OpenAPI](docs/openapi.json)) |

AI agents can read the whole set from [llms.txt](llms.txt), or from [arknet.si/llms.txt](https://arknet.si/llms.txt).

## Feedback

Found a bug in the docs, or missing something you'd like to build? [Open an issue](https://github.com/DotCorr/arknet-releases/issues). To report a safety problem on Arknet itself, use the Report button in the app or see [arknet.si/safety](https://arknet.si/safety).

## For maintainers

- **Docs:** the docs come from the platform repository's `client/public/docs`. To refresh them, run `python3 scripts/sync-docs.py <path to arknet-platform>`.
- **Releases:** publishing a release here posts it to Arknet's `#changelog` through the Releases bot. See [.github/workflows/post-release-to-arknet.yml](.github/workflows/post-release-to-arknet.yml). It needs:
  - the `ARKNET_BOT_KEY` secret: the bot's key, from Server settings → Integrations in the Arknet server
  - the `ARKNET_CHANGELOG_CHANNEL` variable: the `#changelog` channel's id
  - optionally, the `ARKNET_URL` variable, which defaults to `https://arknet.si`
