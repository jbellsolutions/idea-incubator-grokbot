#!/usr/bin/env python3
"""No-AI job, hourly: the watchdog Grok no longer runs. Alarms to Slack (SLACK_WEBHOOK_URL, an incoming
webhook for the Incubator channel) when GrokBot's newest heartbeat on the desk is over 26 hours old, or a lane
failed twice in a row. Alarms once per problem per day (state/worker/alarms.txt). Prints the same lines."""
import json, os, re, sys, time, urllib.request
from _common import PACK, TODAY, WS, state

alarms = []
names = []
sys.path.insert(0, str(PACK / "desk"))
try:
    import desk as D
    names = D.recent("inbox/beats", 3)
except SystemExit as e: alarms.append(f"desk unreadable: {e}")
except Exception as e: alarms.append(f"desk unreadable: {type(e).__name__}")
if names:
    m = re.match(r"(\d{8}T\d{6}Z)", names[-1])
    age = (time.time() - __import__('calendar').timegm(time.strptime(m.group(1), "%Y%m%dT%H%M%SZ"))) / 3600 if m else 999
    if age > 26: alarms.append(f"GrokBot silent {age:.0f}h (last heartbeat {names[-1][:16]})")
elif not alarms: alarms.append("GrokBot has never written a heartbeat to the desk")
runs = WS / "state" / "worker" / "runs.log"
if runs.exists():
    last = {}
    for l in runs.read_text().splitlines()[-400:]:
        p = l.split()
        if len(p) >= 5: last.setdefault(p[1], []).append(p[4])
    for lane, s in last.items():
        if s[-2:] == ["failed", "failed"]: alarms.append(f"lane {lane} failed twice in a row")
sent = state("worker", "alarms.txt"); done = set(sent.read_text().splitlines()) if sent.exists() else set()
hook = os.environ.get("SLACK_WEBHOOK_URL", "")
for a in alarms:
    print("ALARM", a)
    key = f"{TODAY} {a.split(' (')[0]}"
    if key in done or not hook: continue
    req = urllib.request.Request(hook, data=json.dumps({"text": f"Incubator worker watchdog: {a}"}).encode(), headers={"Content-Type": "application/json"})
    try: urllib.request.urlopen(req, timeout=15); done.add(key)
    except Exception as e: print("slack failed", type(e).__name__)
sent.write_text("\n".join(sorted(done)) + "\n")
if not alarms: print("ok")
