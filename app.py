import sys
import os

# ─── HfFolder Compatibility Shim ─────────────────────────────────────────────
# Must run before `import gradio` since Gradio 4.x imports HfFolder at load time.
try:
    from huggingface_hub import HfFolder  # noqa: F401
except ImportError:
    import huggingface_hub

    class _HfFolderStub:
        """Stub for removed huggingface_hub.HfFolder."""
        _token = None

        @classmethod
        def get_token(cls):
            return cls._token

        @classmethod
        def save_token(cls, token):
            cls._token = token

        @classmethod
        def delete_token(cls):
            cls._token = None

    huggingface_hub.HfFolder = _HfFolderStub
    sys.modules["huggingface_hub"].HfFolder = _HfFolderStub
# ──────────────────────────────────────────────────────────────────────────────

import gradio as gr

# ─── ZeroGPU decorator (required if Space hardware = ZeroGPU) ─────────────────
try:
    import spaces
    @spaces.GPU
    def _gpu_placeholder():
        return True
except Exception:
    pass
# ──────────────────────────────────────────────────────────────────────────────

# ─── Import FastAPI app and all its routers from main.py ──────────────────────
from main import app as fastapi_app

# ─── Build the Gradio UI ─────────────────────────────────────────────────────
with gr.Blocks(title="Postify AI Backend") as demo:
    gr.Markdown("# 🚀 Postify AI Backend")
    gr.Markdown(
        "The Postify AI FastAPI backend is **running** on Hugging Face Spaces.\n\n"
        "- 📖 **Swagger Docs:** [Open API Docs](/docs)\n"
        "- ⚡ **API Base:** `/api/ai/`\n"
        "- 🏥 **Health:** [/health](/health)\n"
    )

# ─── Mount ALL FastAPI routes onto Gradio's internal ASGI app ─────────────────
# This is the KEY: Gradio's demo.launch() creates its own FastAPI app internally.
# We attach our routers and middleware to that internal app BEFORE launch.
gradio_fastapi = demo.app

# Copy CORS middleware
from fastapi.middleware.cors import CORSMiddleware
gradio_fastapi.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Copy all routes from our FastAPI app
for route in fastapi_app.routes:
    gradio_fastapi.routes.append(route)

# ─── Launch ──────────────────────────────────────────────────────────────────
# demo.launch() starts Gradio's own Uvicorn server. This is what HF Spaces
# Gradio SDK expects. Do NOT call uvicorn.run() separately.
demo.launch(server_name="0.0.0.0", server_port=7860)
