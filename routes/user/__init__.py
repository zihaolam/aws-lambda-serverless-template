from typing import List
from schemas.user import UserSchema, UserUpdateSchema
from services import UserService
from utils.lambda_helpers import lambda_handler, LambdaEvent


@lambda_handler(response_model=List[UserSchema])
def get_users(event, context):
    _users = UserService.find_all()
    return _users


@lambda_handler(response_model=UserSchema, require_auth=True)
def get_self(event: LambdaEvent, context):
    try:
        _user = UserService.find_by_user_id(event.token_payload.user_id)
    except UserService.user_model.DoesNotExist as e:
        _user = UserService.create(
            UserService.create_schema(email=event.token_payload.email)
        )
        _user.email = event.token_payload.email
        _user.save()

    return _user


@lambda_handler(
    response_model=UserSchema, body_model=UserUpdateSchema, require_auth=True
)
def update(event: LambdaEvent[UserUpdateSchema], context):
    _updated_user = UserService.update(event.token_payload.user_id, event.parsed_body)
    return _updated_user