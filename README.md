# Aaron's Apps — GitHub Pages Hub

Catalog at **https://azzabazza11.github.io/** (redirects to **https://azzabazza11.github.io/apps/**).

The installable hub lives under `/apps/` so its PWA **scope** is only that folder. Child apps (`/chippy-helpers/`, `/photo-slim/`, …) are outside that scope, so Chrome can install the hub **and** each tool as separate home-screen apps.

If an older “Aaron’s Apps” shortcut was installed from the site root, uninstall it once — that copy used scope `/` and blocked the others.

## Camp mother

The hub is the source of truth for **what ships**. Each app keeps a `hub.json` in its own repo (version, description, changelog). A GitHub Action on this repo pulls those files every hour (and on demand), checks them against `APP_VER` in the app source, and writes `apps/catalog.json`.

### One-time: repo secret

Create a **classic PAT** with `repo` scope (or a fine-grained token with **Contents: Read** on every app repo). Then:

```bash
gh secret set HUB_SYNC_TOKEN -R azzabazza11/azzabazza11.github.io
```

Paste the token when prompted. The workflow uses `HUB_SYNC_TOKEN` if set, otherwise `GITHUB_TOKEN` (public repos only).

Manually refresh: **Actions → Camp mother — sync app catalog → Run workflow**.

Apps can ping the hub after they bump `hub.json`:

```bash
gh api -X POST repos/azzabazza11/azzabazza11.github.io/dispatches \
  -f event_type=hub-sync
```

### Adding a new app

1. Add `hub.json` to the app repo (copy any existing one).
2. Register it in `apps/registry.json`.
3. Ship. Camp mother will pick it up on the next sync.

Keep `hub.json` `version` identical to `APP_VER` / `APP_VERSION` in the app.
