#!/usr/bin/env python3
"""No-AI job: daily signals for the watchlist (context/watchlist.txt, default BTC ETH SOL) from Coinbase's free
daily candles, through the pack's signals.py. Writes state/signals/<date>.md and puts it on the desk.
Paper only: a signal opens a paper position under the paper risk rule; nothing real is ever placed."""
import csv, json, subprocess, sys, time
from _common import PACK, TODAY, desk_put, http_json, ledger, state, watchlist

rows = [f"# Signals {TODAY} (paper only)", "", "| Coin | RSI | Volume ratio | DCA multiplier | Paper action |", "|---|---|---|---|---|"]
for s in watchlist():
    try:
        c = http_json(f"https://api.exchange.coinbase.com/products/{s}-USD/candles?granularity=86400")
    except Exception as e:
        rows.append(f"| {s} | | | | no data ({type(e).__name__}) |"); continue
    day = int(time.time()) // 86400 * 86400
    c = [x for x in sorted(c) if x[0] < day][-60:]  # [time, low, high, open, close, volume]; finished days only
    f = state("signals", f"{s}.csv")
    with f.open("w", newline="") as h:
        w = csv.writer(h); w.writerow(["time", "open", "high", "low", "close", "volume"])
        for t, lo, hi, op, cl, v in c: w.writerow([t, op, hi, lo, cl, v])
    r = subprocess.run([sys.executable, str(PACK / "skills" / "markets" / "market-signals" / "signals.py"), str(f)], capture_output=True, text=True)
    try: sig = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception: rows.append(f"| {s} | | | | signals.py failed |"); continue
    act = "-"
    if not sig.get("skip") and (sig.get("multiplier") or 0) >= 1.5 and c:
        act = ledger("open", "signals", s, "long", str(sig.get("paper_size_usd") or 25), str(c[-1][4]), f"rsi {sig.get('rsi')} vol {sig.get('volume_ratio')}")
    rows.append(f"| {s} | {sig.get('rsi')} | {sig.get('volume_ratio')} | {sig.get('multiplier')} | {act} |")
out = state("signals", f"{TODAY}.md"); out.write_text("\n".join(rows) + "\n")
print("\n".join(rows))
desk_put(f"state/signals/{TODAY}.md", out)
