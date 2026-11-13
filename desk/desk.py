#!/usr/bin/env python3
"""The desk: a private GitHub repo between GrokBot (the orchestrator) and the worker box (the doer).

    desk.py order <lane> "<task>" [--ref <id>]     Grok: new work order, inbox/orders/<day>/<id>.md; prints the id
    desk.py orders [--since <id>]                  worker: order ids of the last 2 days
    desk.py get <path>                             either: print one file (small; use usage/scripts/pick.py on JSON)
    desk.py result <order-id> <status> <file>      worker: outbox/results/<day>/<order-id>.md from a local file
    desk.py results [--since <id>]                 Grok: result ids of the last 2 days since an id (newest last)
    desk.py read <order-id>                        Grok: print the result for an order
    desk.py digest [<YYYY-MM-DD>]                  Grok: print outbox/digest/<date>.md (default today, UTC)
    desk.py put <path> <file>                      either, in its own folders only: a new file
    desk.py beat '<line>'                          either: a heartbeat file in its own beats folder

Folders are split by day (<day> = YYYY-MM-DD, UTC; GitHub lists at most 1,000 files a folder).
One writer per folder, and every file is new, never edited (no merge races):
  DESK_SIDE=grok   writes inbox/ only (orders, beats, notes)
  DESK_SIDE=worker writes outbox/ and state/ only (results, digest, beats, paper, sales)
Needs DESK_REPO (owner/name) and GITHUB_TOKEN, from the environment or .secrets/github.env and
context/owner.md (`desk-repo: owner/name`). Lanes: see repo/worker-box/jobs.json."""
import base64, json, os, pathlib, re, secrets, sys, time, urllib.error, urllib.request

HERE = pathlib.Path(__file__).resolve()
WS = pathlib.Path(os.environ.get("BOT_HOME") or HERE.parents[2])
LANE = re.compile(r"^[a-z][a-z0-9-]{1,30}$")
OWN = {"grok": ("inbox/",), "worker": ("outbox/", "state/")}

def env(name):
    v = os.environ.get(name, "")
    if v: return v
    for f in (WS / ".secrets" / "github.env", WS / ".secrets" / ".env", WS / "context" / "owner.md"):
        if f.exists():
            for l in f.read_text(errors="ignore").splitlines():
                m = re.match(rf"\s*{name}\s*[=:]\s*(\S+)", l, re.I) or (name == "DESK_REPO" and re.match(r"\s*desk-repo\s*:\s*(\S+)", l, re.I))
                if m: return m.group(1).strip().strip('"')
    sys.exit(f"missing {name}: set it in the environment or .secrets/github.env (keys) / context/owner.md (desk-repo)")

def api(method, path, body=None):
    url = f"https://api.github.com/repos/{env('DESK_REPO')}/contents/{path}"
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {env('GITHUB_TOKEN')}", "Accept": "application/vnd.github+json",
                                          "User-Agent": "incubator-desk"})
    for i in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            if e.code == 422: sys.exit(f"exists already: {path} (desk files are never edited)")
            if e.code >= 500 and i < 2: time.sleep(2 ** i); continue
            sys.exit(f"desk {method} {path}: HTTP {e.code}")
        except urllib.error.URLError:
            if i < 2: time.sleep(2 ** i); continue
            raise

def side():
    s = os.environ.get("DESK_SIDE", "")
    if s not in OWN: sys.exit("set DESK_SIDE=grok or DESK_SIDE=worker")
    return s

def put(path, text, msg=None):
    if not path.startswith(OWN[side()]): sys.exit(f"held: {side()} writes only {', '.join(OWN[side()])}")
    api("PUT", path, {"message": msg or f"{side()}: {path}", "content": base64.b64encode(text.encode()).decode()})
    return path

def ls(d):
    r = api("GET", d) or []
    return sorted(x["name"] for x in r if x.get("type") == "file")

def get(path):
    r = api("GET", path)
    return base64.b64decode(r["content"]).decode() if r and "content" in r else None

def day_of(oid):
    return f"{oid[:4]}-{oid[4:6]}-{oid[6:8]}"

def recent(base, days=2):
    out = []
    for i in range(days - 1, -1, -1):
        d = time.strftime("%Y-%m-%d", time.gmtime(time.time() - i * 86400))
        out += ls(f"{base}/{d}")
    return out

def new_id(lane):
    return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + f"-{lane}-{secrets.token_hex(2)}"

def since(names, sid):
    ids = [n[:-3] for n in names if n.endswith(".md")]
    return [i for i in ids if not sid or i > sid]

def main(a):
    if not a: print(__doc__); return 2
    c = a[0]
    if c == "order" and len(a) >= 3:
        if side() != "grok": sys.exit("held: only Grok writes orders")
        lane = a[1]
        if not LANE.match(lane): sys.exit("bad lane name")
        task = a[2].strip()
        if not task or len(task) > 8000: sys.exit("task must be 1 to 8000 characters")
        if (WS / "context" / "STOP").exists(): print("stopped"); return 1
        oid = new_id(lane); ref = a[a.index("--ref") + 1] if "--ref" in a else ""
        put(f"inbox/orders/{day_of(oid)}/{oid}.md", f"---\nid: {oid}\nlane: {lane}\nref: {ref}\nat: {int(time.time())}\n---\n\n{task}\n")
        print(oid); return 0
    if c == "orders":
        sid = a[a.index("--since") + 1] if "--since" in a else ""
        print("\n".join(since(recent("inbox/orders"), sid))); return 0
    if c == "results":
        sid = a[a.index("--since") + 1] if "--since" in a else ""
        print("\n".join(since(recent("outbox/results"), sid))); return 0
    if c == "read" and len(a) >= 2:
        t = get(f"outbox/results/{day_of(a[1])}/{a[1]}.md"); print(t if t is not None else "(no result yet)"); return 0 if t else 1
    if c == "get" and len(a) >= 2:
        t = get(a[1]); print(t if t is not None else "(none)"); return 0 if t is not None else 1
    if c == "digest":
        d = a[1] if len(a) > 1 else time.strftime("%Y-%m-%d", time.gmtime())
        t = get(f"outbox/digest/{d}.md"); print(t if t is not None else f"(no digest for {d})"); return 0 if t else 1
    if c == "result" and len(a) >= 4:
        body = pathlib.Path(a[3]).read_text(errors="ignore")[:60000]
        put(f"outbox/results/{day_of(a[1])}/{a[1]}.md", f"---\norder: {a[1]}\nstatus: {a[2]}\nat: {int(time.time())}\n---\n\n{body}\n"); print("ok"); return 0
    if c == "put" and len(a) >= 3:
        put(a[1], pathlib.Path(a[2]).read_text(errors="ignore")); print("ok"); return 0
    if c == "beat" and len(a) >= 2:
        s = side(); base = "inbox/beats" if s == "grok" else "outbox/beats"
        put(f"{base}/{time.strftime('%Y-%m-%d', time.gmtime())}/{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-{secrets.token_hex(2)}.md", a[1][:500]); print("ok"); return 0
    print(__doc__); return 2

if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
