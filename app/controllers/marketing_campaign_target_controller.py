from sqlalchemy.orm import Session
from typing import List
from app.database.models import MarketingCampaignTarget

class MarketingCampaignTargetController:
    @staticmethod
    def create_target(
            db: Session,
            marketing_campaign_id: int,
            region: str,
            target_audience_ages: List[str],
            target_audience_genders: List[str]
    ) -> MarketingCampaignTarget:
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

    @staticmethod
    def get_target_by_id(db: Session, target_id: int) -> MarketingCampaignTarget:
        """Get a target by ID"""
        return db.query(MarketingCampaignTarget).filter(MarketingCampaignTarget.id == target_id).first()

    @staticmethod
    def update_target(db: Session, target_id: int, target_update) -> MarketingCampaignTarget:
        """Update a marketing campaign target"""
        target = db.query(MarketingCampaignTarget).filter(MarketingCampaignTarget.id == target_id).first()
        if not target:
            return None

        # Update only provided fields
        update_data = target_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(target, field, value)

        from datetime import datetime
        target.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(target)
        return target

    @staticmethod
    def delete_target(db: Session, target_id: int) -> bool:
        """Delete a marketing campaign target"""
        try:
            target = db.query(MarketingCampaignTarget).filter(MarketingCampaignTarget.id == target_id).first()
            if target:
                db.delete(target)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            raise e

# Global controller instance
marketing_campaign_target_controller = MarketingCampaignTargetController()