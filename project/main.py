import os
import time
from typing import Any, Callable

from fastapi import FastAPI, Request

from routers import school

os.environ["TZ"] = "UTC"

tags_metadata = [
    {
        "name": "schools",
        "description": "This entity represents an educational organization that includes staff and students who participate in classes and educational activity groups.",
    },
]

api = FastAPI(openapi_tags=tags_metadata)


@api.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable) -> Any:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@api.get(
    "/",
)
def get_metadata():
    return {
        "version": "0.1.0",
        "apiMode": "YearSpecific",
        "dataModels": [
            {
                "name": "Ed-Fi",
                "version": "4.0.0-a",
                "informationalVersion": "The Ed-Fi Data Model 4.0a",
            }
        ],
    }


api.include_router(school.router)
