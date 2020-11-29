from fastapi import FastAPI
from src.utils import base_url
import requests
from src.version import version
from src.database.base import database
from src.database.users import create_first_admin

from src.routes.users import (
    jwt_auth_router,
    register_router,
    reset_password_router,
    users_router
)
from src.routes.store import (
    store_router,
    static_files
)
app = FastAPI(
    title="data_store",
    version=version,
    root_path=requests.utils.urlparse(base_url()).path
)

@app.on_event("startup")
async def startup():
    await database.connect()
    success = await create_first_admin()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# store routes
app.include_router(
    store_router,
    prefix="/store"
)
app.mount(
    "/store",
    static_files,
    name=""
)

# users routers
app.include_router(
    jwt_auth_router,
    prefix="/auth/jwt",
    tags=["auth"]
)
app.include_router(
    register_router,
    prefix="/auth",
    tags=["auth"]
)
# app.include_router(
#     reset_password_router,
#     prefix="/auth",
#     tags=["auth"]
# )
app.include_router(
    users_router,
    prefix="/users",
    tags=["users"]
)


# from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from pydantic import BaseModel
#
# templates = Jinja2Templates(directory="templates")
#
# app = FastAPI()
#
#
# class TextArea(BaseModel):
#     content: str
#
#
# @app.post("/add")
# async def post_textarea(data: TextArea):
#     print(data.dict())
#     return {**data.dict()}
#
#
# @app.get("/")
# async def serve_home(request: Request):
#     return templates.TemplateResponse("home.html", {"request": request})
"""
uvicorn src.api:app --port 8081 --host 0.0.0.0 --reload
"""