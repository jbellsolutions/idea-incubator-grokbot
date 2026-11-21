# Incubator: GrokBot pack

Justin's idea incubator on its own Grok account. **GrokBot is the orchestrator and automator** (3 roles, 5 routines, 35 wake-ups a week); a **worker box** (Hermes on a DigitalOcean droplet or Orgo computer, with Claude Code and Codex on flat subscriptions) does the work: dev ideas, a software factory to Gumroad, markets and crypto on paper, and Hermes agents. A private desk repo carries orders and results between them.

Built from the GrokBot Factory template. Idea: [../IDEA.md](../IDEA.md). Rules this build follows: the factory's `PLAYBOOK.md`.

| File | What |
|---|---|
| [HANDOFF.md](HANDOFF.md) | Paste or attach to GrokBot: Justin's steps, then the bot's |
| [NEEDS-JUSTIN.md](NEEDS-JUSTIN.md) | Sign-ins, keys by name, yeses |
| [AGENTS.md](AGENTS.md), [agents/](agents/) | One agent per role: the bot to make for each, the line to paste into it, and its memory block. Written by `python3 tools/agents.py` |
| [MASTER-PROMPT.md](MASTER-PROMPT.md) | The bot's master prompt |
| [CHARTER.md](CHARTER.md) | Purpose, the loop, KPIs, handoffs, workspace, milestones. Wins over a role charter |
| [worker-box/](worker-box/INSTALL.md) | The worker: install script, job lanes and tiers, runner, no-AI jobs, Hermes profile |
| [desk/desk.py](desk/desk.py) | The desk client both sides use |
| [roles/](roles/) | One charter per role, each with a system prompt section to paste |
| [TRIGGER-MAP.md](TRIGGER-MAP.md) | Every step: started by, role, judgment call, gate. Every routine (50 max) |
| [GATES.md](GATES.md) | The gates and the Ask-first lines for Auto-review |
| [guards/](guards/SKILL.md) | The guard skill and its scripts: suppression, send, spend, trade (always held), paper ledger, Orgo, heartbeat |
| [skills.json](skills.json), [SKILLS-MAP.md](SKILLS-MAP.md), [skills/](skills/) | Which role uses which skill and account, and the skills themselves |
| [.env.example](.env.example) | Key names only |
| `tools/check.py` | Completeness and secret check: `python3 tools/check.py` |
