import pytest
import os
import tempfile
from app import create_app  # ✅ Import correct

def test_config():
    """Test create_app without config."""
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing

def test_index(client):
    """Test index route."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"L'application fonctionne" in response.data

@pytest.fixture
def client():
    # Create a temporary file for the database
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({"DATABASE": db_path, "TESTING": True})
    
    with app.test_client() as client:
        yield client
        
    # Cleanup
    os.close(db_fd)
    os.remove(db_path)


# 🔢 Tests API calculatrice

def test_api_status(client):
    response = client.get("/api/test")
    assert response.status_code == 200
    assert response.get_json() == {'status': 'API fonctionne correctement'}

def test_api_add(client, mocker):
    # Mock the calculator.add method
    mock_add = mocker.patch('app.api.calculator.add')

    mock_add.return_value = 10  # Force a specific return value to prove mock is used and send
    
    response = client.get("/api/add/2/3") 
    
    assert response.status_code == 200
    assert response.get_json() == {"result": 10}
    mock_add.assert_called_once_with(2.0, 3.0)


def test_api_add_invalid_input(client):
    response = client.get("/api/add/two/three")
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Les paramètres doivent être des nombres'}


def test_api_subtract(client):
    response = client.get("/api/subtract/5/3")
    assert response.status_code == 200
    assert response.get_json() == {"result": 2}


def test_api_subtract_invalid_input(client):
    response = client.get("/api/subtract/five/three")
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Les paramètres doivent être des nombres'}


def test_api_multiply(client):
    response = client.get("/api/multiply/2/3")
    assert response.status_code == 200
    assert response.get_json() == {"result": 6}


def test_api_multiply_invalid_input(client):
    response = client.get("/api/multiply/two/three")
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Les paramètres doivent être des nombres'}


def test_api_divide(client):
    response = client.get("/api/divide/6/3")
    assert response.status_code == 200
    assert response.get_json() == {"result": 2}


def test_api_divide_invalid_input(client):
    response = client.get("/api/divide/ten/two")
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Les paramètres doivent être des nombres'}
    

def test_api_divide_by_zero(client):
    response = client.get("/api/divide/5/0")
    assert response.status_code == 400


# 👤 Tests API utilisateurs

def test_create_user(client):
    response = client.post(
        "/api/user",
        json={"username": "test_user", "email": "user@example.com"}
    )
    assert response.status_code == 201
    # L'API actuelle ne renvoie pas 'username' dans la réponse, seulement 'message'
    # Donc il vaut mieux vérifier le message
    assert response.get_json()["message"] == "Utilisateur ajouté avec succès"


def test_create_user_missing_fields(client):
    response = client.post(
        "/api/user",
        json={"username": "incomplete"}
    )
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_user_duplicate(client):
    client.post(
        "/api/user",
        json={"username": "duplicate", "email": "dup@example.com"}
    )
    response = client.post(
        "/api/user",
        json={"username": "duplicate", "email": "dup@example.com"}
    )
    assert response.status_code == 409
    assert "error" in response.get_json()


def test_get_user(client, mocker):
    # Mock the global db variable in app.api directly
    # This prevents before_request from initializing a real database
    mock_db = mocker.patch('app.api.db')
    
    # Configure the mock response
    mock_db.get_user.return_value = {"username": "john", "email": "mocked@example.com"}
    
    response = client.get("/api/user/john")
    
    assert response.status_code == 200
    assert response.get_json()["email"] == "mocked@example.com"
    mock_db.get_user.assert_called_once_with("john")


def test_get_user_not_found(client):
    response = client.get("/api/user/unknown_user")
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_delete_user(client):
    client.post(
        "/api/user",
        json={"username": "alice", "email": "alice@example.com"}
    )

    response = client.delete("/api/user/alice")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Utilisateur supprimé avec succès"


def test_delete_user_not_found(client):
    response = client.delete("/api/user/unknown_user")
    assert response.status_code == 404
    assert "error" in response.get_json()
