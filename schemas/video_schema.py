from pydantic import BaseModel
from typing import List, Optional

# AI ke script ke format ke liye models
class VideoScene(BaseModel):
    visuals: str
    voiceover: str

class VideoScriptResponse(BaseModel):
    scenes: List[VideoScene]

# API Request/Response models
class VideoGenRequest(BaseModel):
    prompt: str
    captions: bool = False # Naya parameter (default False)

# Naya: Job ID ka response
class VideoJobResponse(BaseModel):
    job_id: str
    status: str

# Naya: Status check karne ka response
class VideoStatusResponse(BaseModel):
    status: str
    video_url: Optional[str] = None
    script: Optional[str] = None
    error: Optional[str] = None