from fastapi import APIRouter
from schemas.post_schema import PostRequest, PostResponse
from core.llm_setup import get_llm
from core.prompts import POST_PROMPT
from langchain_core.output_parsers import JsonOutputParser
import urllib.parse # URL encoding ke liye

router = APIRouter()

@router.post("/", response_model=PostResponse)
async def generate_post(request: PostRequest):
    llm = get_llm()
    
    # JSON Parser setup
    parser = JsonOutputParser(pydantic_object=PostResponse)
    
    # AI chain banana
    chain = POST_PROMPT | llm | parser
    
    # AI ko invoke karna (Text + Image Prompt generate hoga)
    response = chain.invoke({
        "topic": request.topic,
        "platform": request.platform,
        "tone": request.tone,
        "format_instructions": parser.get_format_instructions()
    })
    
    # AI ne jo image prompt banaya hai usay nikalna
    img_prompt = response.get("image_prompt", request.topic)
    
    # Free Image Generation (Pollinations.ai)
    # Yeh API bilkul free hai aur isme key ki zaroorat nahi
    encoded_prompt = urllib.parse.quote(img_prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true"
    
    # Response wapas bhejna
    return PostResponse(
        caption=response.get("caption", ""),
        hashtags=response.get("hashtags", []),
        call_to_action=response.get("call_to_action", ""),
        image_prompt=img_prompt,
        image_url=image_url
    )