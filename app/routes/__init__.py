# app/routes/__init__.py
from fastapi import APIRouter
from .web_routes import router as web_router
from .product_routes import router as product_router
from .image_routes import router as image_router
from .marketing_campaign_routes import router as campaign_router
from .marketing_campaign_target_routes import router as campaign_target_router
from .marketing_campaign_content_routes import router as campaign_content_router
from .product_analytics_routes import router as analytics_router


def create_router() -> APIRouter:
    main_router = APIRouter()

    main_router.include_router(product_router, prefix="/api/products", tags=["Products"])
    main_router.include_router(campaign_router, prefix="/api/campaigns", tags=["Marketing Campaigns"])
    main_router.include_router(campaign_target_router, prefix="/api/campaigns", tags=["Campaign Targets"])
    main_router.include_router(campaign_content_router, prefix="/api/campaigns", tags=["Campaign Content"])
    main_router.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])

    #TODO:remove
    main_router.include_router(web_router, prefix="/web")
    main_router.include_router(image_router, prefix="/api/bedrock-demo")

    return main_router