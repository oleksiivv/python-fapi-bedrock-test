# app/routes/campaign_target_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.dto.schema import (
    MarketingCampaignTarget,
    MarketingCampaignTargetCreate,
    MarketingCampaignTargetUpdate
)
from app.controllers.marketing_campaign_controller import marketing_campaign_controller
from app.controllers.marketing_campaign_target_controller import marketing_campaign_target_controller

router = APIRouter()

@router.post("/{campaign_id}/targets/", response_model=MarketingCampaignTarget)
def create_campaign_target(
        campaign_id: int,
        target: MarketingCampaignTargetCreate,
        db: Session = Depends(get_db)
):
    campaign = marketing_campaign_controller.get_campaign_by_id(db=db, campaign_id=campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    target.marketing_campaign_id = campaign_id

    return marketing_campaign_target_controller.create_target(
        db=db,
        marketing_campaign_id=target.marketing_campaign_id,
        region=target.region,
        target_audience_ages=target.target_audience_ages,
        target_audience_genders=target.target_audience_genders
    )

@router.get("/{campaign_id}/targets/", response_model=List[MarketingCampaignTarget])
def get_campaign_targets(
        campaign_id: int,
        db: Session = Depends(get_db)
):
    campaign = marketing_campaign_controller.get_campaign_by_id(db=db, campaign_id=campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    return marketing_campaign_target_controller.get_targets_by_campaign(db=db, campaign_id=campaign_id)

@router.put("/{campaign_id}/targets/{target_id}", response_model=MarketingCampaignTarget)
def update_campaign_target(
        campaign_id: int,
        target_id: int,
        target_update: MarketingCampaignTargetUpdate,
        db: Session = Depends(get_db)
):
    """Update campaign target details"""
    # Verify campaign exists
    campaign = marketing_campaign_controller.get_campaign_by_id(db=db, campaign_id=campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    # Get target to verify it exists and belongs to campaign
    target = marketing_campaign_target_controller.get_target_by_id(db=db, target_id=target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    if target.marketing_campaign_id != campaign_id:
        raise HTTPException(status_code=400, detail="Target does not belong to specified campaign")

    # Update target
    updated_target = marketing_campaign_target_controller.update_target(
        db=db,
        target_id=target_id,
        target_update=target_update
    )

    return updated_target

@router.delete("/{campaign_id}/targets/{target_id}")
def delete_campaign_target(
        campaign_id: int,
        target_id: int,
        db: Session = Depends(get_db)
):
    """Delete a campaign target"""
    # Verify campaign exists
    campaign = marketing_campaign_controller.get_campaign_by_id(db=db, campaign_id=campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    # Get target to verify it belongs to the campaign
    target = marketing_campaign_target_controller.get_target_by_id(db=db, target_id=target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    if target.marketing_campaign_id != campaign_id:
        raise HTTPException(status_code=400, detail="Target does not belong to specified campaign")

    success = marketing_campaign_target_controller.delete_target(db=db, target_id=target_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete target")

    return {"message": f"Target {target_id} deleted successfully"}
