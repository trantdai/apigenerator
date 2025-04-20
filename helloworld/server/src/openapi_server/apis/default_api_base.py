# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr
from typing import Any
from typing_extensions import Annotated
from openapi_server.models.person_name_get200_response import PersonNameGet200Response
from openapi_server.models.person_post_request import PersonPostRequest


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def hello_get(
        self,
    ) -> str:
        """Returns a simple \&quot;Hello World\&quot; message."""
        ...


    async def hello_name_get(
        self,
        name: Annotated[StrictStr, Field(description="The name of the person to greet.")],
    ) -> str:
        """Returns a personalized \&quot;Hello {name}\&quot; message."""
        ...


    async def person_name_get(
        self,
        name: Annotated[StrictStr, Field(description="The name of the person to retrieve.")],
    ) -> PersonNameGet200Response:
        """Retrieves the name of a person by their identifier."""
        ...


    async def person_post(
        self,
        person_post_request: PersonPostRequest,
    ) -> None:
        """Adds a new person name to the system."""
        ...
