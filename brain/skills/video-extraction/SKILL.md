---
name: Video Stream Extraction
tier: 2
description: Skills for extracting direct video URLs from streaming websites for ad-free playback
---

# Video Stream Extraction Skill

## Purpose
Extract direct m3u8/mp4 URLs from streaming websites without ads or DRM for integration into custom video players.

## Core Techniques

### 1. Multi-Level URL Analysis
Most streaming sites use layered architecture:
```
Movie Info Page → Watch Page → Player Iframe → Video Stream
```

**Process:**
1. Start with movie/show page
2. Find "Watch" or "Play" button → extract watch page URL
3. Fetch watch page → find player iframe src
4. Fetch iframe content → extract video stream URL

### 2. Iframe Inspection
```python
from bs4 import BeautifulSoup

def extract_player_iframe(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Common iframe patterns
    iframe = (
        soup.find('iframe', {'id': 'player'}) or
        soup.find('iframe', {'class': 'player'}) or
        soup.find('iframe', src=re.compile(r'player|embed'))
    )
    
    return iframe.get('src') if iframe else None
```

### 3. Video URL Patterns
Look for these patterns in JavaScript/HTML:
```regex
# HLS streams
https?://[^"']+\.m3u8[^"']*

# MP4 files
https?://[^"']+\.mp4[^"']*

# JWPlayer config
file:\s*["']([^"']+)["']

# Generic player config
sources?:\s*\[?\s*["']([^"']+)["']
```

### 4. Network Traffic Capture
Use Selenium with performance logging:
```python
from selenium.webdriver.chrome.options import Options

options = Options()
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

# Capture all network requests
logs = driver.get_log('performance')
for entry in logs:
    if '.m3u8' in entry['message'] or '.mp4' in entry['message']:
        # Extract video URL
        pass
```

## Common Challenges

### Challenge 1: Anti-Bot Protection
**Solution**: Mimic real browser behavior
- Use realistic User-Agent
- Respect rate limits (delays between requests)
- Maintain session cookies
- Add Referer headers

### Challenge 2: Token/Auth in URLs
**Pattern**: `video.m3u8?token=abc123&expires=1234567890`

**Solution**: Extract full URL with params
```python
# Don't parse URL - keep as-is
video_url = match.group(0)  # Full match with query params
```

### Challenge 3: Encrypted Streams
**Pattern**: AES-128 encrypted HLS

**Detection**: Look for `#EXT-X-KEY` in m3u8 manifest

**Solution**: 
- ExoPlayer handles HLS encryption automatically
- No need to decrypt manually

### Challenge 4: Dynamic CDN
URLs change per request/session

**Solution**: Extract URL at playback time, not in advance

## Testing Video URLs

```python
def test_video_url(url):
    """Verify video URL is valid and playable"""
    import requests
    
    try:
        response = requests.head(url, timeout=5)
        
        # Check content type
        content_type = response.headers.get('Content-Type', '')
        
        if 'video' in content_type or 'mpegurl' in content_type:
            return True
        
        # For m3u8, fetch and check content
        if url.endswith('.m3u8'):
            manifest = requests.get(url, timeout=5).text
            return '#EXTM3U' in manifest
            
    except:
        return False
    
    return False
```

## Best Practices

1. **Always test URLs** before storing
2. **Handle failures gracefully** - have backup sources
3. **Respect robots.txt** and site ToS
4. **Cache results** temporarily (URLs may expire)
5. **Log failures** for debugging

## Quick Reference

**Typical extraction flow:**
```python
def extract_video_url(movie_url):
    # 1. Get watch page URL
    watch_url = get_watch_page_url(movie_url)
    
    # 2. Fetch watch page
    watch_html = fetch_page(watch_url)
    
    # 3. Extract iframe src
    iframe_src = extract_iframe(watch_html)
    
    # 4. Fetch iframe content
    iframe_html = fetch_page(iframe_src)
    
    # 5. Extract video URL
    video_url = extract_video_from_html(iframe_html)
    
    # 6. Validate
    if test_video_url(video_url):
        return video_url
    
    return None
```

---

**Use this skill when**: Working with streaming websites, need direct video URLs, building video aggregator apps
