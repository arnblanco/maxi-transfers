from passlib.context import CryptContext
from sqlalchemy import text
from typing import List

from app.response import EmployeeResponse
from core.config import connect
from core.exceptions import DatabaseSQLErrorException, EmployeeNotFoundException, EmployeeDuplicatedException


class EmployeeService:
    def __init__(self):
        ...

    async def format_employee(self, employee)-> EmployeeResponse:
        return EmployeeResponse(
            first_name=employee[0],
            last_name=employee[1],
            birthday=employee[2],
            employee_id=employee[3],
            curp=employee[4],
            ssn=employee[5],
            phone=employee[6],
            nationality=employee[7],
            beneficiary_count=employee[8]
        )

    async def get_employee_by_id(self, employee_id: int, format: bool = True) -> EmployeeResponse:
        try:
            with connect() as conn:
                result = conn.execute(
                    text("EXEC GetEmployeeById :employee_id"),
                    {"employee_id": employee_id}
                )

                employee = result.fetchone()

                if format:
                    if not employee:
                        raise EmployeeNotFoundException
                    
                    return await self.format_employee(employee)
                else:
                    return employee
        except Exception as e:
            raise DatabaseSQLErrorException
                
    async def get_employee_list(self) -> List[EmployeeResponse]:
        with connect() as conn:
            result = conn.execute(
                text("EXEC GetEmployees")
            )
            employees = result.fetchall()
            return [await self.format_employee(employee) for employee in employees]
    
    async def create_employee(self, req)-> EmployeeResponse:
        try:
            verify_employee = await self.get_employee_by_id(req.employee_id, False)

            if verify_employee:
                raise EmployeeDuplicatedException

            with connect() as conn:
                result = conn.execute(
                    text("EXEC InsertEmployee :first_name, :last_name, :birthday, :employee_id, :curp, :ssn, :phone, :nationality"),
                    {
                        "first_name": req.first_name,
                        "last_name": req.last_name,
                        "birthday": req.birthday,
                        "employee_id": req.employee_id,
                        "curp": req.curp,
                        "ssn": req.ssn,
                        "phone": req.phone,
                        "nationality": req.nationality
                    }
                )
                conn.commit()
                
                return await self.get_employee_by_id(req.employee_id)
        except Exception as e:
            raise DatabaseSQLErrorException

    async def update_employee(self, employee_id, req)-> EmployeeResponse:
        try:
            with connect() as conn:
                result = conn.execute(
                    text("EXEC UpdateEmployee :employee_id, :first_name, :last_name, :birthday, :curp, :ssn, :phone, :nationality"),
                    {
                        "employee_id": employee_id,
                        "first_name": req.first_name,
                        "last_name": req.last_name,
                        "birthday": req.birthday,
                        "curp": req.curp,
                        "ssn": req.ssn,
                        "phone": req.phone,
                        "nationality": req.nationality
                    }
                )
                conn.commit()
                
                return await self.get_employee_by_id(employee_id)
        except Exception as e:
            raise DatabaseSQLErrorException

    async def delete_employee(self, employee_id):
        try:
            verify_employee = await self.get_employee_by_id(employee_id)

            with connect() as conn:
                result = conn.execute(
                    text("EXEC DeleteEmployee :employee_id"),
                    {"employee_id": employee_id}
                )
                conn.commit()
                
                return {}
        except Exception as e:
            raise DatabaseSQLErrorException