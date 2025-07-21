from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from . import crud
from .schemas import Product, ProductCreate
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper

session=Depends(db_helper.scoped_session_dependency)

router = APIRouter(tags=["Products"])

@router.get("/", response_model=List[Product])
async def get_products(
    session: AsyncSession = session
    ):
    return await crud.get_products(session=session)

@router.post("/", response_model=Product)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = session
    ):
    return await crud.create_product(session=session, product_in=product_in)

@router.get("/{product_id}/", response_model=Product)
async def get_product(
    product_id: int,
    session: AsyncSession = session
    ):
    product = await crud.get_product(session=session, product_id=product_id)
    if product is not None:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found!"
    )