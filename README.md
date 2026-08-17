# Aaron's Apps — GitHub Pages Hub

Central landing page for free web apps, served at **https://azzabazza11.github.io/**

## Deploy

1. Create a public repo named `azzabazza11.github.io` on GitHub (if it doesn't exist).
2. Push this folder to `main`:

```bash
cd azzabazza11.github.io
git init
git add .
git commit -m "Add apps hub landing page"
git branch -M main
git remote add origin https://github.com/azzabazza11/azzabazza11.github.io.git
git push -u origin main
```

3. In repo **Settings → Pages**, set source to **Deploy from branch → main → / (root)**.

## Adding a new app

Edit the `PROJECTS` array in `index.html`:

- Set `platforms`: `desktop`, `android`, `ios` (PWA / mobile-friendly)
- Set `status`: `live` or `soon`
- Set `desktopUrl` / `appUrl` (phone entry can differ, e.g. Sphere Circles)
- Set `installable: true` to show **Install app** on mobile / Android / iOS filters  
  (links to the app with `?install=1` so that origin can run the install prompt)
- Set `version`: shown as a `v1.2.0` badge on the card (omit if unknown)

The hub picks **Open app** vs desktop entry from the active platform filter and device detection — Android/iOS filters never show a separate desktop-only action.
