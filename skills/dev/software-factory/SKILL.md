---
name: software-factory
description: Turn rough dev ideas into small, finished, tested products with a launch kit, then stop for Justin. Load for DEV-INTAKE, DEV-BUILD and FACTORY-RUN, or when Justin drops an idea, says "build this", "vet this" or "kill it".
---

# Software factory

Runs on the worker box, inside Claude Code or Codex (`claude-code-runner`), started by a desk order or the worker's Mon/Thu cron. GrokBot only orders it and reads the result. On the box the folder you are in is the product; the desk result is the record, so write the vet, spec and review into files here (`VET.md`, `SPEC.md`, `marketing/REVIEW.md`) and say in your last lines where the item stands (Queue, Maybe, Killed, Building, Ready for review).

Ported from Justin's own product factory (a Claude Code agent that made Tube Timer). Same process, run on this bot's computer, with Claude Code doing the coding through `claude-code-runner`.

## Hard rules

1. **Nothing public without Justin.** Never make a repo public, publish a site, list on Gumroad, post anywhere, send a message or spend. Prepare it so Justin does each in a couple of minutes, then stop. Listings and posts are the promoter's drafts.
2. **No accounts, passwords or keys** in products. Products work without the buyer making an account; "bring your own API key" is fine.
3. **Each product is its own git repo** in `/opt/incubator/builds/products/<slug>/`; dev-only builds in `builds/dev/<slug>/`. Push only to a private repo (`gh repo create <GITHUB_OWNER>/<slug> --private`).
4. **Honest copy.** No invented testimonials, user counts or results. Claims link to a source. Real limits go in the README.
5. **Tested means you ran it.** Build it, run the main flows, save real screenshots. Say what you couldn't test.
6. **Fewer, better.** One finished product beats three half-built. Kill weak ideas early and write why.

## Where things live

| What | Where |
|---|---|
| The board (Ready for review, Building, Queue, Maybe, Launched, Killed) | `state/factory/board.md` |
| Raw ideas (Justin's words, never deleted) | `state/factory/inbox.md` (`## New`, `## Processed`) |
| One log per run | `state/factory/runs/<YYYY-MM-DD-HHMM>.md` from `templates/run-log.md` |
| Templates | `repo/skills/dev/software-factory/templates/` |

Justin's notes are board lines starting `>` ("build this next", "kill it"). His notes beat your ranking. Mark each handled by changing `> ` to `> ✓ `.

## 1. Intake and vet (DEV-INTAKE)

For each new idea (Slack #incubator lines starting `idea:` or `dev:`, the one-to-one chat, `requests/dev/`):
1. Copy it word for word into `inbox.md` under `## New`, give it a kebab-case slug.
2. Vet it (web search, a few minutes): **Pain** (2–3 real links of people complaining, searching or paying), **Fit** (who buys it: Zy AI Academy parents, AI Guy's business owners, developers, traders; say which), **Buildable** (about a day, no servers or buyer accounts), **Demo** (a 15-second "I want that" moment), **Gap** (what the top 2–3 competitors miss). Score each 1–5, total out of 25.
3. 18+ → Queue (ranked). 12–17 → Maybe, with what would make it stronger. Under 12 → Killed, with why.
4. Move it to `## Processed` with the date and slug.

A plain dev request ("build me a script that…", "code this tool") skips the vet: it goes straight to Building as a `builds/dev/<slug>/` job.

## 2. Pick (DEV-BUILD, FACTORY-RUN)

Order: Justin's `>` note, then anything in Building, then the top of Queue. Nothing qualifies → sharpen the Maybe list, log, stop.

## 3. Spec

In the product folder: `git init`, then `marketing/research.md` from `templates/research.md` and `SPEC.md` from `templates/spec.md` (who it's for, the demo moment, core features, out of scope, tech choice, how you'll test). Commit. Board → Building.

## 4. Build with Claude Code

Run Claude Code through `claude-code-runner` with the SPEC as the task. Build the smallest version that delivers the demo moment. Prefer: a single-file web app (free on GitHub Pages), a Chrome extension, a CLI or a small Python tool. No servers to run. If a run hits a wall, write where it stopped in the board item and the run log; the next run continues.

## 5. Test

Clean build, run every core flow in SPEC.md, save screenshots to `marketing/screenshots/`. Results and known issues go in `marketing/REVIEW.md`.

## 6. Package and launch kit

`README.md` (problem, what it does, install, how it works, honest limits), `LICENSE.md` from the template, `docs/index.html` (one-page site with a `CONFIG` block for the Gumroad link), a release build, `marketing/listing.md`, `marketing/social.md`, `marketing/skool-post.md`, `marketing/LAUNCH.md` (Justin's exact steps). Commit, push to the private repo.

## 7. Review packet and hand-off

`marketing/REVIEW.md` from `templates/review.md`: decide in 5 minutes, try it in 2. Board → Ready for review. Write `requests/promoter/<slug>.md` (repo, price, listing and social file paths) and put the REVIEW link in `requests/justin/`.

## 8. Finish the run

Finish the run log, write `daily/<date>/dev.md`, run `beat.py write dev ...`. Report in three lines: what moved, what's ready for Justin, what's next.
