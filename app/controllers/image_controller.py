import os
from typing import Optional
from fastapi import HTTPException, UploadFile

from app.dto.schema import ImageAnalysisResponse
from app.services.bedrock import bedrock_service
from app.config.settings import settings

#TODO: remove - simple bedrock usage example
class ImageController:
    """Controller for handling image analysis business logic"""

    def __init__(self):
        self.bedrock_service = bedrock_service
        self.settings = settings

    async def analyze_uploaded_image(
            self,
            file: UploadFile,
            prompt: Optional[str] = None
    ) -> ImageAnalysisResponse:
        """
        Analyze an uploaded image file

        Args:
            file: Uploaded image file
            prompt: Custom analysis prompt

        Returns:
            ImageAnalysisResponse with analysis results
        """
        # Validate file
        self._validate_file(file)

        # Read file data
        image_data = await self._read_file_data(file)

        # Use default prompt if none provided
        analysis_prompt = prompt or self.settings.DEFAULT_ANALYSIS_PROMPT

        # Perform analysis
        analysis, processing_time = self.bedrock_service.analyze_image(
            image_data, analysis_prompt
        )

        return ImageAnalysisResponse(
            analysis=analysis,
            model_used=self._get_model_display_name(),
            image_size=f"{len(image_data)} bytes",
            processing_time=round(processing_time, 2)
        )

    def _validate_file(self, file: UploadFile) -> None:
        """Validate uploaded file"""
        # Check if file exists
        if not file or not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No file provided"
            )

        # Check file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image"
            )

        # Check allowed content types
        if file.content_type not in self.settings.ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported image type. Allowed types: {', '.join(self.settings.ALLOWED_CONTENT_TYPES)}"
            )

        # Check file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in self.settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file extension. Allowed extensions: {', '.join(self.settings.ALLOWED_EXTENSIONS)}"
            )

    async def _read_file_data(self, file: UploadFile) -> bytes:
        """Read and validate file data"""
        try:
            image_data = await file.read()

            if len(image_data) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="Empty file"
                )

            # Check file size
            if len(image_data) > self.settings.MAX_FILE_SIZE_BYTES:
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large. Maximum size is {self.settings.max_file_size_mb}MB"
                )

            return image_data

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to read file: {str(e)}"
            )

    def _get_model_display_name(self) -> str:
        """Get display name for the current model"""
        model_names = {
            "anthropic.claude-3-haiku-20240307-v1:0": "Claude 3 Haiku (Bedrock)",
            "anthropic.claude-3-sonnet-20240229-v1:0": "Claude 3 Sonnet (Bedrock)",
            "anthropic.claude-3-opus-20240229-v1:0": "Claude 3 Opus (Bedrock)"
        }
        return model_names.get(
            self.settings.BEDROCK_MODEL_ID,
            f"Claude 3 ({self.settings.BEDROCK_MODEL_ID})"
        )

    def get_service_health(self) -> dict:
        """Check service health"""
        bedrock_healthy = self.bedrock_service.test_connection()

        return {
            "status": "healthy" if bedrock_healthy else "degraded",
            "service": self.settings.APP_NAME,
            "version": self.settings.APP_VERSION,
            "bedrock_connection": "ok" if bedrock_healthy else "failed",
            "model": self.settings.BEDROCK_MODEL_ID
        }


# Global controller instance
image_controller = ImageController()