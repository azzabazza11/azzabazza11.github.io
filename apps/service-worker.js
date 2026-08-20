const CACHE = 'apps-hub-v1.5.0';
const ASSETS = [
  './',
  './index.html',
  './catalog.json',
  './manifest.webmanifest',
  './icon.svg'
];

async function iconAssets() {
  try {
    const res = await fetch('./catalog.json', { cache: 'no-store' });
    if (!res.ok) return [];
    const data = await res.json();
    const urls = (data.apps || [])
      .map(a => a.iconUrl)
      .filter(Boolean);
    return [...new Set(urls)];
  } catch {
    return [];
  }
}

self.addEventListener('install', event => {
  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE);
      const icons = await iconAssets();
      await cache.addAll([...ASSETS, ...icons]);
      await self.skipWaiting();
    })()
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;
  if (!url.pathname.startsWith('/apps')) return;

  event.respondWith(
    fetch(event.request)
      .then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(event.request, copy));
        return res;
      })
      .catch(() => caches.match(event.request).then(r => r || caches.match('./index.html')))
  );
});
