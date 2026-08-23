from fastapi import FastAPI

app = FastAPI()

products = [
    { "id": 1, "name": "Pizza Margherita", "price": 35, "category": "pizza", "available": True },
    { "id": 2, "name": "Burger de vita", "price": 42, "category": "burger", "available": True },
    { "id": 3, "name": "Paste Carbonara", "price": 39, "category": "paste", "available": False },
    { "id": 4, "name": "Tiramisu", "price": 24, "category": "desert", "available": True },
    { "id": 5, "name": "Cola 500ml", "price": 9, "category": "bautura", "available": True }
]

restaurants = [
    { "id": 1, "name": "Pizza House", "city": "Timisoara", "rating": 4.7, "is_open": True },
    { "id": 2, "name": "Burger Point", "city": "Timisoara", "rating": 4.5, "is_open": False },
    { "id": 3, "name": "Pasta Corner", "city": "Timisoara", "rating": 4.8, "is_open": True }
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

@app.get("/products")
def get_products():
    return products

@app.get("/restaurants")
def get_restaurants():
    return restaurants

@app.get("/categories")
def get_categories():
    return categories

@app.get("/orders")
def get_orders():
    return orders

@app.get("/couriers")
def get_couriers():
    return couriers

"""
1.Creeaza endpoint-ul GET / couriesrs/{courier_id} care returneaza curierul cu id primit in URL. Daca nu exista, returneaza mesaj
2. Modifica endpoint ul GET / restaurants ca sa accepte si querry parameter: city (/restaurants?city=Timisoara)
3. Adauga querry parameter is_open pentru filtru restaurante deschise(/restaurants?is_open=true)
4. Modifica endpoint-ul 
"""

#1
@app.get("/couriers/{courier_id}")
def get_courier_by_id(courier_id: int):
    for courier in couriers:
        if courier["id"] == courier_id:
            return courier
    return {"message": "Curierul nu a fost gasit"}

#2
@app.get("/restaurants")
def get_restaurants(city: str = None):
    filtered = []

    for restaurant in restaurants:
        if city is None or restaurant["city"].lower() == city.lower(): #florin a facut cu city not none and restaurant["city"] != city si continue
            filtered.append(restaurant)

    return filtered

"""
Dacă nu trimiți city → city is None → toate restaurantele trec filtrul.
Dacă trimiți city → verifică fiecare restaurant cu for și îl adaugă doar dacă orașul se potrivește.
"""

#3.
@app.get("/restaurants")
def get_restaurants(city: str = None, is_open: bool = None):
    filtered = []

    for restaurant in restaurants:
        # Filtru city
        if city and restaurant["city"].lower() != city.lower():
            continue

        # Filtru is_open
        if is_open is not None and restaurant["is_open"] != is_open:
            continue

        filtered.append(restaurant)

    return filtered

"""
Pleci de la o listă goală filtered = []
Parcurgi fiecare restaurant cu for r in restaurants
Dacă nu trece filtrul → continue
Dacă trece toate filtrele → îl adaugi în listă
"""