
from fastapi import FastAPI
from pydantic import BaseModel


"""
1. Adauga camp nou in modelul produsului:description
    Descrierea nu trebuie sa fie obligatorie, valoarea implicita va fi un text gol
2. Creeaza modelul CourierCreate pentru curieri
- first_name
- last_name
- phone
- active (implicit True)
3. Creeaza POST /couriers
4. Creeaza modelul pt category
    - nume - text. min 2 caractere
5. Creeaza endpointul POST /categories
6. Verifica categoriile duplicate. Daca exista, returneaza mesaj
"""

#1.

class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str
    available: bool
    description: str = ""

#2.

class CourierCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    active: bool = True

couriers = [
    { "id": 1, "first_name": "Mihai", "last_name": "Popescu", "phone": "0712345678", "active": True },
    { "id": 2, "first_name": "Andrei", "last_name": "Ionescu", "phone": "0723456789", "active": False },
    { "id": 3, "first_name": "Alex", "last_name": "Dumitrescu", "phone": "0734567890", "active": True }
]

#3.

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

#4.

class CategoryCreate(BaseModel):
    name: str = Field(min_length = 2)

#5.

@app.post("/categories", status_code = 201)
def create_category(category: CategoryCreate):
    new_category = {
        "id": len(categories) + 1,
        "name": category.name
    }
    categories.append(new_category)

    return new_category

#6.

@app.post("/categories", status_code = 201)
def create_category(category: CategoryCreate):
    # verificare duplicate
    for category in categories:
        if category["name"].lower() == category.name.lower():
            return {"error": "Categoria exista deja"}

    new_id = len(categories) + 1
    new_category = {
        "id": new_id,
        "name": category.name
    }
    categories.append(new_category)

    return new_category
