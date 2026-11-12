# NEEDS-JUSTIN: Incubator

Only what Justin can do. Each line: what, the exact click or command, what it unblocks. Ticked off in order when he works the list.

| # | What | The exact step | What it unblocks |
|---|---|---|---|
| 1 | [ ] New Grok account for the Incubator | Make a new account (not one another business already uses), sign in at x.ai/bot, check the plan includes bots and routines | Everything |
| 2 | [ ] Create the bot | Grok desktop app: new bot "Incubator", time zone UTC, attach `idea-incubator.zip` from release `idea-incubator-v1`, paste the message in HANDOFF.md Part 1 step 4 | Setup |
| 3 | [ ] Auto-review rules | Paste the Ask-first lines from GATES.md into Auto-review → Custom Rules | Safe routines |
| 4 | [ ] Slack channel | Make a private #incubator, add the bot's Slack app | Plans, scoreboard, idea drops |
| 5 | [ ] Sign-ins | Claude Code (your Claude subscription: Take over, run `claude`, `/login`), Gumroad, X, through Connect apps or Take over when the bot asks | dev, promoter, markets |
| 6 | [ ] Keys, by hidden prompt (names only) | `SLACK_BOT_TOKEN`, `NOTION_TOKEN`, `GITHUB_TOKEN` (fine-grained: create and push private repos only), `ORGO_API_KEY`, `GUMROAD_ACCESS_TOKEN` (optional, read sales) | The tools each role uses |
| 7 | [ ] Orgo computers it may build on | Tell the bot which computers (or say "none yet"); it writes them to `context/owner.md`. A new computer is spend: say yes to its plan with the cost | hermes-builder installs |
| 8 | [ ] Paper bankroll and creators | Confirm 10000 paper, and name creators besides Moon Dev | markets |
| 9 | [ ] Single brain path | "Deploy key" (the bot pushes its daily note) or "Mac pulls" | Reports reach the single brain |
| 10 | [ ] Approve the listing and post types once | Reply yes to the first Gumroad listing draft and the first X post draft; say "auto" for a type once it looks right | Listings and posts |
| 11 | [ ] Every trade, every time | Read tickets in Notion / `requests/justin/trades/`; place any you want yourself. The bot never will | Real money, only by you |
| 12 | [ ] Publishing a product | Follow each product's `marketing/LAUNCH.md`: make the repo public if you want, list on Gumroad | Products on sale |
| 13 | [ ] Intake values (not secrets) | Paste at intake when the bot asks, one at a time: `GITHUB_OWNER`, `GUMROAD_STORE_URL`, `PACK_RELEASE_URL`, `NOTION_PARENT_PAGE`, `SKILLS_SOURCE_REPO`, `HERMES_TEAM_TEMPLATE_REPO`, and `NEVER_TOUCH` (the computers and names it must never touch; the bot writes them to `.secrets/never-touch.txt`) | Repos, listings, the Notion page, skill copying; Orgo work (the guard holds every Orgo action until the never-touch list exists) |
