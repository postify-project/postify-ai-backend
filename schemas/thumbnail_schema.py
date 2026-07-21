from pydantic import BaseModel
from typing import List, Optional

class ThumbRequest(BaseModel):
    video_url: str

# Pehle wala response ab直接 nahi aayega
class ThumbResponse(BaseModel):
    caption: str
    hashtags: List[str]
    thumbnail_url: str

# Naya: Job ID ka response
class ThumbJobResponse(BaseModel):
    job_id: str
    status: str

# Naya: Status check karne ka response
class ThumbStatusResponse(BaseModel):
    status: str
    caption: Optional[str] = None
    hashtags: Optional[List[str]] = None
    thumbnail_url: Optional[str] = None
    error: Optional[str] = None