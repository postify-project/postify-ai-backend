from langchain_core.prompts import PromptTemplate


AUTO_REPLY_PROMPT = PromptTemplate(
    input_variables=["platform", "comment", "context"],
    template="""
    You are an expert social media manager for a {platform} account.
    A user has left this comment: "{comment}"
    
    Context about the post/product: {context}
    
    Write a polite, engaging, and context-aware reply to this comment. 
    Keep it under 50 words. Make it sound natural.
    """
)
from langchain_core.prompts import PromptTemplate

# --- Pehle wala Auto Reply Prompt yahan rehne dein ---
AUTO_REPLY_PROMPT = PromptTemplate(
    input_variables=["platform", "comment", "context"],
    template="""
    You are an expert social media manager for a {platform} account.
    A user has left this comment: "{comment}"
    
    Context about the post/product: {context}
    
    Write a polite, engaging, and context-aware reply to this comment. 
    Keep it under 50 words. Make it sound natural.
    """
)

# --- Naya Metadata Prompt ---
METADATA_PROMPT = PromptTemplate(
    input_variables=["transcript", "platform", "format_instructions"],
    template="""
    You are an expert SEO specialist for {platform}.
    Analyze the following video transcript and generate SEO-optimized metadata.
    
    Transcript: {transcript}
    
    {format_instructions}
    
    Make sure the title is catchy, the description has relevant hashtags, and provide exactly 10 highly relevant tags.
    """
)


# --- Post Generation Prompt (Update kiya gaya) ---
POST_PROMPT = PromptTemplate(
    input_variables=["topic", "platform", "tone", "format_instructions"],
    template="""
    You are an expert social media content creator and graphic designer.
    Write a highly engaging post for {platform} about the following topic: "{topic}".
    The tone of the post should be {tone}.
    
    Follow platform best practices (e.g., short for Twitter, professional for LinkedIn, visual & engaging for Instagram).
    
    Also, create a detailed 'image_prompt' that can be fed into an AI image generator to create a perfect picture for this post. Do not include text in the image prompt.
    
    {format_instructions}
    """
)