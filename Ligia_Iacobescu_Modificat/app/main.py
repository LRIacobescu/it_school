from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import OperationalError
from app.ui import router
from config.settings import settings
from database import Base, engine
import database.models  # noqa: F401

try:
    # Tabelele se verifica si la pornire ca sa nu depindem de o comanda separata dupa prima configurare.
    Base.metadata.create_all(bind=engine)
except OperationalError as exc:
    raise RuntimeError(
        "Nu m am putut conecta la PostgreSQL. Verifica fisierul .env si ruleaza "
        "python -m database.setup_db o singura data pentru setup."
    ) from exc

app = FastAPI(
    title="PDF Data Explorer",
    description="Upload PDF, detectare tabele si filtrare dinamica a datelor.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
