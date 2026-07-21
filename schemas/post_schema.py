from pydantic import BaseModel
from typing import List

class PostRequest(BaseModel):
    topic: str          
    platform: str       
    tone: str = "Professional" 

class PostResponse(BaseModel):
    caption: str
    hashtags: List[str]
    call_to_action: str
    image_prompt: str  
    image_url: str     