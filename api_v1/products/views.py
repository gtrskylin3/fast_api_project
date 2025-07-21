from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from . import crud
from .schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial
from .dependencies import product_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper

session=Depends(db_helper.scoped_session_dependency)

router = APIRouter(tags=["Products"])

@router.get("/", response_model=List[Product])
async def get_products(
    session: AsyncSession = session
    ):
    return await crud.get_products(session=session)

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = session
    ):
    return await crud.create_product(session=session, product_in=product_in)

@router.get("/{product_id}/", response_model=Product)
async def get_product(
    product: Product = Depends(product_by_id),
    ):
    return product

@router.put("/{product_id}/")
async def update_product(
    product_update: ProductUpdate,
    product: Product = Depends(product_by_id),
    session: AsyncSession = session
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update)

@router.patch("/{product_id}/")
async def update_product_partial(
    product_update: ProductUpdatePartial,
    product: Product = Depends(product_by_id),
    session: AsyncSession = session
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True
        )

@router.delete("/{product_id}/", status_code=204)
async def delete_product(
    product: Product = Depends(product_by_id),
    session: AsyncSession = session
) -> None:
    await crud.delete_product(session, product)
    