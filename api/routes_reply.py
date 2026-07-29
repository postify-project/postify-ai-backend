from fastapi import APIRouter
from schemas.reply_schema import ReplyRequest, ReplyResponse
from core.llm_setup import get_llm
from core.prompts import AUTO_REPLY_PROMPT

router = APIRouter()

@router.post("/", response_model=ReplyResponse, summary="Generate Comment Reply", description="Generates an appropriate, context-aware auto-reply to a user comment for a specific platform.")
async def generate_auto_reply(request: ReplyRequest):
    
    llm = get_llm()
    
    formatted_prompt = AUTO_REPLY_PROMPT.format(
        platform=request.platform,
        comment=request.comment,
        context=request.context
    )
    
    response = llm.invoke(formatted_prompt)
    
    return ReplyResponse(
        suggested_reply=response.content,
        sentiment="neutral" 
    )