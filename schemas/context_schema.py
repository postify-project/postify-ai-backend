from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class QuestionResponse(BaseModel):
    id: str
    question: str
    options: Optional[List[str]] = None
    type: str # text, select, etc.

class UserContext(BaseModel):
    accountType: Optional[str] = None
    brandDescription: Optional[str] = None
    brandName: Optional[str] = None
    brandTagline: Optional[str] = None
    contentFormat: Optional[str] = None
    creatorNiche: Optional[str] = None
    creatorPersona: Optional[str] = None
    emojiRule: Optional[str] = None
    hashtags: Optional[str] = None
    imageryStyle: Optional[str] = None
    industry: Optional[str] = None
    keywords: Optional[str] = None
    logoUrl: Optional[str] = None
    primaryCTA: Optional[str] = None
    primaryColor: Optional[str] = None
    secondaryColor: Optional[str] = None
    tone: Optional[str] = None
    website: Optional[str] = None
