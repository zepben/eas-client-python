#  Copyright 2025 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = [
    "OpenDssConfig",
    "OpenDssModelState",
    "GetOpenDssModelsFilterInput",
    "Order",
    "GetOpenDssModelsSortCriteriaInput"
]

from dataclasses import dataclass
from enum import Enum
from typing import Union, Optional, List

from zepben.eas.client.work_package import GeneratorConfig, TimePeriod, FixedTime
from zepben.eas.client.util import HostingCapacityDataclass


@dataclass
class OpenDssConfig(HostingCapacityDataclass):
    """ A data class representing the configuration for an opendss export """
    scenario: str
    year: int
    feeder: str
    load_time: Union[TimePeriod, FixedTime]
    generator_config: Optional[GeneratorConfig] = None
    model_name: Optional[str] = None
    is_public: Optional[bool] = None

    def to_json(self) -> dict:
        _json = super().to_json()
        _json["generationSpec"] = {
            "modelOptions": {
                "feeder": _json.pop('feeder'),
                "scenario": _json.pop('scenario'),
                "year": _json.pop('year'),
            },
            "modulesConfiguration": {
                "common": {},
                "generator": _json.pop('generatorConfig'),
            }
        }
        if isinstance(self.load_time, TimePeriod):
            _json["generationSpec"]["modulesConfiguration"]["common"]["timePeriod"] = _json.pop('loadTime')
        elif isinstance(self.load_time, FixedTime):
            _json["generationSpec"]["modulesConfiguration"]["common"]["fixedTime"] = _json.pop('loadTime')
        return _json


class OpenDssModelState(Enum):
    COULD_NOT_START = "COULD_NOT_START"
    CREATION = "CREATION"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class GetOpenDssModelsFilterInput(HostingCapacityDataclass):
    """ A data class representing the filter to apply to the opendss export run paginated query """
    name: Optional[str] = None
    is_public: Optional[int] = None
    state: Optional[List[OpenDssModelState]] = None


class Order(Enum):
    ASC = "ASC"
    DESC = "DESC"


@dataclass
class GetOpenDssModelsSortCriteriaInput(HostingCapacityDataclass):
    """ A data class representing the sort criteria to apply to the opendss export run paginated query """
    name: Optional[Order] = None
    created_at: Optional[Order] = None
    state: Optional[Order] = None
    is_public: Optional[Order] = None
