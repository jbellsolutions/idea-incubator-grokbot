#!/usr/bin/env python3
"""No-AI job: Gumroad sales of the last day, read-only (GUMROAD_ACCESS_TOKEN). Counts only Gumroad's own
records. Puts state/sales/<date>.md on the desk. Without a token it says so and does nothing."""
import os, time, urllib.parse
from _common import TODAY, desk_put, http_json, state

tok = os.environ.get("GUMROAD_ACCESS_TOKEN", "")
if not tok: print("no GUMROAD_ACCESS_TOKEN: sales not read"); raise SystemExit(0)
after = time.strftime("%Y-%m-%d", time.gmtime(time.time() - 86400))
d = http_json("https://api.gumroad.com/v2/sales?" + urllib.parse.urlencode({"access_token": tok, "after": after}))
sales = d.get("sales") or []
by = {}
for s in sales:
    k = s.get("product_name") or "?"; by.setdefault(k, [0, 0.0]); by[k][0] += 1; by[k][1] += (s.get("price") or 0) / 100
lines = [f"# Gumroad sales since {after}", "", "| Product | Sales | Revenue $ |", "|---|---|---|"] + [f"| {k} | {n} | {v:.2f} |" for k, (n, v) in by.items()]
if not by: lines.append("| (none) | 0 | 0 |")
out = state("sales", f"{TODAY}.md"); out.write_text("\n".join(lines) + "\n"); print("\n".join(lines))
desk_put(f"state/sales/{TODAY}.md", out)
