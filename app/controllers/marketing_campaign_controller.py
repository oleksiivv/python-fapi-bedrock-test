from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
import json
from app.database.models import Product, MarketingCampaign, MarketingCampaignTarget, MarketingCampaignContentItem
from app.dto.schema import MarketingCampaignUpdate


class MarketingCampaignController:
    @staticmethod
    def create_campaign(
            db: Session,
            product_id: int,
            name: str,
            status: str = "draft",
            secondary_product_ids: List[int] = None,
            start_date=None,
            end_date=None
    ) -> MarketingCampaign:
        """Create a new marketing campaign"""
        campaign = MarketingCampaign(
            product_id=product_id,
            name=name,
            status=status,
            secondary_product_ids=secondary_product_ids or [],
            start_date=start_date,
            end_date=end_date
        )
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        return campaign

    @staticmethod
    def get_campaign_by_id(db: Session, campaign_id: int) -> Optional[MarketingCampaign]:
        """Get campaign by ID with relationships"""
        return db.query(MarketingCampaign).filter(MarketingCampaign.id == campaign_id).first()

    @staticmethod
    def get_campaigns_by_product(db: Session, product_id: int) -> List[MarketingCampaign]:
        """Get all campaigns for a product"""
        return db.query(MarketingCampaign).filter(MarketingCampaign.product_id == product_id).all()

    @staticmethod
    def get_campaigns_by_status(db: Session, status: str) -> List[MarketingCampaign]:
        """Get campaigns by status"""
        return db.query(MarketingCampaign).filter(MarketingCampaign.status == status).all()

    @staticmethod
    def update_campaign_status(db: Session, campaign_id: int, status: str) -> Optional[MarketingCampaign]:
        """Update campaign status"""
        campaign = db.query(MarketingCampaign).filter(MarketingCampaign.id == campaign_id).first()
        if campaign:
            campaign.status = status
            db.commit()
            db.refresh(campaign)
        return campaign

    @staticmethod
    def update_campaign(db: Session, campaign_id: int, campaign_update: MarketingCampaignUpdate):
        """Update a marketing campaign"""
        campaign = db.query(MarketingCampaign).filter(MarketingCampaign.id == campaign_id).first()
        if not campaign:
            return None

        # Update only provided fields
        update_data = campaign_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(campaign, field, value)

        campaign.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(campaign)
        return campaign


# Global controller instance
marketing_campaign_controller = MarketingCampaignController()