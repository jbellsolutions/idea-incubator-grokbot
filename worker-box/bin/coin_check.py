#!/usr/bin/env python3
"""No-AI job: check coins Grok's X scout found, with DexScreener's free public API. The order's text lists
symbols or contract addresses, one per line or space-separated. Prints a table with red flags. Research only."""
import sys, time, urllib.parse
from _common import http_json

items = [x.strip("$,") for x in " ".join(sys.argv[1:]).split() if x.strip("$,")][:15]
print("| Query | Pair | Chain | Liquidity $ | 24h volume $ | FDV $ | Age (days) | Flags |\n|---|---|---|---|---|---|---|---|")
for q in items:
    try: pairs = (http_json("https://api.dexscreener.com/latest/dex/search?q=" + urllib.parse.quote(q)) or {}).get("pairs") or []
    except Exception as e: print(f"| {q} | | | | | | | lookup failed ({type(e).__name__}) |"); continue
    if not pairs: print(f"| {q} | none | | | | | | not listed on any DEX pair |"); continue
    p = max(pairs, key=lambda x: (x.get("liquidity") or {}).get("usd") or 0)
    liq = (p.get("liquidity") or {}).get("usd") or 0; vol = (p.get("volume") or {}).get("h24") or 0; fdv = p.get("fdv") or 0
    age = (time.time() * 1000 - (p.get("pairCreatedAt") or time.time() * 1000)) / 86400000
    flags = [f for f, bad in [("liquidity under $50k", liq < 50000), ("pair under 7 days old", age < 7),
             ("volume over 5x liquidity (churn)", liq and vol > 5 * liq), ("FDV over 100x liquidity", liq and fdv > 100 * liq),
             ("many look-alike pairs", len(pairs) > 20)] if bad]
    print(f"| {q} | {p.get('baseToken', {}).get('symbol')}/{p.get('quoteToken', {}).get('symbol')} | {p.get('chainId')} | {liq:,.0f} | {vol:,.0f} | {fdv:,.0f} | {age:.0f} | {'; '.join(flags) or 'none found (still not advice)'} |")
