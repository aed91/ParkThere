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
        caches.open(staticCacheName).then(cache => {
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
                keys.filter(key => key !== staticCacheName && key !== dynamicCacheName)
                    .map(key => caches.delete(key)) // Delete old caches
            );
        })
    );
});

// Fetch event - Handles both static and dynamic requests
self.addEventListener('fetch', evt => {
    if (evt.request.url.indexOf('firestore.googleapis.com') === -1) {
        // Network-first strategy for API calls to fetch parking data
        if (evt.request.url.indexOf('/get-data') > -1) {
            evt.respondWith(
                fetch(evt.request).then(fetchRes => {
                    return caches.open(dynamicCacheName).then(cache => {
                        cache.put(evt.request.url, fetchRes.clone());
                        limitCacheSize(dynamicCacheName, 15); // Limit dynamic cache size
                        return fetchRes;
                    });
                }).catch(() => {
                    return caches.match('/pages/fallback.html');
                })
            );
        } else {
            // Cache-first strategy for other requests (static assets, images, etc.)
            evt.respondWith(
                caches.match(evt.request).then(cacheRes => {
                    return cacheRes || fetch(evt.request).then(fetchRes => {
                        return caches.open(dynamicCacheName).then(cache => {
                            cache.put(evt.request.url, fetchRes.clone());
                            limitCacheSize(dynamicCacheName, 15); // Limit dynamic cache size
                            return fetchRes;
                        });
                    });
                })
            );
        }
    }
});
