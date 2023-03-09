from typing import Optional
import motor.motor_asyncio
import pydantic
from beanie import PydanticObjectId
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase

DATABASE_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["mentor"]


class User(BeanieBaseUser[PydanticObjectId]):
    #username: Optional[str] = None
    username: str
    roles: list[str] = ["student"]

    # @pydantic.validator('username', pre=True, always=True)
    # def default_username(cls, v, *, values, **kwargs):
    #     return v or values['email']


async def get_user_db():
    yield BeanieUserDatabase(User)

