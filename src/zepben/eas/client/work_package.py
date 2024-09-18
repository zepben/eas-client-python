#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

__all__ = [
    "SwitchClass",
    "SwitchMeterPlacementConfig",
    "FixedTime",
    "TimePeriod",
    "LoadPlacement",
    "FeederScenarioAllocationStrategy",
    "MeterPlacementConfig",
    "ModelConfig",
    "SolveMode",
    "SolveConfig",
    "RawResultsConfig",
    "MetricsResultsConfig",
    "StoredResultsConfig",
    "GeneratorConfig",
    "ResultProcessorConfig",
    "WorkPackageConfig",
    "WorkPackageProgress",
    "WorkPackagesProgress",
    "EnhancedMetricsConfig",
    "WriterType",
    "WriterOutputConfig",
    "WriterConfig"
]


class SwitchClass(Enum):
    BREAKER = "BREAKER",
    DISCONNECTOR = "DISCONNECTOR",
    FUSE = "FUSE",
    JUMPER = "JUMPER",
    LOAD_BREAK_SWITCH = "LOAD_BREAK_SWITCH",
    RECLOSER = "RECLOSER"


@dataclass
class SwitchMeterPlacementConfig:
    meter_switch_class: Optional[SwitchClass] = None
    name_pattern: Optional[str] = None


class FixedTime:

    def __init__(self, time: datetime):
        self.time = time.replace(tzinfo=None)


class TimePeriod:

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


class LoadPlacement(Enum):
    PER_ENERGY_CONSUMER = "PER_ENERGY_CONSUMER"
    PER_USAGE_POINT = "PER_USAGE_POINT"


class FeederScenarioAllocationStrategy(Enum):
    RANDOM = "RANDOM"
    ADDITIVE = "ADDITIVE"


@dataclass
class MeterPlacementConfig:
    feeder_head: Optional[bool] = None
    dist_transformers: Optional[bool] = None
    switch_meter_placement_configs: Optional[List[SwitchMeterPlacementConfig]] = None
    energy_consumer_meter_group: Optional[str] = None


@dataclass
class ModelConfig:
    vm_pu: Optional[float] = None
    vmin_pu: Optional[float] = None
    vmax_pu: Optional[float] = None
    load_model: Optional[int] = None
    collapse_swer: Optional[bool] = None
    calibration: Optional[bool] = None
    p_factor_base_exports: Optional[float] = None
    p_factor_forecast_pv: Optional[float] = None
    p_factor_base_imports: Optional[float] = None
    fix_single_phase_loads: Optional[bool] = None
    max_single_phase_load: Optional[float] = None
    fix_overloading_consumers: Optional[bool] = None
    max_load_tx_ratio: Optional[float] = None
    max_gen_tx_ratio: Optional[float] = None
    fix_undersized_service_lines: Optional[bool] = None
    max_load_service_line_ratio: Optional[float] = None
    max_load_lv_line_ratio: Optional[float] = None
    collapse_lv_networks: Optional[bool] = None
    feeder_scenario_allocation_strategy: Optional[FeederScenarioAllocationStrategy] = None
    closed_loop_v_reg_enabled: Optional[bool] = None
    closed_loop_v_reg_replace_all: Optional[bool] = None
    closed_loop_v_reg_set_point: Optional[float] = None
    closed_loop_v_band: Optional[float] = None
    closed_loop_time_delay: Optional[int] = None
    closed_loop_v_limit: Optional[float] = None
    default_tap_changer_time_delay: Optional[int] = None
    default_tap_changer_set_point_pu: Optional[float] = None
    default_tap_changer_band: Optional[float] = None
    split_phase_default_load_loss_percentage: Optional[float] = None
    split_phase_lv_kv: Optional[float] = None
    swer_voltage_to_line_voltage: Optional[List[List[int]]] = None
    load_placement: Optional[LoadPlacement] = None
    load_interval_length_hours: Optional[float] = None
    meter_placement_config: Optional[MeterPlacementConfig] = None


class SolveMode(Enum):
    YEARLY = "YEARLY"
    DAILY = "DAILY"


@dataclass
class SolveConfig:
    norm_vmin_pu: Optional[float] = None
    norm_vmax_pu: Optional[float] = None
    emerg_vmin_pu: Optional[float] = None
    emerg_vmax_pu: Optional[float] = None
    base_frequency: Optional[int] = None
    voltage_bases: Optional[List[float]] = None
    max_iter: Optional[int] = None
    max_control_iter: Optional[int] = None
    mode: Optional[SolveMode] = None
    step_size_minutes: Optional[float] = None


@dataclass
class RawResultsConfig:
    energy_meter_voltages_raw: Optional[bool] = None
    energy_meters_raw: Optional[bool] = None
    results_per_meter: Optional[bool] = None
    overloads_raw: Optional[bool] = None
    voltage_exceptions_raw: Optional[bool] = None


@dataclass
class MetricsResultsConfig:
    calculate_performance_metrics: Optional[bool] = None


@dataclass
class StoredResultsConfig:
    energy_meter_voltages_raw: Optional[bool] = None
    energy_meters_raw: Optional[bool] = None
    overloads_raw: Optional[bool] = None
    voltage_exceptions_raw: Optional[bool] = None


@dataclass
class GeneratorConfig:
    model: Optional[ModelConfig] = None
    solve: Optional[SolveConfig] = None
    raw_results: Optional[RawResultsConfig] = None


@dataclass
class EnhancedMetricsConfig:
    populate_enhanced_metrics: Optional[bool] = None
    populate_enhanced_metrics_profile: Optional[bool] = None
    populate_duration_curves: Optional[bool] = None
    populate_constraints: Optional[bool] = None
    populate_weekly_reports: Optional[bool] = None
    calculate_normal_for_load_thermal: Optional[bool] = None
    calculate_emerg_for_load_thermal: Optional[bool] = None
    calculate_normal_for_gen_thermal: Optional[bool] = None
    calculate_emerg_for_gen_thermal: Optional[bool] = None
    calculate_co2: Optional[bool] = None


class WriterType(Enum):
    POSTGRES = "POSTGRES",
    PARQUET = "PARQUET"


@dataclass
class WriterOutputConfig:
    enhanced_metrics_config: Optional[EnhancedMetricsConfig] = None


@dataclass
class WriterConfig:
    writer_type: Optional[WriterType] = None
    output_writer_config: Optional[WriterOutputConfig] = None


@dataclass
class ResultProcessorConfig:
    stored_results: Optional[StoredResultsConfig] = None
    metrics: Optional[MetricsResultsConfig] = None
    writer_config: Optional[WriterConfig] = None


@dataclass
class WorkPackageConfig:
    """ A data class representing the configuration for a hosting capacity work package """
    feeders: List[str]
    years: List[int]
    scenarios: List[str]
    load_time: Union[TimePeriod, FixedTime]
    quality_assurance_processing: Optional[bool] = None
    generator_config: Optional[GeneratorConfig] = None
    executor_config: Optional[object] = None
    result_processor_config: Optional[ResultProcessorConfig] = None
    name: str = ""


@dataclass
class WorkPackageProgress:
    id: str
    progress_percent: int
    pending: List[str]
    generation: List[str]
    execution: List[str]
    result_processing: List[str]
    failure_processing: List[str]
    complete: List[str]


@dataclass
class WorkPackagesProgress:
    pending: List[str]
    in_progress: List[WorkPackageProgress]
