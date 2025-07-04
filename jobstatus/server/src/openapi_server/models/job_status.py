# coding: utf-8

"""
    Long-Running Jobs API

    API for simulating and tracking long-running jobs

    The version of the OpenAPI document: 1.0.0
    Contact: support@example.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
import pprint
import re  # noqa: F401
from enum import Enum



try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class JobStatus(str, Enum):
    """
    Status of a job
    """

    """
    allowed enum values
    """
    PENDING = 'pending'
    RUNNING = 'running'
    SUCCESSFUL = 'successful'
    FAILED = 'failed'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of JobStatus from a JSON string"""
        return cls(json.loads(json_str))


