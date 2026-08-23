from fastapi import FastAPI
from pydantic import BaseModel, Field # baseModel(construim modele pentru datele primite); Field(reguli suplimentare de validare)

app = FastAPI()

# Creare model ProductCreate
class ProductCreate(BaseModel):
    name: str = Field(min_length = 2)
    description: str = ""
    price: float = Field(gt = 0)
    category: str = Field(min_length = 2)
    available: bool = True

# Model pentru restaurante
class RestaurantCreate(BaseModel):
    name: str = Field(min_length = 2)
    city: str = Field(min_length = 2)
    rating: float = Field(ge = 0, le = 5)
    is_open: bool = True

# Model pentru comenzi
class OrderCreate(BaseModel):
    customer_name: str = Field(min_length = 2)
    total_price: float = Field(gt = 0)
    status: str = "new"

@app.post("/products", status_code = 201)
def create_product(product: ProductCreate):
    for product_existent in products:
        if product_existent["name"].lower() == product.name.lower():
            return {
                "message": "Exista deja un produs cu acelasi nume"
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

@app.post("/restaurants", status_code = 201)
def create_restaurant(restaurant: RestaurantCreate):
    new_restaurant = {
        "id": len(restaurants) + 1,
        "name": restaurant.name,
        "city": restaurant.city,
        "rating": restaurant.rating,
        "is_open": restaurant.is_open
    }
    restaurants.append(new_restaurant)

    return new_restaurant

@app.post("/orders", status_code = 201)
def create_order(order: OrderCreate):
    new_order = {
        "id": len(orders) + 1,
        "customer_name": order.customer_name,
        "total_price": order.total_price,
        "status": order.status
    }
    orders.append(new_order)

    return new_order

"""
1. Adauga camp nou in modelul produsului: description
    Descrierea nu trebuie sa fie obligatorie, valoarea implicita va fi un text gol
2. Creeaza modelul CourierCreate pentru curieri
    - first_name
    - last_name
    - phone
    - active (implicit True)
3. Creeaza POST /couriers
4. Creeaza modelul pt Category
    - name - text, min 2 char
5. Creeaza endpointul POST /categories
6. Verifica categorii duplicate. Daca exista, return message
"""

# 2.
class CourierCreate(BaseModel):
    first_name: str = Field(min_length = 2)
    last_name: str = Field(min_length = 2)
    phone: str = Field(min_length = 10)
    active: bool = True

# 3.
@app.post("/couriers", status_code = 201)
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

# 4.
class CategoryCreate(BaseModel):
    name: str = Field(min_length = 2)

# 5.
@app.post("/categories", status_code = 201)
def create_category(category: CategoryCreate):
    for category_existent in categories:
        if category_existent["name"].lower() == category.name.lower():
            return {
                "message": "Exista deja o categorie cu acelasi nume"
            }
    new_category = {
        "id": len(categories) + 1,
        "name": category.name
    }
    categories.append(new_category)

    return new_category


products = [
    { "id": 1, "name": "Pizza Margherita", "price": 35, "category": "pizza", "available": True },
    { "id": 2, "name": "Burger de vita", "price": 42, "category": "burger", "available": True },
    { "id": 3, "name": "Paste Carbonara", "price": 39, "category": "paste", "available": False },
    { "id": 4, "name": "Tiramisu", "price": 24, "category": "desert", "available": True },
    { "id": 5, "name": "Cola 500ml", "price": 9, "category": "bautura", "available": True }
]

restaurants = [
    { "id": 1, "name": "Pizza House", "city": "Cluj", "rating": 4.7, "is_open": True },
    { "id": 2, "name": "Burger Point", "city": "Timisoara", "rating": 4.5, "is_open": False },
    { "id": 3, "name": "Pasta Corner", "city": "Bucuresti", "rating": 4.8, "is_open": True }
]

categories = [
    { "id": 1, "name": "pizza" },
    { "id": 2, "name": "burger" },
    { "id": 3, "name": "paste" },
    { "id": 4, "name": "desert" },
    { "id": 5, "name": "bautura" }
]

orders = [
    { "id": 1, "customer_name": "Andrei Popescu", "total_price": 87, "status": "new" },
    { "id": 2, "customer_name": "Maria Ionescu", "total_price": 120, "status": "delivered" },
    { "id": 3, "customer_name": "Ioana Stan", "total_price": 64, "status": "new" },
    { "id": 4, "customer_name": "George Marin", "total_price": 45, "status": "cancelled" }
]

couriers = [
    { "id": 1, "first_name": "Mihai", "last_name": "Popescu", "phone": "0712345678", "active": True },
    { "id": 2, "first_name": "Andrei", "last_name": "Ionescu", "phone": "0723456789", "active": False },
    { "id": 3, "first_name": "Alex", "last_name": "Dumitrescu", "phone": "0734567890", "active": True }
]

@app.get("/")
def home():
    return {
        "message": "FastAPI S29 itschool"
    }

@app.get("/status")
def status():
    return {
        "app": "Food Delivery API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/categories")
def get_categories():
    return categories

@app.get("/couriers")
def get_couriers():
    return couriers

# 1. Primul path parameter -> produs dupa id
@app.get("/products/{product_id}") # Ruta dinamica; orice variabila dupa /products/ va fi pusa in variabila product_id
def get_product_by_id(product_id: int):
    for product in products: # parcurgem produsele
        if product["id"] == product_id: # Daca id produsului curent este egal cu id ul primit din URL
            return product # Daca am gasit produsul, il returnam

    return { # Daca am parcurs toate produsele si nu am gasit nimic, returnam un mesaj
        "message": "Produsul nu a fost gasit"
    }

# 2. path parameter pentru restaurante
# Vrem: /restaurants/1 ; /restaurants/2

@app.get("/restaurants/{restaurant_id}")
def get_restaurant_by_id(restaurant_id: int):
    for restaurant in restaurants:
        if restaurant["id"] == restaurant_id:
            return restaurant

    return {
        "message": "Restaurantul nu a fost gasit"
    }

@app.get("/categories/{category_id}")
def get_category_by_id(category_id: int):
    for category in categories:
        if category["id"] == category_id:
            return category

    return {
        "message": "Categoria nu a fost gasita"
    }

# Path parameter pentru comenzi
@app.get("/orders/{order_id}")
def order(order_id: int):
    for order in orders:
        if order["id"] == order_id:
            return order

    return {
        "message": "Comanda nu a fost gasita"
    }

# Query parameter: filtrare produse dupa categorie
# @app.get("/products")
# def get_products(category: str = None): # -> Daca primesc category in URL, il folosesc; daca nu primesc category, valoare va fi none/null
#     if category is None:
#         return products
#
#     filtered_products = []
#
#     for product in products:
#         if product["category"] == category:
#             filtered_products.append(product)
#
#     return filtered_products

# Query parameter pentru disponibilitate
# @app.get("/products")
# def get_products(category: str = None, available: bool = None): # -> Daca primesc category in URL, il folosesc; daca nu primesc category, valoare va fi none/null
#     filtered_products = []
#
#     for product in products:
#         if category is not None and product["category"] != category:
#             continue
#
#         if available is not None and product["available"] != available:
#             continue
#         filtered_products.append(product)
#
#     return filtered_products

# Query parameter pentru pret maxim
@app.get("/products")
def get_products(category: str = None, available: bool = None, max_price: float = None): # -> Daca primesc category in URL, il folosesc; daca nu primesc category, valoare va fi none/null
    filtered_products = []

    for product in products:
        if category is not None and product["category"] != category:
            continue

        if available is not None and product["available"] != available:
            continue

        if max_price is not None and product["price"] > max_price:
            continue

        filtered_products.append(product)

    return filtered_products

"""
1. Creeaza endpoint ul GET /couriers/{courier_id} care returneaza curierul cu id primit in URL. Daca nu exista, returneaza mesaj
2. Modifica endpoint ul GET /restaurants ca sa accepte si query parameter: city (/restaurants?city=Timisoara)
3. Adauga query parameter is_open pentru filtru resturante deschise (/restaurants?is_open=true)
4. Modifica endpoint ul GET /orders ca sa putem filtra dupa status
"""

#1.
@app.get("/couriers/{courier_id}")
def get_courier_by_id(courier_id: int):
    for courier in couriers:
        if courier["id"] == courier_id:
            return courier

    return {
        "message": "Curierul nu a fost gasit"
    }

#2. & 3.
@app.get("/restaurants")
def get_restaurants(city: str = None, is_open: bool = None):
    filtered_restaurants = []

    for restaurant in restaurants:
        if (city is None or restaurant["city"] == city) and (is_open is None or restaurant["is_open"] == is_open):
            filtered_restaurants.append(restaurant)

    return filtered_restaurants


# 4.
@app.get("/orders")
def get_orders(status: str = None):
    filtered_orders = []

    for order in orders:
        if status is None or order["status"] == status:
            filtered_orders.append(order)

    return filtered_orders

