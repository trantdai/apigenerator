# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.http_error import HTTPError
from openapi_server.models.http_validation_error import HTTPValidationError
from openapi_server.models.job_request import JobRequest
from openapi_server.models.job_response import JobResponse
from openapi_server.models.job_status import JobStatus


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def create_job(
        self,
        job_request: JobRequest,
    ) -> JobResponse:
        """Start a new simulated long-running job with configurable parameters.  - **duration_seconds**: How long the job should run before completion - **failure_probability**: Chance the job will fail (0.0-1.0) - **name**: Optional name to identify the job  Returns a job ID that can be used to query the job status. """
        ...


    async def delete_job(
        self,
        job_id: Annotated[StrictStr, Field(description="Job ID to delete")],
    ) -> None:
        """Cancel a running job and remove it from the system.  - **job_id**: The UUID of the job to delete """
        ...


    async def get_job_status(
        self,
        job_id: Annotated[StrictStr, Field(description="Job ID to query")],
    ) -> JobResponse:
        """Query the status of a job by its ID.  The job status can be one of: pending, running, successful, or failed.  - **job_id**: The UUID of the job to query  Returns detailed information about the job including status and completion percentage. """
        ...


    async def list_jobs(
        self,
        status: Annotated[Optional[JobStatus], Field(description="Filter jobs by status")],
    ) -> List[JobResponse]:
        """List all jobs with optional filtering by status.  - **status**: Optional filter parameter to show only jobs with a specific status """
        ...
