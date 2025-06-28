# app/routes/web_routes.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config.settings import settings

router = APIRouter()
templates = Jinja2Templates(directory="app/static/templates")

@router.get("/bedrock-demo", response_class=HTMLResponse)
async def get_main_page(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "app_name": settings.APP_NAME,
        "default_analysis_prompt": settings.DEFAULT_ANALYSIS_PROMPT,
        "max_file_size_mb": settings.max_file_size_mb,
        "allowed_extensions": ", ".join(settings.ALLOWED_EXTENSIONS),
        "model_name": settings.BEDROCK_MODEL_ID.split(".")[-1].replace("-", " ").title()
    })

@router.get("/config")
async def get_configuration():
    """Get application configuration"""
    return {
        "max_file_size_mb": settings.max_file_size_mb,
        "allowed_extensions": settings.ALLOWED_EXTENSIONS,
        "allowed_content_types": settings.ALLOWED_CONTENT_TYPES,
        "default_prompt": settings.DEFAULT_ANALYSIS_PROMPT,
        "model": settings.BEDROCK_MODEL_ID,
        "max_tokens": settings.BEDROCK_MAX_TOKENS,
        "app_name": settings.APP_NAME
    }
