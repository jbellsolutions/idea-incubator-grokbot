#!/usr/bin/env python3
"""Signal maths for the markets role. Stdlib only. Research only: no orders, no keys.

Usage:
  python3 signals.py <ohlcv.csv> [--base-usd 25]   # CSV columns: time,open,high,low,close,volume
  python3 signals.py --gsr <gold> <silver> [--threshold 75]
  python3 signals.py --selftest
Ported (signal logic only) from a private DCA strategy repo: Wilder RSI,
volume ratio vs 20-bar average, DCA multiplier 0.5-2.0, gold-silver ratio split.
"""
import csv, sys, json

def read_ohlcv(path):
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            rows.append({k.strip().lower(): float(r[k]) for k in r if k.strip().lower() != "time" and r[k] != ""})
    return rows

def rsi(closes, period=14):
    if len(closes) < period + 1:
        return None
    d = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    g = [x if x > 0 else 0.0 for x in d]
    l = [-x if x < 0 else 0.0 for x in d]
    ag, al = sum(g[:period]) / period, sum(l[:period]) / period
    for i in range(period, len(g)):
        ag = (ag * (period - 1) + g[i]) / period
        al = (al * (period - 1) + l[i]) / period
    if al == 0:
        return 100.0
    return round(100 - 100 / (1 + ag / al), 2)

def volume_ratio(volumes, lookback=20):
    if len(volumes) < lookback:
        return None
    avg = sum(volumes[-lookback:]) / lookback
    return round(volumes[-1] / avg, 2) if avg > 0 else 1.0

def dca_multiplier(vol_ratio, r):
    """Paper size multiplier, clamped 0.5 to 2.0. High volume plus oversold is the strongest signal."""
    m = 1.0
    if vol_ratio is not None:
        if vol_ratio >= 2.0: m += 0.4
        elif vol_ratio >= 1.5: m += 0.2
        elif vol_ratio < 0.5: m -= 0.2
    if r is not None:
        if r < 25: m += 0.6
        elif r < 30: m += 0.4
        elif r < 40: m += 0.1
        elif r > 75: m -= 0.4
        elif r > 70: m -= 0.3
        if vol_ratio is not None and vol_ratio >= 1.5 and r < 35:
            m += 0.2
    return round(max(0.5, min(2.0, m)), 2)

def skip_flag(vol_ratio, r):
    return bool(r is not None and r > 80 and vol_ratio is not None and vol_ratio < 0.8)

def gold_silver_split(gold, silver, threshold=75):
    ratio = gold / silver
    if ratio > threshold + 10: s, g = 70, 30
    elif ratio > threshold: s, g = 55, 45
    elif ratio < threshold - 10: s, g = 30, 70
    else: s, g = 50, 50
    return {"ratio": round(ratio, 1), "silver_pct": s, "gold_pct": g}

def analyse(rows, base_usd=25.0):
    closes = [r["close"] for r in rows]
    vols = [r["volume"] for r in rows]
    r, v = rsi(closes), volume_ratio(vols)
    m = dca_multiplier(v, r)
    return {"rsi": r, "volume_ratio": v, "multiplier": m,
            "paper_size_usd": 0.0 if skip_flag(v, r) else round(base_usd * m, 2),
            "skip": skip_flag(v, r)}

def selftest():
    # 30 bars falling then a volume spike: expect oversold RSI and a multiplier above 1.
    closes = [100 - i * 1.5 for i in range(30)]
    vols = [100.0] * 29 + [260.0]
    rows = [{"close": c, "volume": v} for c, v in zip(closes, vols)]
    out = analyse(rows, 25)
    print("selftest analyse:", json.dumps(out))
    assert out["rsi"] < 30 and out["volume_ratio"] >= 2.0 and out["multiplier"] == 2.0, out
    assert rsi([1, 2, 3]) is None
    assert rsi(list(range(1, 40))) == 100.0
    g = gold_silver_split(2600, 30)  # ratio 86.7
    print("selftest gsr:", json.dumps(g))
    assert g["silver_pct"] == 70
    assert gold_silver_split(2000, 30)["silver_pct"] == 50  # 66.7
    print("selftest OK")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "--selftest":
        selftest()
    elif a[0] == "--gsr":
        th = float(a[a.index("--threshold") + 1]) if "--threshold" in a else 75
        print(json.dumps(gold_silver_split(float(a[1]), float(a[2]), th)))
    else:
        base = float(a[a.index("--base-usd") + 1]) if "--base-usd" in a else 25.0
        print(json.dumps(analyse(read_ohlcv(a[0]), base)))
