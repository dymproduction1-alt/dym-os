const CACHE_NAME = 'prod-os-v1';
const ASSETS = [
  '/',
  '/index.html',
  // Додай сюди шлях до свого CSS та основних JS файлів
];

// Встановлення
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    })
  );
});

// Активація
self.addEventListener('activate', (e) => {
  console.log('Service Worker: Activated');
});

// Стратегія: Спочатку мережа, якщо немає — кеш
self.addEventListener('fetch', (e) => {
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});