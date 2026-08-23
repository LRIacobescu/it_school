from fastapi import FastAPI # Clasa principala de care ne folosim ca sa cream aplicatia

app = FastAPI() # Aici cream aplicatia FastAPI. Variabila app reprezinta serverul nostru. De aici porneste aplicatia

products = [
    {
        "id": 1,
        "name": "Pizza Margherita",
        "price": 35,
        "category": "Pizza",
        "available": True
    },
{
        "id": 2,
        "name": "Burger vita",
        "price": 50,
        "category": "Burger",
        "available": True
    },
{
        "id": 3,
        "name": "Paste Carbonara",
        "price": 40,
        "category": "Paste",
        "available": False
    },
]

restaurants = [
    {
        "id": 1,
        "name": "Whisper",
        "city": "Timisoara",
        "rating": 4.8,
        "is_open": True
    },
{
        "id": 2,
        "name": "Beraria 700",
        "city": "Timisoara",
        "rating": 4.5,
        "is_open": False
    },
{
        "id": 1,
        "name": "Pasta Corner",
        "city": "Timisoara",
        "rating": 4.7,
        "is_open": True
    }
]

categories = [
    {"id": 1, "name": "Pizza"},
     {"id":2, "name": "Burger"},
      {"id": 3, "name": "Paste"},
       {"id": 4, "name": "desert"}
]
"""
Cand cineva face un request de tip GET pe ruta /, FastAPI va executa functia de dedesubt/ Ruta / este pagina principala
"""
@app.get("/")
def home():
    return {
        "message": "FastAPI S29 itschool" # Returnez un dictionar python iar FastAPI il transforma in JSON
    }

@app.get("/status")
def status():
    return {
        "app": "Food Delivery API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/products")
def get_products():
    return products

@app.get("/restaurants")
def get_restaurants():
    return restaurants

"""
1. Creeaza endpointul GET /hello care returneaza "message": "Salutare colegi"
2. Creeaza endpointul GET /about care returneaza "name": "", "description": " ", "author": " "
3. Creeaza o lista de categorii si endpointul: GET /categories cu lista: 
"id": 1, "name": "Pizza", 
"id":2, "name": "Burger", 
"id": 3, "name": "Paste", 
"id": 4, "name": "desert"
4. Creeaza endpointul GET /available-products care returneaza produsele disponibile
"""

# 1.
@app.get("/hello")
def hello():
    return {"message": "Salutare colegi"}

# 2.
@app.get("/about")
def about():
    return {
        "name": "Food Delivery App",
        "description": "Aplicatie pentru livrare mancare",
        "author": "Florin"
    }

#3.
@app.get("/categories")
def get_categories():
    return categories

# 4.
@app.get("/available_products")
def get_available_products():
    available_products = []

    for product in products:
        if product["available"] == True:
            available_products.append(product)
    return available_products

#5. Returneaza restaurantele deschise
@app.get("/open_restaurants")
def get_open_restaurants():
    open_restaurants = []

    for restaurant in restaurants:
        if restaurant["is_open"] == True:
            open_restaurants.append(restaurant)
    return open_restaurants

