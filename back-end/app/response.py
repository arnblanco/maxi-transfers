from datetime import date
from pydantic import BaseModel, EmailStr, Field, conint, constr


class CreateUserResponseSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    is_active: bool


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class EmployeeResponse(BaseModel):
    first_name: str
    last_name: str
    birthday: str
    employee_id: int
    curp: constr(max_length=18)
    ssn: constr(max_length=10)
    phone: constr(max_length=10)
    nationality: str
    beneficiary_count: int


class BeneficiaryResponse(BaseModel):
    first_name: str
    last_name: str
    birthday: str
    curp: constr(max_length=18)
    ssn: constr(max_length=10)
    phone: constr(max_length=10)
    nationality: str
    percentage: int