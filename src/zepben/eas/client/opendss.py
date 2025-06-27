#  Copyright 2025 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass
from datetime import tzinfo
from enum import Enum
from typing import Union, Optional, List

from zepben.eas.client.work_package import GeneratorConfig, TimePeriod, FixedTime

__all__ = [
    "OpenDssConfig",
    "OpenDssModelState",
    "GetOpenDssModelsFilterInput",
    "Order",
    "GetOpenDssModelsSortCriteriaInput"
]


@dataclass
class OpenDssConfig:
    """ A data class representing the configuration for an opendss export """
    scenario: str
    year: int
    feeder: str
    load_time: Union[TimePeriod, FixedTime]
    generator_config: Optional[GeneratorConfig] = None
    model_name: Optional[str] = None
    is_public: Optional[bool] = None


class OpenDssModelState(Enum):
    COULD_NOT_START = "COULD_NOT_START"
    CREATION = "CREATION"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class GetOpenDssModelsFilterInput:
    """ A data class representing the filter to apply to the opendss export run paginated query """
    name: Optional[str] = None
    is_public: Optional[int] = None
    state: Optional[List[OpenDssModelState]] = None


class Order(Enum):
    ASC = "ASC"
    DESC = "DESC"


@dataclass
class GetOpenDssModelsSortCriteriaInput:
    """ A data class representing the sort criteria to apply to the opendss export run paginated query """
    name: Optional[Order] = None
    created_at: Optional[Order] = None
    state: Optional[Order] = None
    is_public: Optional[Order] = None
