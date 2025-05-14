from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import Any, List
from app.api.deps import get_current_user, get_db
from app.core.security import generate_download_token
from app.schemas.file import FileCreate, FileInDB, FileList
from app.utils.file import validate_file_type, save_upload_file
from bson import ObjectId
import os

router = APIRouter()

@router.post("/upload", response_model=FileInDB)
async def upload_file(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db = Depends(get_db)
) -> Any:
    """
    Upload a file (operations users only).
    """
    if current_user["role"] != "ops":
        raise HTTPException(
            status_code=403,
            detail="Only operations users can upload files"
        )
    

    if not validate_file_type(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only pptx, docx, and xlsx files are allowed"
        )
    
  
    file_path = await save_upload_file(file)
    

    file_in_db = FileInDB(
        filename=file.filename,
        file_path=file_path,
        uploaded_by=str(current_user["_id"]),
        file_type=file.filename.split(".")[-1]
    )
    
    result = await db["files"].insert_one(file_in_db.dict())
    
    return {
        "id": str(result.inserted_id),
        **file_in_db.dict()
    }

@router.get("/", response_model=FileList)
async def list_files(
    current_user = Depends(get_current_user),
    db = Depends(get_db)
) -> Any:
    """
    List all files (client users only).
    """
    if current_user["role"] != "client":
        raise HTTPException(
            status_code=403,
            detail="Only client users can list files"
        )
    
    files = await db["files"].find({"is_active": True}).to_list(None)
    return {
        "files": [
            {
                "id": str(file["_id"]),
                "filename": file["filename"],
                "file_type": file["file_type"],
                "uploaded_at": file["uploaded_at"]
            }
            for file in files
        ]
    }

@router.get("/download/{file_id}")
async def generate_download_link(
    file_id: str,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
) -> Any:
    """
    Generate download link for a file (client users only).
    """
    if current_user["role"] != "client":
        raise HTTPException(
            status_code=403,
            detail="Only client users can download files"
        )
    
    file = await db["files"].find_one({"_id": ObjectId(file_id)})
    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
    
    download_token = generate_download_token(file_id, str(current_user["_id"]))
    
    return {
        "download_link": f"/api/v1/files/download-file/{download_token}",
        "message": "success"
    }

@router.get("/download-file/{token}")
async def download_file(
    token: str,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
) -> Any:
    """
    Download a file using the generated token (client users only).
    """
    if current_user["role"] != "client":
        raise HTTPException(
            status_code=403,
            detail="Only client users can download files"
        )
    
    try:
       
        file_id = token 
        
        file = await db["files"].find_one({"_id": ObjectId(file_id)})
        if not file or not file["is_active"]:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
        
     
        await db["files"].update_one(
            {"_id": ObjectId(file_id)},
            {"$inc": {"download_count": 1}}
        )
        
        return FileResponse(
            file["file_path"],
            filename=file["filename"],
            media_type="application/octet-stream"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired download token"
        )