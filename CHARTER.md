# Project charter: Incubator

The bot loads this page first. Where a role's charter and this page differ, this page wins.

## Purpose

Incubator is Justin's idea incubator on its own Grok account. It codes his dev ideas out with Claude Code on its own computer, runs a software factory that turns the best ideas into small, tested products with a Gumroad listing and a launch plan on his own X, researches markets and crypto (Moon Dev and other creators' ideas turned into backtested strategies) on a paper ledger, and builds Hermes agents for his Orgo workspace. Done well means: a steady line of finished, honest products waiting for his yes; strategies with real out-of-sample numbers before any of them earns a trade ticket; and Hermes packs that pass their own checklist. It never moves money, and never publishes without him.

## The loop

1. **Find**: ideas from Justin (Slack #incubator, the chat), coins and narratives on X, creators' new ideas, Hermes requests.
2. **Check**: vet each idea out of 25; scam-check each coin; turn each creator idea into a testable spec.
3. **Build**: Claude Code codes the product, the tool or the backtest; the hermes-builder writes the pack.
4. **Prove**: tests run, screenshots taken, backtests split in/out of sample, paper trades marked.
5. **Hand off**: REVIEW.md, listing and post drafts, trade tickets, spend plans all land in `requests/justin/` and Notion.
6. **Report**: the evening scoreboard in Slack and Notion, the vault daily note.

Each step's trigger and judgment call is in TRIGGER-MAP.md.

## KPIs

| Measure | Target | Source (Justin's words and date) |
|---|---|---|
| Silent roles | None for more than 26 hours | Factory standard |
| Messages or posts sent without an approved template | 0 | Factory standard |
| Real trades, transfers or wallet actions taken by the bot | 0, always | Factory brief, 2026-11-12 |
| Products reaching "Ready for review" | One per factory run that has a qualifying idea | "the software factory where we put out ideas like on Gumroad" (2026-11-12) |
| Product posts live with a URL | Up to 2 a day once approved | "and then we promote the heck out of them" (2026-11-12) |
| Strategies backtested out of sample | Every creator idea that is testable | "following different creators and their ideas ... code out some different algos and trading bots" (2026-11-12) |
| Hermes packs passing their checklist | Every request | "a specialist for creating Hermes agents" (2026-11-12) |

## Gates

Every gate in [GATES.md](GATES.md). They never move.

## Handoffs between roles

Through files only: `daily/<date>/<role>.md` for what each role did, `requests/<role>/<id>.md` for work handed over, `requests/justin/` for Justin's queue.

| From | What | To |
|---|---|---|
| Any role | Price, terms, an upset person, an account warning | `requests/justin/` |
| dev | A product ready for review: repo, listing and social files | `requests/promoter/<slug>.md` |
| markets | A strategy spec that needs more than a backtest (a tool, a dashboard) | `requests/dev/<id>.md` |
| markets | A strategy that proved itself in paper | `requests/justin/trades/` via `trade_guard.py` |
| hermes-builder | A computer to create or upgrade, with its cost | `requests/justin/` via `spend_guard.py` |
| lead | Justin's new ideas and requests from Slack | `requests/<role>/` |

## Roles

| Role | Job | Routines |
|---|---|---|
| [lead](roles/lead.md) | Plans the day, watchdog, scoreboard, the vault daily note, Justin's queue | 3 |
| [dev](roles/dev.md) | Dev ideas coded with Claude Code; the software factory up to "Ready for review" | 3 |
| [promoter](roles/promoter.md) | Gumroad listings and product posts on Justin's own X, drafts until approved; sales proof | 3 |
| [markets](roles/markets.md) | Market brief, crypto scout on X, creator-follow (Moon Dev first), algo lab, paper ledger, trade tickets | 6 |
| [hermes-builder](roles/hermes-builder.md) | Hermes agent packs, built and installed on Orgo computers Justin named | 2 |

## Workspace

`/workspace/idea-incubator/`: `repo/` (this pack), `context/` (owner, routines-on, standing-approvals, spend-approvals, team-registry, suppression), `daily/<date>/`, `requests/<role>/` and `requests/justin/` (with `trades/`), `builds/` (`dev/`, `products/`, `algos/`, `hermes/`), `approved/`, `data/` (mode 600), `log/runs-<YYYY-MM>.md`, `vault/` (Obsidian: `Daily/`, `People/`, `Decisions.md`), `state/` (`factory/`, `paper/`, `test/`), `.secrets/` (mode 700).

## Milestones

| # | Milestone | Done when |
|---|---|---|
| K0 | Account and bot | Justin signed in to the new Incubator Grok account, the bot has the pack and wrote `log/setup.md` |
| K1 | Read-only | Slack, Notion, GitHub, Gumroad, X, Orgo connected read-only, each with one real record read back; Claude Code answers `OK` |
| K2 | Routines | All 17 routines created and paused, read back into `team-registry.md` |
| K3 | Test day | The first-day run in HANDOFF.md passes with zero sends, zero posts and zero trades |
| K4 | Drafts approved | Justin approved the listing and post types once |
| K5 | Low-risk lanes on | lead, markets (paper), dev and hermes-builder `on` |
| K6 | Promotion on | promoter `on`, with the types Justin marked `auto` |

## Done means

K6 reached: Slack #incubator shows the morning plan and evening scoreboard every day, Notion shows the queue (products to review, drafts, trade tickets, spend plans), the vault has a daily note, and at least one product has gone from idea to "Ready for review" with a live Gumroad listing Justin approved.
