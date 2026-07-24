from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

def upload_image(file_path: str, folder: str = "postify/images") -> Optional[Dict[str, Any]]:
    """
    Uploads an image to Cloudinary securely and returns the upload response.
    Returns a dictionary containing 'secure_url', 'public_id', etc.
    """
    import cloudinary.uploader
    try:
        response = cloudinary.uploader.upload(
            file_path,
            folder=folder,
            resource_type="image"
        )
        return response
    except Exception as e:
        logger.error(f"Error uploading image to Cloudinary: {e}")
        return None

def upload_video(file_path: str, folder: str = "postify/videos") -> Optional[Dict[str, Any]]:
    """
    Uploads a video to Cloudinary securely. Uses chunked upload for robust handling of larger files.
    """
    import cloudinary.uploader
    try:
        response = cloudinary.uploader.upload_large(
            file_path,
            folder=folder,
            resource_type="video",
            chunk_size=6000000 # 6MB chunks for reliability
        )
        return response
    except Exception as e:
        logger.error(f"Error uploading video to Cloudinary: {e}")
        return None

def delete_media(public_id: str, resource_type: str = "image") -> bool:
    """
    Deletes a media asset from Cloudinary using its public_id.
    """
    import cloudinary.uploader
    try:
        response = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        return response.get("result") == "ok"
    except Exception as e:
        logger.error(f"Error deleting media from Cloudinary: {e}")
        return False
