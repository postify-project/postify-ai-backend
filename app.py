import gradio as gr
from main import app
import uvicorn

# We create a simple Gradio interface
def greet():
    return "POSTIFY AI FastAPI Backend is up and running! Visit /docs for the API documentation."

demo = gr.Interface(fn=greet, inputs=[], outputs="text", title="Postify AI Backend")

# Mount the Gradio app onto the FastAPI app
# This satisfies Hugging Face's Gradio SDK requirements while keeping your FastAPI routes fully functional
app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
