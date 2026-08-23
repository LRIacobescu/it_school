from database.repository import DatabaseRepository
from database.session import engine
from database.models import Base
from datetime import datetime


def test_database_crud_operations():
    """
    Test complet pentru DatabaseRepository:
    - create tables
    - insert parcel
    - read parcel
    - update parcel
    - delete parcel
    """

    # 1. Creăm tabelele dacă nu există
    Base.metadata.create_all(bind=engine)

    repo = DatabaseRepository()

    # 2. Parcel de test
    parcel_data = {
        "parcel_id": "999-9999-999",
        "owner_name": "TEST OWNER",
        "owner_street": "123 TEST STREET",
        "city": "TEST CITY",
        "state": "WI",
        "prop_address_1": "123 TEST STREET",
        "prop_address_2": "",
        "section": "33",
        "prop_acres": 0.25,
        "district_1": "TEST DISTRICT 1",
        "district_2": "TEST DISTRICT 2",
        "district_3": "TEST DISTRICT 3",
        "class_value": "G1",
        "acres": 0.25,
        "land": "$10,000",
        "impts": "$0",
        "total": "$10,000",
        "created_at": datetime.utcnow()
    }

    # 3. Insert
    inserted_id = repo.save_parcel(parcel_data)
    assert isinstance(inserted_id, int)

    # 4. Read
    saved = repo.get_by_id(inserted_id)
    assert saved is not None
    assert saved.parcel_id == parcel_data["parcel_id"]
    assert saved.owner_name == parcel_data["owner_name"]
    assert saved.city == parcel_data["city"]
    assert saved.state == parcel_data["state"]
    assert saved.prop_acres == parcel_data["prop_acres"]
    assert saved.total == parcel_data["total"]

    # 5. Update (optional)
    repo.update(inserted_id, {"owner_name": "UPDATED OWNER"})
    updated = repo.get_by_id(inserted_id)
    assert updated.owner_name == "UPDATED OWNER"

    # 6. Delete
    repo.delete(inserted_id)
    assert repo.get_by_id(inserted_id) is None
