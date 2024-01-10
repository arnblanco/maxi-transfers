from passlib.context import CryptContext
from sqlalchemy import text
from typing import List

from app.response import BeneficiaryResponse
from core.config import connect
from core.exceptions import DatabaseSQLErrorException, BeneficiaryNotFoundException, \
    EmployeeNotFoundException, BeneficiaryDuplicatedException
from services import EmployeeService

class BeneficiaryService:
    def __init__(self):
        ...

    async def format_beneficiary(self, beneficiary)-> BeneficiaryResponse:
        return BeneficiaryResponse(
            first_name=beneficiary[0],
            last_name=beneficiary[1],
            birthday=beneficiary[2],
            curp=beneficiary[3],
            ssn=beneficiary[4],
            phone=beneficiary[5],
            nationality=beneficiary[6],
            percentage=beneficiary[7],
        )

    async def get_beneficiary_by_curp(self, curp, employee_id, format: bool = True)-> BeneficiaryResponse:
        try:
            with connect() as conn:
                result = conn.execute(
                    text("EXEC GetBeneficiary :curp, :employee_id"),
                    {"curp": curp, "employee_id": employee_id}
                )
                beneficiary = result.fetchone()

                if format:
                    if not beneficiary:
                        raise BeneficiaryNotFoundException
                    
                    return await self.format_beneficiary(beneficiary)
                else:
                    return beneficiary
        except Exception as error:
            raise DatabaseSQLErrorException

    async def create_beneficiary(self, req)-> BeneficiaryResponse:
        try:
            employee = await EmployeeService().get_employee_by_id(req.employee_id)

            beneficiary = await self.get_beneficiary_by_curp(req.curp, req.employee_id, False)

            if beneficiary:
                raise BeneficiaryDuplicatedException

            with connect() as conn:
                result = conn.execute(
                    text("EXEC InsertBeneficiary :first_name, :last_name, :birthday, :curp, :ssn, :phone, :nationality, :percentage, :employee_id"),
                    {
                        "first_name": req.first_name,
                        "last_name": req.last_name,
                        "birthday": req.birthday,
                        "curp": req.curp,
                        "ssn": req.ssn,
                        "phone": req.phone,
                        "nationality": req.nationality,
                        "percentage": req.percentage,
                        "employee_id": req.employee_id,
                    },
                )
                conn.commit()

                return await self.get_beneficiary_by_curp(req.curp, req.employee_id)
        except Exception as error:
            raise DatabaseSQLErrorException

    async def update_beneficiary(self, req)-> BeneficiaryResponse:
        try:
            beneficiary = await self.get_beneficiary_by_curp(req.curp, req.employee_id)

            with connect() as conn:
                result = conn.execute(
                    text(
                        "EXEC UpdateBeneficiary :first_name, :last_name, :birthday, :curp, :ssn, :phone, :nationality, :percentage, :employee_id"
                    ),
                    {
                        "first_name": req.first_name,
                        "last_name": req.last_name,
                        "birthday": req.birthday,
                        "curp": req.curp,
                        "ssn": req.ssn,
                        "phone": req.phone,
                        "nationality": req.nationality,
                        "percentage": req.percentage,
                        "employee_id": req.employee_id,
                    },
                )
                conn.commit()

                return await self.get_beneficiary_by_curp(req.curp, req.employee_id)
        except Exception as error:
            raise DatabaseSQLErrorException

    async def delete_beneficiary(self, req):
        try:
            beneficiary = await self.get_beneficiary_by_curp(req.curp, req.employee_id)
            
            with connect() as conn:
                result = conn.execute(
                    text("EXEC DeleteBeneficiary :employee_id, :curp"),
                    {"employee_id": req.employee_id, "curp": req.curp},
                )
                conn.commit()

                return {}
        except Exception as error:
            raise DatabaseSQLErrorException

    async def get_employee_beneficiaries(self, employee_id)-> List[BeneficiaryResponse]:
        try:
            with connect() as conn:
                result = conn.execute(
                    text("EXEC GetBeneficiariesByEmployeeId :employee_id"),
                    {"employee_id": employee_id},
                )
                beneficiaries = result.fetchall()
                
                return [await self.format_beneficiary(beneficiary) for beneficiary in beneficiaries]
        except Exception as error:
            raise DatabaseSQLErrorException