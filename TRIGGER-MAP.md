# Trigger map

The loop is deterministic: schedules start every step, and the agent makes only the judgment call inside it. Gates stay on until replies prove good. Every cron is UTC. **50 routines max per bot**: this bot uses 17, every pair at least 5 minutes apart across the week (checked). No webhook routines.

## The loop, step by step

| # | Step | Started by | Role | Judgment call | Human gate |
|---|---|---|---|---|---|
| 1 | Market brief and signals | Schedule `50 12 * * *` | markets | Which signals are worth a paper trade | None (paper only) |
| 2 | Plan the day | Schedule `30 13 * * *` | lead | What matters today in each lane | None |
| 3 | Read the Orgo workspace | Schedule `40 13 * * *` | hermes-builder | Is a named computer healthy | `orgo_guard.py` |
| 4 | Sweep ideas into the board | Schedule `15 */3 * * *` | dev | Vet score: queue, maybe or kill | None |
| 5 | Build the top dev idea | Schedule `45 14,19 * * *` | dev | Scope to cut; is the test real | Push private only |
| 6 | Factory run | Schedule `5 15 * * 1,4` | dev | Which product; is it ready for review | Justin reviews REVIEW.md |
| 7 | Product posts | Schedule `40 15 * * *` | promoter | Hook and angle; is it new vs his last 20 posts | `send_guard.py`; first post is Justin's |
| 8 | Follow a creator | Schedule `35 16 * * *` | markets | Which idea is testable | None (research) |
| 9 | Gumroad listing drafts | Schedule `20 17 * * *` | promoter | Title, price, copy | `send_guard.py`; first listing is Justin's |
| 10 | Algo lab | Schedule `10 18 * * 2,5` | markets | Is the backtest honest (out-of-sample) | None (historical data) |
| 11 | Build or install a Hermes pack | Schedule `25 18 * * *` | hermes-builder | Pack design; does it pass its checklist | `orgo_guard.py`, `spend_guard.py` |
| 12 | Crypto scout on X | Schedule `25 1,5,9,13,17,21 * * *` | markets | Real momentum or a shill; scam checks | `trade_guard.py` holds any trade |
| 13 | Mark the paper book | Schedule `35 2,8,14,20 * * *` | markets | Close on stop rules | None (paper) |
| 14 | Sales proof | Schedule `10 23 * * *` | promoter | Is each sale a real Gumroad record | None (read-only) |
| 15 | Report | Schedule `30 23 * * *` | lead | Proof check on each number | None |
| 16 | Weekly paper review | Schedule `50 21 * * 0` | markets | Which strategy earns a ticket | `trade_guard.py`: Justin places it or not |

## Every schedule and event, by role

### lead

| Kind | When or what | Does |
|---|---|---|
| Schedule | `30 13 * * *` | LEAD-PLAN: morning plan |
| Schedule | `0 */3 * * *` | LEAD-WATCH: watchdog |
| Schedule | `30 23 * * *` | LEAD-SCORE: evening scoreboard and vault daily note |

### dev

| Kind | When or what | Does |
|---|---|---|
| Schedule | `15 */3 * * *` | DEV-INTAKE: sweep new ideas into the board |
| Schedule | `45 14,19 * * *` | DEV-BUILD: move the top dev idea forward with Claude Code |
| Schedule | `5 15 * * 1,4` | FACTORY-RUN: vet, pick, build, package one product |

### promoter

| Kind | When or what | Does |
|---|---|---|
| Schedule | `40 15 * * *` | PROMO-POSTS: draft or post today's product posts |
| Schedule | `20 17 * * *` | PROMO-LISTINGS: Gumroad listing drafts |
| Schedule | `10 23 * * *` | PROMO-SALES: sales proof |

### markets

| Kind | When or what | Does |
|---|---|---|
| Schedule | `50 12 * * *` | MKT-BRIEF: market brief and signals |
| Schedule | `25 1,5,9,13,17,21 * * *` | MKT-SCOUT: crypto scout on X |
| Schedule | `35 2,8,14,20 * * *` | MKT-MARK: mark the paper book |
| Schedule | `35 16 * * *` | MKT-CREATOR-MOONDEV: follow Moon Dev |
| Schedule | `10 18 * * 2,5` | MKT-ALGO-LAB: code and backtest queued strategies |
| Schedule | `50 21 * * 0` | MKT-WEEKLY: paper review |

A new creator is one more routine `MKT-CREATOR-<NAME>` (pick a minute 5+ away from every other) and one file in `skills/markets/creator-follow/creators/`.

### hermes-builder

| Kind | When or what | Does |
|---|---|---|
| Schedule | `40 13 * * *` | HB-CHECK: read the workspace, check named computers |
| Schedule | `25 18 * * *` | HB-BUILD: build or install the next queued pack |
