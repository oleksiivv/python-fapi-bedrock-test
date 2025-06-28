# app/routes/campaign_routes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.database import get_db
from app.dto.schema import (
    MarketingCampaign,
    MarketingCampaignCreate,
    MarketingCampaignUpdate,
    MarketingCampaignWithDetails
)
from app.controllers.marketing_campaign_controller import marketing_campaign_controller
from app.controllers.products_controller import products_controller

router = APIRouter()

@router.post("/", response_model=MarketingCampaign)
def create_campaign(
        campaign: MarketingCampaignCreate,
        db: Session = Depends(get_db)
):
    product = products_controller.get_product_by_id(db=db, product_id=campaign.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return marketing_campaign_controller.create_campaign(
        db=db,
        product_id=campaign.product_id,
        name=campaign.name,
        status=campaign.status,
        secondary_product_ids=campaign.secondary_product_ids,
        start_date=campaign.start_date,
        end_date=campaign.end_date
    )

@router.get("/", response_model=List[MarketingCampaign])
def get_campaigns(
        product_id: Optional[int] = Query(None, description="Filter by product ID"),
        status: Optional[str] = Query(None, description="Filter by status"),
        db: Session = Depends(get_db)
):
    if product_id:
        return marketing_campaign_controller.get_campaigns_by_product(db=db, product_id=product_id)
    elif status:
        return marketing_campaign_controller.get_campaigns_by_status(db=db, status=status)
    else:
        from app.database.models import MarketingCampaign
        return db.query(MarketingCampaign).all()

@router.get("/{campaign_id}", response_model=MarketingCampaignWithDetails)
def get_campaign(
        campaign_id: int,
        db: Session = Depends(get_db)
):
    campaign = marketing_campaign_controller.get_campaign_by_id(db=db, campaign_id=campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.put("/{campaign_id}", response_model=MarketingCampaign)
def update_campaign(
        campaign_id: int,
        campaign_update: MarketingCampaignUpdate,
        db: Session = Depends(get_db)
):
    campaign = marketing_campaign_controller.get_campaign_by_id(db=db, campaign_id=campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    updated_campaign = marketing_campaign_controller.update_campaign(
        db=db,
        campaign_id=campaign_id,
        campaign_update=campaign_update
    )

    if not updated_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    return updated_campaign

@router.put("/{campaign_id}/status", response_model=MarketingCampaign)
def update_campaign_status(
        campaign_id: int,
        status: str = Query(..., description="New status: draft, active, paused, completed"),
        db: Session = Depends(get_db)
):
    valid_statuses = ["draft", "active", "paused", "completed"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )

    campaign = marketing_campaign_controller.update_campaign_status(db=db, campaign_id=campaign_id, status=status)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign
