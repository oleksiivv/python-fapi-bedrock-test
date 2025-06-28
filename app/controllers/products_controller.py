from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
import json
from app.database.models import Product, MarketingCampaign, MarketingCampaignTarget, MarketingCampaignContentItem

class ProductsController:
    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def get_all_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get all products with pagination"""
        return db.query(Product).offset(skip).limit(limit).all()


class MarketingCampaignCRUD:
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


class MarketingCampaignTargetCRUD:
    @staticmethod
    def create_target(
            db: Session,
            marketing_campaign_id: int,
            region: str,
            target_audience_ages: List[str],
            target_audience_genders: List[str]
    ) -> MarketingCampaignTarget:
        """Create a new campaign target"""
        target = MarketingCampaignTarget(
            marketing_campaign_id=marketing_campaign_id,
            region=region,
            target_audience_ages=target_audience_ages,
            target_audience_genders=target_audience_genders
        )
        db.add(target)
        db.commit()
        db.refresh(target)
        return target

    @staticmethod
    def get_targets_by_campaign(db: Session, campaign_id: int) -> List[MarketingCampaignTarget]:
        """Get all targets for a campaign"""
        return db.query(MarketingCampaignTarget).filter(
            MarketingCampaignTarget.marketing_campaign_id == campaign_id
        ).all()


class MarketingCampaignContentItemCRUD:
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
products_controller = ProductsController()