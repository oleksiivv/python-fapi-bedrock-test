from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    """Product model"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    image = Column(String)  # URL or path to product image
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    marketing_campaigns = relationship("MarketingCampaign", back_populates="product")


class MarketingCampaign(Base):
    """Marketing campaign model"""
    __tablename__ = "marketing_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False, default="draft")  # draft, active, paused, completed
    secondary_product_ids = Column(JSON)  # Array of product IDs as JSON
    start_date = Column(Date)
    end_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    product = relationship("Product", back_populates="marketing_campaigns")
    targets = relationship("MarketingCampaignTarget", back_populates="campaign", cascade="all, delete-orphan")
    content_items = relationship("MarketingCampaignContentItem", back_populates="campaign",
                                 cascade="all, delete-orphan")


class MarketingCampaignTarget(Base):
    """Marketing campaign target audience model"""
    __tablename__ = "marketing_campaign_targets"

    id = Column(Integer, primary_key=True, index=True)
    marketing_campaign_id = Column(Integer, ForeignKey("marketing_campaigns.id"), nullable=False)
    region = Column(String, nullable=False)
    target_audience_ages = Column(JSON)  # Array of age ranges as JSON, e.g., ["18-25", "26-35"]
    target_audience_genders = Column(JSON)  # Array of genders as JSON, e.g., ["male", "female", "all"]
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    campaign = relationship("MarketingCampaign", back_populates="targets")


class MarketingCampaignContentItem(Base):
    """Marketing campaign content items model"""
    __tablename__ = "marketing_campaign_content_items"

    id = Column(Integer, primary_key=True, index=True)
    marketing_campaign_id = Column(Integer, ForeignKey("marketing_campaigns.id"), nullable=False)
    content_type = Column(String, nullable=False)  # text, image, video, audio, etc.
    text = Column(Text)  # For text content or descriptions
    content_url = Column(String)  # URL to the actual content file
    category = Column(String)  # e.g., "social_media", "email", "banner", "video_ad"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    campaign = relationship("MarketingCampaign", back_populates="content_items")