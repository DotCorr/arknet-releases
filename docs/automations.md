# Automations

Automations are a server's own small rules: *when this happens, do that*. They need no code. Owners and moderators set them up in **Server settings → Integrations → Automations**, starting from a template or from scratch.

## When

| Trigger | Fires when | Options |
| --- | --- | --- |
| **A message arrives** | someone posts | one channel or any; optionally only when it contains a word or phrase (whole words, any case) |
| **Someone joins** | a person joins the server | |
| **At a set time** | the clock says so | every hour (at a minute), every day or every week (at a time, in UTC) |

## Do

### Say something in a channel

Arknet posts your text in the channel you pick, under the automation's name, with an **App** badge. These are filled in:

| Placeholder | Becomes |
| --- | --- |
| `{user}` | who posted, or who joined |
| `{channel}` | where they posted |
| `{server}` | the server's name |
| `{text}` | what they said |

### Send it to a URL

Arknet sends the event as JSON to an address you give. Slack and Discord incoming-webhook URLs work as they are: the body carries `text`, which Slack reads, and `content`, which Discord reads. Zapier, Make, n8n and IFTTT "catch hook" URLs receive the whole event:

```json
{
  "id": "0c9e8a52-3b1d-4f7e-9a61-2f5d8c4b7e10",
  "type": "message.created",
  "createdAt": "2026-10-25T09:00:03.412Z",
  "automation": { "id": "6731…", "name": "Forward bugs" },
  "server": { "id": "6730…", "name": "Cognitus Lab" },
  "channel": { "id": "6730…", "name": "support" },
  "user": "ada",
  "message": { "id": "6731…", "authorName": "ada", "text": "found a bug in the export" },
  "text": "ada in #support: found a bug in the export",
  "content": "ada in #support: found a bug in the export"
}
```

What Arknet sends is signed like every [outgoing event](webhooks.md#outgoing-events). The automation's signing secret is in its settings.

## Ideas

- **Welcome new members:** when someone joins, say *"Welcome, {user}! Tell us what brings you here."* in #general.
- **Point to the rules:** when a message contains "rules", say *"Hi {user}, the rules are pinned in this channel."*
- **Bugs to your tracker:** when a message in #support contains "bug", send it to a Zapier or Linear webhook.
- **A daily check-in:** every day at 08:00 UTC, say *"Good morning! What are you working on today?"* in #standup.
- **A weekly digest prompt:** every Friday at 16:00 UTC, ask the team to share wins in #wins.

## Rules that keep it sane

- **No loops.** Automations only react to people. They never react to bots, webhooks or other automations, including themselves.
- **Limits.** A server can have 25 automations, and its automations run at most 30 times a minute.
- **Safety.** What automations say goes through Arknet's safety rules like anything else.
- **Try it.** **Try it** runs an automation once, with sample details, so you can check a message or a URL.
- **Errors show.** If a run fails (a deleted channel, a URL that doesn't answer), the reason appears under the automation until it next works.
- **One run per slot.** A scheduled automation runs once per slot, even when Arknet runs on several machines.
