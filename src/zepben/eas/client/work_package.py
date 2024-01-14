#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

__all__ = ["WorkPackageConfig",
           "SwitchClass",
           "SwitchMeterPlacementConfig",
           "ModelConfig",
           "SolveMode",
           "SolveConfig",
           "ResultsConfig",
           "RawResultsConfig",
           "MetricsResultsConfig",
           "StoredResultsConfig",
           "FixedTime",
           "TimePeriod"]


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


class FixedTime:
    time: datetime

    def __init__(self, time: datetime):
        self.time = time.replace(tzinfo=None)


class TimePeriod:
    start_time: datetime
    end_time: datetime

    def __init__(
            self,
            start_time: datetime,
            end_time: datetime
    ):
        self._validate(start_time, end_time)
        self.start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
        self.end_time = end_time.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)

    @staticmethod
    def _validate(start_time: datetime, end_time: datetime):
        ddelta = (end_time - start_time).days

        if ddelta > 365:
            raise ValueError("The difference between 'start_time' and 'end_time' cannot be greater than a year.")

        if ddelta < 1:
            raise ValueError("The difference between 'start_time' and 'end_time' cannot be less than a day.")

        if ddelta < 0:
            raise ValueError("The 'start_time' must be before 'end_time'.")


class ModelConfig:
    load_time: Union[TimePeriod, FixedTime]
    vm_pu: Optional[float]
    vmin_pu: Optional[float]
    vmax_pu: Optional[float]
    load_model: Optional[int]
    collapse_swer: Optional[bool]
    meter_at_hv_source: Optional[bool]
    meters_at_dist_transformers: Optional[bool]
    switch_meter_placement_configs: Optional[List[SwitchMeterPlacementConfig]]
    calibration: Optional[bool]
    p_factor_base_exports: Optional[float]
    p_factor_forecast_pv: Optional[float]
    p_factor_base_imports: Optional[float]
    fix_single_phase_loads: Optional[bool]
    max_single_phase_load: Optional[float]
    fix_overloading_consumers: Optional[bool]
    max_load_tx_ratio: Optional[float]
    max_gen_tx_ratio: Optional[float]
    fix_undersized_service_lines: Optional[bool]
    max_load_line_ratio: Optional[float]

    def __init__(
            self,
            load_time: Union[TimePeriod, FixedTime],
            vm_pu: Optional[float] = None,
            vmin_pu: Optional[float] = None,
            vmax_pu: Optional[float] = None,
            load_model: Optional[int] = None,
            collapse_swer: Optional[bool] = None,
            meter_at_hv_source: Optional[bool] = None,
            meters_at_dist_transformers: Optional[bool] = None,
            switch_meter_placement_configs: Optional[List[SwitchMeterPlacementConfig]] = None,
            calibration: Optional[bool] = None,
            p_factor_base_exports: Optional[float] = None,
            p_factor_forecast_pv: Optional[float] = None,
            p_factor_base_imports: Optional[float] = None,
            fix_single_phase_loads: Optional[bool] = None,
            max_single_phase_load: Optional[float] = None,
            fix_overloading_consumers: Optional[bool] = None,
            max_load_tx_ratio: Optional[float] = None,
            max_gen_tx_ratio: Optional[float] = None,
            fix_undersized_service_lines: Optional[bool] = None,
            max_load_line_ratio: Optional[float] = None,

    ):
        self.load_time = load_time
        self.vm_pu = vm_pu
        self.vmin_pu = vmin_pu
        self.vmax_pu = vmax_pu
        self.load_model = load_model
        self.collapse_swer = collapse_swer
        self.meter_at_hv_source = meter_at_hv_source
        self.meters_at_dist_transformers = meters_at_dist_transformers
        self.switch_meter_placement_configs = switch_meter_placement_configs
        self.calibration = calibration
        self.p_factor_base_exports = p_factor_base_exports
        self.p_factor_forecast_pv = p_factor_forecast_pv
        self.p_factor_base_imports = p_factor_base_imports
        self.fix_single_phase_loads = fix_single_phase_loads
        self.max_single_phase_load = max_single_phase_load
        self.fix_overloading_consumers = fix_overloading_consumers
        self.max_load_tx_ratio = max_load_tx_ratio
        self.max_gen_tx_ratio = max_gen_tx_ratio
        self.fix_undersized_service_lines = fix_undersized_service_lines
        self.max_load_line_ratio = max_load_line_ratio


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


class RawResultsConfig:
    energy_meter_voltages_raw: Optional[bool]
    energy_meters_raw: Optional[bool]
    results_per_meter: Optional[bool]
    over_loads_raw: Optional[bool]
    voltage_exceptions_raw: Optional[bool]

    def __init__(
            self,
            energy_meter_voltages_raw: Optional[bool] = None,
            energy_meters_raw: Optional[bool] = None,
            results_per_meter: Optional[bool] = None,
            over_loads_raw: Optional[bool] = None,
            voltage_exceptions_raw: Optional[bool] = None,
    ):
        self.energy_meter_voltages_raw = energy_meter_voltages_raw
        self.energy_meters_raw = energy_meters_raw
        self.results_per_meter = results_per_meter
        self.over_loads_raw = over_loads_raw
        self.voltage_exceptions_raw = voltage_exceptions_raw


class MetricsResultsConfig:
    calculate_performance_metrics: Optional[bool]

    def __init__(self, calculate_performance_metrics: Optional[bool] = None):
        self.calculate_performance_metrics = calculate_performance_metrics


class StoredResultsConfig:
    energy_meter_voltages_raw: Optional[bool]
    energy_meters_raw: Optional[bool]
    over_loads_raw: Optional[bool]
    voltage_exceptions_raw: Optional[bool]

    def __init__(
            self,
            energy_meter_voltages_raw: Optional[bool] = None,
            energy_meters_raw: Optional[bool] = None,
            over_loads_raw: Optional[bool] = None,
            voltage_exceptions_raw: Optional[bool] = None
    ):
        self.energy_meter_voltages_raw = energy_meter_voltages_raw
        self.energy_meters_raw = energy_meters_raw
        self.over_loads_raw = over_loads_raw
        self.voltage_exceptions_raw = voltage_exceptions_raw


class ResultsConfig:
    raw_config: Optional[RawResultsConfig]
    stored_results_config: Optional[StoredResultsConfig]
    metrics_config: Optional[MetricsResultsConfig]

    def __init__(
            self,
            raw_config: Optional[RawResultsConfig] = None,
            stored_results_config: Optional[StoredResultsConfig] = None,
            metrics_config: Optional[MetricsResultsConfig] = None,
    ):
        self.raw_config = raw_config
        self.stored_results_config = stored_results_config
        self.metrics_config = metrics_config


class WorkPackageConfig:
    """ A data class representing the configuration for a hosting capacity work package """
    feeders: List[str]
    years: List[int]
    scenarios: List[str]
    model_config: Optional[ModelConfig]
    solve_config: Optional[SolveConfig]
    results_config: Optional[ResultsConfig]
    quality_assurance_processing: Optional[bool]

    def __init__(
            self,
            feeders: List[str],
            years: List[int],
            scenarios: List[str],
            model_config: ModelConfig,
            solve_config: Optional[SolveConfig] = None,
            results_config: Optional[ResultsConfig] = None,
            quality_assurance_processing: Optional[bool] = None,
    ):
        self.feeders = feeders
        self.years = years
        self.scenarios = scenarios
        self.model_config = model_config
        self.solve_config = solve_config
        self.results_config = results_config
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
