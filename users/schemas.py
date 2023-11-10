from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class SchUserBase(BaseModel):
    username: str
    email: EmailStr


class SchUserRegister(SchUserBase):
    password: str


class SchUserLogin(BaseModel):
    email: EmailStr
    password: str

