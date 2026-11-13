"""Shared bits for the worker's no-AI jobs: workspace, free public HTTP, the desk."""
import json, os, pathlib, subprocess, sys, time, urllib.request
HERE = pathlib.Path(__file__).resolve()
PACK = HERE.parents[2]
WS = pathlib.Path(os.environ.get("BOT_HOME") or PACK.parent)
os.environ.setdefault("DESK_SIDE", "worker")
TODAY = time.strftime("%Y-%m-%d", time.gmtime())

def http_json(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "incubator-worker", "Accept": "application/json"})
    for i in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r: return json.load(r)
        except Exception:
            if i == 2: raise
            time.sleep(2 ** i)

def desk(*a):
    r = subprocess.run([sys.executable, str(PACK / "desk" / "desk.py"), *a], capture_output=True, text=True, timeout=120)
    return r.returncode, (r.stdout or r.stderr).strip()

def state(*p):
    f = WS.joinpath("state", *p); f.parent.mkdir(parents=True, exist_ok=True); return f

def ledger(*a):
    r = subprocess.run([sys.executable, str(PACK / "guards" / "scripts" / "paper_ledger.py"), *a], capture_output=True, text=True,
                       env={**os.environ, "BOT_HOME": str(WS)})
    return r.stdout.strip()

def watchlist():
    f = WS / "context" / "watchlist.txt"
    syms = f.read_text().split() if f.exists() else ["BTC", "ETH", "SOL"]
    return [s.upper() for s in syms if s.isalnum()]

def price(sym):
    """Last price in USD from Coinbase's free public API. None if it doesn't list the coin."""
    try: return float(http_json(f"https://api.exchange.coinbase.com/products/{sym}-USD/ticker")["price"])
    except Exception: return None
