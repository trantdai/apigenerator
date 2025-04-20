# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictStr  # noqa: F401
from typing import Any  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.person_name_get200_response import PersonNameGet200Response  # noqa: F401
from openapi_server.models.person_post_request import PersonPostRequest  # noqa: F401


def test_hello_get(client: TestClient):
    """Test case for hello_get

    Say Hello World
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/hello",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_hello_name_get(client: TestClient):
    """Test case for hello_name_get

    Say Hello to a person
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/hello/{name}".format(name='John'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_person_name_get(client: TestClient):
    """Test case for person_name_get

    Get a person's name
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/person/{name}".format(name='John'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_person_post(client: TestClient):
    """Test case for person_post

    Add a new person
    """
    person_post_request = PersonPostRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/person",
    #    headers=headers,
    #    json=person_post_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

