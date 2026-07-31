import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api import routes_reply, routes_metadata, routes_post, routes_improvement, routes_video, routes_thumbnail, routes_translate, routes_context 
from cloud_storage.config import init_cloudinary

# Initialize Cloudinary configuration
init_cloudinary()

app = FastAPI(title="POSTIFY AI Backend", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

os.makedirs("images", exist_ok=True)
os.makedirs("videos", exist_ok=True)

app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/videos", StaticFiles(directory="videos"), name="videos")

# Routers
app.include_router(routes_reply.router, prefix="/api/ai/reply", tags=["AI Auto-Reply"])
app.include_router(routes_metadata.router, prefix="/api/ai/metadata", tags=["AI Metadata Generator"])
app.include_router(routes_post.router, prefix="/api/ai/post", tags=["AI Post Generator"])
app.include_router(routes_improvement.router, prefix="/api/ai/improve", tags=["AI Improvement Engine"])
app.include_router(routes_video.router, prefix="/api/ai/video", tags=["AI Video Generator"])
app.include_router(routes_thumbnail.router, prefix="/api/ai/thumbnail", tags=["AI Thumbnail & Caption"])
app.include_router(routes_translate.router, prefix="/api/ai/translate", tags=["AI Video Translator"])
app.include_router(routes_context.router, prefix="/api/ai/context", tags=["User Context"])

@app.get("/health")
def health_check():
    return {"status": "POSTIFY AI Backend is healthy!"}

@app.get("/health/cloudinary", tags=["Health"])
def check_cloudinary_health():
    """
    Pings the Cloudinary API to verify if the credentials are correct and working.
    """
    import cloudinary.api
    try:
        result = cloudinary.api.ping()
        return {
            "status": "success", 
            "message": "Cloudinary is successfully integrated!", 
            "cloudinary_response": result
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": "Cloudinary integration failed.", 
            "details": str(e)
        }

@app.get("/")
def read_root():
    return {"status": "POSTIFY AI Backend is running successfully!"}