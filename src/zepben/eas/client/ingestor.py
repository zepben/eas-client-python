#  Copyright 2025 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
from datetime import datetime

__all__ = [
    "IngestorConfigInput", "IngestorRuntimeKind", "IngestorRunState", "IngestorRun", "IngestorRunsFilterInput", "Order",
    "IngestorRunsSortCriteriaInput"
]


@dataclass
class IngestorConfigInput:
    key: str
    value: str


class IngestorRuntimeKind(Enum):
    AZURE_CONTAINER_APP_JOB = "AZURE_CONTAINER_APP_JOB"
    DOCKER = "DOCKER"
    ECS = "ECS"
    KUBERNETES = "KUBERNETES"
    TEMPORAL_KUBERNETES = "TEMPORAL_KUBERNETES"


class IngestorRunState(Enum):
    INITIALIZED = "INITIALIZED"
    QUEUED = "QUEUED"
    STARTED = "STARTED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    FAILED_TO_START = "FAILED_TO_START"


@dataclass
class IngestorRun:
    id: int
    container_runtime_type: Optional[IngestorRuntimeKind]
    payload: str
    token: str
    status: IngestorRunState
    started_at: datetime
    status_last_updated_at: Optional[datetime]
    completedAt: Optional[datetime]


@dataclass
class IngestorRunsFilterInput:
    id: Optional[int] = None
    status: Optional[List[IngestorRunState]] = None
    completed: Optional[bool] = None
    container_runtime_type: Optional[List[IngestorRuntimeKind]] = None


class Order(Enum):
    ASC = "ASC"
    DESC = "DESC"


@dataclass
class IngestorRunsSortCriteriaInput:
    status: Optional[Order] = None
    started_at: Optional[Order] = None
    status_last_updated_at: Optional[Order] = None
    completed_at: Optional[Order] = None
    container_runtime_type: Optional[Order] = None
