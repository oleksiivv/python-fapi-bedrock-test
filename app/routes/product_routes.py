# app/routes/product_routes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.dto.schema import Product, ProductWithCampaigns
from app.controllers.products_controller import products_controller

router = APIRouter()

@router.get("/", response_model=List[Product])
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return products_controller.get_all_products(db=db, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductWithCampaigns)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = products_controller.get_product_by_id(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
