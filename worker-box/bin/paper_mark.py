#!/usr/bin/env python3
"""No-AI job: mark every open paper position at Coinbase's free public price; on Sundays put the weekly
paper report on the desk. Paper only."""
import json, time
from _common import TODAY, WS, desk, ledger, price, state

f = WS / "state" / "paper" / "ledger.jsonl"
syms = set()
if f.exists():
    opened, closed = {}, set()
    for l in f.read_text().splitlines():
        r = json.loads(l)
        if r["k"] == "open": opened[r["id"]] = r["symbol"]
        if r["k"] == "close": closed.add(r["id"])
    syms = {s for i, s in opened.items() if i not in closed}
for s in sorted(syms):
    p = price(s)
    print(s, ledger("mark", s, str(p)) if p else "no price")
rep = ledger("report")
print(rep)
if time.gmtime().tm_wday == 6 and time.gmtime().tm_hour >= 18:
    out = state("paper", f"weekly-{TODAY}.md"); out.write_text(f"# Paper review {TODAY} (paper, not real money)\n\n```\n{rep}\n```\n")
    print(desk("put", f"state/paper/weekly-{TODAY}.md", str(out))[1])
