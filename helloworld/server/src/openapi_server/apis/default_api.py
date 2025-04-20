# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.default_api_base import BaseDefaultApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictStr
from typing import Any
from typing_extensions import Annotated
from openapi_server.models.person_name_get200_response import PersonNameGet200Response
from openapi_server.models.person_post_request import PersonPostRequest


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/hello",
    responses={
        200: {"model": str, "description": "A successful response."},
    },
    tags=["default"],
    summary="Say Hello World",
    response_model_by_alias=True,
)
async def hello_get(
) -> str:
    """Returns a simple \&quot;Hello World\&quot; message."""
    # if not BaseDefaultApi.subclasses:
    #     raise HTTPException(status_code=500, detail="Not implemented")
    # return await BaseDefaultApi.subclasses[0]().hello_get()
    return "Hello World!"


@router.get(
    "/hello/{name}",
    responses={
        200: {"model": str, "description": "A successful response."},
        404: {"description": "Person not found."},
    },
    tags=["default"],
    summary="Say Hello to a person",
    response_model_by_alias=True,
)
async def hello_name_get(
    name: Annotated[StrictStr, Field(description="The name of the person to greet.")] = Path(..., description="The name of the person to greet."),
) -> str:
    """Returns a personalized \&quot;Hello {name}\&quot; message."""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().hello_name_get(name)


@router.get(
    "/person/{name}",
    responses={
        200: {"model": PersonNameGet200Response, "description": "A successful response."},
        404: {"description": "Person not found."},
    },
    tags=["default"],
    summary="Get a person&#39;s name",
    response_model_by_alias=True,
)
async def person_name_get(
    name: Annotated[StrictStr, Field(description="The name of the person to retrieve.")] = Path(..., description="The name of the person to retrieve."),
) -> PersonNameGet200Response:
    """Retrieves the name of a person by their identifier."""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().person_name_get(name)


@router.post(
    "/person",
    responses={
        201: {"description": "Person added successfully."},
        400: {"description": "Invalid input."},
    },
    tags=["default"],
    summary="Add a new person",
    response_model_by_alias=True,
)
async def person_post(
    person_post_request: PersonPostRequest = Body(None, description=""),
) -> None:
    """Adds a new person name to the system."""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().person_post(person_post_request)
