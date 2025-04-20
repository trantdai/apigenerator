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
from pydantic import Field, StrictStr, BaseModel # MANUAL: Add BaseModel
# from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.http_error import HTTPError
from openapi_server.models.http_validation_error import HTTPValidationError
from openapi_server.models.job_request import JobRequest
from openapi_server.models.job_response import JobResponse
from openapi_server.models.job_status import JobStatus

# MANUAL
from typing import Dict, List, Optional, Literal, Any, TypedDict
from uuid import uuid4
import random
import time
import asyncio
from enum import Enum
import contextlib
from dataclasses import dataclass, field, asdict
import datetime
# END OF MANUAL


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)

# MANUAL
# Using Python 3.12's improved type system
class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESSFUL = "successful"
    FAILED = "failed"

class JobRequest(BaseModel):
    """Input model for job creation"""
    duration_seconds: int = Field(
        ...,
        gt=0,
        description="Duration of the job in seconds"
    )
    failure_probability: float = Field(
        0.2,
        ge=0,
        le=1,
        description="Probability of job failure (0-1)"
    )
    name: Optional[str] = Field(
        None,
        description="Optional job name"
    )

    # Using Python 3.12's improved model validation
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "duration_seconds": 30,
                    "failure_probability": 0.2,
                    "name": "Example Job"
                }
            ]
        }
    }

# class JobResponse(BaseModel):
#     """Output model for job information"""
#     job_id: str
#     status: JobStatus
#     name: Optional[str] = None
#     created_at: float
#     updated_at: float
#     completion_percentage: Optional[float] = None
#     error_message: Optional[str] = None
#     estimated_completion_time: Optional[float] = None

@dataclass
class Job:
    """Internal job representation with all required fields"""
    job_id: str
    status: JobStatus
    name: Optional[str]
    created_at: float
    updated_at: float
    duration_seconds: int
    failure_probability: float
    completion_percentage: float = 0.0
    error_message: Optional[str] = None
    task: Optional[asyncio.Task] = field(default=None, repr=False, init=False, compare=False)  # Exclude from asdict
    estimated_completion_time: Optional[float] = None

    def to_response(self) -> Dict[str, Any]:
        """Convert to response dictionary excluding internal fields"""
        # result = asdict(self)
        # result.pop('task', None)
        # Create a shallow copy of the object with the `task` field set to None
        # job_copy = self.__class__(
        #     **{field.name: getattr(self, field.name) for field in self.__dataclass_fields__.values() if field.name != "task"}
        # )
        # return asdict(job_copy)
        # Manual dictionary creation instead of using asdict()
        return {
            "job_id": self.job_id,
            "status": self.status,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "duration_seconds": self.duration_seconds,
            "failure_probability": self.failure_probability,
            "completion_percentage": self.completion_percentage,
            "error_message": self.error_message,
            "estimated_completion_time": self.estimated_completion_time
        }

# In-memory job storage
jobs_db: Dict[str, Job] = {}

async def process_job(job_id: str, duration_seconds: int, failure_probability: float) -> None:
    """
    Asynchronously simulates the processing of a job over time.
    Uses asyncio.sleep instead of time.sleep to avoid blocking the event loop.
    """
    job = jobs_db[job_id]

    # Update to running state
    job.status = JobStatus.RUNNING
    job.updated_at = time.time()
    job.estimated_completion_time = job.created_at + duration_seconds

    # Calculate sleep intervals for updates (we'll update every 10% of progress)
    interval = duration_seconds / 10

    for i in range(1, 11):
        await asyncio.sleep(interval)
        job.completion_percentage = i * 10
        job.updated_at = time.time()

        # Randomly fail job based on failure probability (but only after some progress)
        if i > 3 and random.random() < failure_probability:
            job.status = JobStatus.FAILED
            job.error_message = random.choice([
                "Connection timeout",
                "Resource not found",
                "Internal server error",
                "Service unavailable",
                "Permission denied"
            ])
            job.updated_at = time.time()
            return

    # Job completed successfully
    job.status = JobStatus.SUCCESSFUL
    job.updated_at = time.time()



# END OF MANUAL

@router.post(
    "/api/jobs",
    responses={
        201: {"model": JobResponse, "description": "Job created with status information"},
        422: {"model": HTTPValidationError, "description": "Validation Error"},
    },
    tags=["default"],
    summary="Create a new long-running job",
    response_model_by_alias=True,
)
async def create_job(
    job_request: JobRequest = Body(None, description=""),
) -> JobResponse:
    # """Start a new simulated long-running job with configurable parameters.  - **duration_seconds**: How long the job should run before completion - **failure_probability**: Chance the job will fail (0.0-1.0) - **name**: Optional name to identify the job  Returns a job ID that can be used to query the job status. """
    # if not BaseDefaultApi.subclasses:
    #     raise HTTPException(status_code=500, detail="Not implemented")
    # return await BaseDefaultApi.subclasses[0]().create_job(job_request)

    # MANUAL
    """
    Start a new simulated long-running job with configurable parameters.

    - **duration_seconds**: How long the job should run before completion
    - **failure_probability**: Chance the job will fail (0.0-1.0)
    - **name**: Optional name to identify the job

    Returns a job ID that can be used to query the job status.
    """
    job_id = str(uuid4())
    current_time = time.time()

    job = Job(
        job_id=job_id,
        name=job_request.name,
        status=JobStatus.PENDING,
        created_at=current_time,
        updated_at=current_time,
        duration_seconds=job_request.duration_seconds,
        failure_probability=job_request.failure_probability,
        completion_percentage=0,
        estimated_completion_time=current_time + job_request.duration_seconds
    )

    jobs_db[job_id] = job

    # Start job processing in background as an asyncio task
    job.task = asyncio.create_task(
        process_job(
            job_id,
            job_request.duration_seconds,
            job_request.failure_probability
        )
    )

    return job.to_response()
    # END OF MANUAL

@router.delete(
    "/api/jobs/{job_id}",
    responses={
        204: {"description": "Job successfully deleted"},
        404: {"model": HTTPError, "description": "Job not found"},
    },
    tags=["default"],
    summary="Cancel and delete a job",
    response_model_by_alias=True,
)
async def delete_job(
    job_id: Annotated[StrictStr, Field(description="Job ID to delete")] = Path(..., description="Job ID to delete"),
) -> None:
    # """Cancel a running job and remove it from the system.  - **job_id**: The UUID of the job to delete """
    # if not BaseDefaultApi.subclasses:
    #     raise HTTPException(status_code=500, detail="Not implemented")
    # return await BaseDefaultApi.subclasses[0]().delete_job(job_id)

    # MANUAL
    """
    Cancel a running job and remove it from the system.

    - **job_id**: The UUID of the job to delete
    """
    if job_id not in jobs_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found"
        )

    job = jobs_db[job_id]

    # Cancel the task if it's still running
    if job.task and not job.task.done():
        job.task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await job.task

    # Remove from storage
    del jobs_db[job_id]
    # END OF MANUAL


@router.get(
    "/api/jobs/{job_id}",
    responses={
        200: {"model": JobResponse, "description": "Current status of the job"},
        404: {"model": HTTPError, "description": "Job not found"},
    },
    tags=["default"],
    summary="Get job status by ID",
    response_model_by_alias=True,
)
async def get_job_status(
    job_id: Annotated[StrictStr, Field(description="Job ID to query")] = Path(..., description="Job ID to query"),
) -> JobResponse:
    # """Query the status of a job by its ID.  The job status can be one of: pending, running, successful, or failed.  - **job_id**: The UUID of the job to query  Returns detailed information about the job including status and completion percentage. """
    # if not BaseDefaultApi.subclasses:
    #     raise HTTPException(status_code=500, detail="Not implemented")
    # return await BaseDefaultApi.subclasses[0]().get_job_status(job_id)

    # MANUAL
    """
    Query the status of a job by its ID.

    The job status can be one of: pending, running, successful, or failed.

    - **job_id**: The UUID of the job to query

    Returns detailed information about the job including status and completion percentage.
    """
    if job_id not in jobs_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found"
        )

    return jobs_db[job_id].to_response()
    # END OF MANUAL


@router.get(
    "/api/jobs",
    responses={
        200: {"model": List[JobResponse], "description": "List of all jobs in the system"},
    },
    tags=["default"],
    summary="List all jobs",
    response_model_by_alias=True,
)
async def list_jobs(
    status: Annotated[Optional[JobStatus], Field(description="Filter jobs by status")] = Query(None, description="Filter jobs by status", alias="status"),
) -> List[JobResponse]:
    # """List all jobs with optional filtering by status.  - **status**: Optional filter parameter to show only jobs with a specific status """
    # if not BaseDefaultApi.subclasses:
    #     raise HTTPException(status_code=500, detail="Not implemented")
    # return await BaseDefaultApi.subclasses[0]().list_jobs(status)

    # MANUAL
    # Extra endpoints that could be helpful for testing and management
    """
    List all jobs with optional filtering by status.

    - **status**: Optional filter parameter to show only jobs with a specific status
    """
    if status:
        return [job.to_response() for job in jobs_db.values() if job.status == status]
    return [job.to_response() for job in jobs_db.values()]
    # END OF MANUAL
