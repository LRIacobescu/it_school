"""
1. ce este un API
2. diferenta intre client si server
3. ce este un request
4. ce este un response
5. ce este un endpoint
6. start proiect FastAPI
7. creare endpointuri cu GET
8. returnare date in format JSON
9. testare API in browser si Swagger UI
"""


# Backend -> primeste cereri, proceseaza date, comunica cu DB si trimite raspunsuri inapoi

# Ce este o functie? -> O bucata de cod reutilizabila care face o anumita actiune
# Ce poate returna o functie? -> un text, un intreg, o lista, un dictionar etc
# Ce este un dictionar? -> Un tip de date care tine informatii in perechi cheie-valoare
# Ce este JSON? -> Un format de date foarte folosit in web apps; seamana mult cu dictionarele si listele in python

# Un endpoint FastAPI este o functie python apelabila din browser, mobile app sau frontend
def get_product():
    return {
        "name": "Pizza",
        "price": 35
    }


# In FastAPI, functia aceasta poate deveni o adresa web: GET /product; cand intram in browser pe adresa respectiva, primim datele

""""
Ce este FaspAPI?
- Framework python folosit pentru construirea de API uri
- Framework -> set de reguli si functii care ne ajuta sa construim aplicatii mei repede

Cu FastAPI poti face endpoint-uri de genul:
- GET /products
- POST /orders
- PUT /products/1
- DELETE /products/3

Ce este un API?
- Application Programming Interface
- O modalitate prin care doua aplicatii comunica intre ele

Analogie restaurant
1. Clientul nu intra in bucatarie sa isi faca mancarea
2. Clientul vorbeste cu ospatarul si spune: Vreau o pizza
3. Ospatarul duce cererea la bucatarie
4. Bucataria pregateste mancarea
5. Ospatarul aduce raspunsul inapoi

Clientul = browser
Osparatul = API-ul
Bucataria = backend + DB + logica aplicatiei

Clientul este cel care trimite cererea: browser, mobile app, Postman, Swagger UI etc
Serverul este aplicatia care primeste cereri si trimite raspunsuri -> serverul va fi aplicatia de FastAPI
Ex: clientul cere GET /products -> Serverul raspunde "lista produse"

Ce este un request? 
- Cand un client vrea ceva de la server, el va trimite un request
Ex: 
    - Vreau toate produsele
    - Vreau produsul cu id 3
    - Vreau toate restaurantele deschise
    - Vreau sa creez o comanda
In aplicatii web, cererile acestea sunt trimise prin HTTP

Ce este un response?
- Serverul primeste request-ul, executa logica si trimite inapoi un response

Ce este HTTP?
- protocolul prin care clientul si serverul comunica
- are:
    - metode
    - rute / endpoint uri
    - status codes
    - request body
    - response body

Metode HTTP:
- GET -> citire date
- POST -> creare date
- PUT -> modificare completa
- PATCH -> modificare partiala
- DELETE -> stergere date

GET 
- Folosit cand vrem sa citim date
GET /products
GET /restaurant
GET /orders

POST
- Cand vrem sa cream date
POST /products
POST /orders
POST /customers

PUT 
- Cand vrem sa inlocuim complet o resursa
PUT /products/1 -> modificam complet produsul cu ID 1

PATCH
- Cand vrem sa modificam doar o parte din resursa
PATCH /orders/5/status -> modificam doar statusul comenzii 5

DELETE 
- Cand vrem sa stergem ceva
DELETE /products/3

Ce este un endpoint?
- O adresa din API
Exemple:
    - /
    - /status
    - /products
    - /restaurant
    - /orders
O usa prin care clientul cere ceva de la server

Ce este JSON in API
- cel mai des datele sunt trimise in format JSON
- FastAPI face automat conversia din dictionar in JSON
"""

"""
1. instalare fastapi:
pip install "fastapi[standard]"

2. Mediu virtual:
windows:
python -m venv venv
venv/Scripts/activate

macos
python3 -m venv venv
source venv/bin/activate

3. Ca sa rulam aplicatia:
- Rulam in terminal: fastapi dev main_s29.py
"""

"""
1. Nu uitati sa porniti serverul
fastapi dev nume_fisier.py

2. Nu uitati de slash la rute/endpoint uri
@app.get("/products")

3. Nu duplicati functiile
@app.get("products")
def get_data(): -> mai bine get_products
    ...
    
@app.get("/restaurants")
def get_data(): -> mai bine get_restaurants
    ...
    
*** CTRL + C ca sa opriti serverul ***
"""



