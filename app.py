import sys

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

# ─── ZeroGPU Compatibility ───────────────────────────────────────────────────
try:
    import spaces
    @spaces.GPU
    def _gpu_placeholder():
        return True
except Exception:
    pass
# ──────────────────────────────────────────────────────────────────────────────

import gradio as gr
from main import app as fastapi_app

# ─── Build Gradio Landing Page ───────────────────────────────────────────────
with gr.Blocks(title="Postify AI Backend") as demo:
    gr.Markdown("# 🚀 Postify AI Backend")
    gr.Markdown(
        "The Postify AI FastAPI backend is **running** on Hugging Face Spaces.\n\n"
        "- 📖 **Swagger Docs:** [/docs](/docs)\n"
        "- ⚡ **API Base:** `/api/ai/`\n"
        "- 🏥 **Health Check:** [/health](/health)\n"
    )

# ─── Mount Gradio onto FastAPI App ───────────────────────────────────────────
# Hugging Face Spaces automatically discovers the `app` object in app.py
# and serves it using its internal ASGI server on port 7860.
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
