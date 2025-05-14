from pydantic import BaseModel
from datetime import datetime
from typing import List

class FileBase(BaseModel):
    filename: str
    file_type: str

class FileCreate(FileBase):
    pass

class FileInDB(FileBase):
    file_path: str
    uploaded_by: str
    upload_date: datetime = datetime.utcnow()
    download_count: int = 0
    is_active: bool = True

class FileList(BaseModel):
    files: List[FileBase]