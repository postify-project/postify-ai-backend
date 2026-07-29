import sys

# ─── Compatibility shim ────────────────────────────────────────────────────────
try:
    from huggingface_hub import HfFolder  # noqa: F401
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

# ─── ZeroGPU Compatibility ───────────────────────────────────────────────────
try:
    import spaces
    @spaces.GPU
    def _gpu_init_check():
        return "ZeroGPU Ready"
except Exception:
    pass
# ──────────────────────────────────────────────────────────────────────────────

import gradio as gr
import uvicorn
from main import app as fastapi_app

# Create a clean Gradio interface as the landing page
with gr.Blocks(title="Postify AI Backend") as demo:
    gr.Markdown("# 🚀 Postify AI Backend")
    gr.Markdown(
        "The Postify AI FastAPI backend is running successfully!\n\n"
        "- 📖 **Interactive API Documentation (Swagger):** [/docs](/docs)\n"
        "- ⚡ **Base API Route:** `/api/ai/`\n"
        "- 🏥 **Health Check:** [/health](/health)\n"
    )

# Mount Gradio at root "/" so Hugging Face health check (/config, /info) succeeds
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=7860)
