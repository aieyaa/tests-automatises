import pytest
from app.database import Database


@pytest.fixture
def database():
    """
    Fixture pytest :
    - crée une base propre avant chaque test
    - garantit qu’aucun test n’influence un autre
    """
    db = Database(":memory:")
    db.connect()
    yield db
    db.disconnect()


def test_add_user(database):
    user = {
        "username": "test_user",
        "email": "test@example.com"
    }

    database.add_user(user["username"], user["email"])
    
    retrieved_user = database.get_user("test_user")
    assert retrieved_user is not None
    assert retrieved_user["username"] == "test_user"


def test_get_user(database):
    user = {
        "username": "john",
        "email": "john@example.com"
    }

    database.add_user(user["username"], user["email"])
    retrieved_user = database.get_user("john")

    assert retrieved_user is not None
    assert retrieved_user["email"] == "john@example.com"


def test_get_user_not_found(database):
    retrieved_user = database.get_user("unknown")
    assert retrieved_user is None


def test_delete_user(database):
    user = {
        "username": "alice",
        "email": "alice@example.com"
    }

    database.add_user(user["username"], user["email"])
    database.delete_user("alice")

    assert database.get_user("alice") is None
