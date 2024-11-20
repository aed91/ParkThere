const staticCacheName = 'site-static-v2'; // Update cache version for static assets
const dynamicCacheName = 'site-dynamic-v2'; // Update cache version for dynamic assets

const assets = [
  '/',
  '/index.html',
  '/js/app.js',
  '/js/ui.js',
  '/js/materialize.min.js',
  '/css/styles.css',
  '/css/materialize.min.css',
  '/img/parktherelogo.png',
  'https://fonts.googleapis.com/icon?family=Material+Icons',
  '/pages/fallback.html', // Fallback page for when offline
];

// Cache size limit function
const limitCacheSize = (name, size) => {
  caches.open(name).then(cache => {
    cache.keys().then(keys => {
      if (keys.length > size) {
        cache.delete(keys[0]).then(() => limitCacheSize(name, size)); // Recursively delete until size is under limit
      }
    });
  });
};

// Install event
self.addEventListener('install', evt => {
  console.log('Service Worker: Installing...');
  evt.waitUntil(
    caches.open(staticCacheName).then((cache) => {
      console.log('Service Worker: Caching static assets');
      cache.addAll(assets); // Cache the static assets
    })
  );
});

// Activate event
self.addEventListener('activate', evt => {
  console.log('Service Worker: Activating...');
  evt.waitUntil(
    caches.keys().then(keys => {
      // Delete caches that are not needed (clear old versions)
      return Promise.all(
        keys
          .filter(key => key !== staticCacheName && key !== dynamicCacheName)
          .map(key => caches.delete(key)) // Delete old caches
      );
    })
  );
});

// Fetch event - Handles both static and dynamic requests
self.addEventListener('fetch', evt => {
  // Exclude Firestore API requests from being cached
  if (evt.request.url.indexOf('firestore.googleapis.com') === -1) {
    evt.respondWith(
      caches.match(evt.request).then(cacheRes => {
        // Return cached response if found, otherwise fetch and cache dynamically
        return cacheRes || fetch(evt.request).then(fetchRes => {
          // Cache the dynamic content (e.g., images, API requests)
          return caches.open(dynamicCacheName).then(cache => {
            cache.put(evt.request.url, fetchRes.clone());
            limitCacheSize(dynamicCacheName, 15); // Limit dynamic cache size to 15 items
            return fetchRes;
          });
        });
      }).catch(() => {
        // If the fetch request fails (e.g., offline), serve fallback page for HTML files
        if (evt.request.url.indexOf('.html') > -1) {
          return caches.match('/pages/fallback.html');
        }
        // Fallback to a generic 404 if it's a non-HTML request (e.g., CSS, JS)
        if (evt.request.url.indexOf('.css') > -1 || evt.request.url.indexOf('.js') > -1) {
          return caches.match('/pages/fallback.html'); // Or some other fallback if necessary
        }
        // If offline and the request is an image, return a fallback image
        if (evt.request.url.indexOf('.jpg') > -1 || evt.request.url.indexOf('.png') > -1) {
          return caches.match('/img/parktherelogo.png'); // Provide a default image when offline
        }
        // If none of the above, return a 404 page if needed (e.g., for other file types)
        return caches.match('/pages/fallback.html');
      })
    );
  }
});
