from fastapi import APIRouter, HTTPException, status

from data import categories, products
from schemas import CategoryCreate, CategoryUpdate, CategoryPatch
from services.category_service import CategoryService

router = APIRouter(prefix = "/categories", tags = ["Categories"])

category_service = CategoryService(
    categories,
    products
)

"""
1. get_categories
2. get_category_by_id
3. create_category
4. delete_category
"""

@router.get("")
def get_categories():
    return category_service.get_all()

@router.get("/{category_id}")
def get_category_by_id(category_id: int):
    category = category_service.find_by_id(category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria nu a fost gasita"
        )
    return category

@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate):
    if category_service.name_exists(category.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Exista deja o categorie cu acest nume"
        )

    return category_service.create(category)

@router.put("/{category_id}")
def update_category(category_id: int, updated_category: CategoryUpdate):
    category = category_service.find_by_id(category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria nu a fost gasita"
        )

    if category_service.name_exists(updated_category.name, category_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Exista deja o categorie cu acest nume"
        )

    return category_service.update(category, updated_category)

@router.patch("/{category_id}")
def patch_category(category_id: int, category_update: CategoryPatch):
    category = category_service.find_by_id(category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria nu a fost gasita"
        )

    updates = category_update.model_dump(exclude_unset=True)

    if len(updates) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trebuie trimis cel putin un camp"
        )

    if "name" in updates:
        if category_service.name_exists(updates["name"], category_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Exista deja o categorie cu acest nume"
            )

    return category_service.patch(category, updates)

@router.delete("/{category_id}")
def delete_category(category_id: int):
    category = category_service.find_by_id(category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria nu a fost gasita"
        )

    deleted_category = category_service.delete(category)

    return {
        "message": "Categoria a fost stearsa",
        "deleted_category": deleted_category
    }