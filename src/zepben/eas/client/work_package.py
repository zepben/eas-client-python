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
    """The CIM class of Switch to create meters at"""

    name_pattern: Optional[str] = None
    """
    A Regex pattern to match on for Switch names. 
    The IdentifiedObject.name field will be used when matching against switches of the corresponding Switch class.
    """


class FixedTime:
    """
    A single point in time to model. Should be precise to the minute, and load data must be
    present for the provided time in the load database for accurate results.
    """

    def __init__(self, time: datetime):
        self.time = time.replace(tzinfo=None)


class TimePeriod:
    """
    A time period to model, from a start time to an end time. Maximum of 1 year.

    Load data must be available in the load database between the provided start and end time for accurate results.
    """

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
    """Whether to place a meter at the voltage source at the feeder head."""

    dist_transformers: Optional[bool] = None
    """Whether to place a meter at the secondary winding of each distribution transformer."""

    switch_meter_placement_configs: Optional[List[SwitchMeterPlacementConfig]] = None
    """Specifies which switch classes to place meters at, and the regex pattern to match for in the switch names."""

    energy_consumer_meter_group: Optional[str] = None
    """The ID of the meter group to use for populating EnergyMeters at EnergyConsumers."""


@dataclass
class ModelConfig:
    vm_pu: Optional[float] = None
    """Voltage per-unit of voltage source."""

    vmin_pu: Optional[float] = None
    """
    Minimum per unit voltage for which the load model selected and generator model is assumed to apply. Below this value, the load/gen model reverts to a 
    constant impedance model. For generator model used, this is used to determine the upper current limit. For example, if Vminpu is 0.90 then the current 
    limit is (1/0.90) = 111%.
    """

    vmax_pu: Optional[float] = None
    """
    Maximum per unit voltage for which the load model selected and generator model is assumed to apply. Above this value, the load/gen model reverts to a 
    constant impedance model.
    """

    load_model: Optional[int] = None
    """
    Specifies how loads and generators in OpenDSS should be modelled. Options:
    1: Standard constant P+jQ load. (Default)
    2: Constant impedance load.
    3: Const P, Quadratic Q (like a motor).
    4: Nominal Linear P, Quadratic Q (feeder mix). Use this with CVRfactor.
    5: Constant Current Magnitude
    6: Const P, Fixed Q
    7: Const P, Fixed Impedance Q
    """

    collapse_swer: Optional[bool] = None
    """Whether to collapse/simplify SWER network."""

    calibration: Optional[bool] = None
    """
    Whether to apply calibration modifications to the model. This will create point-in-time models using PQ data.
    """

    p_factor_base_exports: Optional[float] = None
    """
    Power factor to set for base model Generators during model translation. If null the model will use the reactive power specified in the load profiles.
    """

    p_factor_forecast_pv: Optional[float] = None
    """
    Power factor to set for scenario (forecast) model Generators during model translation.
    """

    p_factor_base_imports: Optional[float] = None
    """
    Power factor to set for base model Loads during model translation. If null the model will use the reactive power specified in the load profiles.
    """

    fix_single_phase_loads: Optional[bool] = None
    """
    Finds consumers that have a peak load (within the modelled time period) greater than the configured max_single_phase_load value (default 30kW), and upgrades
    them to three-phase loads. The intent is to correct data inaccuracies where the number of phases reported for a consumer appears to be incorrect. 
    By default, we expect a 30kW load would not appear on a single phase consumer, so we upgrade them to three-phase. This consists of tracing upstream to the 
    distribution transformer and spreading 3 phases (ABCN) back to the transformer where possible.
    """

    max_single_phase_load: Optional[float] = None
    """
    The max peak load for a single phase customer, beyond which will trigger the single phase load fixing algorithm mentioned above.
    """

    fix_overloading_consumers: Optional[bool] = None
    """
    Finds consumers that have peak load or generation (within the modelled time period) greater than the capacity of the transformer they are attached to by a 
    configurable factor, and then reconfigures them to be HV consumers (attached above the transformer). The aim is to identify HV consumers that have been 
    incorrectly connected as LV consumers, and resolve this connectivity.
    """

    max_load_tx_ratio: Optional[float] = None
    """
    The maximum load to transformer rating ratio for a single consumer to trigger the overloading consumer fixer.
    For example given a ratio of 2, if a customer with a peak 30kW load was downstream of a 10kVA transformer, this would be a ratio of 3:1 and thus trigger
    the overloading consumers fixer.
    """

    max_gen_tx_ratio: Optional[float] = None
    """
    The maximum generation to transformer rating ratio for a single consumer to trigger the overloading consumer fixer.
    For example given a ratio of 2, if a customer with peak generation of 30kW was downstream of a 10kVA transformer, this would be a ratio of 3:1 and thus 
    trigger the overloading consumers fixer.
    """

    fix_undersized_service_lines: Optional[bool] = None
    """
    Finds consumers that have a peak load (within the modelled time period) greater than the capacity of the service line of the consumer by some configured 
    factor. The intent is to find service lines that have unrealistically low current ratings which would stop convergence, and upgrade them to sensible 
    ratings. 
    
    When a conductors rating is upgraded, we also then upgrade the impedances to a type in line with the new rating, utilising a pre-configured
    catalogue of rating and impedance data, and matching the phase configuration of the consumer.
    """

    max_load_service_line_ratio: Optional[float] = None
    """
    The maximum load to service line rating ratio to trigger the undersized service lines fixer. For example given a ratio of 2, if a customer with peak 
    load of 10kW had a service line supporting only 5kVA, this would be a ratio of 2:1 and thus 
    trigger the undersized service line fixer.
    
    Note service lines are generally considered to be the conductors immediately connecting to a consumer.
    """

    max_load_lv_line_ratio: Optional[float] = None
    """
    The maximum load to LV line rating ratio to trigger the undersized service lines fixer for LV conductors. For example given a ratio of 5, if a customer 
    with peak load of 50kW was connected to LV backbone conductors supporting only 10kVA, this would be a ratio of 5:1 and thus 
    trigger the undersized service line fixer for the LV conductors.
    
    Note the LV line fixer will fix all conductors upstream of the consumer up to the distribution transformer they are connected to.
    """

    collapse_lv_networks: Optional[bool] = None
    """Flag to control whether to collapse lv network in the model."""

    feeder_scenario_allocation_strategy: Optional[FeederScenarioAllocationStrategy] = None
    """
    Strategy for scenario ev, pv and bess allocation. ADDITIVE will be each year is built upon the last years allocation, 
    while RANDOM will be a different allocation every year.
    """

    closed_loop_v_reg_enabled: Optional[bool] = None
    """Create models with a Closed Loop Voltage Regulator at the Zone sub. If false, existing voltage regulator's in the zone sub will be used."""

    closed_loop_v_reg_replace_all: Optional[bool] = None
    """
    Replace all existing Voltage Regulators with Closed Loop Voltage Regulator. If false existing zone sub regulators will be
    modelled as-is which may be in non-closed loop configuration.
    """

    closed_loop_v_reg_set_point: Optional[float] = None
    """Scaling factor for the base voltage to form the set point (0.0-2.0)."""

    closed_loop_v_band: Optional[float] = None
    """VBand value in percentage."""

    closed_loop_time_delay: Optional[int] = None
    """Time delay in seconds."""

    closed_loop_v_limit: Optional[float] = None
    """Maximum voltage at regulating transformer's secondary bus."""

    default_tap_changer_time_delay: Optional[int] = None
    """Time delay in seconds for the default tap changer"""

    default_tap_changer_set_point_pu: Optional[float] = None
    """Default tap changer set point"""

    default_tap_changer_band: Optional[float] = None
    """Default tap changer band value"""

    split_phase_default_load_loss_percentage: Optional[float] = None
    """
    Default load loss percentage for split phase transformers.
    """

    split_phase_lv_kv: Optional[float] = None

    swer_voltage_to_line_voltage: Optional[List[List[int]]] = None
    """
    Mapping of SWER voltages to L2L voltages.
    """

    load_placement: Optional[LoadPlacement] = None
    """
    Where to create loads - either for each UsagePoint or for each EnergyConsumer.
    """

    load_interval_length_hours: Optional[float] = None
    """
    Fraction of an hour for load data. 1.0 = 60 minute intervals, 0.5 = 30 minute intervals.
    """

    meter_placement_config: Optional[MeterPlacementConfig] = None
    """Configuration to determine where to place EnergyMeters for collecting results"""

    seed: Optional[int] = None
    """A seed to use when generating the model. Re-using the same seed will result in the same model being generated."""

    default_load_watts: Optional[List[float]] = None
    """
    A list of readings to be used as default load watts when no load data is found.
    Can be either a yearly or daily profile. 
    The number of entries must match the expected number for the configured load_interval_length_hours.
    For load_interval_length_hours:
        0.25: 96 entries for daily and 35040 for yearly
        0.5: 48 entries for daily and 17520 for yearly
        1.0: 24 entries for daily and 8760 for yearly
    """

    default_gen_watts: Optional[List[float]] = None
    """
    A list of readings to be used as default gen watts when no load data is found.
    Can be either a yearly or daily profile.
    The number of entries must match the expected number for the configured load_interval_length_hours.
    For load_interval_length_hours:
        0.25: 96 entries for daily and 35040 for yearly
        0.5: 48 entries for daily and 17520 for yearly
        1.0: 24 entries for daily and 8760 for yearly
    """

    default_load_var: Optional[List[float]] = None
    """
    A list of readings to be used as default load car when no load data is found.
    Can be either a yearly or daily profile.
    The number of entries must match the number of entries in default_load_watts, and the expected number for the configured load_interval_length_hours.
    For load_interval_length_hours:
        0.25: 96 entries for daily and 35040 for yearly
        0.5: 48 entries for daily and 17520 for yearly
        1.0: 24 entries for daily and 8760 for yearly
    """

    default_gen_var: Optional[List[float]] = None
    """
    A list of readings to be used as default gen var when no load data is found.
    Can be either a yearly or daily profile.
    The number of entries must match the number of entries in default_gen_watts, and the expected number for the configured load_interval_length_hours.
    For load_interval_length_hours:
        0.25: 96 entries for daily and 35040 for yearly
        0.5: 48 entries for daily and 17520 for yearly
        1.0: 24 entries for daily and 8760 for yearly
    """


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
    """Max iterations before failing"""

    max_control_iter: Optional[int] = None
    """Max control iterations before failing"""

    mode: Optional[SolveMode] = None
    """Run OpenDSS in yearly or daily mode"""

    step_size_minutes: Optional[float] = None
    """The step size to solve"""


@dataclass
class RawResultsConfig:
    """
    Whether to produce raw results generated from OpenDSS.
    You will likely always want defaults for this, as setting any of these to False will limit
    the results you get and should only be used as a potential performance optimisation if they are unnecessary.
    """

    energy_meter_voltages_raw: Optional[bool] = None
    """
    Produce energy meter voltages results.
    """

    energy_meters_raw: Optional[bool] = None
    """
    Produce energy meter results.
    """

    results_per_meter: Optional[bool] = None
    """
    Produce results per EnergyMeter
    """

    overloads_raw: Optional[bool] = None
    """
    Produce overloads
    """

    voltage_exceptions_raw: Optional[bool] = None
    """
    Produce voltage exceptions
    """


@dataclass
class MetricsResultsConfig:
    """
    Calculated metrics based off the raw results
    """

    calculate_performance_metrics: Optional[bool] = None
    """Whether to calculate basic performance metrics"""


@dataclass
class StoredResultsConfig:
    """
    The raw results that will be stored.
    Note storing raw results will utilise a lot of storage space and should be avoided for
    large runs.
    """

    energy_meter_voltages_raw: Optional[bool] = None
    """
    WARNING: Will store a significant amount of data
    Store the raw EnergyMeter timeseries voltage results
    """

    energy_meters_raw: Optional[bool] = None
    """
    WARNING: Will store a significant amount of data
    Store the raw EnergyMeter timeseries results
    """

    overloads_raw: Optional[bool] = None
    """
    WARNING: Will store a significant amount of data
    Store the raw overload results
    """

    voltage_exceptions_raw: Optional[bool] = None
    """
    WARNING: Will store a significant amount of data
    Store the raw voltage exception results
    """


@dataclass
class GeneratorConfig:
    """
    Configuration settings for the OpenDSS model.
    These settings make changes to the network and specific OpenDSS settings prior to model execution.
    """

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
    """
    Whether to write output to Parquet files or a Postgres database.
    Check with your administrator which result types are supported.
    """

    output_writer_config: Optional[WriterOutputConfig] = None
    """The results to store"""


@dataclass
class ResultProcessorConfig:
    """
    Configuration specific to processing of results.
    """

    stored_results: Optional[StoredResultsConfig] = None
    """Raw results to be stored"""

    metrics: Optional[MetricsResultsConfig] = None
    """Whether to calculate and store basic performance metrics"""

    writer_config: Optional[WriterConfig] = None
    """Where results should be stored (Parquet or Postgres) and which metrics to store"""


@dataclass
class WorkPackageConfig:
    """ A data class representing the configuration for a hosting capacity work package """
    name: str
    feeders: List[str]
    """The feeders to process in this work package"""

    years: List[int]
    """
    The years to process for the specified feeders in this work package.
    The years should be configured in the input database forecasts for all supplied scenarios.
    """

    scenarios: List[str]
    """
    The scenarios to model. These should be configured in the input.scenario_configuration table.
    """

    load_time: Union[TimePeriod, FixedTime]
    """
    The time to use for the base load data. The provided time[s] must be available in the
    load database for accurate results. Specifying an invalid time (i.e one with no load data) will
    result in inaccurate results.
    """

    quality_assurance_processing: Optional[bool] = None
    """Whether to enable QA processing"""

    generator_config: Optional[GeneratorConfig] = None
    """Configuration for the OpenDSS model generator"""

    executor_config: Optional[object] = None
    """Executor config - currently unused."""

    result_processor_config: Optional[ResultProcessorConfig] = None
    """Configuration for processing and storing results"""


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
