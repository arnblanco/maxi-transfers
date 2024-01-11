import pytest
from fastapi.testclient import TestClient
from app.request import CreateBeneficiaryRequest
from app.response import BeneficiaryResponse
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

# Datos de prueba para CreateBeneficiaryRequest
beneficiary_data = {
    "employee_id": 15001,
    "first_name": "BeneficiaryFirstName",
    "last_name": "BeneficiaryLastName",
    "birthday": "1990-01-01",
    "curp": "BeneficiaryCURP123",
    "ssn": "BeneficiarySSN",
    "phone": "1234567890",
    "nationality": "BeneficiaryNationality",
    "percentage": 50,
}

# Prueba de crear un empleado
def test_create_employee():
    response = client.post("/employee", json=employee_data, headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert response.json()["employee_id"] == employee_data["employee_id"]

# Prueba de crear un beneficiario
def test_create_beneficiary():
    response = client.post("/beneficiary", json=beneficiary_data, headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert response.json()["employee_id"] == beneficiary_data["employee_id"]

# Prueba de obtener un beneficiario por CURP y ID de empleado
def test_get_beneficiary_by_curp():
    response = client.get("/beneficiary/15001/BeneficiaryCURP123", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert response.json()["curp"] == "BeneficiaryCURP123"

# Prueba de actualizar un beneficiario
def test_update_beneficiary():
    updated_data = {**beneficiary_data, "first_name": "UpdatedBeneficiaryFirstName"}
    response = client.patch("/beneficiary", json=updated_data, headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert response.json()["first_name"] == "UpdatedBeneficiaryFirstName"

# Prueba de obtener todos los beneficiarios de un empleado
def test_get_employee_beneficiaries():
    response = client.get("/employee/15001/beneficiaries", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Prueba de obtener un beneficiario inexistente por CURP y ID de empleado
def test_get_nonexistent_beneficiary_by_curp():
    response = client.get("/beneficiary/15001/NonexistentCURP", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 404  # Not Found

# Prueba de eliminar un beneficiario
def test_delete_beneficiary():
    response = client.delete("/beneficiary/15001/BeneficiaryCURP123456", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert response.json() == {}
    
# Prueba de eliminar un empleado por ID
def test_delete_employee_by_id():
    response = client.delete("/employee/15001", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert response.json() == {}