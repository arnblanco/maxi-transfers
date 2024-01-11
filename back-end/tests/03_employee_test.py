import pytest
from fastapi.testclient import TestClient
from app.request import CreateEmployeeRequest
from app.response import EmployeeResponse
from dateutil import parser
from server import app

# Configuración de cliente de prueba
client = TestClient(app)

# Datos de prueba para LoginRequest
test_token = ''
login_data = {
    "username": "johndoe",
    "password": "secretpassword",
}

# Prueba de registro y luego inicio de sesión exitoso
def test_login_success():
    global test_token

    # Inicio de sesión con el usuario registrado
    response_login = client.post("/auth/login", json=login_data)
    assert response_login.status_code == 200
    assert "access_token" in response_login.json()
    assert "refresh_token" in response_login.json()

    test_token = response_login.json()["access_token"]

# Datos de prueba para CreateEmployeeRequest
employee_data = {
    "first_name": "TestFirstName",
    "last_name": "TestLastName",
    "birthday": "1990-01-01",
    "employee_id": 15001,
    "curp": "ABCDEFGHI123456789",
    "ssn": "TestSSN123",
    "phone": "1234567890",
    "nationality": "TestNationality",
}

# Prueba de crear un empleado
def test_create_employee():
    response = client.post("/employee", json=employee_data, headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert response.json()["employee_id"] == employee_data["employee_id"]

# Prueba de obtener un empleado por ID
def test_get_employee_by_id():
    response = client.get("/employee/15001", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert response.json()["employee_id"] == 15001

# Prueba de actualizar un empleado por ID
def test_update_employee_by_id():
    updated_data = {**employee_data, "first_name": "UpdatedFirstName"}
    response = client.patch("/employee/15001", json=updated_data, headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert response.json()["first_name"] == "UpdatedFirstName"

# Prueba de crear un empleado con datos faltantes
def test_create_employee_missing_data():
    invalid_employee_data = {key: value for key, value in employee_data.items() if key != "employee_id"}
    response = client.post("/employee", json=invalid_employee_data, headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 422  # Unprocessable Entity

# Prueba de crear un empleado con ID duplicado
def test_create_employee_duplicate_id():
    client.post("/employee", json=employee_data)  # Crear el empleado inicialmente
    response = client.post("/employee", json=employee_data, headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 404  # Not Found

# Prueba de eliminar un empleado por ID
def test_delete_employee_by_id():
    response = client.delete("/employee/15001", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert response.json() == {}