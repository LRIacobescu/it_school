from database import Base, engine
import database.models  # noqa: F401

Base.metadata.create_all(bind=engine)
print("Tabele create/verificate cu succes.")
