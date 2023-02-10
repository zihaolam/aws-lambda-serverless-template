from pynamodb.attributes import (
    UnicodeAttribute,
    BooleanAttribute,
)

from models.helpers import generate_key
from .base import BaseModel
from models.constants import ModelTypes
from utils.ulid_helper import new_ulid


class UserModel(BaseModel, discriminator=ModelTypes.USER):
    # pk is USER::{email}
    sk = UnicodeAttribute(null=False, default=ModelTypes.DETAIL, range_key=True)
    email = UnicodeAttribute()
    username = UnicodeAttribute(null=True)