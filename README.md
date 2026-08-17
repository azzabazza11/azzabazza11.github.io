# Aaron's Apps — GitHub Pages Hub

Catalog at **https://azzabazza11.github.io/** (redirects to **https://azzabazza11.github.io/apps/**).

The installable hub lives under `/apps/` so its PWA **scope** is only that folder. Child apps (`/chippy-helpers/`, `/photo-slim/`, …) are outside that scope, so Chrome can install the hub **and** each tool as separate home-screen apps.

If an older “Aaron’s Apps” shortcut was installed from the site root, uninstall it once — that copy used scope `/` and blocked the others.

## Deploy

Push `main`. Pages source: **Deploy from branch → main → / (root)**.

## Adding a new app

Edit the `PROJECTS` array in `apps/index.html`.
