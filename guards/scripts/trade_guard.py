#!/usr/bin/env python3
"""Trade guard. Run before anything that would move money: an order, a swap, wallet funding,
a transfer, a withdrawal, connecting a wallet or an exchange key with trade rights.

    trade_guard.py ticket <symbol> <buy|sell|fund|transfer> <size-usd> "<thesis>"
    trade_guard.py check <anything>        always prints held

It always prints held and exits 1. There is no approval file and no auto state: the bot never
places a real trade. `ticket` writes requests/justin/trades/<date>-<symbol>-<n>.md for Justin,
who places it himself if he wants it. Paper trades go to paper_ledger.py instead."""
import sys, datetime
from _ws import p

def main(a):
    if not a: print(__doc__); return 2
    if a[0] == "ticket" and len(a) >= 5:
        sym, side, usd, thesis = a[1].upper(), a[2].lower(), a[3], " ".join(a[4:])
        d = p("requests", "justin", "trades"); d.mkdir(parents=True, exist_ok=True)
        day = datetime.date.today().isoformat()
        n = len(list(d.glob(f"{day}-{sym}-*.md"))) + 1
        f = d / f"{day}-{sym}-{n}.md"
        f.write_text(f"# Trade ticket for Justin: {side} {sym} ${usd}\n\n"
                     f"Status: held. The bot does not place this. Justin decides and places it himself.\n\n"
                     f"## Thesis\n\n{thesis}\n\n## Paper record\n\nSee `python3 repo/guards/scripts/paper_ledger.py report`.\n")
        print(f"held: ticket {f.relative_to(p())}")
        return 1
    print("held: real trades, wallet funding and transfers are Justin's; file a ticket")
    return 1

if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
