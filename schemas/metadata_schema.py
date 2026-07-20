from pydantic import BaseModel
from typing import List

class MetadataRequest(BaseModel):
    video_transcript: str # Video ka text ya summary
    platform: str = "YouTube" # Kis platform ke liye chahiye

class MetadataResponse(BaseModel):
    title: str
    description: str
    tags: List[str]