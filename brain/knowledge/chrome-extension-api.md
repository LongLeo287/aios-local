# Chrome Extension API — Knowledge Base

## Description
Technical reference for Manifest V3 extension development, focusing on bookmarks, storage, and service worker best practices for the Smart Bookmark Manager.

## Manifest V3 Key Differences

### Service Worker (replaces background page)
```js
// manifest.json
"background": {
  "service_worker": "src/background/worker.js"
}
// NOT: "scripts": ["background.js"]
```

### Storage (use chrome.storage, not localStorage)
```js
// localStorage does NOT work in service workers
// Use chrome.storage.local instead
await chrome.storage.local.set({ key: value });
const data = await chrome.storage.local.get('key');
```

### Bookmarks API Quick Reference
```js
// Get full tree
const [tree] = await chrome.bookmarks.getTree();

// Root nodes
tree.children[0] = Bookmarks Bar (id: "1")
tree.children[1] = Other Bookmarks (id: "2")

// Create
await chrome.bookmarks.create({ parentId: "1", title, url });

// Listen for changes
chrome.bookmarks.onCreated.addListener((id, bookmark) => {});
chrome.bookmarks.onRemoved.addListener((id, removeInfo) => {});
chrome.bookmarks.onChanged.addListener((id, changeInfo) => {});
chrome.bookmarks.onMoved.addListener((id, moveInfo) => {});
```

### Favicon API
```js
// Get favicon URL
const favIconUrl = `chrome-extension://${chrome.runtime.id}/_favicon/?pageUrl=${encodeURIComponent(url)}&size=16`;
```

### Action API (popup trigger)
```js
// In popup.js - no special setup needed
// Extension icon click → opens popup.html automatically
```

## Common Pitfalls

1. **Service Worker sleep**: SW can be killed by Chrome. Don't rely on in-memory state.
2. **CSP restrictions**: No inline scripts, no remote scripts.
3. **localStorage**: Not shared between popup and SW. Use chrome.storage.
4. **Permissions**: Request minimal permissions to pass Chrome Web Store review.
5. **Async APIs**: Always use await/Promise, never callbacks for modern code.

## Debugging Tips
```
chrome://extensions/ → Enable Developer mode → Inspect popup
chrome://bookmarks/ → Test bookmark operations
Ctrl+Shift+J → Extension errors in console
```
