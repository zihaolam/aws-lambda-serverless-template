from typing import List, Union

from models.user import UserModel
from schemas.user import (
    CreateUserSchema,
    CreateUserAuthProviderSchema,
    UserSchema,
    UserUpdateSchema,
)
from models.helpers import generate_key
from models.constants import ModelTypes
from services.helpers import map_attributes
from utils.lambda_helpers import LambdaException


class UserService(UserModel):
    user_prefix = ModelTypes.USER
    user_model = UserModel

    @classmethod
    def generate_pk(cls, email: str) -> str:
        return generate_key(cls.user_prefix, email)

    create_schema = CreateUserSchema

    @classmethod
    def create(cls, body: create_schema):
        new_user = UserModel(cls.generate_pk(body.email), ModelTypes.DETAIL)
        new_user.save()
        return new_user


    @classmethod
    def find_all(last_evaluated_key=None, limit=None) -> List[UserModel]:
        filters = {}
        if last_evaluated_key is not None:
            filters.update(last_evaluated_key=last_evaluated_key)
        if limit is not None:
            filters.update(limit=limit)

        return list(UserModel.scan(**filters))

    @classmethod
    def find_by_user_id(
        cls, user_id: str
    ) -> Union[UserModel, UserSchema]:
        _user = UserModel.get(user_id, ModelTypes.DETAIL)
        return _user


    @classmethod
    def find_by_email(cls, email: str) -> UserModel:
        return cls.find_by_user_id(cls.generate_pk(email))

    update_user_schema = UserUpdateSchema

    @classmethod
    def update(cls, user_id: str, body: update_user_schema) -> UserModel:
        _user = cls.find_by_user_id(user_id)

        map_attributes(body, _user, exclude=body.fields_to_exclude_when_mapping())

        _user.save()
        return _user
    

    add_user_auth_provider_schema = CreateUserAuthProviderSchema

    @classmethod
    def add_user_auth_provider(
        cls, email: str, body: add_user_auth_provider_schema
    ) -> UserModel:
        _user = cls.find_by_email(email)
        _user.provider_ids = _user.provider_ids.add("_".join([body.provider, body.id]))
        return _user
