"""
lightrag_adapter.py — AI OS Corp wrapper cho LightRAG
Phase 3: Corp Knowledge Graph (OPEN-004)

Ket noi brain/knowledge/ vao LightRAG graph retrieval.
Khong can AI model ben ngoai — co the dung Ollama local (mien phi).

4 query modes:
  naive  → simple keyword match (nhanh nhat)
  local  → entity-level context (tot cho entity-specific)
  global → cross-document themes (tot cho overview)
  hybrid → local + global combined (RECOMMENDED)

Noop mode: chay binh thuong khi chua cai lightrag-hku.
"""

from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger("aios.lightrag")

# ── Observability ─────────────────────────────────────────────────────────────
try:
    from plugins.observability.observability_adapter import get_obs
    _OBS_AVAILABLE = True
except ImportError:
    _OBS_AVAILABLE = False
    get_obs = None  # type: ignore

# ── Try import lightrag ────────────────────────────────────────────
try:
    from lightrag import LightRAG, QueryParam
    from lightrag.llm.ollama import ollama_model_complete, ollama_embed
    from lightrag.utils import EmbeddingFunc
    _LIGHTRAG_AVAILABLE = True
except ImportError:
    LightRAG = None  # type: ignore
    QueryParam = None  # type: ignore
    _LIGHTRAG_AVAILABLE = False
    logger.warning(
        "[lightrag] lightrag-hku chua duoc cai. "
        "De kich hoat: pip install lightrag-hku"
    )

# ── Root AI OS Corp ────────────────────────────────────────────────
# Dùng env var AOS_ROOT nếu có (set bởi setup.ps1/START_AIOS.ps1)
# Fallback: tính từ vị trí file hiện tại (ecosystem/plugins/LightRAG/lightrag_adapter.py → 4 cấp lên)
_AOS_ROOT = Path(os.getenv("AOS_ROOT") or Path(__file__).resolve().parents[3])
_DEFAULT_WORKING_DIR = _AOS_ROOT / "brain" / "rag_storage" / "lightrag"
_DEFAULT_KNOWLEDGE_DIR = _AOS_ROOT / "brain" / "knowledge"


class LightRAGAdapter:
    """
    AI OS Corp wrapper cho LightRAG.

    Connects brain/knowledge/ to graph-based RAG (OPEN-004).

    Features:
    - insert(text)           — them document vao graph
    - insert_file(path)      — doc file va insert
    - insert_folder(path)    — insert toan bo folder (brain/knowledge/)
    - query(question, mode)  — query theo 4 modes
    - hybrid_query(question) — recommended shortcut (hybrid mode)
    - status()               — kiem tra trang thai

    Noop mode: khi chua cai lightrag-hku hoac Ollama offline.
    """

    def __init__(
        self,
        working_dir: str | Path | None = None,
        llm_model: str | None = None,
        embedding_model: str | None = None,
    ):
        self._working_dir = Path(working_dir or _DEFAULT_WORKING_DIR)
        self._llm_model = llm_model or os.getenv("LIGHTRAG_LLM_MODEL", "gemma2:2b")
        self._embed_model = embedding_model or os.getenv("LIGHTRAG_EMBED_MODEL", "nomic-embed-text")
        self._ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self._rag = None
        self._noop = True
        self._mode = "noop"

        if not _LIGHTRAG_AVAILABLE:
            logger.warning("[lightrag] Noop mode: module khong co san")
            return

        try:
            self._working_dir.mkdir(parents=True, exist_ok=True)
            self._rag = LightRAG(
                working_dir=str(self._working_dir),
                llm_model_func=ollama_model_complete,
                llm_model_name=self._llm_model,
                llm_model_kwargs={
                    "host": self._ollama_url,
                    "options": {"num_ctx": 32768},
                },
                embedding_func=EmbeddingFunc(
                    embedding_dim=768,
                    max_token_size=8192,
                    func=lambda texts: ollama_embed(
                        texts,
                        embed_model=self._embed_model,
                        host=self._ollama_url,
                    ),
                ),
            )
            self._noop = False
            self._mode = f"local-ollama ({self._llm_model} + {self._embed_model})"
            logger.info("[lightrag] Khoi tao thanh cong: %s", self._mode)
        except Exception as e:
            logger.error("[lightrag] Khoi tao that bai: %s", e)
            logger.warning(
                "[lightrag] Noop mode. "
                "Kiem tra Ollama dang chay tai %s va da pull model %s.",
                self._ollama_url, self._llm_model
            )

    # ── Ingest ─────────────────────────────────────────────────────

    def insert(self, text: str, source_hint: str = "") -> bool:
        """
        Them 1 document text vao knowledge graph.
        Hook: onKnowledgeIngest
        """
        if self._noop:
            logger.debug("[lightrag][noop] insert: %d chars", len(text))
            return False
        try:
            self._rag.insert(text)
            if source_hint:
                logger.info("[lightrag] Inserted from %s (%d chars)", source_hint, len(text))
            return True
        except Exception as e:
            logger.error("[lightrag] insert that bai: %s", e)
            return False

    def insert_file(self, path: str | Path) -> bool:
        """
        Doc file (md/txt/pdf text) va insert vao graph.
        """
        if self._noop:
            logger.debug("[lightrag][noop] insert_file: %s", path)
            return False
        try:
            content = Path(path).read_text(encoding="utf-8", errors="ignore")
            if content.strip():
                return self.insert(content, source_hint=str(path))
            logger.warning("[lightrag] File rong: %s", path)
            return False
        except Exception as e:
            logger.error("[lightrag] insert_file that bai %s: %s", path, e)
            return False

    def insert_folder(self, folder: str | Path | None = None, extensions: list[str] | None = None) -> int:
        """
        Insert toan bo folder vao knowledge graph.
        Mac dinh: brain/knowledge/ | extensions: [.md, .txt]

        Hook: onIndexKnowledge — goi sau khi them tai lieu moi.
        """
        folder = Path(folder or _DEFAULT_KNOWLEDGE_DIR)
        extensions = extensions or [".md", ".txt"]

        if self._noop:
            logger.debug("[lightrag][noop] insert_folder: %s", folder)
            return 0

        inserted = 0
        for ext in extensions:
            for f in folder.rglob(f"*{ext}"):
                if self.insert_file(f):
                    inserted += 1

        logger.info("[lightrag] Inserted %d files from %s", inserted, folder)
        return inserted

    # ── Query ─────────────────────────────────────────────────────

    def query(self, question: str, mode: str = "hybrid") -> str:
        """
        Query knowledge graph.

        Modes:
          naive  → keyword match (nhanh, it ton)
          local  → entity context (tot cho specific entities)
          global → cross-doc themes (tot cho overview)
          hybrid → local + global (RECOMMENDED)

        Hook: onQuery
        """
        if self._noop:
            logger.debug("[lightrag][noop] query: %s", question[:60])
            return ""
        try:
            result = self._rag.query(question, param=QueryParam(mode=mode))
            logger.info("[lightrag] Query [%s]: %d chars returned", mode, len(result or ""))
            return result or ""
        except Exception as e:
            logger.error("[lightrag] query that bai: %s", e)
            return ""

    def hybrid_query(self, question: str) -> str:
        """Shortcut: query voi hybrid mode (recommended cho most use cases)."""
        return self.query(question, mode="hybrid")

    def naive_query(self, question: str) -> str:
        """Shortcut: simple keyword match (khi can result nhanh)."""
        return self.query(question, mode="naive")

    # ── Pipeline Helpers ──────────────────────────────────────────

    def index_brain_knowledge(self) -> int:
        """
        Index toan bo brain/knowledge/ vao graph.
        Chay mot lan dau de build index. Sau do chi insert khi co file moi.
        Tuong duong ops/scripts/index_skills_lightrag.py
        """
        logger.info("[lightrag] Indexing brain/knowledge/...")
        count = self.insert_folder(_DEFAULT_KNOWLEDGE_DIR)
        logger.info("[lightrag] Index hoan tat: %d documents", count)
        return count

    def pipeline_ingest_and_query(self, text: str, question: str) -> str:
        """
        Insert text moi → query ngay.
        Pipeline helper cho real-time knowledge augmentation.
        """
        self.insert(text)
        return self.hybrid_query(question)

    # ── Status ────────────────────────────────────────────────────

    def status(self) -> dict:
        return {
            "plugin": "lightrag",
            "available": _LIGHTRAG_AVAILABLE,
            "mode": self._mode,
            "working_dir": str(self._working_dir),
            "knowledge_dir": str(_DEFAULT_KNOWLEDGE_DIR),
            "noop": self._noop,
            "ready": not self._noop,
            "llm_model": self._llm_model,
            "embed_model": self._embed_model,
        }


# ── Singleton factory ─────────────────────────────────────────────
_instance: LightRAGAdapter | None = None


def get_lightrag(working_dir: str | Path | None = None) -> LightRAGAdapter:
    """Lay singleton LightRAGAdapter. Tao moi neu chua co."""
    global _instance
    if _instance is None:
        _instance = LightRAGAdapter(working_dir=working_dir)
    return _instance
