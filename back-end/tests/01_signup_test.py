import pytest
from fastapi.testclient import TestClient
from app.request import CreateUserRequestSchema
from server import app


# Configuración de cliente de prueba
client = TestClient(app)

# Datos de prueba para CreateUserRequestSchema
user_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "username": "johndoe",
    "password": "secretpassword",
}

# Prueba de registro exitoso
def test_signup_success():
    response = client.post("/auth/signup", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"]


# Prueba de registro con datos faltantes
def test_signup_missing_data():
    invalid_user_data = {key: value for key, value in user_data.items() if key != "password"}
    response = client.post("/auth/signup", json=invalid_user_data)
    assert response.status_code == 422  # 422 Unprocessable Entity


# Prueba de registro con nombre de usuario duplicado
def test_signup_duplicate_username():
    # Registro del mismo usuario dos veces
    client.post("/auth/signup", json=user_data)
    response = client.post("/auth/signup", json=user_data)
    assert response.status_code == 404  # 404 Bad Request
