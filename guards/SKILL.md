---
name: bot-guards
description: The checks every role runs in code before it drafts, sends, spends, trades or touches an Orgo computer, and the heartbeat it writes at the end. Load on every run.
---

# Guards

These are code, not advice. Run them; don't reason around them. Paths are relative to the workspace.

| Before you | Run | It answers |
|---|---|---|
| Draft to anyone | `python3 repo/guards/scripts/suppression.py check "<name, business, email or url>"` | `clear` or `held`. Held means stop on that person |
| Someone says no | `python3 repo/guards/scripts/suppression.py add "<who>" "<reason>"` | Done for every role |
| Send anything | `python3 repo/guards/scripts/send_guard.py <message-type> --routine <NAME>` | `auto`, `draft` or `stopped`. Draft means it goes to `requests/justin/` |
| Spend anything | `python3 repo/guards/scripts/spend_guard.py <plan-id> <usd>` | `approved` or `held`. Held means the plan and its cost go to `requests/justin/` |
| Anything that moves money (order, swap, wallet funding, transfer, exchange connection) | `python3 repo/guards/scripts/trade_guard.py ticket <symbol> <side> <usd> "<thesis>"` | Always `held`; files a ticket in `requests/justin/trades/`. There is no way to approve it in the bot |
| A paper trade | `python3 repo/guards/scripts/paper_ledger.py open\|close\|mark\|report ...` | `opened`, `closed`, or `held` over the paper risk rule (5% a position, 30% open) |
| Any Orgo call, reads included | `python3 repo/guards/scripts/orgo_guard.py check "<computer>" <action>` | `clear` or `held`. Never-touch computers, unnamed computers, spend without approval, stop/delete are held. `orgo.py` runs it itself too |
| End a run | `python3 repo/guards/scripts/beat.py write <role> '<line>' found=N drafted=N sent=N` | Your heartbeat. The watchdog alarms on a silent role |
| Watchdog | `python3 repo/guards/scripts/beat.py status --hours 26` | `SILENT <role>` lines to alarm on |

Never print the suppression list, read `.secrets/`, or edit a guard or a switch file to get past it.
