from dateutil import parser
from fastapi import APIRouter, Depends, FastAPI, Header, Request, Response
from fastapi.responses import JSONResponse
from typing import List

from app.request import CreateUserRequestSchema, LoginRequest, CreateEmployeeRequest, \
    UpdateEmployeeRequest, CreateBeneficiaryRequest, DeleteBeneficiaryRequest, getBeneficiaryRequest
from app.response import CreateUserResponseSchema, LoginResponse, EmployeeResponse, \
    BeneficiaryResponse
from core import create_app
from core.exceptions import UserNotFoundException
from core.permission import PermissionDependency, IsAuthenticated
from services import UserService, EmployeeService, BeneficiaryService


#Start FastApi application
app = create_app()


@app.get('/')
def index(request: Request): 
    engine = connect()

    return JSONResponse(content={ "msg": f"Welcome to MaxiTransfers Api!" })


@app.post(
    "/auth/login",
    response_model=LoginResponse
)
async def login(
    request: LoginRequest,
    service: UserService = Depends(UserService)
):
    return await service.verify_login(request)


@app.post(
    "/auth/signup",
    response_model=CreateUserResponseSchema
)
async def signup(
    request: CreateUserRequestSchema,
    service: UserService = Depends(UserService)
):
    return await service.create_user(request)


@app.get(
    "/employee",
    response_model=List[EmployeeResponse],
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_employee(
    request: Request,
    service: EmployeeService = Depends(EmployeeService)
):
    return await service.get_employee_list()


@app.post(
    "/employee",
    response_model=EmployeeResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def post_employee(
    request: CreateEmployeeRequest,
    service: EmployeeService = Depends(EmployeeService)
):
    request.birthday = parser.parse(request.birthday)
    return await service.create_employee(request)

@app.get(
    "/employee/{employee_id}",
    response_model=EmployeeResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_employee(
    employee_id: int,
    service: EmployeeService = Depends(EmployeeService)
):
    return await service.get_employee_by_id(employee_id)

@app.patch(
    "/employee/{employee_id}",
    response_model=EmployeeResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def edit_employee(
    employee_id: int,
    request: UpdateEmployeeRequest,
    service: EmployeeService = Depends(EmployeeService)
):
    return await service.update_employee(employee_id, request)

@app.delete(
    "/employee/{employee_id}",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def delete_employee(
    employee_id: int,
    service: EmployeeService = Depends(EmployeeService)
):
    return await service.delete_employee(employee_id)

@app.get(
    "/employee/{employee_id}/beneficiaries",
    response_model=List[BeneficiaryResponse],
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_employee_beneficiaries(
    employee_id: int,
    service: BeneficiaryService = Depends(BeneficiaryService)
):
    return await service.get_employee_beneficiaries(employee_id)

@app.post(
    "/beneficiary",
    response_model=BeneficiaryResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def post_beneficiary(
    request: CreateBeneficiaryRequest,
    service: BeneficiaryService = Depends(BeneficiaryService)
):
    return await service.create_beneficiary(request)

@app.patch(
    "/beneficiary",
    response_model=BeneficiaryResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def patch_beneficiary(
    request: CreateBeneficiaryRequest,
    service: BeneficiaryService = Depends(BeneficiaryService)
):
    return await service.update_beneficiary(request)


@app.delete(
    "/beneficiary/{employe_id}/{curp}",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def delete_beneficiary(
    employe_id: int,
    curp: str,
    service: BeneficiaryService = Depends(BeneficiaryService)
):
    return await service.delete_beneficiary(employe_id, curp)


@app.get(
    "/beneficiary/{employe_id}/{curp}",
    response_model=BeneficiaryResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_beneficiary(
    employe_id: int,
    curp: str,
    service: BeneficiaryService = Depends(BeneficiaryService)
):
    return await service.get_beneficiary_by_curp(curp, employe_id)