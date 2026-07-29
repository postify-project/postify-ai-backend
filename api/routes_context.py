from fastapi import APIRouter
from schemas.context_schema import UserContext, QuestionResponse
from typing import List

router = APIRouter()

# In-memory storage for the sake of the mock API
mock_context = {
    "accountType": "Influencer / Creator",
    "brandDescription": "social media automation",
    "brandName": "postify",
    "brandTagline": "automate your social media",
    "contentFormat": "Text Threads & Short Tips",
    "creatorNiche": "Software Development & AI",
    "creatorPersona": "The Curious Builder (Raw & Behind-the-Scenes)",
    "emojiRule": "Minimal (1-2 total in caption)",
    "hashtags": "#buildinpublic #indiehackers #postify",
    "imageryStyle": "Real Photography & Clean",
    "industry": "B2B SaaS & Tech",
    "keywords": "saas, nextjs, ai tools, webdev",
    "logoUrl": "",
    "primaryCTA": "DM me 'GROWTH' to start",
    "primaryColor": "#8b5cf6",
    "secondaryColor": "#ec4899",
    "tone": "Professional & Corporate",
    "website": ""
}

@router.get("/questions", response_model=List[QuestionResponse], summary="Get Onboarding Questions", description="Returns a list of questions to ask the user to build their context.")
async def get_questions():
    return [
        {"id": "accountType", "question": "What is your account type?", "options": ["Influencer / Creator", "Brand / Business", "Personal"], "type": "select"},
        {"id": "brandName", "question": "What is your brand or creator name?", "type": "text"},
        {"id": "brandTagline", "question": "What is your brand's tagline?", "type": "text"},
        {"id": "brandDescription", "question": "Briefly describe your brand or content.", "type": "text"},
        {"id": "contentFormat", "question": "What is your preferred content format?", "options": ["Text Threads & Short Tips", "Long-form Videos", "Short-form Videos", "Images & Carousels"], "type": "select"},
        {"id": "creatorNiche", "question": "What is your niche?", "type": "text"},
        {"id": "creatorPersona", "question": "How would you describe your persona?", "options": ["The Curious Builder (Raw & Behind-the-Scenes)", "The Expert (Authoritative & Educational)", "The Entertainer (Fun & Engaging)"], "type": "select"},
        {"id": "emojiRule", "question": "What is your rule for emojis?", "options": ["Minimal (1-2 total in caption)", "Heavy (Lots of emojis)", "None"], "type": "select"},
        {"id": "hashtags", "question": "What are your primary hashtags?", "type": "text"},
        {"id": "imageryStyle", "question": "What is your preferred imagery style?", "options": ["Real Photography & Clean", "Illustrations", "AI Generated", "Minimalist"], "type": "select"},
        {"id": "industry", "question": "What industry are you in?", "type": "text"},
        {"id": "keywords", "question": "What are some keywords associated with your brand?", "type": "text"},
        {"id": "primaryCTA", "question": "What is your primary Call to Action (CTA)?", "type": "text"},
        {"id": "primaryColor", "question": "What is your primary brand color (Hex)?", "type": "text"},
        {"id": "secondaryColor", "question": "What is your secondary brand color (Hex)?", "type": "text"},
        {"id": "tone", "question": "What is your brand's tone of voice?", "options": ["Professional & Corporate", "Casual & Friendly", "Humorous & Witty", "Inspirational"], "type": "select"},
    ]

@router.get("/", response_model=UserContext, summary="Get User Context", description="Returns the current user's context and preferences.")
async def get_context():
    return mock_context

@router.post("/", response_model=UserContext, summary="Update User Context", description="Updates and saves the user's context and preferences.")
async def update_context(context: UserContext):
    global mock_context
    updated_data = context.model_dump(exclude_unset=True)
    mock_context.update(updated_data)
    return mock_context
