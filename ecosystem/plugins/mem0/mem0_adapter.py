"""
mem0_adapter.py — AI OS Corp wrapper for mem0ai
Plugin: mem0 | Version: 1.0.0 | Date: 2026-03-23

Provides a standardized interface for mem0 memory operations
that integrates with AI OS Corp plugin hooks system.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── Observability ─────────────────────────────────────────────────────────────
try:
    from plugins.observability.observability_adapter import get_obs
    _OBS_AVAILABLE = True
except ImportError:
    _OBS_AVAILABLE = False
    get_obs = None  # type: ignore

# Telemetry setup
LOG_DIR = Path(__file__).parent.parent.parent / "telemetry" / "receipts" / "mem0"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("mem0_adapter")


def _log_activation(agent: str, action: str, details: dict):
    """Log every mem0 activation to telemetry/receipts/mem0/"""
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = LOG_DIR / f"{today}.jsonl"
    entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent,
        "action": action,
        **details
    }
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        logger.warning(f"[mem0] Telemetry log failed: {e}")


class Mem0Adapter:
    """
    AI OS Corp wrapper for mem0ai Memory.

    Usage:
        mem = Mem0Adapter(agent_id="acp")

        # Store memory after task
        mem.add(messages, user_id="CEO")

        # Retrieve before task
        results = mem.search("CEO preferred format", user_id="CEO")

        # Inject into system prompt
        context = mem.build_context_string(results)
    """

    def __init__(self, agent_id: str = "acp"):
        self.agent_id = agent_id
        self.available = False
        self._memory = None
        self._init_mem0()

    def _init_mem0(self):
        """Initialize mem0 — gracefully fails if not installed."""
        try:
            from mem0 import Memory

            # Use local storage (no external API required)
            config = {
                "vector_store": {
                    "provider": "qdrant",
                    "config": {
                        "collection_name": f"ai_os_{self.agent_id}",
                        "host": "localhost",
                        "port": 6333,
                        "embedding_model_dims": 1536,
                    }
                }
            }

            # Fallback: in-memory if qdrant not available
            try:
                self._memory = Memory.from_config(config)
            except Exception:
                # Use default local storage (SQLite + local vectors)
                self._memory = Memory()

            self.available = True
            logger.info(f"[mem0] Initialized for agent: {self.agent_id}")

        except ImportError:
            logger.warning(
                "[mem0] mem0ai not installed. Run: pip install mem0ai\n"
                "       Plugin will operate in no-op mode until installed."
            )
        except Exception as e:
            logger.warning(f"[mem0] Init failed (non-critical): {e}")

    # ─── Core API ─────────────────────────────────────────────────────────────

    def add(self, messages: list, user_id: str = "CEO", metadata: dict = None) -> dict:
        """
        Store new memories from a conversation.
        Called in onTaskComplete hook.

        Args:
            messages: List of {"role": "user/assistant", "content": "..."}
            user_id: "CEO", "agent_name", etc.
            metadata: Optional extra info (task_id, dept, etc.)

        Returns:
            dict with memory_id(s) or {"status": "no-op"} if unavailable
        """
        if not self.available:
            return {"status": "no-op", "reason": "mem0 not installed"}

        try:
            result = self._memory.add(
                messages,
                user_id=user_id,
                agent_id=self.agent_id,
                metadata=metadata or {}
            )
            _log_activation(self.agent_id, "add", {
                "user_id": user_id,
                "message_count": len(messages),
                "memories_added": len(result.get("results", []))
            })
            return result
        except Exception as e:
            logger.error(f"[mem0] add failed: {e}")
            return {"status": "error", "error": str(e)}

    def search(self, query: str, user_id: str = "CEO", limit: int = 5) -> list:
        """
        Retrieve relevant memories for a query.
        Called in onTaskStart hook.

        Args:
            query: Natural language query
            user_id: Who to search memories for
            limit: Max number of results

        Returns:
            List of memory dicts with 'memory' and 'score' fields
        """
        if not self.available:
            return []

        try:
            results = self._memory.search(query, user_id=user_id, limit=limit)
            memories = results.get("results", [])
            _log_activation(self.agent_id, "search", {
                "user_id": user_id,
                "query": query[:100],
                "results_count": len(memories)
            })
            return memories
        except Exception as e:
            logger.error(f"[mem0] search failed: {e}")
            return []

    def get_all(self, user_id: str = "CEO") -> list:
        """Get all stored memories for a user."""
        if not self.available:
            return []
        try:
            results = self._memory.get_all(user_id=user_id)
            return results.get("results", [])
        except Exception as e:
            logger.error(f"[mem0] get_all failed: {e}")
            return []

    # ─── AI OS Hooks ──────────────────────────────────────────────────────────

    def on_task_start(self, task_description: str, user_id: str = "CEO") -> str:
        """
        Hook: onTaskStart
        Retrieves relevant memories and returns context string to inject
        into the agent's system prompt.

        Returns:
            str: Formatted memory context block, or empty string
        """
        memories = self.search(task_description, user_id=user_id)
        return self.build_context_string(memories)

    def on_task_complete(self, messages: list, user_id: str = "CEO", metadata: dict = None):
        """
        Hook: onTaskComplete
        Stores learnings from the completed task.
        """
        return self.add(messages, user_id=user_id, metadata=metadata)

    def on_handoff(self, target_agent: str, context: dict, user_id: str = "CEO") -> dict:
        """
        Hook: onHandoff
        Packages memories for cross-agent context transfer.
        """
        memories = self.get_all(user_id=user_id)
        context["mem0_context"] = memories[:10]  # top 10 memories
        return context

    # ─── Utilities ────────────────────────────────────────────────────────────

    def build_context_string(self, memories: list) -> str:
        """
        Format retrieved memories as a system prompt context block.

        Example output:
            [MEMORY CONTEXT]
            - CEO prefers JSON format for reports
            - ClawTask runs on port 7474
        """
        if not memories:
            return ""

        lines = ["[MEMORY CONTEXT — from previous sessions]"]
        for m in memories:
            memory_text = m.get("memory", "")
            score = m.get("score", 0)
            if memory_text:
                lines.append(f"- {memory_text}")

        return "\n".join(lines) + "\n"

    @property
    def status(self) -> dict:
        """Return plugin status for health checks."""
        return {
            "plugin": "mem0",
            "agent_id": self.agent_id,
            "available": self.available,
            "version": "1.0.0"
        }


# ─── Singleton factory ──────────────────────────────────────────────────────

_instances: dict[str, Mem0Adapter] = {}


def get_mem0(agent_id: str = "acp") -> Mem0Adapter:
    """Get or create a Mem0Adapter instance for the given agent."""
    if agent_id not in _instances:
        _instances[agent_id] = Mem0Adapter(agent_id=agent_id)
    return _instances[agent_id]
