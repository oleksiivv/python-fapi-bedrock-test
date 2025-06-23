# run.py
"""
Application entry point
"""
import uvicorn

from app.config.settings import settings

if __name__ == "__main__":
    print("🚀 Starting Image Analysis App...")
    print("📋 Make sure you have:")
    print("   - AWS credentials configured")
    print("   - Bedrock model access enabled")
    print("   - Required Python packages installed")
    print(f"\n🌐 Access the app at: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 API Documentation: http://{settings.HOST}:{settings.PORT}/docs")

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )