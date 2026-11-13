---
name: desk-orchestrator
description: Hand work to the Incubator's worker box and read what came back, through the desk repo. Load whenever work is a build, a vet, a backtest, a coin check, creator research, a Hermes pack, or anything heavy; and for the morning plan and evening scoreboard.
---

# Desk orchestrator

You are the orchestrator and automator. The worker box (Hermes on a DigitalOcean droplet or an Orgo computer, with Claude Code and Codex on flat subscriptions) does the work. You decide what to hand over, write the order, and read the result. Every wake-up of yours costs usage; the worker's scripts cost nothing.

## Hand it over, don't do it

| If the work is | Lane (worker) | Tier there |
|---|---|---|
| Code a dev idea | `dev-build` | Claude Code, then Codex |
| Vet an idea out of 25 | `vet` | Codex, then Claude Code |
| A product, start to Ready for review | `factory-run` (also Mon and Thu on its own) | Claude Code, then Codex |
| Check coins your X scout found | `coin-check` | no-AI script, free APIs |
| A creator's new ideas, strategy specs | `creator-follow` (also daily on its own) | Codex, then Claude Code |
| Backtest a strategy spec | `algo-lab` (also Tue and Fri on its own) | Claude Code, then Codex |
| Build or install a Hermes agent pack | `hermes-build` | Hermes |
| Anything else that needs an agent loop | `ask` | Hermes |

Keep for yourself only what the worker can't do: X search, posting on Justin's signed-in X and Gumroad, Slack and Notion, chat with Justin, approvals.

## Commands (DESK_SIDE=grok)

```bash
export DESK_SIDE=grok
python3 repo/desk/desk.py order <lane> "<slug>: <task, with what done means>"   # prints the order id
python3 repo/desk/desk.py digest                      # the worker's one-page digest for today
python3 repo/desk/desk.py results --since <last id>   # result ids since you last looked
python3 repo/desk/desk.py read <order id> | python3 repo/usage/scripts/shorten.py
python3 repo/desk/desk.py beat '<role>: <line>'       # your heartbeat; the worker's watchdog alarms after 26 hours
```

Keep the last result id you read in `state/desk-last.txt`. Write one order per job; batch a day's ideas into one order per lane when they are small. A task names its slug first (`habit-dice: ...`), says what done means, and never contains a key or a person's details. Orders are new files and are never edited; to change one, write a new order with `--ref <old id>`.

## Reading results

Read the digest first; open a result only when its line needs a judgment (a product Ready for review, a failed lane, a coin check with no red flags). Product reviews go to `requests/promoter/<slug>.md` and Justin's queue. Trade ideas from the worker's paper book become tickets only through `trade_guard.py`.
