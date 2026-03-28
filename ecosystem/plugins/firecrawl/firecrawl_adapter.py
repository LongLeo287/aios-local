"""
firecrawl_adapter.py — AI OS Corp wrapper cho firecrawl
Phase 2: Web Intelligence Plugin

KHÔNG cần AI model — firecrawl chi la web scraper/HTML cleaner.
AI model (Claude/Ollama) dung SAU de xu ly text da co.

Che do hoat dong (theo thu tu uu tien):
  1. Self-hosted: FIRECRAWL_URL=http://localhost:3002  (khong can API key)
  2. Cloud API:   FIRECRAWL_API_KEY=fc-...             (can API key)
  3. Noop:        ca hai deu khong co                  (tra ve empty, khong crash)

Kich hoat self-hosted:
  cd plugins/firecrawl && docker compose up -d
  (server tu dong chay tai localhost:3002)
"""

from __future__ import annotations

import os
import logging
from typing import Any

logger = logging.getLogger("aios.firecrawl")

# ── Observability ─────────────────────────────────────────────────────────────
try:
    from ecosystem.plugins.observability.observability_adapter import get_obs
    _OBS_AVAILABLE = True
except ImportError:
    _OBS_AVAILABLE = False
    get_obs = None  # type: ignore

# ── Try import firecrawl-py ────────────────────────────────────────
try:
    from firecrawl import FirecrawlApp as _FirecrawlApp
    _FIRECRAWL_AVAILABLE = True
except ImportError:
    _FirecrawlApp = None  # type: ignore
    _FIRECRAWL_AVAILABLE = False


class FirecrawlAdapter:
    """
    AI OS Corp wrapper cho firecrawl.

    Tu dong chon che do:
    - Self-hosted (FIRECRAWL_URL set) → dung localhost, khong can API key
    - Cloud (FIRECRAWL_API_KEY set)   → dung firecrawl.dev
    - Noop                            → log warning, tra ve empty
    """

    def __init__(self, api_key: str | None = None, api_url: str | None = None):
        self._api_key  = api_key  or os.getenv("FIRECRAWL_API_KEY", "")
        self._api_url  = api_url  or os.getenv("FIRECRAWL_URL", "")
        self._client   = None
        self._noop     = True
        self._mode     = "noop"

        if not _FIRECRAWL_AVAILABLE:
            logger.warning(
                "[firecrawl] firecrawl-py chua cai. "
                "De kich hoat: pip install firecrawl-py"
            )
            return

        # ── Uu tien 1: Self-hosted ─────────────────────────────────
        if self._api_url:
            try:
                # self-hosted: api_key co the bo trong hoac dat "self-hosted"
                key = self._api_key or "self-hosted"
                self._client = _FirecrawlApp(api_key=key, api_url=self._api_url)
                self._noop   = False
                self._mode   = f"self-hosted ({self._api_url})"
                logger.info("[firecrawl] Self-hosted mode: %s", self._api_url)
            except Exception as e:
                logger.error("[firecrawl] Self-hosted khoi tao that bai: %s", e)
            return

        # ── Uu tien 2: Cloud API ───────────────────────────────────
        if self._api_key:
            try:
                self._client = _FirecrawlApp(api_key=self._api_key)
                self._noop   = False
                self._mode   = "cloud (firecrawl.dev)"
                logger.info("[firecrawl] Cloud mode voi API key")
            except Exception as e:
                logger.error("[firecrawl] Cloud khoi tao that bai: %s", e)
            return

        # ── Noop ───────────────────────────────────────────────────
        logger.warning(
            "[firecrawl] Noop mode. "
            "Self-host: docker compose up -d trong plugins/firecrawl/, "
            "sau do set FIRECRAWL_URL=http://localhost:3002 trong MASTER.env. "
            "Hoac Cloud: set FIRECRAWL_API_KEY=fc-..."
        )

    # ── Core API ───────────────────────────────────────────────────

    def scrape_url(self, url: str, formats: list[str] | None = None) -> str:
        """Scrape 1 URL → markdown. Hook: onResearch"""
        if self._noop:
            logger.debug("[firecrawl][noop] scrape_url: %s", url)
            return ""
        try:
            formats = formats or ["markdown"]
            result  = self._client.scrape_url(url, formats=formats)
            content = result.get("markdown", "") if isinstance(result, dict) else str(result)
            logger.info("[firecrawl] Scraped %d chars tu %s", len(content), url)
            return content
        except Exception as e:
            logger.error("[firecrawl] scrape_url that bai %s: %s", url, e)
            return ""

    def crawl_site(self, url: str, limit: int = 100) -> list[str]:
        """Crawl toan bo site → list markdown. Hook: onCrawlDocs"""
        if self._noop:
            logger.debug("[firecrawl][noop] crawl_site: %s", url)
            return []
        try:
            result = self._client.crawl_url(
                url,
                params={"limit": limit, "scrapeOptions": {"formats": ["markdown"]}}
            )
            pages = []
            data  = result.get("data", []) if isinstance(result, dict) else []
            for page in data:
                md = page.get("markdown", "") if isinstance(page, dict) else ""
                if md:
                    pages.append(md)
            logger.info("[firecrawl] Crawled %d pages tu %s", len(pages), url)
            return pages
        except Exception as e:
            logger.error("[firecrawl] crawl_site that bai %s: %s", url, e)
            return []

    def extract_structured(self, url: str, schema: dict) -> dict:
        """Extract data co cau truc theo schema. Hook: onExtractData"""
        if self._noop:
            logger.debug("[firecrawl][noop] extract_structured: %s", url)
            return {}
        try:
            result = self._client.extract_url(url, schema=schema)
            logger.info("[firecrawl] Extracted tu %s", url)
            return result if isinstance(result, dict) else {}
        except Exception as e:
            logger.error("[firecrawl] extract_structured that bai %s: %s", url, e)
            return {}

    def batch_scrape(self, urls: list[str]) -> list[str]:
        """Scrape nhieu URLs → list markdown"""
        if self._noop:
            return []
        return [c for url in urls if (c := self.scrape_url(url))]

    def map_site(self, url: str) -> list[str]:
        """Lay danh sach tat ca URLs cua site"""
        if self._noop:
            return []
        try:
            result = self._client.map_url(url)
            urls   = result if isinstance(result, list) else result.get("links", [])
            logger.info("[firecrawl] Mapped %d URLs tu %s", len(urls), url)
            return urls
        except Exception as e:
            logger.error("[firecrawl] map_site that bai %s: %s", url, e)
            return []

    # ── Pipeline Helpers ──────────────────────────────────────────

    def research_url(self, url: str) -> str:
        """onResearch hook: scrape 1 URL → markdown cho agent"""
        return self.scrape_url(url)

    def ingest_to_rag(self, url: str, rag_insert_fn: Any, limit: int = 50) -> int:
        """
        Pipeline: crawl site → insert tung page vao RAG.
        Vi du: fc.ingest_to_rag(url, lightrag.insert)
        """
        pages    = self.crawl_site(url, limit=limit)
        inserted = 0
        for page in pages:
            try:
                rag_insert_fn(page)
                inserted += 1
            except Exception as e:
                logger.error("[firecrawl] rag insert that bai: %s", e)
        logger.info("[firecrawl] Ingested %d/%d pages vao RAG", inserted, len(pages))
        return inserted

    # ── Status ────────────────────────────────────────────────────

    def status(self) -> dict:
        return {
            "plugin":       "firecrawl",
            "available":    _FIRECRAWL_AVAILABLE,
            "mode":         self._mode,
            "api_key_set":  bool(self._api_key),
            "api_url_set":  bool(self._api_url),
            "noop":         self._noop,
            "ready":        not self._noop,
        }


# ── Singleton factory ─────────────────────────────────────────────
_instance: FirecrawlAdapter | None = None


def get_firecrawl(api_key: str | None = None, api_url: str | None = None) -> FirecrawlAdapter:
    """Lay singleton FirecrawlAdapter. Tao moi neu chua co."""
    global _instance
    if _instance is None:
        _instance = FirecrawlAdapter(api_key=api_key, api_url=api_url)
    return _instance
