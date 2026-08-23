from typing import Optional

from fastapi import APIRouter, HTTPException, status

from data import categories, products
from schemas import ProductCreate, ProductPatch, ProductUpdate
from services.product_service import ProductService

router = APIRouter(prefix = "/products", tags = ["Products"])

product_service = ProductService(
    products,
    categories
)

@router.get("")
def get_products(
    category: Optional[str] = None,
    # category: str | None = None
    available: Optional[bool] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    name: Optional[str] = None
):
    if min_price is not None and max_price is not None:
        if min_price > max_price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail = "pretul minim nu poate fi mai mare decat pretul maxim"
            )
    return product_service.get_all(
        category,
        available,
        min_price,
        max_price,
        name
    )

@router.get("/{product_id}")
def get_product_by_id(product_id: int):
    product = product_service.find_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Produsul nu a fost gasit"
        )
    return product

@router.post("", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    if product_service.category_exists(product.category) is False:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Categoria nu exista"
        )

    if product_service.name_exists(product.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Exista deja un produs cu acest nume"
        )

    return product_service.create(product)

@router.put("/{product_id}")
def update_product(
    product_id: int,
    updated_product: ProductUpdate
):
    product = product_service.find_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produsul nu a fost gasit"
        )

    if product_service.category_exists(updated_product.category) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Categoria nu exista"
        )
    if product_service.name_exists(updated_product.name, product_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Exista deja un produs cu acest nume"
        )
    return product_service.update(product, updated_product)

@router.patch("/{product_id}")
def patch_product(
    product_id: int,
    product_update: ProductPatch
):
    product = product_service.find_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "produsul nu a fost gasit"
        )

    updates = product_update.model_dump(exclude_unset=True)

    if len(updates) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="trebuie trimis cel putin un camp"
        )

    if "category" in updates:
        if product_service.category_exists(updates["category"]) is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Categoria nu exista"
            )

        updates["category"] = updates["category"].lower()

    if "name" in updates:
        if product_service.name_exists(updates["name"], product_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Exista deja un produs cu acest nume"
            )

    return product_service.patch(product, updates)

@router.delete("/{product_id}")
def delete_product(product_id: int):
    product = product_service.find_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produsul nu a fost gasit"
        )

    deleted_product = product_service.delete(product)

    return {
        "message": "Produsul a fost sters",
        "deleted_product": deleted_product
    }