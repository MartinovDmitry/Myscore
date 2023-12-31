from fastapi import HTTPException, status


class MyscoreException(HTTPException):
    status_code = 500
    detail = ''
    headers = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail, headers=self.headers)


class UserAlreadyExistsException(MyscoreException):
    status_code = status.HTTP_409_CONFLICT
    detail = {'Message': 'User already exists'}


class AlreadyExistsException(MyscoreException):
    status_code = status.HTTP_409_CONFLICT
    detail = {'Message': 'Already exists'}


class WrongUserCredentialsException(MyscoreException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = {'Message': 'Something wrong with credentials'}


class WrongCredentialsException(MyscoreException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = {'Message': 'Something wrong with credentials'}


class InvalidRefreshTokenException(MyscoreException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = {'Message': 'Refresh token is invalid'}
    headers = {'WWW-Authenticate': 'Bearer'}


class InvalidRefreshTokenExpireException(MyscoreException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = {'Message': 'Invalid refresh token. Expire is over'}


class UserIsNotAuthenticatedException(MyscoreException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = {'Message': 'You are not authenticated'}


class ALotOfRecordsRefreshTokens(MyscoreException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = {'Message': 'A lot of case of authentication'}


class PermissionAdminException(MyscoreException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = {'Message': 'You have no permission. Please be sure your role is ADMIN or higher'}


class PermissionClientException(MyscoreException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = {'Message': 'You have no permission. Please be sure your role is CLIENT or higher'}


class PermissionVerifiedException(MyscoreException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = {'Message': 'You have to be verified. Please, log in'}
