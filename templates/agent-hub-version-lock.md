# Agent setup prompt — Aaron's Apps version lock

Copy-paste this into each app repo's agent (Sphere Circles, Golf Tracker, etc.).
The agent should implement it once; the Cursor rule keeps it forever.

---

## Prompt (paste this)

```
Set up automatic version lock with Aaron's Apps camp mother for this repo.

### What "bump" means
A version bump is raising the shippable version string (e.g. 1.6.3 → 1.6.4) whenever we ship a fix or feature. Patch = bugfix, minor = feature, major = breaking. The hub card badge comes from hub.json — not from guessing the UI.

### Do this setup (one-time)
1. Ensure hub.json exists at the repo root with: id, title, version, desc, icon, iconPath (SVG preferred), platforms, status, installable, desktopUrl, appUrl, tags, changelog[].
2. Find APP_VER / APP_VERSION / const VERSION in source (and any service-worker CACHE name that embeds the version). Make hub.json.version identical to that string right now. If they drift, prefer the in-app APP_VER as truth and update hub.json + prepend a changelog entry for today.
3. Add .cursor/rules/hub-camp-mother.mdc (alwaysApply: true) that hard-requires: every version change updates APP_VER and hub.json.version together, prepends changelog {version, date YYYY-MM-DD, notes}, and never edits azzabazza11.github.io catalog/fallbacks from this app repo.
4. Add .github/workflows/notify-hub.yml that on push of hub.json to main/master dispatches:
   gh api -X POST repos/azzabazza11/azzabazza11.github.io/dispatches -f event_type=hub-sync
   Use secrets.HUB_SYNC_TOKEN || secrets.HUB_TOKEN. If neither secret exists, exit 0 with a note that camp mother polls hourly.
5. Delete any obsolete workflows that sed/edit azzabazza11.github.io apps/index.html directly — camp mother owns the hub catalog now.
6. Commit and push. Confirm hub.json.version == APP_VER. Optionally ping hub-sync once.

### Ongoing rule for every future change
When shipping anything user-visible, bump APP_VER and hub.json in the same commit, keep strings identical, add a one-line changelog note. Do not ask me to remember — just do it.
```

---

## Optional secret (faster than hourly)

On each app repo (once):

```bash
# Same classic PAT with repo scope used for hub HUB_SYNC_TOKEN, or reuse HUB_TOKEN
gh secret set HUB_SYNC_TOKEN -R azzabazza11/<app-repo>
```

Without the secret, camp mother still syncs within about an hour.
