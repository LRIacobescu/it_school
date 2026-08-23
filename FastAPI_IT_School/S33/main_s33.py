from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Food Delivery API",
    version="1.0.0"
)


class ProductCreate(BaseModel):
    name: str = Field(min_length=2)
    description: str = ""
    price: float = Field(gt=0)
    category: str = Field(min_length=2)
    available: bool = True


class ProductUpdate(BaseModel):
    name: str = Field(min_length=2)
    description: str = ""
    price: float = Field(gt=0)
    category: str = Field(min_length=2)
    available: bool = True


class ProductPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2)
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    category: Optional[str] = Field(default=None, min_length=2)
    available: Optional[bool] = None


class RestaurantCreate(BaseModel):
    name: str = Field(min_length=2)
    city: str = Field(min_length=2)
    address: str = Field(min_length=5)
    rating: float = Field(ge=0, le=5)
    is_open: bool = True


class RestaurantUpdate(BaseModel):
    name: str = Field(min_length=2)
    city: str = Field(min_length=2)
    address: str = Field(min_length=5)
    rating: float = Field(ge=0, le=5)
    is_open: bool = True


class RestaurantPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2)
    city: Optional[str] = Field(default=None, min_length=2)
    address: Optional[str] = Field(default=None, min_length=5)
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    is_open: Optional[bool] = None


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2)


class CategoryUpdate(BaseModel):
    name: str = Field(min_length=2)


class CategoryPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2)


class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=2)
    total_price: float = Field(gt=0)
    number_of_products: int = Field(gt=0)
    delivery_fee: float = Field(default=10, ge=0)
    status: str = "new"


class OrderUpdate(BaseModel):
    customer_name: str = Field(min_length=2)
    total_price: float = Field(gt=0)
    number_of_products: int = Field(gt=0)
    delivery_fee: float = Field(ge=0)
    status: str = Field(min_length=2)


class OrderPatch(BaseModel):
    customer_name: Optional[str] = Field(default=None, min_length=2)
    total_price: Optional[float] = Field(default=None, gt=0)
    number_of_products: Optional[int] = Field(default=None, gt=0)
    delivery_fee: Optional[float] = Field(default=None, ge=0)
    status: Optional[str] = Field(default=None, min_length=2)


class OrderStatusUpdate(BaseModel):
    status: str = Field(min_length=2)


class CourierCreate(BaseModel):
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    phone: str = Field(min_length=10, max_length=15)
    active: bool = True


class CourierUpdate(BaseModel):
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    phone: str = Field(min_length=10, max_length=15)
    active: bool = True


class CourierPatch(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=2)
    last_name: Optional[str] = Field(default=None, min_length=2)
    phone: Optional[str] = Field(default=None, min_length=10, max_length=15)
    active: Optional[bool] = None


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
        "status": "preparing"
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


valid_order_statuses = [
    "new",
    "accepted",
    "preparing",
    "ready_for_delivery",
    "picked_up",
    "delivered",
    "cancelled"
]


def get_next_product_id():
    max_id = 0

    for product in products:
        if product["id"] > max_id:
            max_id = product["id"]

    return max_id + 1


def get_next_restaurant_id():
    max_id = 0

    for restaurant in restaurants:
        if restaurant["id"] > max_id:
            max_id = restaurant["id"]

    return max_id + 1


def get_next_category_id():
    max_id = 0

    for category in categories:
        if category["id"] > max_id:
            max_id = category["id"]

    return max_id + 1


def get_next_order_id():
    max_id = 0

    for order in orders:
        if order["id"] > max_id:
            max_id = order["id"]

    return max_id + 1


def get_next_courier_id():
    max_id = 0

    for courier in couriers:
        if courier["id"] > max_id:
            max_id = courier["id"]

    return max_id + 1


def find_product_by_id(product_id):
    for product in products:
        if product["id"] == product_id:
            return product

    return None


def find_restaurant_by_id(restaurant_id):
    for restaurant in restaurants:
        if restaurant["id"] == restaurant_id:
            return restaurant

    return None


def find_category_by_id(category_id):
    for category in categories:
        if category["id"] == category_id:
            return category

    return None


def find_order_by_id(order_id):
    for order in orders:
        if order["id"] == order_id:
            return order

    return None


def find_courier_by_id(courier_id):
    for courier in couriers:
        if courier["id"] == courier_id:
            return courier

    return None


def category_exists(category_name):
    for category in categories:
        if category["name"].lower() == category_name.lower():
            return True

    return False


def order_status_is_valid(order_status):
    if order_status.lower() in valid_order_statuses:
        return True

    return False


@app.get("/")
def home():
    return {
        "message": "Salut din Food Delivery API!"
    }


@app.get("/status")
def get_status():
    return {
        "app": "Food Delivery API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/products")
def get_products(
    category: Optional[str] = None,
    available: Optional[bool] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    name: Optional[str] = None
):
    if min_price is not None and max_price is not None:
        if min_price > max_price:
            return {
                "message": "Pretul minim nu poate fi mai mare decat pretul maxim"
            }

    filtered_products = []

    for product in products:
        if category is not None:
            if product["category"].lower() != category.lower():
                continue

        if available is not None:
            if product["available"] != available:
                continue

        if min_price is not None:
            if product["price"] < min_price:
                continue

        if max_price is not None:
            if product["price"] > max_price:
                continue

        if name is not None:
            if name.lower() not in product["name"].lower():
                continue

        filtered_products.append(product)

    return filtered_products


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    product = find_product_by_id(product_id)

    if product is None:
        return {
            "message": "Produsul nu a fost gasit"
        }

    return product


@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    if category_exists(product.category) is False:
        return {
            "message": "Categoria nu exista"
        }

    for existing_product in products:
        if existing_product["name"].lower() == product.name.lower():
            return {
                "message": "Exista deja un produs cu acest nume"
            }

    new_product = {
        "id": get_next_product_id(),
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category.lower(),
        "available": product.available
    }

    products.append(new_product)

    return new_product


@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    updated_product: ProductUpdate
):
    product = find_product_by_id(product_id)

    if product is None:
        return {
            "message": "Produsul nu a fost gasit"
        }

    if category_exists(updated_product.category) is False:
        return {
            "message": "Categoria nu exista"
        }

    for existing_product in products:
        same_name = (
            existing_product["name"].lower()
            == updated_product.name.lower()
        )

        different_id = existing_product["id"] != product_id

        if same_name and different_id:
            return {
                "message": "Exista deja un produs cu acest nume"
            }

    product["name"] = updated_product.name
    product["description"] = updated_product.description
    product["price"] = updated_product.price
    product["category"] = updated_product.category.lower()
    product["available"] = updated_product.available

    return product


@app.patch("/products/{product_id}")
def patch_product(
    product_id: int,
    product_update: ProductPatch
):
    product = find_product_by_id(product_id)

    if product is None:
        return {
            "message": "Produsul nu a fost gasit"
        }

    updates = product_update.model_dump(exclude_unset=True)

    if len(updates) == 0:
        return {
            "message": "Trebuie trimis cel putin un camp"
        }

    if "category" in updates:
        if category_exists(updates["category"]) is False:
            return {
                "message": "Categoria nu exista"
            }

        updates["category"] = updates["category"].lower()

    if "name" in updates:
        for existing_product in products:
            same_name = (
                existing_product["name"].lower()
                == updates["name"].lower()
            )

            different_id = existing_product["id"] != product_id

            if same_name and different_id:
                return {
                    "message": "Exista deja un produs cu acest nume"
                }

    for key in updates:
        product[key] = updates[key]

    return product


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    product = find_product_by_id(product_id)

    if product is None:
        return {
            "message": "Produsul nu a fost gasit"
        }

    products.remove(product)

    return {
        "message": "Produsul a fost sters",
        "deleted_product": product
    }


@app.get("/restaurants")
def get_restaurants(
    city: Optional[str] = None,
    is_open: Optional[bool] = None,
    min_rating: Optional[float] = None
):
    filtered_restaurants = []

    for restaurant in restaurants:
        if city is not None:
            if restaurant["city"].lower() != city.lower():
                continue

        if is_open is not None:
            if restaurant["is_open"] != is_open:
                continue

        if min_rating is not None:
            if restaurant["rating"] < min_rating:
                continue

        filtered_restaurants.append(restaurant)

    return filtered_restaurants


@app.get("/restaurants/{restaurant_id}")
def get_restaurant_by_id(restaurant_id: int):
    restaurant = find_restaurant_by_id(restaurant_id)

    if restaurant is None:
        return {
            "message": "Restaurantul nu a fost gasit"
        }

    return restaurant


@app.post("/restaurants", status_code=201)
def create_restaurant(restaurant: RestaurantCreate):
    for existing_restaurant in restaurants:
        same_name = (
            existing_restaurant["name"].lower()
            == restaurant.name.lower()
        )

        same_city = (
            existing_restaurant["city"].lower()
            == restaurant.city.lower()
        )

        if same_name and same_city:
            return {
                "message": "Restaurantul exista deja in acest oras"
            }

    new_restaurant = {
        "id": get_next_restaurant_id(),
        "name": restaurant.name,
        "city": restaurant.city,
        "address": restaurant.address,
        "rating": restaurant.rating,
        "is_open": restaurant.is_open
    }

    restaurants.append(new_restaurant)

    return new_restaurant


@app.put("/restaurants/{restaurant_id}")
def update_restaurant(
    restaurant_id: int,
    updated_restaurant: RestaurantUpdate
):
    restaurant = find_restaurant_by_id(restaurant_id)

    if restaurant is None:
        return {
            "message": "Restaurantul nu a fost gasit"
        }

    restaurant["name"] = updated_restaurant.name
    restaurant["city"] = updated_restaurant.city
    restaurant["address"] = updated_restaurant.address
    restaurant["rating"] = updated_restaurant.rating
    restaurant["is_open"] = updated_restaurant.is_open

    return restaurant


@app.patch("/restaurants/{restaurant_id}")
def patch_restaurant(
    restaurant_id: int,
    restaurant_update: RestaurantPatch
):
    restaurant = find_restaurant_by_id(restaurant_id)

    if restaurant is None:
        return {
            "message": "Restaurantul nu a fost gasit"
        }

    updates = restaurant_update.model_dump(exclude_unset=True)

    if len(updates) == 0:
        return {
            "message": "Trebuie trimis cel putin un camp"
        }

    for key in updates:
        restaurant[key] = updates[key]

    return restaurant


@app.delete("/restaurants/{restaurant_id}")
def delete_restaurant(restaurant_id: int):
    restaurant = find_restaurant_by_id(restaurant_id)

    if restaurant is None:
        return {
            "message": "Restaurantul nu a fost gasit"
        }

    restaurants.remove(restaurant)

    return {
        "message": "Restaurantul a fost sters",
        "deleted_restaurant": restaurant
    }


@app.get("/categories")
def get_categories():
    return categories


@app.get("/categories/{category_id}")
def get_category_by_id(category_id: int):
    category = find_category_by_id(category_id)

    if category is None:
        return {
            "message": "Categoria nu a fost gasita"
        }

    return category


@app.post("/categories", status_code=201)
def create_category(category: CategoryCreate):
    for existing_category in categories:
        if existing_category["name"].lower() == category.name.lower():
            return {
                "message": "Categoria exista deja"
            }

    new_category = {
        "id": get_next_category_id(),
        "name": category.name.lower()
    }

    categories.append(new_category)

    return new_category


@app.put("/categories/{category_id}")
def update_category(
    category_id: int,
    updated_category: CategoryUpdate
):
    category = find_category_by_id(category_id)

    if category is None:
        return {
            "message": "Categoria nu a fost gasita"
        }

    for existing_category in categories:
        same_name = (
            existing_category["name"].lower()
            == updated_category.name.lower()
        )

        different_id = existing_category["id"] != category_id

        if same_name and different_id:
            return {
                "message": "Categoria exista deja"
            }

    old_name = category["name"]
    new_name = updated_category.name.lower()

    category["name"] = new_name

    for product in products:
        if product["category"].lower() == old_name.lower():
            product["category"] = new_name

    return category


@app.patch("/categories/{category_id}")
def patch_category(
    category_id: int,
    category_update: CategoryPatch
):
    category = find_category_by_id(category_id)

    if category is None:
        return {
            "message": "Categoria nu a fost gasita"
        }

    updates = category_update.model_dump(exclude_unset=True)

    if len(updates) == 0:
        return {
            "message": "Trebuie trimis cel putin un camp"
        }

    new_name = updates["name"].lower()

    for existing_category in categories:
        same_name = existing_category["name"].lower() == new_name
        different_id = existing_category["id"] != category_id

        if same_name and different_id:
            return {
                "message": "Categoria exista deja"
            }

    old_name = category["name"]
    category["name"] = new_name

    for product in products:
        if product["category"].lower() == old_name.lower():
            product["category"] = new_name

    return category


@app.delete("/categories/{category_id}")
def delete_category(category_id: int):
    category = find_category_by_id(category_id)

    if category is None:
        return {
            "message": "Categoria nu a fost gasita"
        }

    for product in products:
        if product["category"].lower() == category["name"].lower():
            return {
                "message": "Categoria nu poate fi stearsa deoarece este folosita de produse"
            }

    categories.remove(category)

    return {
        "message": "Categoria a fost stearsa",
        "deleted_category": category
    }


@app.get("/orders")
def get_orders(
    order_status: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    customer_name: Optional[str] = None
):
    if min_price is not None and max_price is not None:
        if min_price > max_price:
            return {
                "message": "Pretul minim nu poate fi mai mare decat pretul maxim"
            }

    filtered_orders = []

    for order in orders:
        if order_status is not None:
            if order["status"].lower() != order_status.lower():
                continue

        if min_price is not None:
            if order["total_price"] < min_price:
                continue

        if max_price is not None:
            if order["total_price"] > max_price:
                continue

        if customer_name is not None:
            if customer_name.lower() not in order["customer_name"].lower():
                continue

        filtered_orders.append(order)

    return filtered_orders


@app.get("/orders/{order_id}")
def get_order_by_id(order_id: int):
    order = find_order_by_id(order_id)

    if order is None:
        return {
            "message": "Comanda nu a fost gasita"
        }

    return order


@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    if order_status_is_valid(order.status) is False:
        return {
            "message": "Statusul comenzii nu este valid"
        }

    new_order = {
        "id": get_next_order_id(),
        "customer_name": order.customer_name,
        "total_price": order.total_price,
        "number_of_products": order.number_of_products,
        "delivery_fee": order.delivery_fee,
        "status": order.status.lower()
    }

    orders.append(new_order)

    return new_order


@app.put("/orders/{order_id}")
def update_order(
    order_id: int,
    updated_order: OrderUpdate
):
    order = find_order_by_id(order_id)

    if order is None:
        return {
            "message": "Comanda nu a fost gasita"
        }

    if order_status_is_valid(updated_order.status) is False:
        return {
            "message": "Statusul comenzii nu este valid"
        }

    order["customer_name"] = updated_order.customer_name
    order["total_price"] = updated_order.total_price
    order["number_of_products"] = updated_order.number_of_products
    order["delivery_fee"] = updated_order.delivery_fee
    order["status"] = updated_order.status.lower()

    return order


@app.patch("/orders/{order_id}")
def patch_order(
    order_id: int,
    order_update: OrderPatch
):
    order = find_order_by_id(order_id)

    if order is None:
        return {
            "message": "Comanda nu a fost gasita"
        }

    updates = order_update.model_dump(exclude_unset=True)

    if len(updates) == 0:
        return {
            "message": "Trebuie trimis cel putin un camp"
        }

    if "status" in updates:
        if order_status_is_valid(updates["status"]) is False:
            return {
                "message": "Statusul comenzii nu este valid"
            }

        updates["status"] = updates["status"].lower()

    for key in updates:
        order[key] = updates[key]

    return order


@app.patch("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate
):
    order = find_order_by_id(order_id)

    if order is None:
        return {
            "message": "Comanda nu a fost gasita"
        }

    if order_status_is_valid(status_update.status) is False:
        return {
            "message": "Statusul comenzii nu este valid"
        }

    order["status"] = status_update.status.lower()

    return order


@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    order = find_order_by_id(order_id)

    if order is None:
        return {
            "message": "Comanda nu a fost gasita"
        }

    if order["status"] == "delivered":
        return {
            "message": "O comanda livrata nu poate fi stearsa"
        }

    orders.remove(order)

    return {
        "message": "Comanda a fost stearsa",
        "deleted_order": order
    }


@app.get("/couriers")
def get_couriers(
    active: Optional[bool] = None,
    first_name: Optional[str] = None
):
    filtered_couriers = []

    for courier in couriers:
        if active is not None:
            if courier["active"] != active:
                continue

        if first_name is not None:
            if first_name.lower() not in courier["first_name"].lower():
                continue

        filtered_couriers.append(courier)

    return filtered_couriers


@app.get("/couriers/{courier_id}")
def get_courier_by_id(courier_id: int):
    courier = find_courier_by_id(courier_id)

    if courier is None:
        return {
            "message": "Curierul nu a fost gasit"
        }

    return courier


@app.post("/couriers", status_code=201)
def create_courier(courier: CourierCreate):
    for existing_courier in couriers:
        if existing_courier["phone"] == courier.phone:
            return {
                "message": "Exista deja un curier cu acest numar de telefon"
            }

    new_courier = {
        "id": get_next_courier_id(),
        "first_name": courier.first_name,
        "last_name": courier.last_name,
        "phone": courier.phone,
        "active": courier.active
    }

    couriers.append(new_courier)

    return new_courier


@app.put("/couriers/{courier_id}")
def update_courier(
    courier_id: int,
    updated_courier: CourierUpdate
):
    courier = find_courier_by_id(courier_id)

    if courier is None:
        return {
            "message": "Curierul nu a fost gasit"
        }

    for existing_courier in couriers:
        same_phone = existing_courier["phone"] == updated_courier.phone
        different_id = existing_courier["id"] != courier_id

        if same_phone and different_id:
            return {
                "message": "Exista deja un curier cu acest numar de telefon"
            }

    courier["first_name"] = updated_courier.first_name
    courier["last_name"] = updated_courier.last_name
    courier["phone"] = updated_courier.phone
    courier["active"] = updated_courier.active

    return courier


@app.patch("/couriers/{courier_id}")
def patch_courier(
    courier_id: int,
    courier_update: CourierPatch
):
    courier = find_courier_by_id(courier_id)

    if courier is None:
        return {
            "message": "Curierul nu a fost gasit"
        }

    updates = courier_update.model_dump(exclude_unset=True)

    if len(updates) == 0:
        return {
            "message": "Trebuie trimis cel putin un camp"
        }

    if "phone" in updates:
        for existing_courier in couriers:
            same_phone = existing_courier["phone"] == updates["phone"]
            different_id = existing_courier["id"] != courier_id

            if same_phone and different_id:
                return {
                    "message": "Exista deja un curier cu acest numar de telefon"
                }

    for key in updates:
        courier[key] = updates[key]

    return courier


@app.delete("/couriers/{courier_id}")
def delete_courier(courier_id: int):
    courier = find_courier_by_id(courier_id)

    if courier is None:
        return {
            "message": "Curierul nu a fost gasit"
        }

    if courier["active"] is True:
        return {
            "message": "Un curier activ nu poate fi sters"
        }

    couriers.remove(courier)

    return {
        "message": "Curierul a fost sters",
        "deleted_courier": courier
    }

""