# src/utils/helpers.py

import os
from typing import List
from dotenv import load_dotenv
from fastapi import APIRouter

load_dotenv()

def get_env_variable(key):
    return os.getenv(key)

def init_router(endpoint: str, tag: str, dependencies: List = None) -> APIRouter:
    """Creates and returns a FastAPI Router object. Adds optional dependencies to the
    router, if provided."""

    router = APIRouter(tags=[tag], dependencies=dependencies)
    env = os.environ.get("SERVICE_BASE_PATH")

    if env is None:
        router.prefix = "/" + endpoint
    else:
        router.prefix = "/" + env + "/" + endpoint

    return router
