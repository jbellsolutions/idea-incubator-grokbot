# NEEDS-JUSTIN: Incubator

Only what Justin can do, in dependency order. Each item: the exact click or command, what it costs if it is spend, what it needs first, and what it unblocks. Tick them off in order. The worker box comes first: GrokBot only orchestrates.

Prices were read on 2026-11-15. Spend items are marked **SPEND**.

## A. One decision (needs nothing)

- [ ] **1. Which worker box.** Say `droplet`, or name an Orgo computer used for the Incubator only.
  - `droplet`: a new DigitalOcean droplet, Ubuntu 24.04, 2 vCPU / 4 GB / 80 GB (`s-2vcpu-4gb`). **SPEND: $24.00 a month** ($0.03571 an hour), DigitalOcean's own price list.
  - Orgo: a Linux computer, 2 vCPU / 4 GB / 40 GB. **SPEND: about $20 a month** as plan add-ons ($2.50 per GB of RAM and $2.50 per half vCPU, from orgo.ai/pricing.md; that size is not listed, so the total is worked out from those rates), or nothing extra if the plan has unused capacity.
  - The installer was run end to end on Ubuntu 24.04 in a local container (systemd absent, with and without supervisor). It has not run on a real droplet or a real Orgo computer yet.
  - Unblocks: items 7 to 13, every heavy job off GrokBot's usage.

## B. Can be done now, before the box exists (need nothing)

- [ ] **2. The worker's GitHub token.** github.com → Settings → Developer settings → Fine-grained tokens → Generate new token. Name `incubator-worker`. Pick one:
  - Desk only (start here): Repository access → Only select repositories → the desk repo; Permissions → Contents: Read and write. Builds then stay on the box and each result says `not pushed`.
  - Desk plus private product repos: Repository access → All repositories; Contents: Read and write, Administration: Read and write. GitHub needs Administration to create a repo, and that permission can also delete repos and change visibility. `worker.py` only ever creates private repos and refuses to push to a public one, but the token itself is that strong.
  - Keep the token in your password manager until item 9. Unblocks: the desk (orders in, results and digest out).
- [ ] **3. Slack channel and webhook.** Slack → new private channel `#incubator`. Then api.slack.com/apps → Create New App → From scratch → Incoming Webhooks → on → Add New Webhook to Workspace → `#incubator`. Keep the webhook URL for item 9 (`SLACK_WEBHOOK_URL`). Unblocks: watchdog alarms; later the bot's plans and scoreboard.
- [ ] **4. Claude Code token.** On your Mac: `claude setup-token` (your Claude subscription, no new spend). Keep the token for item 10. Unblocks: dev builds, the factory, backtests.
- [ ] **5. Hermes model key with a monthly cap. SPEND: the cap you set.** In the model provider's console, make a key for the Incubator and set its monthly limit there. Keep it for item 12. Unblocks: the `hermes-build` and `ask` lanes only; everything else runs without it.
- [ ] **6. New Grok account for the Incubator. SPEND if the plan is paid (price not checked).** Make a new account (not one another business already uses), sign in at x.ai/bot, check the plan includes bots and routines, and set a monthly additional-usage limit at grok.com/dashboard/billing. Unblocks: items 14 to 19.

## C. The worker box (needs item 1)

- [ ] **7. Create the box. SPEND, see item 1.** Your typed yes, every time.
  - Droplet: `doctl compute droplet create incubator-worker --image ubuntu-24-04-x64 --size s-2vcpu-4gb --region nyc3 --ssh-keys <your-ssh-key-id> --enable-monitoring --tag-name incubator --wait --format Name,PublicIPv4,Status` (key ids: `doctl compute ssh-key list`). Or in the console: Create → Droplets → New York → Ubuntu 24.04 (LTS) x64 → Basic, Regular, $24/mo (4 GB / 2 CPUs / 80 GB) → your SSH key → hostname `incubator-worker` → Create.
  - Orgo: `orgo computers create --name incubator-worker --os linux --cpu 2 --ram 4 --disk 40`.
- [ ] **8. Install.** Your typed yes. As root on the box (droplet: `ssh root@<ip>`; Orgo: the computer's terminal), four lines:

  ```bash
  apt-get update && apt-get install -y unzip curl
  curl -fsSL -o /root/idea-incubator.zip https://github.com/jbellsolutions/idea-incubator-grokbot/releases/latest/download/idea-incubator.zip
  rm -rf /root/pack && unzip -q /root/idea-incubator.zip -d /root/pack
  bash /root/pack/worker-box/install.sh /root/pack
  ```

  It makes two users, installs Node, Claude Code, Codex and `gh`, the cron lines and an empty key file. It installs no keys and creates nothing that costs money. On an Orgo computer also run `ln -sf /usr/share/zoneinfo/UTC /etc/localtime`. Unblocks: items 9 to 13.
- [ ] **9. Worker keys, typed on the box** (needs 2 and 3). `nano /opt/incubator/.secrets/worker.env` and fill `DESK_REPO` (owner/name), `GITHUB_TOKEN` (item 2), `GITHUB_OWNER`, `SLACK_WEBHOOK_URL` (item 3); optional `GUMROAD_ACCESS_TOKEN` (Gumroad → Settings → Advanced → Applications, read sales) and `ORGO_API_KEY`. Then one name per line in `nano /opt/incubator/.secrets/never-touch.txt` and `chown incubator:incubator /opt/incubator/.secrets/never-touch.txt; chmod 600 /opt/incubator/.secrets/never-touch.txt`. Unblocks: the desk, alarms, sales, private pushes; Orgo work stays held until the never-touch list exists.
- [ ] **10. Claude Code on the box** (needs 4). `sudo -u incubator-coder -i`, then `echo 'export CLAUDE_CODE_OAUTH_TOKEN=<token>' >> ~/.profile; chmod 600 ~/.profile`. Check: `claude -p "Reply ok"`. Unblocks: `dev-build`, `factory-run`, `algo-lab`.
- [ ] **11. Codex on the box.** `sudo -u incubator-coder -i`, then `codex login --device-auth` and enter the code it prints at the address it shows, with your ChatGPT account (no new spend). Check: `codex exec --skip-git-repo-check "Reply ok"`. Unblocks: `vet`, `creator-follow`, and the fallback when Claude is out of usage.
- [ ] **12. Hermes on the box** (needs 5). `sudo -u incubator -i`, then:

  ```bash
  curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
  hermes profile create incubator-worker
  cp /opt/incubator/repo/worker-box/hermes/SOUL.md ~/.hermes/profiles/incubator-worker/SOUL.md
  hermes -p incubator-worker model
  ```

  Paste the capped key when `hermes model` asks. Check: `hermes -p incubator-worker chat -q "Reply ok" -Q --oneshot`. Unblocks: `hermes-build`, `ask`.
- [ ] **13. The check** (needs 9). As `incubator`: `. /opt/incubator/.secrets/worker.env; python3 /opt/incubator/repo/worker-box/bin/worker.py lanes`, then `python3 /opt/incubator/repo/worker-box/bin/worker.py run digest`. Pass: it prints `done` and `outbox/digest/<date>.md` is on the desk. Unblocks: the bot's first plan has a digest to read.

## D. The bot (needs 6; best after 13)

- [ ] **14. Create the bot.** Grok desktop app: new bot "Incubator", time zone UTC, paste the one-link line in HANDOFF.md Part 1 step 4. Unblocks: setup.
- [ ] **15. Auto-review rules.** Paste the Ask-first lines from GATES.md and the three usage lines from HANDOFF.md into Auto-review → Custom Rules. Unblocks: safe routines.
- [ ] **16. Bot sign-ins and keys.** Gumroad and X through Connect apps or Take over; add the bot's Slack app to `#incubator`; by hidden prompt `SLACK_BOT_TOKEN`, `NOTION_TOKEN`, `GITHUB_TOKEN` (the bot's own fine-grained token: the desk repo only, Contents read and write; made like item 2, named `incubator-bot`). Unblocks: promoter, markets, lead; the Slack, Notion, GitHub and Desk checks.
- [ ] **17. Intake values (not secrets).** When the bot asks, one at a time: `DESK_REPO`, `GITHUB_OWNER`, `GUMROAD_STORE_URL`, `PACK_RELEASE_URL`, `NOTION_PARENT_PAGE`, `SKILLS_SOURCE_REPO`, `HERMES_TEAM_TEMPLATE_REPO`, `NEVER_TOUCH`. Unblocks: the desk, listings, the Notion page.
- [ ] **18. Paper bankroll and creators.** Confirm 10000 paper, and name creators besides Moon Dev (each is one file on the box). Unblocks: markets.
- [ ] **19. Single brain path.** Say "deploy key" (the bot pushes its daily note) or "Mac pulls". Unblocks: reports reach the single brain.

## E. After the first-day test run (needs 13 to 18)

- [ ] **20. Approve the listing and post types once.** Reply yes to the first Gumroad listing draft and the first X post draft; say "auto" for a type once it looks right. Unblocks: listings and posts.
- [ ] **21. Every trade, every time.** Read tickets in Notion / `requests/justin/trades/`; place any you want yourself. Neither the bot nor the box ever will. Real money, only by you.
- [ ] **22. Publishing a product.** Follow each product's `marketing/LAUNCH.md`: make its repo public if you want, list on Gumroad. Unblocks: products on sale.
