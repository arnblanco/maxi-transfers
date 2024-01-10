from http import HTTPStatus


class CustomException(Exception):
    code = HTTPStatus.BAD_GATEWAY
    error_code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message=None):
        if message:
            self.message = message


class BadRequestException(CustomException):
    code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    message = HTTPStatus.BAD_REQUEST.description


class NotFoundException(CustomException):
    code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    message = HTTPStatus.NOT_FOUND.description


class ForbiddenException(CustomException):
    code = HTTPStatus.FORBIDDEN
    error_code = HTTPStatus.FORBIDDEN
    message = HTTPStatus.FORBIDDEN.description


class UnauthorizedException(CustomException):
    code = HTTPStatus.UNAUTHORIZED
    error_code = HTTPStatus.UNAUTHORIZED
    message = HTTPStatus.UNAUTHORIZED.description


class UnprocessableEntity(CustomException):
    code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    message = HTTPStatus.UNPROCESSABLE_ENTITY.description


class DuplicateValueException(CustomException):
    code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    message = HTTPStatus.UNPROCESSABLE_ENTITY.description


class DecodeTokenException(CustomException):
    code = 400
    error_code = "TOKEN__DECODE_ERROR"
    message = "token decode error"


class ExpiredTokenException(CustomException):
    code = 400
    error_code = "TOKEN__EXPIRE_TOKEN"
    message = "expired token"

    
class DatabaseConnectionErrorException(CustomException):
    code = HTTPStatus.NOT_FOUND
    error_code = 'DATABASE_Connection_ERROR_EXCEPTION'
    message = 'Database connection error exception'


class DatabaseSQLErrorException(CustomException):
    code = HTTPStatus.NOT_FOUND
    error_code = 'DATABASE_SQL_ERROR_EXCEPTION'
    message = 'Database SQL error exception'


class UserNotFoundException(CustomException):
    code = HTTPStatus.NOT_FOUND
    error_code = 'USER_NOT_FOUND'
    message = 'User not found'


class EmployeeNotFoundException(CustomException):
    code = HTTPStatus.NOT_FOUND
    error_code = 'EMPLOYEE_NOT_FOUND'
    message = 'Employee not found'


class EmployeeDuplicatedException(CustomException):
    code = HTTPStatus.NOT_FOUND
    error_code = 'EMPLOYEE_DUMPLICATED'
    message = 'Employee id is duplicated'


class BeneficiaryNotFoundException(CustomException):
    code = HTTPStatus.NOT_FOUND
    error_code = 'BENEFICIARY_NOT_FOUND'
    message = 'Beneficiary not found'


class BeneficiaryDuplicatedException(CustomException):
    code = HTTPStatus.NOT_FOUND
    error_code = 'BENEFICIARY_DUMPLICATED'
    message = 'Beneficiary id is duplicated'