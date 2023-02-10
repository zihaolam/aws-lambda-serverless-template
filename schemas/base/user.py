from typing import List, Optional
from schemas import CustomBaseModel


class UserBase(CustomBaseModel):
    username: Optional[str]
    email: Optional[str]
