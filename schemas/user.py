from typing import Optional, List
from schemas import CustomBaseModel
from schemas.base.user import UserBase


class CreateUserSchema(CustomBaseModel):
    email: str


class CreateUserAuthProviderSchema(CustomBaseModel):
    id: str
    provider: str


class UserUpdateSchema(UserBase):
    def fields_to_exclude_when_mapping(cls):
        return {"email"}


class UserSchema(UserBase):
    pass
