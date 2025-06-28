# app/routes/image_routes.py
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import Optional
from app.dto.schema import ImageAnalysisResponse
from app.controllers.image_controller import image_controller

router = APIRouter()

#TODO: remove, just a simple bedrock usage example
@router.post("/analyze", response_model=ImageAnalysisResponse)
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
