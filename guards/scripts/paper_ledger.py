#!/usr/bin/env python3
"""Paper ledger. Pretend money only; never touches an exchange or a wallet.

    paper_ledger.py open <strategy> <symbol> <long|short> <size-usd> <entry-price> ["<why>"]
    paper_ledger.py close <id> <exit-price> ["<why>"]
    paper_ledger.py mark <symbol> <price>          record a price for open positions in <symbol>
    paper_ledger.py report [--strategy S]           open positions, closed P&L, win rate, by strategy

The bankroll is state/paper/bankroll.txt (default 10000). Risk rule: one position is at most 5% of the
bankroll; the open book at most 30%. Over that, open prints held. Data: state/paper/ledger.jsonl."""
import sys, json, time
from _ws import p, stopped

L = p("state", "paper", "ledger.jsonl")

def rows():
    return [json.loads(l) for l in L.read_text().splitlines() if l.strip()] if L.exists() else []

def add(r):
    L.parent.mkdir(parents=True, exist_ok=True)
    with L.open("a") as h: h.write(json.dumps(r) + "\n")

def book():
    pos = {}
    for r in rows():
        if r["k"] == "open": pos[r["id"]] = dict(r, last=r["entry"])
        elif r["k"] == "close" and r["id"] in pos: pos[r["id"]].update(closed=r["exit"])
        elif r["k"] == "mark":
            for q in pos.values():
                if q["symbol"] == r["symbol"] and "closed" not in q: q["last"] = r["price"]
    return pos

def pnl(q, price):
    move = (price - q["entry"]) / q["entry"]
    return round(q["size"] * (move if q["side"] == "long" else -move), 2)

def bankroll():
    f = p("state", "paper", "bankroll.txt")
    return float(f.read_text().strip()) if f.exists() else 10000.0

def main(a):
    if not a: print(__doc__); return 2
    if a[0] == "open" and len(a) >= 6:
        if stopped(): print("stopped"); return 1
        strat, sym, side, size, entry = a[1], a[2].upper(), a[3].lower(), float(a[4]), float(a[5])
        if side not in ("long", "short"): print("side must be long or short"); return 2
        br = bankroll(); openb = sum(q["size"] for q in book().values() if "closed" not in q)
        if size > 0.05 * br or openb + size > 0.3 * br:
            print(f"held: over the paper risk rule (5% per position, 30% open; bankroll {br:.0f}, open {openb:.0f})"); return 1
        pid = f"P{int(time.time())}{len(rows())}"
        add({"k": "open", "id": pid, "t": int(time.time()), "strategy": strat, "symbol": sym, "side": side,
             "size": size, "entry": entry, "why": " ".join(a[6:])})
        print(f"opened {pid}"); return 0
    if a[0] == "close" and len(a) >= 3:
        q = book().get(a[1])
        if not q or "closed" in q: print("no open position " + a[1]); return 1
        add({"k": "close", "id": a[1], "t": int(time.time()), "exit": float(a[2]), "why": " ".join(a[3:])})
        print(f"closed {a[1]} pnl {pnl(q, float(a[2]))}"); return 0
    if a[0] == "mark" and len(a) >= 3:
        add({"k": "mark", "t": int(time.time()), "symbol": a[1].upper(), "price": float(a[2])}); print("ok"); return 0
    if a[0] == "report":
        only = a[a.index("--strategy") + 1] if "--strategy" in a else None
        by = {}
        for q in book().values():
            if only and q["strategy"] != only: continue
            s = by.setdefault(q["strategy"], {"open": 0, "unreal": 0.0, "closed": 0, "real": 0.0, "wins": 0})
            if "closed" in q:
                v = pnl(q, q["closed"]); s["closed"] += 1; s["real"] += v; s["wins"] += v > 0
            else:
                s["open"] += 1; s["unreal"] += pnl(q, q["last"])
        print(f"bankroll {bankroll():.0f} (paper)")
        for k, s in sorted(by.items()):
            wr = f"{100 * s['wins'] / s['closed']:.0f}%" if s["closed"] else "n/a"
            print(f"{k}: open {s['open']} unrealised {s['unreal']:+.2f} | closed {s['closed']} realised {s['real']:+.2f} win rate {wr}")
        if not by: print("no positions")
        return 0
    print(__doc__); return 2

if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
