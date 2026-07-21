from fastapi import APIRouter
from schemas.post_schema import PostRequest, PostResponse
from core.llm_setup import get_llm
from core.prompts import POST_PROMPT
from langchain_core.output_parsers import JsonOutputParser
import urllib.parse
import requests # Pic download karne ke liye
import uuid # Unique naam banane ke liye
import os

router = APIRouter()

@router.post("/", response_model=PostResponse)
async def generate_post(request: PostRequest):
    llm = get_llm()
    
    # JSON Parser setup
    parser = JsonOutputParser(pydantic_object=PostResponse)
    chain = POST_PROMPT | llm | parser
    
    # AI se text aur image prompt generate karna
    response = chain.invoke({
        "topic": request.topic,
        "platform": request.platform,
        "tone": request.tone,
        "format_instructions": parser.get_format_instructions()
    })
    
    img_prompt = response.get("image_prompt", request.topic)
    
    # 1. Pollinations se Image URL banana
    encoded_prompt = urllib.parse.quote(img_prompt)
    external_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true"
    
    # 2. Image ko download karna
    try:
        img_data = requests.get(external_image_url).content
        
        # 3. Unique file name banana (e.g., post_1234-abcd.jpg)
        filename = f"post_{uuid.uuid4().hex[:8]}.jpg"
        filepath = os.path.join("images", filename)
        
        # 4. Image ko apne folder mein save karna
        with open(filepath, 'wb') as f:
            f.write(img_data)
            
        # 5. Apna server URL return karna (jo FastAPI serve karega)
        local_image_url = f"http://localhost:8000/images/{filename}"
        
    except Exception as e:
        # Agar internet issue ya error aaye toh empty URL return kare
        print(f"Image download error: {e}")
        local_image_url = ""
    
    # Response wapas bhejna
    return PostResponse(
        caption=response.get("caption", ""),
        hashtags=response.get("hashtags", []),
        call_to_action=response.get("call_to_action", ""),
        image_prompt=img_prompt,
        image_url=local_image_url # Ab yahan humara apna URL aayega
    )