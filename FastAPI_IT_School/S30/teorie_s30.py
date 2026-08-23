# Path Parameters & Query parameters

"""
Obiective:
1. Path parameter
2. query parameter
3. creare endpoint uri dinamice dupa id
4. filtru liste dictionare pe baza parametrilor
5. sa intelegem cum fastapi converteste automat datele din URL
6. folosire parametri tip int, str, bool, float
7. testare endpoint uri

endpoint uri simple sesiunea 29:
- GET /
- GET /status
- GET /available-products
...

in loc de
- GET /products

avem si
- GET /products/1
- GET /restaurants/2
- GET /products?category=pizza
...

endpoint uri statice
- /products/1
- /products/2

@app.get("/products/1")
def get_products_1():
    return products[0]

Path parameter
- O valoare care face parte din ruta
Ex:
- /products/1 -> 1 este path parameter

In FastAPI scriem path parameter intre acolade

@app.get("/products/{product_id}") -> Orice valoare apare dupa /products/ va fi pusa in variabila product_id

Ex:
@app.get("/products/{product_id}")
def get_product(product_id: int): -> type hint
    return {
        "product_id": product_id
    }

Query parameter
- Este o valoare trimisa dupa semnul ? in URL
Ex:
- /products?category=pizza

Path parameter -> folosit de obicei cand vrem o resursa clara, identificata prin id
- /products/1 -? da-mi produsul cu id 1

Query parameter -? Folosit pentru filtrare, cautare. sortare etc
- /products?category=pizza -> da-mi produsele din categoria pizza
"""