# Incubator: the handoff

What Justin does, then what the bot does on its own. Follows the factory PLAYBOOK and the client-build GrokBot standard. Unverified platform facts are flagged *(unverified)*.

## Part 1: Justin

1. **Account.** Make a new Grok account for the **Incubator** only (not one another business already uses: one account per business, and every bot on an account shares one computer). Sign in at x.ai/bot. Check the plan covers bots and routines. The bot never buys a plan.
2. **Desktop app.** Open the Grok desktop app. Setup runs in the one-to-one chat there (approval, secret and sign-in requests only show there).
3. **The bot.** Create one bot named **Incubator**, pin it, and set Settings → General → Bot → Timezone to **UTC**.
4. **The pack.** Download `idea-incubator.zip` from the factory's release `idea-incubator-v1` (`<PACK_RELEASE_URL>`, set at intake), attach it to the first message *(zip route unverified)* and paste:

   > You are Incubator. Unpack the attached zip into /workspace/idea-incubator/repo/ and follow HANDOFF.md, Part 2, from step 1. Read MASTER-PROMPT.md and CHARTER.md first. Ask me one thing at a time. Nothing sends, posts, spends, trades or publishes until I say yes in this chat.

5. **Auto-review rules.** At Part 2 step 4, paste the Ask-first lines it shows into Auto-review → Custom Rules.
6. **Sign-ins and keys.** When it asks, sign in through Connect apps or **Take over**, one at a time: Claude Code (your Claude subscription), Gumroad, X. Keys go only through a secure secret card or the hidden terminal prompt with **Take over**. Rotate first any key ever pasted in a chat. Never give it a wallet key or seed phrase.

## Part 2: the bot

1. **Workspace.** Create `/workspace/idea-incubator/` with `context/`, `daily/`, `requests/` (one folder per role, plus `justin/` and `justin/trades/`), `builds/` (`dev/`, `products/`, `algos/`, `hermes/`), `approved/`, `data/` (mode 600), `log/`, `vault/` (Obsidian: `Daily/`, `People/`, `Decisions.md`), `state/` (`factory/` with `board.md` and `inbox.md`, `paper/`, `test/`), `.secrets/` (mode 700). Write `context/routines-on.md` with every routine `off`, `context/standing-approvals.md` (empty), `context/spend-approvals.md` (empty) and `context/team-registry.md`. Don't create `context/STOP`. Start `log/setup.md`. Run `python3 repo/tools/check.py` and paste its RESULT line into `log/setup.md`.
2. **Memory and skills.** Save MASTER-PROMPT.md to memory word for word, then each role's "System prompt section" from `roles/`. Save `guards/SKILL.md` and every `skills/<role>/<skill>/SKILL.md` as a private skill. Put each secret key name in `.env.example` (the ones above the intake-values block) into `.secrets/<system>.env` by hidden prompt, one at a time. The intake values are not secrets; they come at step 3.
3. **Intake.** Ask Justin, one at a time: the Slack channel (default: a new private #incubator), the Notion page for the scoreboard and the queue (default: "Incubator" under `<NOTION_PARENT_PAGE>`, set at intake), which Orgo computers are yours to build on (`orgo-computers:` in `context/owner.md`), the never-touch list of computers and names (write it to `.secrets/never-touch.txt`, one per line, mode 600, before any Orgo call: without it `orgo_guard.py` holds every Orgo action), the paper bankroll (default 10000 in `state/paper/bankroll.txt`), which creators besides Moon Dev, and any dev ideas to start with. Then the intake values from `.env.example` (NEEDS-JUSTIN item 13), one at a time: write each to `context/owner.md` as `github-owner:`, `gumroad-store-url:`, `pack-release-url:`, `notion-parent-page:`, `skills-source-repo:`, `hermes-team-template-repo:` (the never-touch list goes only to `.secrets/never-touch.txt`). Write `context/owner.md`. Start `context/suppression.csv` (empty is fine: this bot doesn't write to people).
4. **Approval rules.** Show Justin the Ask-first lines from GATES.md to paste, with `<NEVER_TOUCH>` replaced by the names in `.secrets/never-touch.txt`.
5. **Connect, read-only, one at a time.** Each gets a Check that reads one real record into `log/setup.md`.

   | App | Roles | Check |
   |---|---|---|
   | Slack #incubator | lead, dev | Read the last message |
   | Notion | lead | Read the Incubator page title |
   | Claude Code | dev, markets | Install, Justin signs in (Take over), `claude -p "reply with OK" --max-turns 1` prints OK *(unverified on Grok)* |
   | GitHub | dev, hermes-builder | `gh repo list <GITHUB_OWNER> --limit 1` |
   | Gumroad | promoter | Read the product list (browser) |
   | X | promoter, markets | Read Justin's last post (browser) |
   | Market data | markets | `python3 repo/skills/markets/market-signals/signals.py --selftest` and one free price read |
   | Orgo | hermes-builder | `python3 repo/skills/hermes-builder/orgo-computer-use/scripts/orgo.py list` |

6. **Old agents.** None known doing this job. If Justin runs an older product factory elsewhere, it stays as is and this bot's board is separate, so they never write the same repo. Justin confirms.
7. **Routines, switched off.** Create all 17 routines in TRIGGER-MAP.md, paused. Each prompt starts `Role: <role>.` then the routine name (for example `Role: markets. MKT-SCOUT.`). Record each in `team-registry.md` with role, cron, time zone and next run. A next run an hour or more off means the time zone isn't set.
8. **Report.** Read back every routine and connection into `team-registry.md`, and send Justin the list plus what isn't done and why.

## Usage kit (usage-mastery v1.0.0)

From the usage-mastery kit. Do these right after the workspace and memory steps.

1. Run `bash repo/usage/scripts/install.sh` (free, pinned, no keys) and paste its last line into `log/setup.md`.
2. Save `repo/usage/SKILL.md` as a private skill named usage-saver.
3. Copy `repo/usage/LEDGER.md` to `log/usage-ledger.md`. Ask Justin for the baseline reading (Settings → Usage: % used and reset date) before the first test day, and again after it.
4. The weekly audit (`repo/usage/AUDIT.md`) runs inside the Monday evening report; it adds no routine and changes nothing.
5. Check: `bash repo/usage/scripts/grep_lines.sh 'usage-mastery v' repo/usage/.. 3` prints at least one line (the rules are in place and the scripts run).
6. Show Justin the two owner-only steps, once per Grok account, and record the answers in `log/setup.md`:
   - A spending cap: grok.com/dashboard/billing → a monthly additional-usage limit, or Auto top-up off. The bot never changes billing.
   - Three lines for Auto-review → Custom Rules (chat only; routines never wait on approvals):

     ```
     Ask first before opening more than 5 web pages for one task.
     Ask first before starting a sub-agent or a second bot on a job.
     Ask first before re-running a step that has already failed twice.
     ```
## Bring-up order

| # | Role | Why this order | Turned on first |
|---|---|---|---|
| 1 | lead | Plans, watchdog, scoreboard | LEAD-PLAN, LEAD-WATCH, LEAD-SCORE |
| 2 | markets | Research and paper only; nothing reaches a person | MKT-BRIEF, MKT-MARK, then MKT-SCOUT, the creators, MKT-ALGO-LAB, MKT-WEEKLY |
| 3 | dev | Builds in private repos; nothing public | DEV-INTAKE, then DEV-BUILD, FACTORY-RUN |
| 4 | hermes-builder | Touches Orgo computers (guarded) | HB-CHECK, then HB-BUILD |
| 5 | promoter | Public posts and listings on Justin's accounts: last | PROMO-SALES, PROMO-LISTINGS, then PROMO-POSTS |

## The first-day test run

Every routine is `test` in `context/routines-on.md`, so nothing reaches a person, a post, a computer or money. **Test on a routine does real work**: the `test` line goes in before every Test press.

| Step | Role | Do | Pass when |
|---|---|---|---|
| 1 | lead | LEAD-PLAN | A plan for every role in `daily/<date>/lead.md` and in Slack |
| 2 | markets | MKT-BRIEF | A brief with signals in `daily/<date>/markets.md`; any trade idea is a paper line |
| 3 | markets | MKT-SCOUT | A watchlist with scam checks; no wallet touched |
| 4 | markets | Trade test: ask it to buy $10 of any coin | `trade_guard.py` prints held and a ticket appears in `requests/justin/trades/`; nothing else happens |
| 5 | markets | MKT-CREATOR-MOONDEV | One Moon Dev idea turned into a strategy spec |
| 6 | dev | DEV-INTAKE with one test idea | It is on the board with a score out of 25 |
| 7 | dev | DEV-BUILD | Claude Code builds the test idea in `builds/dev/<slug>/`, tests run, commits local, no public repo |
| 8 | hermes-builder | HB-CHECK | `orgo.py list` read; a check on a name from the never-touch list prints held |
| 9 | promoter | PROMO-POSTS and PROMO-LISTINGS | Drafts in `requests/justin/`; nothing posted or listed |
| 10 | All | Suppression test | A name added to `context/suppression.csv` is held by `suppression.py` |
| 11 | All | STOP test | Create `context/STOP`; the next run of every role says stopped and does nothing; remove it |
| 12 | lead | LEAD-SCORE | Every role has a line; today's vault note exists; `beat.py status` shows no SILENT; nothing was sent, posted, listed or traded |

The day passes when every row passes and `state/` shows 0 sends, 0 posts and 0 trades. Then Justin approves the listing and post types once, and roles go `on` one at a time.

## Reporting back

| Where | What | Written by |
|---|---|---|
| Slack #incubator | Morning plan, alarms (silent roles, unapproved sends, unread trade tickets), evening scoreboard, Justin's queue | lead |
| Notion | Scoreboard row a day; "Incubator: waiting on Justin" (products to review, drafts, trade tickets, spend plans) | lead |
| The workspace vault | `vault/Daily/<date>.md`, `People/`, `Decisions.md` | lead writes the daily note; each role adds its section |
| The single brain | A scrubbed status line and the daily summary, no raw transcripts, keys or wallet addresses | lead's nightly routine (deploy key) or Justin's Mac pulls: decision on NEEDS-JUSTIN |
