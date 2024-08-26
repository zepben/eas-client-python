#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
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


class SwitchMeterPlacementConfig:
    meter_switch_class: Optional[SwitchClass]
    name_pattern: Optional[str]

    def __init__(
            self,
            meter_switch_class: Optional[SwitchClass],
            name_pattern: Optional[str]
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


class LoadPlacement(Enum):
    PER_ENERGY_CONSUMER = "PER_ENERGY_CONSUMER"
    PER_USAGE_POINT = "PER_USAGE_POINT"


class FeederScenarioAllocationStrategy(Enum):
    RANDOM = "RANDOM"
    ADDITIVE = "ADDITIVE"


class MeterPlacementConfig:
    feeder_head: Optional[bool]
    dist_transformers: Optional[bool]
    switch_meter_placement_configs: Optional[List[SwitchMeterPlacementConfig]]
    energy_consumer_meter_group: Optional[str]

    def __init__(
            self,
            feeder_head: Optional[bool] = None,
            dist_transformers: Optional[bool] = None,
            switch_meter_placement_configs: Optional[List[SwitchMeterPlacementConfig]] = None,
            energy_consumer_meter_group: Optional[str] = None
    ):
        self.feeder_head = feeder_head
        self.dist_transformers = dist_transformers
        self.switch_meter_placement_configs = switch_meter_placement_configs
        self.energy_consumer_meter_group = energy_consumer_meter_group


class ModelConfig:
    vm_pu: Optional[float]
    vmin_pu: Optional[float]
    vmax_pu: Optional[float]
    load_model: Optional[int]
    collapse_swer: Optional[bool]
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
    max_load_service_line_ratio: Optional[float]
    max_load_lv_line_ratio: Optional[float]
    collapse_lv_networks: Optional[bool]
    feeder_scenario_allocation_strategy: Optional[FeederScenarioAllocationStrategy]
    closed_loop_v_reg_enabled: Optional[bool]
    closed_loop_v_reg_replace_all: Optional[bool]
    closed_loop_v_reg_set_point: Optional[float]
    closed_loop_v_band: Optional[float]
    closed_loop_time_delay: Optional[int]
    closed_loop_v_limit: Optional[float]
    default_tap_changer_time_delay: Optional[int]
    default_tap_changer_set_point_pu: Optional[float]
    default_tap_changer_band: Optional[float]
    split_phase_default_load_loss_percentage: Optional[float]
    split_phase_lv_kv: Optional[float]
    swer_voltage_to_line_voltage: Optional[List[List[int]]]
    load_placement: Optional[LoadPlacement]
    load_interval_length_hours: Optional[float]
    meter_placement_config: Optional[MeterPlacementConfig]

    def __init__(
            self,
            vm_pu: Optional[float] = None,
            vmin_pu: Optional[float] = None,
            vmax_pu: Optional[float] = None,
            load_model: Optional[int] = None,
            collapse_swer: Optional[bool] = None,
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
            max_load_service_line_ratio: Optional[float] = None,
            max_load_lv_line_ratio: Optional[float] = None,
            collapse_lv_networks: Optional[bool] = None,
            feeder_scenario_allocation_strategy: Optional[FeederScenarioAllocationStrategy] = None,
            closed_loop_v_reg_enabled: Optional[bool] = None,
            closed_loop_v_reg_replace_all: Optional[bool] = None,
            closed_loop_v_reg_set_point: Optional[float] = None,
            closed_loop_v_band: Optional[float] = None,
            closed_loop_time_delay: Optional[int] = None,
            closed_loop_v_limit: Optional[float] = None,
            default_tap_changer_time_delay: Optional[int] = None,
            default_tap_changer_set_point_pu: Optional[float] = None,
            default_tap_changer_band: Optional[float] = None,
            split_phase_default_load_loss_percentage: Optional[float] = None,
            split_phase_lv_kv: Optional[float] = None,
            swer_voltage_to_line_voltage: Optional[List[List[int]]] = None,
            load_placement: Optional[LoadPlacement] = None,
            load_interval_length_hours: Optional[float] = None,
            meter_placement_config: Optional[MeterPlacementConfig] = None,
    ):
        self.vm_pu = vm_pu
        self.vmin_pu = vmin_pu
        self.vmax_pu = vmax_pu
        self.load_model = load_model
        self.collapse_swer = collapse_swer
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
        self.max_load_service_line_ratio = max_load_service_line_ratio
        self.max_load_lv_line_ratio = max_load_lv_line_ratio
        self.collapse_lv_networks = collapse_lv_networks
        self.feeder_scenario_allocation_strategy = feeder_scenario_allocation_strategy
        self.closed_loop_v_reg_enabled = closed_loop_v_reg_enabled
        self.closed_loop_v_reg_replace_all = closed_loop_v_reg_replace_all
        self.closed_loop_v_reg_set_point = closed_loop_v_reg_set_point
        self.closed_loop_v_band = closed_loop_v_band
        self.closed_loop_time_delay = closed_loop_time_delay
        self.closed_loop_v_limit = closed_loop_v_limit
        self.default_tap_changer_time_delay = default_tap_changer_time_delay
        self.default_tap_changer_set_point_pu = default_tap_changer_set_point_pu
        self.default_tap_changer_band = default_tap_changer_band
        self.split_phase_default_load_loss_percentage = split_phase_default_load_loss_percentage
        self.split_phase_lv_kv = split_phase_lv_kv
        self.swer_voltage_to_line_voltage = swer_voltage_to_line_voltage
        self.load_placement = load_placement
        self.load_interval_length_hours = load_interval_length_hours
        self.meter_placement_config = meter_placement_config


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
    overloads_raw: Optional[bool]
    voltage_exceptions_raw: Optional[bool]

    def __init__(
            self,
            energy_meter_voltages_raw: Optional[bool] = None,
            energy_meters_raw: Optional[bool] = None,
            results_per_meter: Optional[bool] = None,
            overloads_raw: Optional[bool] = None,
            voltage_exceptions_raw: Optional[bool] = None,
    ):
        self.energy_meter_voltages_raw = energy_meter_voltages_raw
        self.energy_meters_raw = energy_meters_raw
        self.results_per_meter = results_per_meter
        self.overloads_raw = overloads_raw
        self.voltage_exceptions_raw = voltage_exceptions_raw


class MetricsResultsConfig:
    calculate_performance_metrics: Optional[bool]

    def __init__(self, calculate_performance_metrics: Optional[bool] = None):
        self.calculate_performance_metrics = calculate_performance_metrics


class StoredResultsConfig:
    energy_meter_voltages_raw: Optional[bool]
    energy_meters_raw: Optional[bool]
    overloads_raw: Optional[bool]
    voltage_exceptions_raw: Optional[bool]

    def __init__(
            self,
            energy_meter_voltages_raw: Optional[bool] = None,
            energy_meters_raw: Optional[bool] = None,
            overloads_raw: Optional[bool] = None,
            voltage_exceptions_raw: Optional[bool] = None,
    ):
        self.energy_meter_voltages_raw = energy_meter_voltages_raw
        self.energy_meters_raw = energy_meters_raw
        self.overloads_raw = overloads_raw
        self.voltage_exceptions_raw = voltage_exceptions_raw


class GeneratorConfig:
    model: Optional[ModelConfig]
    solve: Optional[SolveConfig]
    raw_results: Optional[RawResultsConfig]

    def __init__(
            self,
            model: Optional[ModelConfig] = None,
            solve: Optional[SolveConfig] = None,
            raw_results: Optional[RawResultsConfig] = None,
    ):
        self.model = model
        self.solve = solve
        self.raw_results = raw_results


class EnhancedMetricsConfig:
    populate_enhanced_metrics: Optional[bool]
    populate_enhanced_metrics_profile: Optional[bool]
    populate_duration_curves: Optional[bool]
    populate_constraints: Optional[bool]
    populate_weekly_reports: Optional[bool]
    calculate_normal_for_load_thermal: Optional[bool]
    calculate_emerg_for_load_thermal: Optional[bool]
    calculate_normal_for_gen_thermal: Optional[bool]
    calculate_emerg_for_gen_thermal: Optional[bool]
    calculate_co2: Optional[bool]

    def __init__(
            self,
            populate_enhanced_metrics: Optional[bool] = None,
            populate_enhanced_metrics_profile: Optional[bool] = None,
            populate_duration_curves: Optional[bool] = None,
            populate_constraints: Optional[bool] = None,
            populate_weekly_reports: Optional[bool] = None,
            calculate_normal_for_load_thermal: Optional[bool] = None,
            calculate_emerg_for_load_thermal: Optional[bool] = None,
            calculate_normal_for_gen_thermal: Optional[bool] = None,
            calculate_emerg_for_gen_thermal: Optional[bool] = None,
            calculate_co2: Optional[bool] = None
    ):
        self.populate_enhanced_metrics = populate_enhanced_metrics
        self.populate_enhanced_metrics_profile = populate_enhanced_metrics_profile
        self.populate_duration_curves = populate_duration_curves
        self.populate_constraints = populate_constraints
        self.populate_weekly_reports = populate_weekly_reports
        self.calculate_normal_for_load_thermal = calculate_normal_for_load_thermal
        self.calculate_emerg_for_load_thermal = calculate_emerg_for_load_thermal
        self.calculate_normal_for_gen_thermal = calculate_normal_for_gen_thermal
        self.calculate_emerg_for_gen_thermal = calculate_emerg_for_gen_thermal
        self.calculate_co2 = calculate_co2


class WriterType(Enum):
    POSTGRES = "POSTGRES",
    PARQUET = "PARQUET"


class WriterOutputConfig:
    enhanced_metrics_config: Optional[EnhancedMetricsConfig]

    def __init__(
            self,
            enhanced_metrics_config: Optional[EnhancedMetricsConfig] = None
    ):
        self.enhanced_metrics_config = enhanced_metrics_config


class WriterConfig:
    writer_type: Optional[WriterType]
    output_writer_config: Optional[WriterOutputConfig]

    def __init__(
            self,
            writer_type: Optional[WriterType] = None,
            output_writer_config: Optional[WriterOutputConfig] = None
    ):
        self.writer_type = writer_type
        self.output_writer_config = output_writer_config


class ResultProcessorConfig:
    stored_results: Optional[StoredResultsConfig]
    metrics: Optional[MetricsResultsConfig]
    writer_config: Optional[WriterConfig]

    def __init__(
            self,
            stored_results: Optional[StoredResultsConfig] = None,
            metrics: Optional[MetricsResultsConfig] = None,
            writer_config: Optional[WriterConfig] = None
    ):
        self.stored_results = stored_results
        self.metrics = metrics
        self.writer_config = writer_config


class WorkPackageConfig:
    """ A data class representing the configuration for a hosting capacity work package """
    feeders: List[str]
    years: List[int]
    scenarios: List[str]
    load_time: Union[TimePeriod, FixedTime]
    quality_assurance_processing: Optional[bool]
    generator_config: Optional[GeneratorConfig]
    executor_config: Optional[object]
    result_processor_config: Optional[ResultProcessorConfig]

    def __init__(
            self,
            feeders: List[str] = None,
            years: List[int] = None,
            scenarios: List[str] = None,
            load_time: Union[TimePeriod, FixedTime] = None,
            quality_assurance_processing: Optional[bool] = None,
            generator_config: Optional[GeneratorConfig] = None,
            executor_config: Optional[object] = None,
            result_processor_config: Optional[ResultProcessorConfig] = None,
    ):
        self.feeders = feeders
        self.years = years
        self.scenarios = scenarios
        self.load_time = load_time
        self.quality_assurance_processing = quality_assurance_processing
        self.generator_config = generator_config
        self.executor_config = executor_config
        self.result_processor_config = result_processor_config


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
