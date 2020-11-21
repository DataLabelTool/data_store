from typing import List, Optional

from fastapi import FastAPI, File, UploadFile, APIRouter, Body, Depends
from pydantic import BaseModel, HttpUrl
from fastapi.staticfiles import StaticFiles

from src.database.store import (
    post_file,
    delete_file
)
from src.models.store import (
    ErrorResponseModel,
    ResponseModel,
    StoreModel
)
from src.models.users import User
from src.routes.users import fastapi_users
from src.utils import project_root, static_path

store_router = APIRouter()


@store_router.post("/", response_description="Files added into the database")
async def post_files_data(
        files: List[UploadFile] = File(...),
        user: User = Depends(fastapi_users.get_current_active_user)
):
    if not user.is_superuser:
        return ErrorResponseModel(
            "An error occurred",
            403,
            "User does not have admin privilegies",
        )
    else:
        urls = []
        for file in files:
            url = await post_file(file, user)
            urls.append(url)
        error_urls = len([True for url in urls if url is None])
        success_urls = len([True for url in urls if url is not None])
        if error_urls > 0 and success_urls > 0:
            return ResponseModel(urls, "Not all Files added successfully!")
        elif success_urls == 0 and error_urls > 0:
            return ErrorResponseModel(
                "An error occurred",
                503,
                "Error while load files into the database",
            )
        elif error_urls == 0 and success_urls > 0:
            return ResponseModel(urls, "Files added successfully.")


@store_router.delete("/", response_description="Files deleted from the database")
async def delete_files_data(
        urls: List[str] = Body(...),
        user: User = Depends(fastapi_users.get_current_active_user)
):
    if not user.is_superuser:
        return ErrorResponseModel(
            "An error occurred",
            503,
            "User does not have admin privilegies",
        )
    else:
        results = []
        for url in urls:
            result = await delete_file(url, user)
            results.append(result)
        error_urls = len([True for result in results if result is False])
        success_urls = len([True for result in results if result is True])
        if error_urls > 0 and success_urls > 0:
            return ResponseModel(results, "Not all Files deleted successfully!")
        elif success_urls == 0 and error_urls > 0:
            return ErrorResponseModel(
                "An error occurred",
                503,
                "Error while delete files into the database",
            )
        elif error_urls == 0 and success_urls > 0:
            return ResponseModel(results, "Files deleted successfully.")

static_files = StaticFiles(directory=str(project_root()/static_path()))
