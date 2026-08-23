"""
1. GET vs POST
2. request body
3. trimiere date JSON catre FastAPI
4. Pydantic
5. BaseModel
6. date obligatorii vs date cu valori implicite
7. creare elemente noi in liste
8. generare automata id
9. testare POST
10. erori de validare generate automat

POST -> creeaza un produs nou
- POST /products

Diferente:
    GET:
        - citeste date
        - nu creeaza ceva nou
        - parametrii pot veni din URL
    POST:
        - creeaza date
        - trimite info catre server
        - date vin de obicei in request body

request body -> partea dntr-un request in care trimitem datele catre server

ex:
{
name
price: nu stiu
category
available
}

3 locuri din care putem primi date
- 1. path -> inclus in ruta (/products/3)
- 2. query -> trimis dupa semnul ?
- 3. body -> obiect JSON trimis catre server

Pydantic -> biblioteca pentru validarea datelor. Ne permite sa descriem cum trebuie sa arate datele primite
- un produs trebuie sa aiba
1. name - text
2. price - numar
3. category - text
4. available - true/false

from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    category: str
    available: bool

Pydantic creeaza n obiect de tip ProductCreate si putem accesa datele folosind atribute
product.name
product.price
product.category
product.available

Camp obligatoriu
name: str

clientul trebuie sa trimita name, altfel primeste eroare

Camp cu valoare implicita
available: bool = True

daca userul nu trimite available, valoare e automat True

class Productcreate(BaseModel):
    name: str
    price: float
    category: str
    available: bool = True

Clientul poate trimite:
{
"name": "Pizza ...",
"price": 50,
"category": "pizza"
}

Field -> tipurile de date verifica daca o valoare e text, bool etc
Field ofera reguli suplimentare
ex:
- pretul trebuie sa fie > 0
- numele produsului sa aibe minim 2 caractere
...

class Productcreate(BaseModel):
    name: str = Field(min_length = 2)
    price: float = Field(gt = 0)
    category: str = Field(min_length = 2)
    available: bool = True
"""