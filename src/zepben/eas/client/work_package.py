#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

__all__ = ["WorkPackageConfig",
           "SwitchClass",
           "SwitchMeterPlacementConfig",
           "ModelConfig",
           "SolveMode",
           "SolveConfig",
           "ResultsDetailLevel"]


class SwitchClass(Enum):
    BREAKER = "BREAKER",
    DISCONNECTOR = "DISCONNECTOR",
    FUSE = "FUSE",
    JUMPER = "JUMPER",
    LOAD_BREAK_SWITCH = "LOAD_BREAK_SWITCH",
    RECLOSER = "RECLOSER"


@dataclass
class SwitchMeterPlacementConfig:
    meterSwitchClass: Optional[SwitchClass] = None
    namePattern: Optional[str] = None


@dataclass
class ModelConfig:
    vmPu: Optional[float] = None
    vMinPu: Optional[float] = None
    vMaxPu: Optional[float] = None
    loadModel: Optional[int] = None
    collapseSWER: Optional[bool] = None
    meterAtHVSource: Optional[bool] = None
    metersAtDistTransformers: Optional[bool] = None
    switchMeterPlacementConfigs: Optional[List[SwitchMeterPlacementConfig]] = None


class SolveMode(Enum):
    YEARLY = "YEARLY"
    DAILY = "DAILY"


@dataclass
class SolveConfig:
    normVMinPu: Optional[float] = None
    normVMaxPu: Optional[float] = None
    emergVMinPu: Optional[float] = None
    emergVMaxPu: Optional[float] = None
    baseFrequency: Optional[int] = None
    voltageBases: Optional[List[float]] = None
    maxIter: Optional[int] = None
    maxControlIter: Optional[int] = None
    mode: Optional[SolveMode] = None
    stepSizeMinutes: Optional[float] = None


class ResultsDetailLevel(Enum):
    STANDARD = "STANDARD"
    BASIC = "BASIC"
    EXTENDED = "EXTENDED"
    RAW = "RAW"


@dataclass
class WorkPackageConfig:
    """ A data class representing the configuration for a hosting capacity work package """
    feeders: List[str]
    years: List[int]
    scenarios: List[str]
    modelConfig: Optional[ModelConfig] = None
    solveConfig: Optional[SolveConfig] = None
    resultsDetailLevel: Optional[ResultsDetailLevel] = None
    qualityAssuranceProcessing: Optional[bool] = None
