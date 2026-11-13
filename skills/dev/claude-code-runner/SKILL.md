---
name: claude-code-runner
description: How the worker box runs Claude Code and Codex on Justin's flat subscriptions for builds, vetting and backtests, with fallback between them and the safety settings. Load when writing a TASK.md for a cli lane, or when a cli lane fails.
---

# Coding CLIs on the worker box

GrokBot never codes. The worker box runs two coding CLIs, each on its own flat subscription, so heavy work never touches Grok's usage:

| CLI | Plan | Login on the box | Headless call (the runner builds it) |
|---|---|---|---|
| Claude Code | Justin's Claude subscription | `CLAUDE_CODE_OAUTH_TOKEN` from `claude setup-token`, in `incubator-coder`'s `~/.profile` | `claude -p "<read TASK.md>" --settings .claude/settings.json --permission-mode acceptEdits --max-turns 80` |
| Codex | Justin's ChatGPT subscription | `codex login` as `incubator-coder` | `codex exec --approve-for-me --skip-git-repo-check "<read TASK.md>"` (workspace-write sandbox) |

`worker-box/jobs.json` gives each cli lane an order (`["claude", "codex"]` or the reverse, to spread load). When the first is out of usage or fails, the next takes over in the same run; the result says which ran.

## How a cli job runs

1. `worker.py` makes the build folder (`/opt/incubator/builds/<dev|products|algos|work>/<slug>/`), copies `settings.json` into `.claude/`, and writes `TASK.md`: the order's text, the rules, and the lane's skill.
2. The CLI runs as `incubator-coder`, who can't read `/opt/incubator/.secrets/`. The prompt is only "Read TASK.md and do it"; the task never goes into a shell command.
3. It commits locally and never pushes. For `dev-build` and `factory-run` the runner pushes to a private repo under `GITHUB_OWNER` (only if that repo is private), then writes the result to the desk.

## The settings file

`settings.json` (next to this file; also installed as the coder's user settings) allows building and testing in the folder, and denies `git push`, `gh`, publishing, `curl` POSTs, wallet CLIs, and reads of the box's `.secrets/` and `context/`. That is the second layer. The first is the unix user: the keys are in a folder the coder can't open. No wallet key, seed phrase or exchange key with trade rights exists on the box at all.

## Tested (2026-11-13, on a Mac against the real desk)

A `dev-build` order ran through Claude Code: code, 4 passing tests, 3 commits, result on the desk. A `vet` order ran through Codex: a score out of 25 with sources, committed, result on the desk.
