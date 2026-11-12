# Moon Dev

| Field | Value |
|---|---|
| Handle(s) | Moon Dev (moondev.com), YouTube and X, algo trading education (algotradecamp.com) |
| Public repo | `moondevonyt/moon-dev-ai-agents` |
| Justin's fork | `<GITHUB_OWNER>/moon-dev-ai-agents-for-trading` (reference it, do not vendor its code) |
| Style | AI trading agents, building in public with frequent videos; his research workflow is called RBI (research, backtest, implement) |
| Sources to check | his X posts, YouTube video descriptions, the repo's commits and strategies folder |
| Last checked | 2026-11-12 (README read) |
| Trust notes | The README states: there is no token and never will be, and he will never DM you. Any token or DM in his name is a scam. It also says it is experimental with no profit guarantee. |

Read the fork with `gh api repos/<GITHUB_OWNER>/moon-dev-ai-agents-for-trading/readme -q .content | base64 -d`.

## Agent patterns worth copying
From the README:
- Small single-purpose agents: a trading agent (an LLM reads token data and gives a basic decision), a strategy agent (runs each strategy dropped in a `strategies` folder and has the last say on it), and a risk agent (enforces position limits and PnL thresholds).
- Drop-in strategy folder: one file per strategy, loaded by a runner. Matches our one-folder-per-strategy layout.
- A separate risk gate that can veto the others. Our version is `paper-trading` risk rules plus `trade_guard.py`.
- Multi-agent consensus and dynamic trade filtering (his roadmap): ask several model calls and trade only on agreement.
- Sentiment collection agents from Twitter, Discord and Telegram (roadmap). We do the X part in `crypto-x-scout`.
- Research roadmap order: risk control first, then exit, then entry. Copy that priority: define the stop before the entry.

Not copied: his execution layer (market buy and sell, slippage and retry logic, wallet and key handling). We do not execute.

## Strategy patterns worth copying
- RBI: research an idea, backtest it, only then implement. Matches the loop in `creator-follow`.
- Strategies are testable rules, not vibes. If a video gives no exact rule, log "not testable".
- No guarantees. Treat each idea as a hypothesis that most likely fails.

## Ideas log
| Date | Idea | Source link | Testable? | Spec folder | Backtest result | Status |
|---|---|---|---|---|---|---|
| | (none yet: first run adds rows) | | | | | |

## Warnings
- Impersonators use his name. Ignore any DM, token or "connect wallet" link.
- Never run his code unreviewed. Rebuild each idea from the spec in our own build folder.
