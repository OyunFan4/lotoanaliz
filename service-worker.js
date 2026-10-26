'use strict';
const CACHE='lotoanaliz-auto-db-v16';
const FILES=['./','./index.html','./app.js','./performance-engine.js','./style.css','./manifest.webmanifest','./icons/icon-192.png','./icons/icon-512.png'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil((async()=>{await Promise.all((await caches.keys()).filter(k=>k.startsWith('lotoanaliz-')&&k!==CACHE).map(k=>caches.delete(k)));await self.clients.claim()})()));
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(e.request.method!=='GET'||u.origin!==self.location.origin||u.pathname.startsWith('/api/')||u.pathname.startsWith('/.netlify/functions/'))return;
e.respondWith((async()=>{try{const r=await fetch(e.request);if(r.ok){const cache=await caches.open(CACHE);cache.put(e.request,r.clone());}return r}catch{return await caches.match(e.request)||await caches.match('./index.html')||Response.error()}})())});
