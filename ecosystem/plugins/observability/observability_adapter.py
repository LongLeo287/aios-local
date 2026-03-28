import os
import sys
import time
import functools
import logging
from contextlib import contextmanager
from pathlib import Path

# =========================================================================
# Fix sys.path natively (Issue #85) without blind relative dot "path append"
# =========================================================================
AOS_ROOT = os.getenv("AOS_ROOT")
if AOS_ROOT and AOS_ROOT not in sys.path:
    sys.path.append(AOS_ROOT)

logger = logging.getLogger(__name__)

# Resolve config statically without dependency loops
if AOS_ROOT:
    env_file = Path(AOS_ROOT) / "system" / "ops" / "secrets" / "MASTER.env"
else:
    env_file = Path() / "system" / "ops" / "secrets" / "MASTER.env"

def _load_env():
    env_vars = {}
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('=', 1)
                    if len(parts) == 2:
                        env_vars[parts[0].strip()] = parts[1].strip()
    return env_vars

_env = _load_env()
OBSERVABILITY_MODE = _env.get("OBSERVABILITY_MODE", "noop").lower()

class _NoopSpan:
    def __init__(self, name):
        self.name = name
        self.output = None
    def update(self, **kwargs):
        if "output" in kwargs:
            self.output = kwargs["output"]

class ObservabilityManager:
    """
    Central AI OS Tracing Manager via Langfuse/Langsmith.
    Restored exactly as per ecosystem/skills/observability/SKILL.md protocol.
    """
    def __init__(self):
        self.mode = OBSERVABILITY_MODE
        self.langfuse = None
        self.langsmith = None
        self.initialized = False
        
        if "langfuse" in self.mode or "both" in self.mode:
            try:
                from langfuse import Langfuse
                self.langfuse = Langfuse(
                    public_key=_env.get("LANGFUSE_PUBLIC_KEY"),
                    secret_key=_env.get("LANGFUSE_SECRET_KEY"),
                    host=_env.get("LANGFUSE_HOST", "http://localhost:3000")
                )
                self.initialized = True
            except ImportError:
                logger.warning("Langfuse runtime absent. Defaulting Observability to NOOP.")
        
        if "langsmith" in self.mode or "both" in self.mode:
            try:
                import langsmith
                self.langsmith = langsmith.Client(
                    api_key=_env.get("LANGSMITH_API_KEY"),
                    project_name=_env.get("LANGSMITH_PROJECT", "ai-os-corp")
                )
                self.initialized = True
            except ImportError:
                logger.warning("LangSmith SDK absent. Defaulting to Observability NOOP.")
                
        if not self.initialized:
            self.mode = "noop"

    @contextmanager
    def span(self, name: str):
        if self.mode == "noop":
            yield _NoopSpan(name)
            return

        start_time = time.time()
        span_obj = _NoopSpan(name)
        try:
            yield span_obj
        finally:
            end_time = time.time()
            if "langfuse" in self.mode and self.langfuse:
                try:
                    self.langfuse.span(
                        name=name,
                        start_time=start_time,
                        end_time=end_time,
                        output=span_obj.output
                    )
                except Exception as e:
                    logger.debug(f"Span logging failed gracefully: {e}")

    def trace_llm(self, name: str, model: str, input_text: str, output_text: str, tokens_in: int, tokens_out: int, latency_ms: float):
        """Standard LLM Tracing per Corp Policy"""
        if self.mode == "noop":
            logger.debug(f"[LLM Trace NOOP] {name}|{model}: {tokens_in}in/{tokens_out}out ({latency_ms:.2f}ms)")
            return

        if "langfuse" in self.mode and self.langfuse:
            try:
                self.langfuse.generation(
                    name=name,
                    model=model,
                    input=input_text,
                    output=output_text,
                    usage={"promptTokens": tokens_in, "completionTokens": tokens_out},
                    metadata={"latency_ms": latency_ms}
                )
                self.langfuse.flush()
            except Exception as e:
                logger.debug(f"LLM Generation tracing failed gracefully: {e}")


# -------------------------------------------------------------------------
# Singleton & Decorator Exports for Core OS Components
# -------------------------------------------------------------------------

_instance = None

def get_obs() -> ObservabilityManager:
    global _instance
    if _instance is None:
        _instance = ObservabilityManager()
    return _instance

def trace(name: str):
    """
    Function-level decorator to send execution spans directly into Observability DB.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = None
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                latency = (time.time() - start) * 1000
                obs = get_obs()
                if obs.mode != "noop":
                    if "langfuse" in obs.mode and obs.langfuse:
                        try:
                            # Safe truncation or mapping of arguments to prevent giant payload serialization overload
                            safe_args = str(args)[:2048] if args else ""
                            obs.langfuse.span(
                                name=name,
                                input={"args_trunc": safe_args},
                                output=str(result)[:2048] if result else None,
                            )
                        except Exception:
                            pass
                else:
                    logger.debug(f"[Trace NOOP] '{name}' execution completed in {latency:.2f}ms")
        return wrapper
    return decorator
