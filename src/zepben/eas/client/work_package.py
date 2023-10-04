#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime
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


class SwitchMeterPlacementConfig:
    meter_switch_class: Optional[SwitchClass]
    name_pattern: Optional[str]

    def __init__(
            self,
            meter_switch_class: Optional[SwitchClass] = None,
            name_pattern: Optional[str] = None,
    ):
        self.meter_switch_class = meter_switch_class
        self.name_pattern = name_pattern


class TimePeriod:
    start_time: datetime
    end_time: datetime

    def __init__(
            self,
            start_time: datetime,
            end_time: datetime,
    ):
        self.start_time = start_time
        self.end_time = end_time


class ModelConfig:
    vm_pu: Optional[float]
    vmin_pu: Optional[float]
    vmax_pu: Optional[float]
    load_model: Optional[int]
    collapse_swer: Optional[bool]
    meter_at_hv_source: Optional[bool]
    meters_at_dist_transformers: Optional[bool]
    switch_meter_placement_configs: Optional[List[SwitchMeterPlacementConfig]]
    fixed_time: Optional[datetime]
    time_period: Optional[TimePeriod]

    def __init__(
            self,
            vm_pu: Optional[float] = None,
            vmin_pu: Optional[float] = None,
            vmax_pu: Optional[float] = None,
            load_model: Optional[int] = None,
            collapse_swer: Optional[bool] = None,
            meter_at_hv_source: Optional[bool] = None,
            meters_at_dist_transformers: Optional[bool] = None,
            switch_meter_placement_configs: Optional[List[SwitchMeterPlacementConfig]] = None,
            fixed_time: Optional[datetime] = None,
            time_period: Optional[TimePeriod] = None,
    ):
        self.vm_pu = vm_pu
        self.vmin_pu = vmin_pu
        self.vmax_pu = vmax_pu
        self.load_model = load_model
        self.collapse_swer = collapse_swer
        self.meter_at_hv_source = meter_at_hv_source
        self.meters_at_dist_transformers = meters_at_dist_transformers
        self.switch_meter_placement_configs = switch_meter_placement_configs
        self.fixed_time = fixed_time
        self.time_period = time_period


class SolveMode(Enum):
    YEARLY = "YEARLY"
    DAILY = "DAILY"


class SolveConfig:
    norm_vmin_pu: Optional[float]
    norm_vmax_pu: Optional[float]
    emerg_vmin_pu: Optional[float]
    emerg_vmax_pu: Optional[float]
    base_frequency: Optional[int]
    voltage_bases: Optional[List[float]]
    max_iter: Optional[int]
    max_control_iter: Optional[int]
    mode: Optional[SolveMode]
    step_size_minutes: Optional[float]

    def __init__(
            self,
            norm_vmin_pu: Optional[float] = None,
            norm_vmax_pu: Optional[float] = None,
            emerg_vmin_pu: Optional[float] = None,
            emerg_vmax_pu: Optional[float] = None,
            base_frequency: Optional[int] = None,
            voltage_bases: Optional[List[float]] = None,
            max_iter: Optional[int] = None,
            max_control_iter: Optional[int] = None,
            mode: Optional[SolveMode] = None,
            step_size_minutes: Optional[float] = None,
    ):
        self.norm_vmin_pu = norm_vmin_pu
        self.norm_vmax_pu = norm_vmax_pu
        self.emerg_vmin_pu = emerg_vmin_pu
        self.emerg_vmax_pu = emerg_vmax_pu
        self.base_frequency = base_frequency
        self.voltage_bases = voltage_bases
        self.max_iter = max_iter
        self.max_control_iter = max_control_iter
        self.mode = mode
        self.step_size_minutes = step_size_minutes


class ResultsDetailLevel(Enum):
    STANDARD = "STANDARD"
    BASIC = "BASIC"
    EXTENDED = "EXTENDED"
    RAW = "RAW"


class WorkPackageConfig:
    """ A data class representing the configuration for a hosting capacity work package """
    feeders: List[str]
    years: List[int]
    scenarios: List[str]
    model_config: Optional[ModelConfig]
    solve_config: Optional[SolveConfig]
    results_detail_level: Optional[ResultsDetailLevel]
    quality_assurance_processing: Optional[bool]

    def __init__(
            self,
            feeders: List[str],
            years: List[int],
            scenarios: List[str],
            model_config: Optional[ModelConfig] = None,
            solve_config: Optional[SolveConfig] = None,
            results_detail_level: Optional[ResultsDetailLevel] = None,
            quality_assurance_processing: Optional[bool] = None,
    ):
        self.feeders = feeders
        self.years = years
        self.scenarios = scenarios
        self.model_config = model_config
        self.solve_config = solve_config
        self.results_detail_level = results_detail_level
        self.quality_assurance_processing = quality_assurance_processing


class WorkPackageProgress:
    id: str
    progress_percent: int
    pending: List[str]
    generation: List[str]
    execution: List[str]
    result_processing: List[str]
    failure_processing: List[str]
    complete: List[str]

    def __init__(
            self,
            id: str,
            progress_percent: int,
            pending: List[str],
            generation: List[str],
            execution: List[str],
            result_processing: List[str],
            failure_processing: List[str],
            complete: List[str],
    ):
        self.id = id
        self.progress_percent = progress_percent
        self.pending = pending
        self.generation = generation
        self.execution = execution
        self.result_processing = result_processing
        self.failure_processing = failure_processing
        self.complete = complete


class WorkPackagesProgress:
    pending: List[str]
    in_progress: List[WorkPackageProgress]

    def __init__(
            self,
            pending: List[str],
            in_progress: List[WorkPackageProgress],
    ):
        self.pending = pending
        self.in_progress = in_progress
