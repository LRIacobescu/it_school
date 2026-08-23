from database import Base, engine
import database.models  # noqa: F401 - incarca modelele in metadata


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
