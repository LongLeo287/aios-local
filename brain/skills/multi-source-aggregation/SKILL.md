---
name: Multi-Source Video Aggregation
tier: 2
description: Pattern for building apps that aggregate video content from multiple sources with failover
---

# Multi-Source Video Aggregation Skill

## Purpose
Build video player apps that aggregate content from multiple sources with automatic failover and seamless user experience.

## Architecture Pattern

```
[Multiple Sources] → [Unified Data Model] → [Smart Player] → [User]
                           ↓
                    [Priority System]
                           ↓
                    [Auto Failover]
```

## Data Model

### Movie/Video Object
```json
{
  "_id": "unique_movie_id",
  "title": "Movie Title",
  "poster": "https://cdn.com/poster.jpg",
  "overview": "Description...",
  "sources": [
    {
      "server": "source1",
      "url": "https://source1.com/video.m3u8",
      "quality": "1080p",
      "priority": 1,
      "type": "hls"
    },
    {
      "server": "source2", 
      "url": "https://source2.com/video.mp4",
      "quality": "720p",
      "priority": 2,
      "type": "mp4"
    }
  ]
}
```

## Smart Player Implementation

### 1. Source Selection
```kotlin
class VideoPlayer {
    private var currentSourceIndex = 0
    private var sources: List<VideoSource> = emptyList()
    
    fun loadVideo(movie: Movie) {
        // Sort by priority
        sources = movie.sources.sortedBy { it.priority }
        
        // Try first source
        playSource(sources[0])
    }
    
    private fun playSource(source: VideoSource) {
        when (source.type) {
            "hls" -> playHLS(source.url)
            "mp4" -> playMP4(source.url)
            else -> playDirect(source.url)
        }
    }
}
```

### 2. Auto Failover
```kotlin
private fun setupErrorHandling() {
    player.addListener(object : Player.Listener {
        override fun onPlayerError(error: PlaybackException) {
            handlePlaybackError(error)
        }
    })
}

private fun handlePlaybackError(error: PlaybackException) {
    currentSourceIndex++
    
    if (currentSourceIndex < sources.size) {
        // Try next source
        val nextSource = sources[currentSourceIndex]
        showToast("Switching to ${nextSource.server}...")
        playSource(nextSource)
    } else {
        // All sources failed
        showError("No available sources")
    }
}
```

### 3. Manual Source Selection
```kotlin
fun showSourceSelector() {
    val sourceNames = sources.map { "${it.server} (${it.quality})" }
    
    AlertDialog.Builder(context)
        .setTitle("Select Source")
        .setItems(sourceNames.toTypedArray()) { _, position ->
            currentSourceIndex = position
            playSource(sources[position])
        }
        .show()
}
```

## Data Aggregation

### Merging Multiple Sources
```python
from fuzzywuzzy import fuzz

def merge_movies(all_sources):
    """Merge movies from multiple scrapers by title matching"""
    merged = []
    
    for source_data in all_sources:
        for movie in source_data['movies']:
            # Find existing movie with similar title
            existing = find_similar(merged, movie['title'])
            
            if existing:
                # Add source to existing movie
                existing['sources'].append({
                    'server': source_data['source'],
                    'url': movie['url'],
                    'priority': len(existing['sources']) + 1
                })
            else:
                # Create new movie entry
                merged.append({
                    'title': movie['title'],
                    'poster': movie['poster'],
                    'sources': [{
                        'server': source_data['source'],
                        'url': movie['url'],
                        'priority': 1
                    }]
                })
    
    return merged

def find_similar(movies, title, threshold=85):
    """Find movie with similar title using fuzzy matching"""
    for movie in movies:
        ratio = fuzz.ratio(title.lower(), movie['title'].lower())
        if ratio >= threshold:
            return movie
    return None
```

## Priority System

### Strategy 1: Quality-Based
```python
def assign_priorities_by_quality(sources):
    quality_order = ['2160p', '1080p', '720p', '480p', 'SD']
    
    for source in sources:
        try:
            priority = quality_order.index(source['quality']) + 1
        except ValueError:
            priority = len(quality_order) + 1
        
        source['priority'] = priority
```

### Strategy 2: Reliability-Based
```python
def assign_priorities_by_reliability(sources, stats):
    """Use historical success rate"""
    for source in sources:
        server = source['server']
        success_rate = stats.get(server, {}).get('success_rate', 0.5)
        
        # Higher success rate = lower priority number
        source['priority'] = int((1 - success_rate) * 10)
```

### Strategy 3: Speed-Based
```python
import time
import requests

def test_source_speed(url):
    """Measure response time"""
    try:
        start = time.time()
        requests.head(url, timeout=5)
        return time.time() - start
    except:
        return float('inf')

def assign_priorities_by_speed(sources):
    for source in sources:
        source['speed'] = test_source_speed(source['url'])
    
    # Sort by speed, assign priority
    sources.sort(key=lambda s: s['speed'])
    for i, source in enumerate(sources):
        source['priority'] = i + 1
```

## User Experience Patterns

### Transparent Failover
```kotlin
// Don't interrupt user - silently switch
private var isFailoverInProgress = false

override fun onPlayerError(error: PlaybackException) {
    if (!isFailoverInProgress) {
        isFailoverInProgress = true
        
        // Save playback position
        val position = player.currentPosition
        
        // Switch source
        switchToNextSource()
        
        // Resume from same position
        player.seekTo(position)
        
        isFailoverInProgress = false
    }
}
```

### Progress Indication
```kotlin
// Show subtle notification
showSnackbar(
    "Loading from ${nextSource.server}...",
    duration = Snackbar.LENGTH_SHORT
)
```

### Source Quality Badge
```xml
<!-- Show current source in player UI -->
<TextView
    android:id="@+id/sourceIndicator"
    android:text="Source 1 • 1080p"
    android:alpha="0.7"/>
```

## Handling Different Video Types

```kotlin
fun getMediaItem(source: VideoSource): MediaItem {
    return when (source.type) {
        "hls" -> MediaItem.Builder()
            .setUri(source.url)
            .setMimeType(MimeTypes.APPLICATION_M3U8)
            .build()
            
        "dash" -> MediaItem.Builder()
            .setUri(source.url)
            .setMimeType(MimeTypes.APPLICATION_MPD)
            .build()
            
        else -> MediaItem.fromUri(source.url)
    }
}
```

## Analytics & Optimization

```kotlin
class SourceAnalytics {
    fun recordPlaybackStart(source: VideoSource) {
        logEvent("playback_start", mapOf(
            "server" to source.server,
            "quality" to source.quality
        ))
    }
    
    fun recordPlaybackError(source: VideoSource, error: String) {
        logEvent("playback_error", mapOf(
            "server" to source.server,
            "error" to error
        ))
    }
    
    fun recordSuccessfulPlayback(source: VideoSource, duration: Long) {
        logEvent("playback_success", mapOf(
            "server" to source.server,
            "duration" to duration
        ))
    }
}
```

## Best Practices

1. **Always have fallbacks** - minimum 2 sources per video
2. **Test sources** before showing to user
3. **Cache working sources** temporarily
4. **Provide manual override** - let users choose
5. **Track failures** - improve priority algorithm
6. **Respect timeouts** - don't wait forever
7. **Handle edge cases** - what if all sources fail?

## Common Pitfalls

❌ **Don't**: Try sources sequentially for every playback  
✅ **Do**: Remember last working source

❌ **Don't**: Show error immediately on first failure  
✅ **Do**: Auto-retry with next source silently

❌ **Don't**: Hardcode source priorities  
✅ **Do**: Make priorities dynamic/configurable

---

**Use this skill when**: Building video aggregator apps, implementing failover systems, working with multiple CDNs
