from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
import json
from app.database.models import Product, MarketingCampaign, MarketingCampaignTarget, MarketingCampaignContentItem

class MarketingCampaignContentController:
    @staticmethod
    def create_content_item(
            db: Session,
            marketing_campaign_id: int,
            content_type: str,
            text: str = None,
            content_url: str = None,
            category: str = None
    ) -> MarketingCampaignContentItem:
        """Create a new content item"""
        content_item = MarketingCampaignContentItem(
            marketing_campaign_id=marketing_campaign_id,
            content_type=content_type,
            text=text,
            content_url=content_url,
            category=category
        )
        db.add(content_item)
        db.commit()
        db.refresh(content_item)
        return content_item

    @staticmethod
    def get_content_items_by_campaign(db: Session, campaign_id: int) -> List[MarketingCampaignContentItem]:
        """Get all content items for a campaign"""
        return db.query(MarketingCampaignContentItem).filter(
            MarketingCampaignContentItem.marketing_campaign_id == campaign_id
        ).all()

    @staticmethod
    def get_content_items_by_type(db: Session, campaign_id: int, content_type: str) -> List[
        MarketingCampaignContentItem]:
        """Get content items by type for a campaign"""
        return db.query(MarketingCampaignContentItem).filter(
            MarketingCampaignContentItem.marketing_campaign_id == campaign_id,
            MarketingCampaignContentItem.content_type == content_type
        ).all()

# Global controller instance
marketing_campaign_content_controller = MarketingCampaignContentController()