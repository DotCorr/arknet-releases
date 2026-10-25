# Webhooks

Webhooks connect Arknet to everything else, in both directions.

- **Incoming:** a secret URL that anything can `POST` to, to say something in one channel. Use it for deploys, alerts, form submissions or scripts.
- **Outgoing:** Arknet sends what happens in a server to a URL of yours. Your [bot](bots.md#events-let-arknet-tell-your-bot) can get events, and an [automation](automations.md) can send them on to Slack, Discord, Zapier, Make or n8n.

## Incoming webhooks

### Make one

Owners and moderators open **Server settings → Integrations → Incoming webhooks**, name it (say, "Deploys") and pick a channel. Arknet shows the URL **once**:

```
https://arknet.si/api/cogs/hooks/6730f9b2c3d4e5f607182930/Xb7…
```

The last part is the secret. Anyone with the URL can post to that channel, so keep it out of public code. Delete the webhook to switch the URL off at once.

### Post to it

Send JSON with `text` and, optionally, a `username` to show instead of the webhook's name:

```bash
curl -X POST https://arknet.si/api/cogs/hooks/WEBHOOK_ID/SECRET \
  -H "Content-Type: application/json" \
  -d '{"text": "Deploy finished: v1.4.2 is live", "username": "CI"}'
```

Arknet also reads Discord-style `content`, so many tools that post to Discord work as they are.

The message appears with an **App** badge. Markdown works, as in the app.

### Answers

| Status | Meaning |
| --- | --- |
| `200` | Posted: `{ "id": "<message id>", "channelId": "…" }` |
| `400` | Nothing to say: send `text` or `content` |
| `404` | Unknown webhook, or a wrong secret |
| `410` | The webhook's channel was deleted |
| `422` | Arknet's safety rules refused it; `error` says why |
| `429` | More than 30 posts in a minute; slow down |

### Examples

**GitHub Actions**, as a step at the end of a deploy job:

```yaml
- name: Tell Arknet
  run: |
    curl -sS -X POST "$ARKNET_WEBHOOK" \
      -H "Content-Type: application/json" \
      -d "{\"text\": \"Deployed ${GITHUB_SHA::7} to production\", \"username\": \"GitHub\"}"
  env:
    ARKNET_WEBHOOK: ${{ secrets.ARKNET_WEBHOOK }}
```

**Python**

```python
import json, urllib.request

def say(url: str, text: str) -> None:
    body = json.dumps({"text": text}).encode()
    request = urllib.request.Request(url, body, {"Content-Type": "application/json"})
    urllib.request.urlopen(request, timeout=10)

say(WEBHOOK_URL, "The nightly backup finished.")
```

## Outgoing events

Arknet sends events as signed JSON `POST`s, from the address you set in two places:

- a **bot's Event URL**: the server's messages and joins. See [Bots → Events](bots.md#events-let-arknet-tell-your-bot).
- an **automation's "Send it to a URL" action**: what that automation reacts to. See [Automations](automations.md#send-it-to-a-url).

Every delivery has these headers:

| Header | Value |
| --- | --- |
| `Arknet-Event` | The event type, such as `message.created` |
| `Arknet-Delivery` | A unique id; retries reuse it |
| `Arknet-Signature` | `t=<unix seconds>,v1=<hex>`: an HMAC-SHA256 of `t` + `.` + the raw body, keyed with the signing secret |
| `User-Agent` | `Arknet-Webhooks/1.0` |

Arknet waits 5 seconds for an answer. Anything but `2xx` is retried after 10 seconds and again after a minute; answer `410` to stop. Only public `https://` addresses are reached: private, internal and loopback addresses are refused, and the address is checked again at connection time.

To check a signature, see the code in [Bots → Check the signature](bots.md#check-the-signature).
