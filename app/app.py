from functools import lru_cache
from beanie import init_beanie
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from app.config import Settings
from app.db import User, db
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import (
    auth_cookie_backend,
    auth_jwt_backend,
    current_active_user,
    fastapi_users,
)
from ai.chatgpt import chat_improve_resume

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_cookie_backend), prefix="/auth/cookie", tags=["auth"]
)
app.include_router(
    fastapi_users.get_auth_router(auth_jwt_backend), prefix="/auth/bearer", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[
            User,
        ],
    )

@lru_cache
def get_settings():
    return Settings()

@app.get("/vars")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "default variable": settings.DEFAULT_VAR,
        "api key": settings.API_KEY,
        "app max integer": settings.APP_MAX,
    }

class Resume(BaseModel):
    resume: str
    job: str


@app.post("/chat/resume")
async def improve_resume(resume: Resume):
    result_text = chat_improve_resume(resume.resume, resume.job)
    return {"message": result_text}