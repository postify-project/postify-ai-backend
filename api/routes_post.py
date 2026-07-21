from fastapi import APIRouter
from schemas.post_schema import PostRequest, PostResponse
from core.llm_setup import get_llm
from core.prompts import POST_PROMPT
from langchain_core.output_parsers import JsonOutputParser
import urllib.parse
import requests 
import uuid 
import os

router = APIRouter()

@router.post("/", response_model=PostResponse)
async def generate_post(request: PostRequest):
    llm = get_llm()
    
    # JSON Parser setup
    parser = JsonOutputParser(pydantic_object=PostResponse)
    chain = POST_PROMPT | llm | parser
    
    # Generate text and prompt for image
    response = chain.invoke({
        "topic": request.topic,
        "platform": request.platform,
        "tone": request.tone,
        "format_instructions": parser.get_format_instructions()
    })
    
    img_prompt = response.get("image_prompt", request.topic)
    
    # 1. Image Creation
    encoded_prompt = urllib.parse.quote(img_prompt)
    external_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true"
    
    # 2. Download Image
    try:
        img_data = requests.get(external_image_url).content
        
        # 3. Generate a unique filename
        filename = f"post_{uuid.uuid4().hex[:8]}.jpg"
        filepath = os.path.join("images", filename)
        
        # 4. Save the image to your local folder.
        with open(filepath, 'wb') as f:
            f.write(img_data)
            
        # 5. Return the URL of your FastAPI server
        local_image_url = f"http://localhost:8000/images/{filename}"
        
    except Exception as e:
        # If there is an internet issue or an error, return an empty URL.
        print(f"Image download error: {e}")
        local_image_url = ""
    
    # Return the response
    return PostResponse(
        caption=response.get("caption", ""),
        hashtags=response.get("hashtags", []),
        call_to_action=response.get("call_to_action", ""),
        image_prompt=img_prompt,
        image_url=local_image_url # Ab yahan humara apna URL aayega
    )