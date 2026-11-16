#!/usr/bin/env python3
"""No-AI job: one short digest of the last 24 hours for Grok's morning plan, so Grok reads one small file
instead of the whole desk: job results (lane, status, first line), signals, paper book, sales, failures.
Writes outbox/digest/<date>.md."""
import re, time
from _common import TODAY, WS, desk_put, ledger, state

cut = time.time() - 86400
res = []
for f in sorted((WS / "state" / "worker" / "results").glob("*.md")):
    if f.stat().st_mtime < cut: continue
    t = f.read_text(errors="ignore")
    lane = re.search(r"lane: (\S+)", t); status = re.search(r"status: (\S+)", t)
    body = t.split("\n\n", 1)[1].strip().splitlines() if "\n\n" in t else []
    res.append(f"| {f.stem} | {lane.group(1) if lane else '?'} | {status.group(1) if status else '?'} | {(body[-1] if body else '')[:140].replace('|', '/')} |")
sig = (WS / "state" / "signals" / f"{TODAY}.md")
sales = (WS / "state" / "sales" / f"{TODAY}.md")
out = [f"# Worker digest {TODAY}", "", "## Jobs, last 24 hours", "", "| Result | Lane | Status | Last line |", "|---|---|---|---|"] + (res or ["| (none) | | | |"])
out += ["", "## Paper book (paper, not real money)", "", "```", ledger("report") or "no positions", "```"]
out += ["", "## Signals", "", sig.read_text().split("\n", 2)[-1].strip() if sig.exists() else "(not run today)"]
out += ["", "## Sales", "", sales.read_text().split("\n", 2)[-1].strip() if sales.exists() else "(not read)"]
f = state("digest", f"{TODAY}.md"); f.write_text("\n".join(out) + "\n"); print("\n".join(out))
desk_put(f"outbox/digest/{TODAY}.md", f)
