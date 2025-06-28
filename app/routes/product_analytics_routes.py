# app/routes/analytics_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db

router = APIRouter()

@router.get("/products/")
def get_product_analytics(db: Session = Depends(get_db)):
    from app.database.models import Product, MarketingCampaign
    from sqlalchemy import func

    total_products = db.query(Product).count()

    # Products with most campaigns
    products_with_campaigns = db.query(
        Product.name,
        func.count(MarketingCampaign.id).label('campaign_count')
    ).join(MarketingCampaign, Product.id == MarketingCampaign.product_id) \
        .group_by(Product.id, Product.name) \
        .order_by(func.count(MarketingCampaign.id).desc()) \
        .limit(10).all()

    return {
        "total_products": total_products,
        "top_products_by_campaigns": [
            {"product_name": name, "campaign_count": count}
            for name, count in products_with_campaigns
        ]
    }