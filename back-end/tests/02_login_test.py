import pytest
from fastapi.testclient import TestClient
from app.request import CreateUserRequestSchema, LoginRequest
from app.response import LoginResponse
from server import app

# Configuración de cliente de prueba
client = TestClient(app)

# Datos de prueba para LoginRequest
login_data = {
    "username": "johndoe",
    "password": "secretpassword",
}

# Prueba de registro y luego inicio de sesión exitoso
def test_login_success():
    # Inicio de sesión con el usuario registrado
    response_login = client.post("/auth/login", json=login_data)
    assert response_login.status_code == 200
    assert "access_token" in response_login.json()
    assert "refresh_token" in response_login.json()

# Prueba de inicio de sesión con credenciales incorrectas
def test_login_wrong_credentials():
    wrong_login_data = {**login_data, "password": "wrongpassword"}
    response = client.post("/auth/login", json=wrong_login_data)
    assert response.status_code == 404  # Not Found

# Prueba de inicio de sesión con usuario no registrado
def test_login_user_not_found():
    non_existent_login_data = {**login_data, "username": "nonexistentuser"}
    response = client.post("/auth/login", json=non_existent_login_data)
    assert response.status_code == 404  # Not Found
