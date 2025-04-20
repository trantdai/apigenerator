# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictStr  # noqa: F401
from typing import Any, List, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.http_error import HTTPError  # noqa: F401
from openapi_server.models.http_validation_error import HTTPValidationError  # noqa: F401
from openapi_server.models.job_request import JobRequest  # noqa: F401
from openapi_server.models.job_response import JobResponse  # noqa: F401
from openapi_server.models.job_status import JobStatus  # noqa: F401


def test_create_job(client: TestClient):
    """Test case for create_job

    Create a new long-running job
    """
    job_request = [ {
  "duration_seconds" : 30,
  "failure_probability" : 0.2,
  "name" : "Example Job"
} ]

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/api/jobs",
    #    headers=headers,
    #    json=job_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_job(client: TestClient):
    """Test case for delete_job

    Cancel and delete a job
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/api/jobs/{job_id}".format(job_id='job_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_job_status(client: TestClient):
    """Test case for get_job_status

    Get job status by ID
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/jobs/{job_id}".format(job_id='job_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_list_jobs(client: TestClient):
    """Test case for list_jobs

    List all jobs
    """
    params = [("status", openapi_server.JobStatus())]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/jobs",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

