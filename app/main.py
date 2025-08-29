# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.api.routes import router
# from app.core.config import settings
# import os

# app = FastAPI(
#     title="Video Exercise Analyzer API",
#     description="Upload a video (no audio needed) to get exercise descriptions from the visuals.",
#     version="1.0.0",
# )

# # Create upload dir if not exists
# if not os.path.exists(settings.UPLOAD_DIR):
#     os.makedirs(settings.UPLOAD_DIR)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(router)
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.core.config import settings
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Video Exercise Analyzer API",
    description="Upload a video (no audio needed) to get comprehensive exercise analysis from the visuals.",
    version="1.0.0",
)

# Create upload dir if not exists
if not os.path.exists(settings.UPLOAD_DIR):
    os.makedirs(settings.UPLOAD_DIR)
if not os.path.exists(settings.AUDIO_DIR):
    os.makedirs(settings.AUDIO_DIR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "An internal server error occurred. Please try again later."},
    )

@app.get("/")
async def root():
    return {"message": "Video Exercise Analyzer API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "openai_configured": bool(settings.OPENAI_API_KEY)}

app.include_router(router)