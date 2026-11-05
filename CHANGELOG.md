# Changelog

What changed in each Arknet release. Versions follow [semantic versioning](https://semver.org); everything before 1.0 is a preview.

## v0.2.5: Match device follows your Mac

- **Match device:** with the theme set to Match device, Arknet follows your Mac's light or dark appearance in every window, without a reload.
- **New windows in your colours:** a new window, like settings, starts in your theme's colours instead of dark.

## v0.2.4: calls that keep ringing, and full screen

- **Calls keep ringing:** a call no longer goes quiet when another Arknet window reloads or closes while it rings, and a ring that goes quiet on its own starts again within a second.
- **Full screen on a Mac:** the server list and settings start at the top of the screen, without the empty band kept for the traffic lights, which come down with the menu bar.

## v0.2.3: calls that reach you, and an .rpm

- **Calls ring with the window closed:** on a Mac, closing the window no longer stops Arknet listening. It rings with its own sound, bounces its Dock icon until the call ends, and shows a notification you can answer or decline from.
- **Notifications on a Mac:** macOS asks once whether Arknet may notify you, and Arknet appears in System Settings > Notifications.
- **Right-click menus:** servers, channels, direct messages and messages get a proper menu: Open in a New Window, invites, server settings, reply, react, pin, Copy Link and more.
- **Settings in a window of their own:** Arknet > Settings (Cmd+,) and the settings button open one settings window.
- **No title bar:** the window's top belongs to Arknet. On a Mac the traffic lights sit over the server list and the sidebar is frosted. On Linux, Arknet draws its own window buttons.
- **Linux:** an `.rpm` for Fedora and openSUSE, beside the `.deb` and the AppImage. The `.deb` and the `.rpm` now update themselves.

## v0.2.1: more like a desktop app

- **Several windows:** File > New Window (Cmd+N, or Ctrl+N on Linux), and Open This Page in a New Window (Cmd+Shift+N, or Ctrl+Shift+N).
- **A cleaner title bar:** it takes the colour of the page instead of standing apart from it.
- **Location on a Mac:** the map and location sharing now ask macOS, so they can work in the app.
- **Dropped files:** files you drag onto the window now reach the page.

## v0.2.0: the Mac and Linux apps

Arknet in its own window, for Mac and Linux. Get them from [Releases](https://github.com/DotCorr/arknet-releases/releases/tag/v0.2.0).

- **Mac:** signed and notarized by Apple, for Intel and Apple silicon, on macOS 12 or later.
- **Linux:** a `.deb` and an AppImage. Calls don't work in the Linux app yet, so it offers to open them in your browser.
- Google and GitHub sign-in run in your browser and come back to the app.
- Downloads, notifications and the unread badge use your system's own.
- The app updates itself. The Arknet inside it updates with the site.

## v0.1.0: preview

The first public preview of Arknet.

### Talk

- Servers with text and voice channels, categories, and threads that nest five deep and fold away in the channel list.
- Direct messages and group DMs, replies, @mentions, reactions, pins, file uploads, and per-channel drafts.
- Channel icons, server icons, banners and wallpapers.
- Voice and video calls that ring like a phone, with the caller's name, a missed-call log, screen sharing, and a pop-out window that stays on top.
- An "In a call" status that sets and clears itself.
- A notification center for mentions, replies, missed calls, friend requests and market news.
- Sign in with email, Google or GitHub.

### Cog-S and cultivation

- Cultivation rooms and a hub that follows Cog-S's development.
- A cultivation market: list a server's cultivation, and merge others into your own, with payouts through Stripe Connect.

### Safety and privacy

- Platform rules on everything posted, reports a person decides, statements of reasons, and appeals.
- Privacy controls: blocking, who can DM you, see you online or find you, and whether Cog-S may learn from your messages.
- Protections for members under 18. You can download your data or delete your account.

### Build on Arknet

- **API keys** that act as you, with read, write and manage permissions. Posts made with them are labelled *via AI agent*.
- **MCP**: connect Claude, ChatGPT, Cursor, VS Code or any MCP client.
- **Bots**: a server's own member, driven by a key, with signed events.
- **Incoming webhooks** to post from GitHub, CI or monitoring.
- **Automations**: greet newcomers, answer keywords, post on a schedule, or forward to Slack and Discord.
- [Developer docs](docs/index.md) and an [OpenAPI description](docs/openapi.json).
