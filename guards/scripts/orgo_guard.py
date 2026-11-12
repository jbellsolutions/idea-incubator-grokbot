#!/usr/bin/env python3
"""Orgo guard. Run before ANY Orgo call, reads included.

    orgo_guard.py check "<computer name or id>" <action>

Actions: read, run, screenshot, install (free on a computer Justin named);
create, start, resize, upgrade (spend: held unless spend_guard approves plan orgo-<computer>);
stop, delete, wipe (never: drafted for Justin).
Prints clear or held; exit 0 only for clear. The never-touch computers are held for every action,
reads too: a read wakes them. A computer is in reach only if context/owner.md lists it under
`orgo-computers:`.

The never-touch list (computer names, ids or name fragments, given at intake) comes from env
NEVER_TOUCH (comma-separated) and/or .secrets/never-touch.txt (one per line or comma-separated;
# comments allowed). If neither gives a single entry, every action is held: fail closed."""
import os, sys, re, subprocess, pathlib
from _ws import p, stopped, norm

FREE = {"read", "run", "screenshot", "install", "logs", "list"}
SPEND = {"create", "start", "resize", "upgrade"}

def never_touch():
    raw = os.environ.get("NEVER_TOUCH", "")
    f = p(".secrets", "never-touch.txt")
    if f.exists():
        raw += "\n" + f.read_text(errors="ignore")
    out = []
    for line in raw.splitlines():
        if line.lstrip().startswith("#"): continue
        for x in line.split(","):
            n = norm(x)
            if n: out.append(n)
    return out

def named():
    f = p("context", "owner.md")
    if not f.exists(): return []
    m = re.search(r"orgo-computers:\s*(.+)", f.read_text(errors="ignore"))
    return [norm(x) for x in m.group(1).split(",")] if m else []

def main(a):
    if len(a) < 3 or a[0] != "check": print(__doc__); return 2
    who, act = a[1], a[2].lower()
    if stopped(): print("held: stopped"); return 1
    never = never_touch()
    if not never: print("held: never-touch list missing (set NEVER_TOUCH or .secrets/never-touch.txt)"); return 1
    if any(n in norm(who) for n in never): print("held: never-touch computer"); return 1
    if act in ("stop", "delete", "wipe", "destroy"): print("held: draft it for Justin"); return 1
    if act == "list" and norm(who) in ("all", "workspace"): print("clear"); return 0
    if norm(who) not in named(): print("held: not in context/owner.md orgo-computers"); return 1
    if act in FREE: print("clear"); return 0
    if act in SPEND:
        g = pathlib.Path(__file__).with_name("spend_guard.py")
        plan = "orgo-" + norm(who).replace(" ", "-")
        r = subprocess.run([sys.executable, str(g), plan, a[3] if len(a) > 3 else "1"], capture_output=True, text=True)
        if r.returncode == 0: print("clear"); return 0
        print(f"held: spend; write plan {plan} with its cost to requests/justin/"); return 1
    print("held: unknown action"); return 1

if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
