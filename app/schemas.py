from typing import Optional
from beanie import PydanticObjectId
from fastapi_users import schemas


class UserRead(schemas.BaseUser[PydanticObjectId]):
    username: Optional[str] = None
    roles: list[str] = ["student"]


class UserCreate(schemas.BaseUserCreate):
    username: Optional[str] = None
    roles: list[str] = ["student"]


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    roles: list[str] = ["student"]

