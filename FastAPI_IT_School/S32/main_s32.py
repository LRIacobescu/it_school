from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class ProductCreate(BaseModel):
    name: str = Field(min_length=2)
    description: str = ""
    price: float = Field(gt=0)
    category: str = Field(min_length=2)
    available: bool = True


class RestaurantCreate(BaseModel):
    name: str = Field(min_length=2)
    city: str = Field(min_length=2)
    address: str = Field(min_length=5)
    rating: float = Field(ge=0, le=5)
    is_open: bool = True


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2)


class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=2)
    total_price: float = Field(gt=0)
    number_of_products: int = Field(gt=0)
    delivery_fee: float = Field(default=10, ge=0)
    status: str = "new"


class CourierCreate(BaseModel):
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    phone: str = Field(min_length=10)
    active: bool = True


products = [
    {
        "id": 1,
        "name": "Pizza Margherita",
        "description": "Pizza cu sos de rosii si mozzarella",
        "price": 35,
        "category": "pizza",
        "available": True
    },
    {
        "id": 2,
        "name": "Burger de vita",
        "description": "Burger cu carne de vita si cartofi",
        "price": 42,
        "category": "burger",
        "available": True
    },
    {
        "id": 3,
        "name": "Paste Carbonara",
        "description": "Paste cu pancetta, ou si parmezan",
        "price": 39,
        "category": "paste",
        "available": False
    },
    {
        "id": 4,
        "name": "Tiramisu",
        "description": "Desert italian cu mascarpone",
        "price": 24,
        "category": "desert",
        "available": True
    },
    {
        "id": 5,
        "name": "Cola 500ml",
        "description": "Bautura racoritoare",
        "price": 9,
        "category": "bautura",
        "available": True
    }
]


restaurants = [
    {
        "id": 1,
        "name": "Pizza House",
        "city": "Timisoara",
        "address": "Strada Unirii 10",
        "rating": 4.7,
        "is_open": True
    },
    {
        "id": 2,
        "name": "Burger Point",
        "city": "Timisoara",
        "address": "Strada Victoriei 15",
        "rating": 4.5,
        "is_open": False
    },
    {
        "id": 3,
        "name": "Pasta Corner",
        "city": "Timisoara",
        "address": "Bulevardul Central 8",
        "rating": 4.8,
        "is_open": True
    }
]


categories = [
    {
        "id": 1,
        "name": "pizza"
    },
    {
        "id": 2,
        "name": "burger"
    },
    {
        "id": 3,
        "name": "paste"
    },
    {
        "id": 4,
        "name": "desert"
    },
    {
        "id": 5,
        "name": "bautura"
    }
]


orders = [
    {
        "id": 1,
        "customer_name": "Andrei Popescu",
        "total_price": 87,
        "number_of_products": 2,
        "delivery_fee": 10,
        "status": "new"
    },
    {
        "id": 2,
        "customer_name": "Maria Ionescu",
        "total_price": 120,
        "number_of_products": 3,
        "delivery_fee": 0,
        "status": "delivered"
    },
    {
        "id": 3,
        "customer_name": "Ioana Stan",
        "total_price": 64,
        "number_of_products": 2,
        "delivery_fee": 10,
        "status": "new"
    },
    {
        "id": 4,
        "customer_name": "George Marin",
        "total_price": 45,
        "number_of_products": 1,
        "delivery_fee": 10,
        "status": "cancelled"
    }
]


couriers = [
    {
        "id": 1,
        "first_name": "Mihai",
        "last_name": "Popescu",
        "phone": "0712345678",
        "active": True
    },
    {
        "id": 2,
        "first_name": "Andrei",
        "last_name": "Ionescu",
        "phone": "0723456789",
        "active": False
    },
    {
        "id": 3,
        "first_name": "Alex",
        "last_name": "Dumitrescu",
        "phone": "0734567890",
        "active": True
    }
]


@app.get("/")
def home():
    return {
        "message": "Food Delivery app"
    }


@app.get("/status")
def get_status():
    return {
        "app": "Food Delivery APP",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/products")
def get_products(
    category: str = None,
    available: bool = None,
    min_price: float = None,
    max_price: float = None,
    name: str = None
):
    filtered_products = []

    for product in products:
        if category is not None and product["category"] != category:
            continue

        if available is not None and product["available"] != available:
            continue

        if min_price is not None and product["price"] < min_price:
            continue

        if max_price is not None and product["price"] > max_price:
            continue

        if name is not None:
            if name.lower() not in product["name"].lower():
                continue

        filtered_products.append(product)

    return filtered_products


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    return {
        "message": "Produsul nu a fost gasit"
    }


@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    for existing_product in products:
        if existing_product["name"].lower() == product.name.lower():
            return {
                "message": "Exista deja un produs cu acest nume"
            }

    new_product = {
        "id": len(products) + 1,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category,
        "available": product.available
    }

    products.append(new_product)

    return new_product


@app.get("/restaurants")
def get_restaurants(
    city: str = None,
    is_open: bool = None,
    min_rating: float = None
):
    filtered_restaurants = []

    for restaurant in restaurants:
        if city is not None and restaurant["city"] != city:
            continue

        if is_open is not None and restaurant["is_open"] != is_open:
            continue

        if min_rating is not None and restaurant["rating"] < min_rating:
            continue

        filtered_restaurants.append(restaurant)

    return filtered_restaurants


@app.get("/restaurants/{restaurant_id}")
def get_restaurant_by_id(restaurant_id: int):
    for restaurant in restaurants:
        if restaurant["id"] == restaurant_id:
            return restaurant

    return {
        "message": "Restaurantul nu a fost gasit"
    }


@app.post("/restaurants", status_code=201)
def create_restaurant(restaurant: RestaurantCreate):
    new_restaurant = {
        "id": len(restaurants) + 1,
        "name": restaurant.name,
        "city": restaurant.city,
        "address": restaurant.address,
        "rating": restaurant.rating,
        "is_open": restaurant.is_open
    }

    restaurants.append(new_restaurant)

    return new_restaurant


@app.get("/categories")
def get_categories():
    return categories


@app.get("/categories/{category_id}")
def get_category_by_id(category_id: int):
    for category in categories:
        if category["id"] == category_id:
            return category

    return {
        "message": "Categoria nu a fost gasita"
    }


@app.post("/categories", status_code=201)
def create_category(category: CategoryCreate):
    for existing_category in categories:
        if existing_category["name"].lower() == category.name.lower():
            return {
                "message": "Categoria exista deja"
            }

    new_category = {
        "id": len(categories) + 1,
        "name": category.name
    }

    categories.append(new_category)

    return new_category


@app.get("/orders")
def get_orders(
    status: str = None,
    min_price: float = None,
    max_price: float = None,
    customer_name: str = None
):
    filtered_orders = []

    for order in orders:
        if status is not None and order["status"] != status:
            continue

        if min_price is not None and order["total_price"] < min_price:
            continue

        if max_price is not None and order["total_price"] > max_price:
            continue

        if customer_name is not None:
            if customer_name.lower() not in order["customer_name"].lower():
                continue

        filtered_orders.append(order)

    return filtered_orders


@app.get("/orders/{order_id}")
def get_order_by_id(order_id: int):
    for order in orders:
        if order["id"] == order_id:
            return order

    return {
        "message": "Comanda nu a fost gasita"
    }


@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    new_order = {
        "id": len(orders) + 1,
        "customer_name": order.customer_name,
        "total_price": order.total_price,
        "number_of_products": order.number_of_products,
        "delivery_fee": order.delivery_fee,
        "status": order.status
    }

    orders.append(new_order)

    return new_order


@app.get("/couriers")
def get_couriers(
    active: bool = None,
    first_name: str = None
):
    filtered_couriers = []

    for courier in couriers:
        if active is not None and courier["active"] != active:
            continue

        if first_name is not None:
            if first_name.lower() not in courier["first_name"].lower():
                continue

        filtered_couriers.append(courier)

    return filtered_couriers


@app.get("/couriers/{courier_id}")
def get_courier_by_id(courier_id: int):
    for courier in couriers:
        if courier["id"] == courier_id:
            return courier

    return {
        "message": "Curierul nu a fost gasit"
    }


@app.post("/couriers", status_code=201)
def create_courier(courier: CourierCreate):
    new_courier = {
        "id": len(couriers) + 1,
        "first_name": courier.first_name,
        "last_name": courier.last_name,
        "phone": courier.phone,
        "active": courier.active
    }

    couriers.append(new_courier)

    return new_courier

"""
1. creeaza modelul pt restaurante si endpointul pt PUT(toate campurile sunt obligatorii
2. PATCH pentru restaurante. Model +endpoint
"""

#1.

class RestaurantUpdate(BaseModel): # acesta e modelul
    name: str = Field(min_length=2)
    city: str = Field(min_length=2)
    address: str = Field(min_length=5)
    rating: float = Field(ge=0, le=5)
    is_open: bool

@app.put("/restaurants/{restaurant_id}")
def update_restaurant(restaurant_id: int, restaurant: RestaurantUpdate):
    for existing_restaurant in restaurants:
        if restaurant["id"] == restaurant_id:
            restaurant["name"] = updated_restaurant.name
            restaurant["city"] = updated_restaurant.city
            restaurant["address"] = updated_restaurant.address
            restaurant["rating"] = updated_restaurant.rating
            restaurant["is_open"] = updated_restaurant.is_open

            return existing_restaurant

    return {"message": "Restaurantul nu a fost gasit"}

#2.

class RestaurantPatch(BaseModel):
    name: str | None = Field(default=None, min_length=2)
    city: str | None = Field(default=None, min_length=2)
    address: str | None = Field(default=None, min_length=5)
    rating: float | None = Field(default=None, ge=0, le=5)
    is_open: bool | None = None

@app.patch("/restaurants/{restaurant_id}")
def patch_restaurant(restaurant_id: int, restaurant: RestaurantPatch):
    for existing_restaurant in restaurants:
        if existing_restaurant["id"] == restaurant_id:

            if restaurant.name is not None:
                existing_restaurant["name"] = restaurant.name

            if restaurant.city is not None:
                existing_restaurant["city"] = restaurant.city

            if restaurant.address is not None:
                existing_restaurant["address"] = restaurant.address

            if restaurant.rating is not None:
                existing_restaurant["rating"] = restaurant.rating

            if restaurant.is_open is not None:
                existing_restaurant["is_open"] = restaurant.is_open

            return existing_restaurant

    return {"message": "Restaurantul nu a fost gasit"