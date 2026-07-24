import os
from dotenv import load_dotenv

# Ensure we import the pip package, not the local folder (to prevent circular imports)
import sys
import os as _os

# Professional Setup: Initialize Configuration
load_dotenv()

def init_cloudinary():
    """
    Initializes Cloudinary configuration globally.
    Ensure you have CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET in your .env file.
    """
    import cloudinary
    cloudinary.config( 
        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"), 
        api_key = os.getenv("CLOUDINARY_API_KEY"), 
        api_secret = os.getenv("CLOUDINARY_API_SECRET"),
        secure = True
    )
