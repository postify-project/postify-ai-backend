from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import routes_reply, routes_metadata, routes_post # routes_post add kiya

app = FastAPI(
    title="QRYZON AI Backend",
    description="AI APIs for Social Media Management",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto Reply Router
app.include_router(routes_reply.router, prefix="/api/ai/reply", tags=["AI Auto-Reply"])

# Metadata Router
app.include_router(routes_metadata.router, prefix="/api/ai/metadata", tags=["AI Metadata Generator"])

# Post Generation Router (Naya)
app.include_router(routes_post.router, prefix="/api/ai/post", tags=["AI Post Generator"])

@app.get("/")
def read_root():
    return {"status": "QRYZON AI Backend is running successfully!"}