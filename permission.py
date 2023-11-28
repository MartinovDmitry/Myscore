from fastapi import HTTPException, status
from fastapi.requests import Request
from jose import jwt

from config import settings
from exceptions import UserIsNotAuthenticatedException, PermissionAdminException, PermissionClientException
from users.models import Role


class Permission:
    @staticmethod
    def get_payload_from_cookie(request: Request):
        access_token = request.cookies.get('access_token')
        if not access_token:
            raise UserIsNotAuthenticatedException
        payload: dict = jwt.decode(access_token, settings.JWT_KEY, algorithms=[settings.ALGORITHM])
        return payload

    @classmethod
    def check_role_client_of_user(cls, request: Request):
        payload: dict = cls.get_payload_from_cookie(request=request)
        role = payload['role'][5:]
        if role is not Role.CLIENT:
            raise PermissionClientException
        return role

    @classmethod
    def check_role_admin_of_user(cls, request: Request):
        payload: dict = cls.get_payload_from_cookie(request=request)
        role = payload['role'][5:]
        if role is not Role.ADMIN:
            raise PermissionAdminException
        return role


permission = Permission()