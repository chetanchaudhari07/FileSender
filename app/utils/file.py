import os
import aiofiles
from fastapi import UploadFile
from app.core.config import settings
import magic
from datetime import datetime

def validate_file_type(filename: str) -> bool:
    """Validate file extension."""
    return filename.split(".")[-1].lower() in settings.ALLOWED_EXTENSIONS

async def save_upload_file(file: UploadFile) -> str:
    """Save uploaded file to disk."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    async with aiofiles.open(file_path, "wb") as buffer:
        content = await file.read()
        await buffer.write(content)
    
    return file_path