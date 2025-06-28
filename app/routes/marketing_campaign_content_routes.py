# app/routes/campaign_content_routes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.database import get_db
from app.dto.schema import MarketingCampaignContentItem
from app.controllers.marketing_campaign_controller import marketing_campaign_controller
from app.controllers.marketing_campaign_content_controller import marketing_campaign_content_controller

router = APIRouter()

@router.get("/{campaign_id}/content/", response_model=List[MarketingCampaignContentItem])
def get_campaign_content(
        campaign_id: int,
        content_type: Optional[str] = Query(None, description="Filter by content type"),
        db: Session = Depends(get_db)
):
    campaign = marketing_campaign_controller.get_campaign_by_id(db=db, campaign_id=campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    if content_type:
        return marketing_campaign_content_controller.get_content_items_by_type(
            db=db, campaign_id=campaign_id, content_type=content_type
        )
    else:
        return marketing_campaign_content_controller.get_content_items_by_campaign(
            db=db, campaign_id=campaign_id
        )
