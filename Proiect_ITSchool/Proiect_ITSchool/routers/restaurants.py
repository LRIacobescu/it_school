from fastapi import APIRouter, HTTPException, status
from typing import Optional

from data import restaurants
from schemas import RestaurantCreate, RestaurantUpdate, RestaurantPatch
from services.restaurant_service import RestaurantService

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

restaurant_service = RestaurantService(restaurants)

@router.get("")
def get_restaurants(
    city: Optional[str] = None,
    is_open: Optional[bool] = None
):
    return restaurant_service.get_all(city, is_open)

@router.get("/{restaurant_id}")
def get_restaurant_by_id(restaurant_id: int):
    restaurant = restaurant_service.find_by_id(restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurantul nu a fost gasit"
        )
    return restaurant

@router.post("", status_code=status.HTTP_201_CREATED)
def create_restaurant(restaurant: RestaurantCreate):
    if restaurant_service.name_exists_in_city(restaurant.name, restaurant.city):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Exista deja un restaurant cu acest nume in orasul respectiv"
        )

    return restaurant_service.create(restaurant)

@router.put("/{restaurant_id}")
def update_restaurant(restaurant_id: int, updated_restaurant: RestaurantUpdate):
    restaurant = restaurant_service.find_by_id(restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurantul nu a fost gasit"
        )

    if restaurant_service.name_exists_in_city(
        updated_restaurant.name,
        updated_restaurant.city,
        restaurant_id
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Exista deja un restaurant cu acest nume in oras"
        )

    return restaurant_service.update(restaurant, updated_restaurant)

@router.patch("/{restaurant_id}")
def patch_restaurant(restaurant_id: int, restaurant_update: RestaurantPatch):
    restaurant = restaurant_service.find_by_id(restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurantul nu a fost gasit"
        )

    updates = restaurant_update.model_dump(exclude_unset=True)

    if len(updates) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trebuie trimis cel putin un camp"
        )

    if "name" in updates and "city" in updates:
        if restaurant_service.name_exists_in_city(
            updates["name"],
            updates["city"],
            restaurant_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Exista deja un restaurant cu acest nume in oras"
            )

    return restaurant_service.patch(restaurant, updates)

@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: int):
    restaurant = restaurant_service.find_by_id(restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurantul nu a fost gasit"
        )

    deleted_restaurant = restaurant_service.delete(restaurant)

    return {
        "message": "Restaurantul a fost sters",
        "deleted_restaurant": deleted_restaurant
    }