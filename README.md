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
- Add `links` with GitHub Pages URLs

Individual apps link back to this hub from their Share sections.
