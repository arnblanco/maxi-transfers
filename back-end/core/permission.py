from abc import ABC, abstractmethod
from typing import List

from fastapi import Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase

from core.exceptions import CustomException, UnauthorizedException


class BasePermission(ABC):
    exception = CustomException

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        pass


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        return request.user.username is not None


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: List[type[BasePermission]]):
        self.permissions = permissions
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request):
        has_permission = False

        for permission in self.permissions:
            cls = permission()
            if await cls.has_permission(request=request):
                has_permission = True
                break
        if not has_permission:
            raise UnauthorizedException