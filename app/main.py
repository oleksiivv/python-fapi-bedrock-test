# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config.settings import settings
from app.routes.routes import router as image_router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount static files (CSS, JS, images)
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # Include routers
    app.include_router(image_router, prefix="")

    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": str(exc) if settings.DEBUG else "An unexpected error occurred"
            }
        )

    # Startup event
    @app.on_event("startup")
    async def startup_event():
        print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
        print(f"📍 Running on {settings.HOST}:{settings.PORT}")
        print(f"🤖 Using model: {settings.BEDROCK_MODEL_ID}")
        print(f"🌍 AWS Region: {settings.AWS_REGION}")
        print(f"📁 Max file size: {settings.max_file_size_mb}MB")

        # Test Bedrock connection
        from app.services.bedrock import bedrock_service
        if bedrock_service.test_connection():
            print("✅ Bedrock connection: OK")
        else:
            print("❌ Bedrock connection: Failed")
            print("   Please check your AWS credentials and Bedrock access")

    return app


# Create the app instance
app = create_app()