from fastapi import APIRouter, Request
from schemas.post_schema import PostRequest, PostResponse
from core.llm_setup import get_llm
from core.prompts import POST_PROMPT
from langchain_core.output_parsers import JsonOutputParser
from cloud_storage.services import upload_image
import urllib.parse
import requests 
import uuid 
import os

router = APIRouter()

@router.post("/", response_model=PostResponse, summary="Generate Social Media Post", description="Generates a complete social media post including caption, hashtags, call-to-action, and a relevant AI-generated image based on the provided topic.")
async def generate_post(request: PostRequest, req: Request):
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
    
    # 1. Generate Image via Pollinations
    encoded_prompt = urllib.parse.quote(img_prompt)
    external_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true"
    
    image_url = ""
    try:
        img_data = requests.get(external_image_url, timeout=30).content
        
        # 2. Save temporarily to disk so we can upload
        temp_filename = f"temp_post_{uuid.uuid4().hex[:8]}.jpg"
        temp_filepath = os.path.join("images", temp_filename)
        with open(temp_filepath, 'wb') as f:
            f.write(img_data)
        
        # 3. Upload to Cloudinary and get a permanent public URL
        upload_result = upload_image(temp_filepath, folder="postify/posts")
        if upload_result:
            image_url = upload_result.get("secure_url", "")
        
        # 4. Clean up local temp file
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
            
    except Exception as e:
        print(f"Image upload error: {e}")
        image_url = ""
    
    # Return the response with the permanent Cloudinary URL
    return PostResponse(
        caption=response.get("caption", ""),
        hashtags=response.get("hashtags", []),
        call_to_action=response.get("call_to_action", ""),
        image_prompt=img_prompt,
        image_url=image_url
    )