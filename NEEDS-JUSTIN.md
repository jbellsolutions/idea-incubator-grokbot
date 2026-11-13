# NEEDS-JUSTIN: Incubator

Only what Justin can do. Each line: what, the exact click or command, what it unblocks. Ticked off in order when he works the list. The worker box comes first: GrokBot only orchestrates.

| # | What | The exact step | What it unblocks |
|---|---|---|---|
| 1 | [ ] The worker box (spend, or a computer you name) | Say "droplet" (a new DigitalOcean droplet, Ubuntu 24.04, 2 vCPU / 4 GB, a monthly cost, your click in DigitalOcean) or name an Orgo computer for the Incubator only | Every heavy job off GrokBot's usage |
| 2 | [ ] Install on the box | As root: unpack the pack, `bash <pack>/worker-box/install.sh <pack>` (worker-box/INSTALL.md) | The worker |
| 3 | [ ] Worker keys, typed on the box | `nano /opt/incubator/.secrets/worker.env`: `DESK_REPO`, `GITHUB_TOKEN` (the worker's: desk plus private repos), `GITHUB_OWNER`, `SLACK_WEBHOOK_URL`, optional `GUMROAD_ACCESS_TOKEN`, `ORGO_API_KEY`; the never-touch list in `.secrets/never-touch.txt` | Desk, pushes, alarms, sales, Hermes builds |
| 4 | [ ] Claude Code on your Claude subscription | On your Mac `claude setup-token`; on the box `sudo -u incubator-coder -i`, `export CLAUDE_CODE_OAUTH_TOKEN=...` in `~/.profile`, `chmod 600 ~/.profile` | Builds, the factory, backtests |
| 5 | [ ] Codex on your ChatGPT subscription | On the box `sudo -u incubator-coder -i`, then `codex login` (device-code option on a box with no browser) | Vetting, creator research, the fallback when Claude is out of usage |
| 6 | [ ] Hermes model key with a monthly cap (spend) | Set the cap in the provider's console, then give the key to the `incubator-worker` Hermes profile on the box | hermes-build and ask lanes only |
| 7 | [ ] New Grok account for the Incubator | Make a new account (not one another business already uses), sign in at x.ai/bot, check the plan includes bots and routines; set a monthly additional-usage limit at grok.com/dashboard/billing | The orchestrator |
| 8 | [ ] Create the bot | Grok desktop app: new bot "Incubator", time zone UTC, paste the one-link line in HANDOFF.md Part 1 step 4 | Setup |
| 9 | [ ] Auto-review rules | Paste the Ask-first lines from GATES.md and the three usage lines from HANDOFF.md into Auto-review → Custom Rules | Safe routines |
| 10 | [ ] Slack channel | Make a private #incubator, add the bot's Slack app and an incoming webhook (the webhook URL is item 3's `SLACK_WEBHOOK_URL`) | Plans, scoreboard, idea drops, alarms |
| 11 | [ ] Bot sign-ins and keys | Gumroad and X through Connect apps or Take over; by hidden prompt `SLACK_BOT_TOKEN`, `NOTION_TOKEN`, `GITHUB_TOKEN` (the bot's: the desk repo only) | promoter, markets, lead |
| 12 | [ ] Intake values (not secrets) | When the bot asks, one at a time: `DESK_REPO`, `GITHUB_OWNER`, `GUMROAD_STORE_URL`, `PACK_RELEASE_URL`, `NOTION_PARENT_PAGE`, `SKILLS_SOURCE_REPO`, `HERMES_TEAM_TEMPLATE_REPO`, `NEVER_TOUCH` | The desk, listings, the Notion page; Orgo work stays held until the never-touch list exists |
| 13 | [ ] Paper bankroll and creators | Confirm 10000 paper, and name creators besides Moon Dev (each is one file on the box) | markets |
| 14 | [ ] Single brain path | "Deploy key" (the bot pushes its daily note) or "Mac pulls" | Reports reach the single brain |
| 15 | [ ] Approve the listing and post types once | Reply yes to the first Gumroad listing draft and the first X post draft; say "auto" for a type once it looks right | Listings and posts |
| 16 | [ ] Every trade, every time | Read tickets in Notion / `requests/justin/trades/`; place any you want yourself. Neither the bot nor the box ever will | Real money, only by you |
| 17 | [ ] Publishing a product | Follow each product's `marketing/LAUNCH.md`: make its repo public if you want, list on Gumroad | Products on sale |
