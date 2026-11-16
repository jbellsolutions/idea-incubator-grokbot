# The Incubator worker box

GrokBot orchestrates and automates; this box does the work. Grok writes work orders to the desk (a private GitHub repo) and reads one small digest each morning. Everything heavy runs here, on the cheapest tier that can do it:

| Tier | What runs | What it costs |
|---|---|---|
| script | signals, paper marking, coin checks, sales, the digest, the watchdog, the desk sync | Nothing: plain Python on free public APIs |
| cli | dev builds, vetting, the factory run, creator-follow, the algo lab | Claude Code (Claude subscription) and Codex (ChatGPT subscription), flat; when one is out of usage the other takes over |
| hermes | Hermes agent packs, and anything Grok hands over that needs an agent loop | A model key with a monthly cap set by Justin |

The lanes, their tier and their schedule are in [jobs.json](jobs.json); the cron lines in [crontab.txt](crontab.txt).

## Which box

The Incubator's own box, never one another agent lives on:
- **A new DigitalOcean droplet** (default): Ubuntu 24.04, 2 vCPU / 4 GB, the smallest size that runs two CLIs and Hermes. It costs money every month: Justin's yes and his click.
- **An Orgo computer** Justin names for the Incubator only. Orgo adds a desktop, which the browser lanes can use later.

## Install (Justin starts it, the steps are copy-paste)

1. On the box, as root: `apt-get update && apt-get install -y unzip curl`, `curl -fsSL -o /root/idea-incubator.zip https://github.com/jbellsolutions/idea-incubator-grokbot/releases/latest/download/idea-incubator.zip`, `rm -rf /root/pack && unzip -q /root/idea-incubator.zip -d /root/pack`, `bash /root/pack/worker-box/install.sh /root/pack`. Running it again later (a new pack version) keeps the keys, the logins and the builds.
2. Keys, never in chat: `nano /opt/incubator/.secrets/worker.env` and fill the names (`DESK_REPO`, `GITHUB_TOKEN` scoped to the desk and private product repos, `GITHUB_OWNER`, `SLACK_WEBHOOK_URL`, optional `GUMROAD_ACCESS_TOKEN`, `ORGO_API_KEY`). Write the never-touch list to `/opt/incubator/.secrets/never-touch.txt`.
3. Claude Code, as the coder user: on your Mac run `claude setup-token` (Claude subscription), then on the box `sudo -u incubator-coder -i`, add `export CLAUDE_CODE_OAUTH_TOKEN=<token>` to `~/.profile`, and `chmod 600 ~/.profile`.
4. Codex, as the coder user: `sudo -u incubator-coder -i`, then `codex login` with your ChatGPT account (`codex login --device-auth` on a box with no browser: it prints a code to enter at the address it shows; the flag is in codex-cli 0.167 and later).
5. Hermes, as the jobs user: `sudo -u incubator -i`, then `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash` (Hermes' own installer; it lands in `~/.local/bin/hermes`, which `HERMES_BIN` in `worker.env` points at), `hermes profile create incubator-worker`, `cp /opt/incubator/repo/worker-box/hermes/SOUL.md ~/.hermes/profiles/incubator-worker/SOUL.md`, then `hermes -p incubator-worker model` and paste a model key that has a monthly cap set in the provider's console. Check: `hermes -p incubator-worker chat -q "Reply ok" -Q --oneshot`. *(Not yet run on a real box: if the installer puts `hermes` somewhere else, set `HERMES_BIN` to what `command -v hermes` prints.)*
6. Time and cron: `date` must show UTC (DigitalOcean's default; on an Orgo computer `ln -sf /usr/share/zoneinfo/UTC /etc/localtime`, since Orgo has no systemd and so no `timedatectl`), because the cron lines are UTC. `pgrep -x cron` must print a number: `install.sh` starts cron through systemd on a droplet and through supervisor on an Orgo computer, and warns if it couldn't.
7. The check, as `incubator`: `python3 /opt/incubator/repo/worker-box/bin/worker.py lanes`, then `worker.py run digest`. The digest appears on the desk at `outbox/digest/<date>.md`.

## Why two users

Claude Code and Codex read web pages, creators' repos and posts. They run as `incubator-coder`, which can't read `/opt/incubator/.secrets/`. The GitHub, Slack, Orgo and model keys stay with `incubator`, which only runs fixed scripts. No wallet key, seed phrase or exchange key with trade rights exists on this box, ever: markets are research and paper only.

## The desk

| Folder | Written by | What |
|---|---|---|
| `inbox/orders/<day>/` | GrokBot | One new file per work order: lane and task |
| `inbox/beats/<day>/` | GrokBot | Grok's heartbeats; the watchdog alarms on 26 hours of silence |
| `outbox/results/<day>/` | Worker | One file per order: status and what happened |
| `outbox/digest/` | Worker | One short digest a day, for Grok's morning plan |
| `state/` | Worker | Signals, paper reports, sales |

Files are only ever added, never edited, so the two sides never collide. Folders split by day keep each listing small (GitHub lists at most 1,000 files a folder). A new box starts a cursor at its first tick and never replays older orders. `repo/desk/desk.py` is the client for both.

## STOP

`touch /opt/incubator/context/STOP` stops every job on the box; GrokBot's own STOP stops new orders.
