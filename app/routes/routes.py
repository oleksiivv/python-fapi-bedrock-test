# app/routes/image_routes.py
from typing import Optional
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.models.schema import ImageAnalysisResponse, HealthCheckResponse
from app.controllers.image_controller import image_controller
from app.config.settings import settings

# Create router for image-related routes
router = APIRouter()

# Setup Jinja2 templates
templates = Jinja2Templates(directory="app/static/templates")


@router.get("/", response_class=HTMLResponse, tags=["Web Interface"])
async def get_main_page(request: Request):
    """
    Serve the main HTML interface for image analysis using Jinja2 template
    """
    return templates.TemplateResponse("index.html", {
        "request": request,
        "app_name": settings.APP_NAME,
        "default_analysis_prompt": settings.DEFAULT_ANALYSIS_PROMPT,
        "max_file_size_mb": settings.max_file_size_mb,
        "allowed_extensions": ", ".join(settings.ALLOWED_EXTENSIONS),
        "model_name": settings.BEDROCK_MODEL_ID.split(".")[-1].replace("-", " ").title()
    })


@router.post("/api/analyze", response_model=ImageAnalysisResponse, tags=["Image Analysis"])
async def analyze_image(
        file: UploadFile = File(..., description="Image file to analyze"),
        prompt: Optional[str] = Form(None, description="Custom analysis prompt")
):
    """
    Analyze an uploaded image using AI

    - **file**: Image file (JPEG, PNG, GIF, BMP, WebP)
    - **prompt**: Custom prompt for analysis (optional)

    Returns detailed AI analysis of the image.
    """
    try:
        return await image_controller.analyze_uploaded_image(file, prompt)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """
    Check the health status of the image analysis service
    """
    try:
        health_data = image_controller.get_service_health()
        return HealthCheckResponse(**health_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@router.get("/api/models", tags=["Information"])
async def get_available_models():
    """
    Get information about available AI models
    """
    return {
        "current_model": settings.BEDROCK_MODEL_ID,
        "available_models": [
            {
                "id": "anthropic.claude-3-haiku-20240307-v1:0",
                "name": "Claude 3 Haiku",
                "description": "Fast and cost-effective for simple tasks"
            },
            {
                "id": "anthropic.claude-3-sonnet-20240229-v1:0",
                "name": "Claude 3 Sonnet",
                "description": "Balanced performance and cost"
            },
            {
                "id": "anthropic.claude-3-opus-20240229-v1:0",
                "name": "Claude 3 Opus",
                "description": "Most capable for complex analysis"
            }
        ]
    }


@router.get("/api/config", tags=["Information"])
async def get_configuration():
    """
    Get current service configuration
    """
    return {
        "max_file_size_mb": settings.max_file_size_mb,
        "allowed_extensions": settings.ALLOWED_EXTENSIONS,
        "allowed_content_types": settings.ALLOWED_CONTENT_TYPES,
        "default_prompt": settings.DEFAULT_ANALYSIS_PROMPT,
        "model": settings.BEDROCK_MODEL_ID,
        "max_tokens": settings.BEDROCK_MAX_TOKENS,
        "app_name": settings.APP_NAME
    }