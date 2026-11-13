# Project charter: Incubator

The bot loads this page first. Where a role's charter and this page differ, this page wins.

## Purpose

Incubator is Justin's idea incubator on its own Grok account. GrokBot is the orchestrator and automator; a worker box (Hermes on the Incubator's own DigitalOcean droplet or Orgo computer, with Claude Code and Codex on flat subscriptions) does the work. Together they code his dev ideas out, run a software factory that turns the best ideas into small, tested products with a Gumroad listing and a launch plan on his own X, researches markets and crypto (Moon Dev and other creators' ideas turned into backtested strategies) on a paper ledger, and builds Hermes agents for his Orgo workspace. Done well means: a steady line of finished, honest products waiting for his yes; strategies with real out-of-sample numbers before any of them earns a trade ticket; and Hermes packs that pass their own checklist. It never moves money, and never publishes without him.

## The loop

1. **Find** (GrokBot): ideas from Justin (Slack #incubator, the chat), coins and narratives on X, creators' new ideas, Hermes requests.
2. **Check** (worker): vet each idea out of 25; scam-check each coin; turn each creator idea into a testable spec.
3. **Build** (worker): Claude Code or Codex codes the product, the tool or the backtest; Hermes writes the agent pack. GrokBot writes the order and reads the result.
4. **Prove** (worker): tests run, screenshots taken, backtests split in/out of sample, paper trades marked.
5. **Hand off** (GrokBot): REVIEW.md, listing and post drafts, trade tickets, spend plans all land in `requests/justin/` and Notion.
6. **Report** (GrokBot, from the worker's digest): the evening scoreboard in Slack and Notion, the vault daily note.

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
| lead | Work for the worker box | A desk order (`desk.py order <lane>`) |
| Worker (via lead) | A product ready for review: repo, listing and social files | `requests/promoter/<slug>.md` |
| markets | Coins found on X | A desk `coin-check` order |
| markets | A strategy that proved itself in paper | `requests/justin/trades/` via `trade_guard.py` |
| Worker (via lead) | A computer to create or upgrade, with its cost | `requests/justin/` via `spend_guard.py` |
| lead | Justin's new ideas and requests from Slack | `requests/<role>/` |

## Roles (on GrokBot: the orchestrator)

| Role | Job | Routines |
|---|---|---|
| [lead](roles/lead.md) | Plans from the worker's digest, writes desk orders, routes results, scoreboard, vault note, Justin's queue | 3 |
| [promoter](roles/promoter.md) | Gumroad listings and product posts on Justin's own X, drafts until approved | 1 |
| [markets](roles/markets.md) | X search for coins and narratives, candidates to the worker, trade tickets for Justin | 1 |

## Lanes (on the worker box: the doer)

The worker box runs every heavy job on the cheapest tier that can do it ([worker-box/INSTALL.md](worker-box/INSTALL.md), [worker-box/jobs.json](worker-box/jobs.json)):

| Tier | Lanes | Cost |
|---|---|---|
| script (no AI) | signals, paper-mark, coin-check, sales, digest, watchdog, the desk sync | Nothing |
| cli (Claude Code, Codex; one falls back to the other) | dev-build, vet, factory-run, creator-follow, algo-lab | Flat subscriptions |
| hermes | hermes-build, ask | A capped model key |

## Workspace

`/workspace/idea-incubator/`: `repo/` (this pack), `context/` (owner, routines-on, standing-approvals, spend-approvals, team-registry, suppression), `daily/<date>/`, `requests/<role>/` and `requests/justin/` (with `trades/`), `builds/` (`dev/`, `products/`, `algos/`, `hermes/`), `approved/`, `data/` (mode 600), `log/runs-<YYYY-MM>.md`, `vault/` (Obsidian: `Daily/`, `People/`, `Decisions.md`), `state/` (`factory/`, `paper/`, `test/`), `.secrets/` (mode 700).

## Milestones

| # | Milestone | Done when |
|---|---|---|
| K0 | Account and bot | Justin signed in to the new Incubator Grok account, the bot has the pack and wrote `log/setup.md` |
| K1 | Worker box | The Incubator's own droplet or Orgo computer runs `install.sh`; `worker.py run digest` puts a digest on the desk; Claude Code and Codex each finish one test order |
| K2 | Read-only | Slack, Notion, the desk, Gumroad and X connected read-only, each with one real record read back; the bot reads the worker's digest |
| K3 | Routines | All 5 routines created and paused, read back into `team-registry.md` |
| K4 | Test day | The first-day run in HANDOFF.md passes with zero sends, zero posts and zero trades |
| K5 | Drafts approved | Justin approved the listing and post types once |
| K6 | Lanes on | lead and markets `on`, then promoter with the types Justin marked `auto` |

## Done means

K6 reached, with GrokBot waking 35 times a week: Slack #incubator shows the morning plan and evening scoreboard every day, Notion shows the queue (products to review, drafts, trade tickets, spend plans), the vault has a daily note, and at least one product has gone from idea to "Ready for review" with a live Gumroad listing Justin approved.
