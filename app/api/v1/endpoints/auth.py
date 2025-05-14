from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from app.core.security import (
    create_access_token,
    verify_password,
    get_password_hash,
    generate_verification_token
)
from app.schemas.user import UserCreate, User, UserInDB
from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.utils.email import send_verification_email
from datetime import timedelta
from bson import ObjectId

router = APIRouter()

@router.post("/register", response_model=User)
async def register(
    user_in: UserCreate,
    db = Depends(get_db)
) -> Any:
    """
    Register new client user.
    """
    user = await db["users"].find_one({"email": user_in.email})
    if user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    
    verification_token = generate_verification_token()
    user_in_db = UserInDB(
        **user_in.dict(),
        hashed_password=get_password_hash(user_in.password),
        role="client",
        is_verified=False,
        verification_token=verification_token
    )
    
    result = await db["users"].insert_one(user_in_db.dict())
    
  
    await send_verification_email(
        email_to=user_in.email,
        token=verification_token
    )
    
    return {
        "id": str(result.inserted_id),
        "email": user_in.email,
        "role": "client",
        "is_verified": False
    }

@router.post("/login", response_model=dict)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db = Depends(get_db)
) -> Any:
    """
    OAuth2 compatible token login.
    """
    user = await db["users"].find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )
    
    if user["role"] == "client" and not user["is_verified"]:
        raise HTTPException(
            status_code=400,
            detail="Please verify your email first"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user["_id"], expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "role": user["role"]
        }
    }

@router.get("/verify/{token}")
async def verify_email(token: str, db = Depends(get_db)) -> Any:
    """
    Verify user email.
    """
    user = await db["users"].find_one({"verification_token": token})
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid verification token"
        )
    
    await db["users"].update_one(
        {"_id": user["_id"]},
        {
            "$set": {"is_verified": True},
            "$unset": {"verification_token": ""}
        }
    )
    
    return {"message": "Email verified successfully"}