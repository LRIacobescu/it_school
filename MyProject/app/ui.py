from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database.repository import DatabaseRepository

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

repo = DatabaseRepository()


# Pagina principală: listă parcele

@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    parcels = repo.get_all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "parcels": parcels}
    )


# Pagina detalii parcel

@router.get("/parcel/{parcel_id}", response_class=HTMLResponse)
def parcel_detail(request: Request, parcel_id: int):
    parcel = repo.get_by_id(parcel_id)
    if not parcel:
        return HTMLResponse("<h1>Parcel not found</h1>", status_code=404)

    return templates.TemplateResponse(
        "parcel_detail.html",
        {"request": request, "parcel": parcel}
    )
