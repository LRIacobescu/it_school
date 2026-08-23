from fastapi import FastAPI
from routers import products
from routers import categories
from routers import restaurants

app = FastAPI(title = "Aplicatie IT School")

app.include_router(products.router)
app.include_router(categories.router)
app.include_router(restaurants.router)

@app.get("/", tags = ["General"])
def home():
    return {
        "message": "Salut din Food Delivery API!"
    }

@app.get("/status", tags = ["General"])
def get_status():
    return {
        "app": "Food Delivery API",
        "status": "running",
        "version": "1.0.0"
    }

"""
Conectare router pentru categorii
"""