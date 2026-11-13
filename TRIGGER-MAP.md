# Trigger map

GrokBot is the orchestrator and automator. It wakes 5 times a day (35 runs a week, down from about 376 in v1), and only for what it alone can do: X search, signed-in posting, Slack and Notion, chat and approvals. Everything heavy runs on the worker box (`worker-box/`), on the cheapest tier that can do it: a no-AI script, then Claude Code or Codex on flat subscriptions, then Hermes. The desk repo carries orders one way and results the other. Every cron is UTC. **50 routines max per bot**; this bot uses 5, at least 5 minutes apart.

## The loop, step by step

| # | Step | Started by | Where | Judgment call | Human gate |
|---|---|---|---|---|---|
| 1 | Sales, signals, digest | Worker cron `0 12`, `10 12`, `20 12` | worker (script) | None: code | None (read-only, paper) |
| 2 | Plan the day, write orders | Schedule `30 13 * * *` | Grok: lead | What matters today; which ideas get built | None |
| 3 | Run orders | Worker cron every 10 minutes | worker (script, cli or hermes) | Inside the CLI or Hermes job | Push to private repos only |
| 4 | Scout X, hand candidates over | Schedule `25 14 * * *` | Grok: markets | Real momentum or a shill | `trade_guard.py` holds any trade |
| 5 | Listings and posts | Schedule `40 15 * * *` | Grok: promoter | Hook and angle; new vs his last 20 posts | `send_guard.py`; first post and listing are Justin's |
| 6 | Factory run, creator-follow, algo lab | Worker cron (Mon/Thu, daily, Tue/Fri) | worker (cli) | Inside the job | None (private repos, historical data) |
| 7 | New ideas to orders, results to the queue | Schedule `45 19 * * *` | Grok: lead | Vet or build; is a product ready for Justin | Justin reviews REVIEW.md |
| 8 | Report | Schedule `30 23 * * *` | Grok: lead | Proof check on each number | None |
| 9 | Watchdog | Worker cron hourly | worker (script) | None: code | Alarms to Slack |

The worker's own schedule is in `worker-box/jobs.json` and `worker-box/crontab.txt`; none of it is a Grok routine and none of it wakes Grok.

## Every schedule and event, by role

### lead

| Kind | When or what | Does |
|---|---|---|
| Schedule | `30 13 * * *` | LEAD-PLAN: read the digest, plan, write the day's orders |
| Schedule | `45 19 * * *` | DESK-SYNC: new ideas to orders, results to the queue |
| Schedule | `30 23 * * *` | LEAD-SCORE: scoreboard, vault note, heartbeat on the desk |

### promoter

| Kind | When or what | Does |
|---|---|---|
| Schedule | `40 15 * * *` | PROMO-POSTS: listing and post drafts, or publish approved ones |

### markets

| Kind | When or what | Does |
|---|---|---|
| Schedule | `25 14 * * *` | MKT-SCOUT: X search, candidates to the worker |
