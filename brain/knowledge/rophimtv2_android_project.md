---
source: D:\Project\DATA\Archive\Antigravity-Workspace\MASTER_PROMPT.md
ingested_at: 2026-03-16T10:34:00+07:00
domain: Project|Android|TV|Architecture
trust_level: LOCAL_DOC
vet_status: PASS
tags: [rophimtv2, android-tv, kotlin, ddd, clean-architecture, exoplayer, jetpack-compose, web-scraping]
---

# RophimTV2 — Android TV Project Master Prompt

**Project:** RophimTV2 — Vietnamese movie Android TV app  
**Source file:** `Antigravity-Workspace/MASTER_PROMPT.md`  
**Platform:** Android TV, min SDK 21 (Android 5.0+)  
**Language:** Kotlin with Jetpack Compose for TV

---

## Architecture

```
Domain Layer → Data Layer (Repository) → UI Layer
(DDD sequence — DO NOT skip)
```

### Tech Stack
| Module | Tech |
|--------|------|
| UI | Jetpack Compose for TV / Leanback Library |
| Navigation | D-Pad only (10-foot UI) |
| Scraping | Jsoup + Kotlin Coroutines (Dispatchers.IO) |
| Video | ExoPlayer for TV |
| YouTube | NewPipeExtractor (NOT YouTube Data API v3) |

---

## Data Sources Strategy

### YouTube (Muse VN, POPS, Ani-One)
```kotlin
// MUST use NewPipeExtractor — NOT:
// ❌ YouTube Data API v3 (quota limits)
// ❌ WebView iframe embed
// ✅ NewPipeExtractor → raw .mp4 → ExoPlayer
```

### Standard Web Sources (AnimeVsub, GogoPhim, RoPhimTV)
```kotlin
// Jsoup + Coroutines on Dispatchers.IO
// Cross-reference con IMDb cho metadata + posters
```

### Cloudflare-Protected Sources (Motchill, PhimMoi, Phim4k, 30phim)
```kotlin
// KHÔNG dùng Jsoup trực tiếp → 403 Forbidden
// PHẢI dùng HeadlessWebView (background, invisible)
// Override shouldInterceptRequest()
// Capture .m3u8 hoặc .ts URLs → ExoPlayer
```

---

## Reference Architecture Map

| Module | Primary Ref | Secondary Ref |
|--------|-------------|---------------|
| TV UI + Leanback | Google-TV-Samples | Shiru |
| Video (ExoPlayer) | SmartTubeNext | decompiled_apks/Rophim |
| YouTube Extract | NewPipeExtractor | — |
| Scraping | CloudStream3 | decompiled_apks/Phim4K |
| Anime TV UI | Anime-TV | animevsub-web |
| Ad-blocking | decompiled_apks/AnimeTV | — |
| DDD Architecture | awesome-ddd | typescript-ddd-example |

---

## APIs Available

| API | URL | Auth |
|-----|-----|------|
| OPhim | https://ophim1.com/ | Free |
| KKPhim | https://phimapi.com/ | Free |
| NguonC | https://phim.nguonc.com/api/ | Free |
| TMDB | https://api.themoviedb.org/3/ | API Key |
| OMDb | https://www.omdbapi.com/ | API Key |
| Trakt | https://api.trakt.tv/ | API Key |

---

## Project Structure Constraint (STRICT)
```
RophimTV2/
 ┣ build.gradle.kts
 ┣ settings.gradle.kts
 ┗ app/src/main/
    ┣ AndroidManifest.xml (MUST: android.software.leanback)
    ┗ java/com/longleo/rophimtv2/
       ┣ core/         (Scraper, Network utils)
       ┣ data/         (Repository, Room, Remote)
       ┣ domain/       (Entities, UseCases, Repo interfaces)
       ┗ presentation/ (UI, ViewModels)
```

---

## Relevance cho AI OS
File này là **project context** cho RophimTV2 — không trực tiếp liên quan đến AI OS architecture nhưng:
- Pattern DDD tốt để reference cho future projects
- Cloudflare bypass pattern (HeadlessWebView) useful
- NewPipeExtractor pattern cho YouTube extraction
