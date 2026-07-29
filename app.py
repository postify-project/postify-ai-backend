import sys

# ─── Compatibility shim ────────────────────────────────────────────────────────
# Newer versions of huggingface_hub removed HfFolder, but gradio[oauth]==4.x
# still imports it. We inject a stub before gradio loads to avoid ImportError.
try:
    from huggingface_hub import HfFolder  # noqa: F401 - already exists, skip
except ImportError:
    import types
    import huggingface_hub

    class _HfFolderStub:
        """Minimal stub for the removed huggingface_hub.HfFolder class."""
        token: str | None = None

        @classmethod
        def get_token(cls) -> str | None:
            return cls.token

        @classmethod
        def save_token(cls, token: str) -> None:
            cls.token = token

        @classmethod
        def delete_token(cls) -> None:
            cls.token = None

    huggingface_hub.HfFolder = _HfFolderStub  # type: ignore[attr-defined]
    sys.modules["huggingface_hub"].HfFolder = _HfFolderStub  # type: ignore[attr-defined]
# ──────────────────────────────────────────────────────────────────────────────

import gradio as gr
from main import app as fastapi_app

# Minimal Gradio UI – all real traffic goes through FastAPI routes at /api/ai/
with gr.Blocks(title="Postify AI Backend") as demo:
    gr.Markdown("## 🚀 Postify AI Backend")
    gr.Markdown(
        "The Postify AI FastAPI backend is **running**.\n\n"
        "- 📖 **API Docs:** [/docs](/docs)\n"
        "- ⚡ **Base URL:** `/api/ai/`"
    )

# Mount FastAPI under the Gradio ASGI app
app = gr.mount_gradio_app(fastapi_app, demo, path="/ui")
