#!/usr/bin/env bash
# Install the Incubator worker on a fresh Ubuntu box (a DigitalOcean droplet or an Orgo computer used for the
# Incubator only, never a box another agent lives on). Run as root:  bash install.sh <path-to-unpacked-pack>
# Two users: `incubator` runs the jobs and holds the keys; `incubator-coder` runs Claude Code and Codex and cannot
# read the keys. They share build folders through the incubator-coder group. It installs no keys: the owner fills
# /opt/incubator/.secrets/worker.env (mode 600) and the CLI logins in the coder's home. It creates nothing that costs
# money and changes no firewall or DNS.
set -euo pipefail
PACK="${1:?bash install.sh <unpacked pack folder>}"
H=/opt/incubator
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq && apt-get install -y -qq python3 git rsync curl cron sudo ca-certificates >/dev/null
id incubator-coder >/dev/null 2>&1 || useradd -m -s /bin/bash incubator-coder
id incubator >/dev/null 2>&1 || useradd -m -s /bin/bash incubator
usermod -aG incubator-coder incubator
mkdir -p $H/{repo,context,state,builds,log,.secrets}
rsync -a --delete "$PACK/" $H/repo/
chown -R incubator:incubator $H; chmod 700 $H/.secrets
# the coder may pass through /opt/incubator to builds/ and read the (public) pack, nothing else
chmod 711 $H; chmod 750 $H/context $H/state $H/log
touch $H/.secrets/worker.env; chmod 600 $H/.secrets/worker.env; chown incubator:incubator $H/.secrets/worker.env
# shared builds: group incubator-coder, setgid, group-writable; both users work with umask 002
chown incubator:incubator-coder $H/builds; chmod 2775 $H/builds
grep -q 'umask 002' /home/incubator-coder/.profile 2>/dev/null || echo 'umask 002' >> /home/incubator-coder/.profile
chown incubator-coder:incubator-coder /home/incubator-coder/.profile; chmod 600 /home/incubator-coder/.profile
for u in incubator incubator-coder; do
  sudo -u $u git config --global safe.directory '*'
  sudo -u $u git config --global user.name "Incubator worker"; sudo -u $u git config --global user.email "worker@incubator.local"
done
# the runner may start a shell as the coder, nothing else; checked before it goes live
S=$(mktemp)
printf 'incubator ALL=(incubator-coder) NOPASSWD: /bin/bash, /usr/bin/bash\n' > "$S"
visudo -cf "$S" >/dev/null && install -m 440 "$S" /etc/sudoers.d/incubator; rm -f "$S"
command -v node >/dev/null || { curl -fsSL https://deb.nodesource.com/setup_22.x | bash - >/dev/null && apt-get install -y -qq nodejs >/dev/null; }
command -v claude >/dev/null || npm install -g @anthropic-ai/claude-code >/dev/null
command -v codex >/dev/null || npm install -g @openai/codex >/dev/null
command -v gh >/dev/null || apt-get install -y -qq gh >/dev/null || true
# the coder's own Claude settings (user level is trusted in headless mode; each build folder gets a copy too)
install -d -o incubator-coder -m 700 /home/incubator-coder/.claude
install -o incubator-coder -m 600 $H/repo/skills/dev/claude-code-runner/settings.json /home/incubator-coder/.claude/settings.json
grep -q WORKER_CODER_USER $H/.secrets/worker.env || cat >> $H/.secrets/worker.env <<'ENV'
# names only until the owner fills them in (see repo/.env.example, worker section)
export WORKER_CODER_USER=incubator-coder
export DESK_SIDE=worker
export DESK_REPO=
export GITHUB_TOKEN=
export GITHUB_OWNER=
export SLACK_WEBHOOK_URL=
export GUMROAD_ACCESS_TOKEN=
export ORGO_API_KEY=
ENV
crontab -u incubator $H/repo/worker-box/crontab.txt
[ "$(date +%Z)" = "UTC" ] || echo "warning: the box is not on UTC; the cron lines are UTC (timedatectl set-timezone UTC)"
echo "installed. Next: the owner's steps in repo/worker-box/INSTALL.md (tokens, Hermes profile, the check)."
