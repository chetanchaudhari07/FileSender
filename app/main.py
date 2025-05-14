from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.security import create_access_token
from datetime import timedelta

app = FastAPI(
    title="Secure File Sharing API",
    description="API for secure file sharing between operations and client users",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(api_router, prefix="/api/v1")