import psycopg
from psycopg import sql
from config.settings import settings


def create_database_if_missing():
    # Intram mai intai pe db ul postgres ca sa putem crea db ul aplicatiei.
    with psycopg.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        dbname="postgres",
        user=settings.DB_USER,
        password=settings.DB_PASS,
        autocommit=True,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (settings.DB_NAME,),
            )

            if cursor.fetchone():
                print("DB ul exista deja: " + settings.DB_NAME)
                return

            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(settings.DB_NAME))
            )
            print("Am creat db ul: " + settings.DB_NAME)


def create_tables():
    # Importurile sunt aici ca sa cream db ul inainte sa deschidem conexiunea aplicatiei.
    from database import Base, engine
    import database.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    print("Tabelele sunt gata.")


def setup_db():
    create_database_if_missing()
    create_tables()


if __name__ == "__main__":
    setup_db()
