from datetime import date
from pydantic import BaseModel, EmailStr, Field, conint, constr


class CreateUserRequestSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class CreateEmployeeRequest(BaseModel):
    first_name: constr(min_length=3, max_length=50) = Field(..., description="Employee First Name")
    last_name: constr(min_length=3, max_length=50) = Field(..., description="Employee Last Name")
    birthday: str = Field(..., description="Employee Birthday")
    employee_id: int = Field(..., description="Employee Number")
    curp: constr(min_length=18, max_length=18) = Field(..., description="Employee CURP.")
    ssn: constr(min_length=6, max_length=12) = Field(..., description="Employee SSN.")
    phone: constr(min_length=10, max_length=10) = Field(..., description="Employee Phone Number.")
    nationality: str = Field(..., description="Employee Nationality.")

    @property
    def is_adult(self):
        min_adult_age = 18
        min_birthdate = date.today().replace(year=date.today().year - min_adult_age)

        return self.birthday <= min_birthdate

    @classmethod
    def validate_birthday(cls, value):
        if not cls(is_adult=False, birthday=value).is_adult:
            raise ValueError("El empleado debe ser mayor de edad.")

        return value

class UpdateEmployeeRequest(BaseModel):
    first_name: constr(min_length=3, max_length=50) = Field(..., description="Employee First Name")
    last_name: constr(min_length=3, max_length=50) = Field(..., description="Employee Last Name")
    birthday: str = Field(..., description="Employee Birthday")
    curp: constr(min_length=18, max_length=18) = Field(..., description="Employee CURP.")
    ssn: constr(min_length=6, max_length=12) = Field(..., description="Employee SSN.")
    phone: constr(min_length=10, max_length=10) = Field(..., description="Employee Phone Number.")
    nationality: str = Field(..., description="Employee Nationality.")

    @property
    def is_adult(self):
        min_adult_age = 18
        min_birthdate = date.today().replace(year=date.today().year - min_adult_age)

        return self.birthday <= min_birthdate

    @classmethod
    def validate_birthday(cls, value):
        if not cls(is_adult=False, birthday=value).is_adult:
            raise ValueError("El empleado debe ser mayor de edad.")

        return value


class CreateBeneficiaryRequest(BaseModel):
    employee_id: int
    first_name: constr(min_length=3, max_length=50) = Field(..., description="Beneficiary First Name")
    last_name: constr(min_length=3, max_length=50) = Field(..., description="Beneficiary Last Name")
    birthday: str = Field(..., description="Beneficiary Birthday")
    curp: constr(min_length=18, max_length=18) = Field(..., description="Beneficiary CURP.")
    ssn: constr(min_length=6, max_length=12) = Field(..., description="Beneficiary SSN.")
    phone: constr(min_length=10, max_length=10) = Field(..., description="Beneficiary Phone Number.")
    nationality: str = Field(..., description="Beneficiary Nationality.")
    percentage: conint(ge=1, le=100) = Field(..., description="Beneficiary Percent.")

    @property
    def is_adult(self):
        min_adult_age = 18
        min_birthdate = date.today().replace(year=date.today().year - min_adult_age)

        return self.birthday <= min_birthdate

    @classmethod
    def validate_birthday(cls, value):
        if not cls(is_adult=False, birthday=value).is_adult:
            raise ValueError("El empleado debe ser mayor de edad.")

        return value


class DeleteBeneficiaryRequest(BaseModel):
    employee_id: int
    curp: constr(min_length=18, max_length=18) = Field(..., description="Beneficiary CURP.")