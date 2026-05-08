// Service Worker for Ahmed Elhediny Portfolio
const CACHE_NAME = 'ahmed-portfolio-v1.0.3';
const STATIC_CACHE = 'static-v1.0.3';
const DYNAMIC_CACHE = 'dynamic-v1.0.3';

// Files to cache immediately
const STATIC_FILES = [
  '/',
  '/index.html',
  '/manifest.json',
  'assets/css/styles.css',
  'assets/js/main.js',
  'assets/img/logo png 2 -dark.png',
  'assets/img/logo png 3 - lightt.png',
  'assets/img/ahmed elhediny.jpg',
  'assets/img/photoshop.png',
  'assets/img/adobe-illustrator.png',
  'assets/img/Adobe_InDesign_CC_icon.svg.png',
  'assets/img/eXpresso.jpg',
  'https://cdn.tailwindcss.com',
  'https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&family=Caveat:wght@700&display=swap',
  'https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&display=swap'
];

// Install event - cache static files
self.addEventListener('install', event => {
  console.log('Service Worker: Installing...');
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => {
        console.log('Service Worker: Caching static files');
        return cache.addAll(STATIC_FILES);
      })
      .then(() => {
        console.log('Service Worker: Static files cached');
        return self.skipWaiting();
      })
      .catch(err => console.log('Service Worker: Cache failed', err))
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('Service Worker: Activating...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== STATIC_CACHE && cache !== DYNAMIC_CACHE) {
            console.log('Service Worker: Clearing old cache', cache);
            return caches.delete(cache);
          }
        })
      );
    }).then(() => {
      console.log('Service Worker: Activated');
      return self.clients.claim().then(() => {
        // Force refresh all clients
        self.clients.matchAll().then(clients => {
          clients.forEach(client => client.navigate(client.url));
        });
      });
    })
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') return;

  // Skip external requests (except fonts and CDN)
  const url = new URL(event.request.url);
  if (url.origin !== location.origin &&
    !url.hostname.includes('googleapis.com') &&
    !url.hostname.includes('tailwindcss.com')) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached version if available
        if (response) {
          console.log('Service Worker: Serving from cache', event.request.url);
          return response;
        }

        // Otherwise fetch from network
        return fetch(event.request)
          .then(fetchResponse => {
            // Check if valid response
            if (!fetchResponse || fetchResponse.status !== 200 || fetchResponse.type !== 'basic') {
              return fetchResponse;
            }

            // Clone response for caching
            const responseToCache = fetchResponse.clone();

            // Cache dynamic content
            caches.open(DYNAMIC_CACHE)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });

            return fetchResponse;
          })
          .catch(() => {
            // Offline fallback
            if (event.request.destination === 'document') {
              return caches.match('/index.html');
            }
          });
      })
  );
});

// Background sync for contact form
self.addEventListener('sync', event => {
  if (event.tag === 'contact-form-sync') {
    event.waitUntil(syncContactForm());
  }
});

async function syncContactForm() {
  try {
    const requests = await getStoredRequests();
    for (const request of requests) {
      try {
        await fetch('/api/contact', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(request.data)
        });
        await removeStoredRequest(request.id);
        console.log('Service Worker: Contact form synced');
      } catch (error) {
        console.log('Service Worker: Sync failed, will retry', error);
      }
    }
  } catch (error) {
    console.log('Service Worker: Background sync error', error);
  }
}

// Helper functions for offline form storage
async function getStoredRequests() {
  const db = await openDB();
  const transaction = db.transaction(['requests'], 'readonly');
  const store = transaction.objectStore('requests');
  return store.getAll();
}

async function removeStoredRequest(id) {
  const db = await openDB();
  const transaction = db.transaction(['requests'], 'readwrite');
  const store = transaction.objectStore('requests');
  return store.delete(id);
}

async function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('PortfolioOfflineDB', 1);
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains('requests')) {
        db.createObjectStore('requests', { keyPath: 'id', autoIncrement: true });
      }
    };
  });
}