from fastapi import APIRouter
from schemas.reply_schema import ReplyRequest, ReplyResponse
from core.llm_setup import get_llm
from core.prompts import AUTO_REPLY_PROMPT

router = APIRouter()

@router.post("/", response_model=ReplyResponse)
async def generate_auto_reply(request: ReplyRequest):
    # 1. LLM ko initialize karein
    llm = get_llm()
    
    # 2. Prompt tayyar karein
    formatted_prompt = AUTO_REPLY_PROMPT.format(
        platform=request.platform,
        comment=request.comment,
        context=request.context
    )
    
    # 3. AI se reply generate karein
    response = llm.invoke(formatted_prompt)
    
    # 4. Web team ko JSON response bhejna
    return ReplyResponse(
        suggested_reply=response.content,
        sentiment="neutral" 
    )