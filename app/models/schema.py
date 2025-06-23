# app/models/schemas.py
from typing import Optional
from pydantic import BaseModel, Field

class ImageAnalysisRequest(BaseModel):
    """Request model for image analysis"""
    prompt: Optional[str] = Field(
        default="Analyze this image and describe what you see in detail.",
        description="Custom prompt for image analysis"
    )

class ImageAnalysisResponse(BaseModel):
    """Response model for image analysis"""
    analysis: str = Field(description="AI-generated image analysis")
    model_used: str = Field(description="AI model used for analysis")
    image_size: Optional[str] = Field(default=None, description="Size of uploaded image")
    processing_time: Optional[float] = Field(default=None, description="Processing time in seconds")

class HealthCheckResponse(BaseModel):
    """Health check response model"""
    status: str = Field(description="Service status")
    service: str = Field(description="Service name")
    version: str = Field(description="Service version")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")
    error_code: Optional[str] = Field(default=None, description="Error code")