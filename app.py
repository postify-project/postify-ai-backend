import gradio as gr
from main import app as fastapi_app

# A minimal Gradio interface to satisfy HF Spaces Gradio SDK requirement.
# All actual API routes are served via FastAPI (/api/ai/...)
with gr.Blocks() as demo:
    gr.Markdown("## 🚀 Postify AI Backend")
    gr.Markdown(
        "This is the Postify AI FastAPI backend running on Hugging Face Spaces.\n\n"
        "**API Docs:** [/docs](/docs)\n\n"
        "**Base URL for all endpoints:** `/api/ai/`"
    )

# Mount FastAPI app onto Gradio's ASGI app - Gradio 5 compatible
app = gr.mount_gradio_app(fastapi_app, demo, path="/ui")
