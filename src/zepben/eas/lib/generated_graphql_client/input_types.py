from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import (
    CandidateGenerationType,
    HcFeederScenarioAllocationStrategy,
    HcLoadPlacement,
    HcSolveMode,
    HcSwitchClass,
    HcWriterType,
    IngestorRunState,
    IngestorRuntimeKind,
    InterventionClass,
    SectionType,
    SortOrder,
)


class AppOptionsInput(BaseModel):
    """Input for updating application configuration options."""

    asset_name_format: Optional[str] = Field(alias="assetNameFormat", default=None)
    pole_string_format: Optional[str] = Field(alias="poleStringFormat", default=None)


class CandidateGenerationConfigInput(BaseModel):
    average_voltage_spread_threshold: Optional[int] = Field(
        alias="averageVoltageSpreadThreshold", default=None
    )
    "The threshold for average line voltage spread under the transformer over the year, in volts. Voltage spread at each timestep is calculated by taking the difference between the maximum and minimum phase-to-phase voltage over the nodes under the transformer, for each phase, then taking the maximum of that difference across all phases. When the average voltage spread exceeds this threshold, it indicates that the transformer is experiencing a significant voltage swing that may impact system stability. Only used when `type` is `TAP_OPTIMIZATION`."
    intervention_criteria_name: Optional[str] = Field(
        alias="interventionCriteriaName", default=None
    )
    "The ID of the set of criteria used to select intervention candidates from enhanced metrics of the base work package run. Only used when `type` is `CRITERIA`."
    tap_weighting_factor_lower_threshold: Optional[float] = Field(
        alias="tapWeightingFactorLowerThreshold", default=None
    )
    "The minimum threshold for the tap weighting factor, used to determine when a positive tap adjustment (increasing voltage) is prioritized. If the tap weighting factor falls below this threshold, it indicates that the voltage is significantly under the desired range and requires corrective action. This setting is usually negative. Only used when `type` is `TAP_OPTIMIZATION`."
    tap_weighting_factor_upper_threshold: Optional[float] = Field(
        alias="tapWeightingFactorUpperThreshold", default=None
    )
    "The maximum threshold for the tap weighting factor, used to determine when a negative tap adjustment (decreasing voltage) is prioritized. If the tap weighting factor exceeds this threshold, it indicates that the voltage is significantly over the desired range and requires corrective action. This setting is usually positive. Only used when `type` is `TAP_OPTIMIZATION`."
    type_: CandidateGenerationType = Field(alias="type")
    "The type of method for generating the intervention candidates."
    voltage_over_limit_hours_threshold: Optional[int] = Field(
        alias="voltageOverLimitHoursThreshold", default=None
    )
    "The threshold for number of hours a transformer is above the nominal voltage range. Only used when `type` is `TAP_OPTIMIZATION`."
    voltage_under_limit_hours_threshold: Optional[int] = Field(
        alias="voltageUnderLimitHoursThreshold", default=None
    )
    "The threshold for number of hours a transformer is below the nominal voltage range. Only used when `type` is `TAP_OPTIMIZATION`."


class DvmsConfigInput(BaseModel):
    lower_limit: float = Field(alias="lowerLimit")
    "The lower limit of voltage (p.u.) considered acceptable for the purposes of DVMS."
    lower_percentile: float = Field(alias="lowerPercentile")
    "The lowest percentile of customers' voltages to consider when applying DVMS."
    max_iterations: int = Field(alias="maxIterations")
    "The number of iterations to attempt DVMS for each timestep before moving on."
    regulator_config: "DvmsRegulatorConfigInput" = Field(alias="regulatorConfig")
    "Configures the voltage regulator to apply if the zone is already satisfactory according to the above limits."
    upper_limit: float = Field(alias="upperLimit")
    "The upper limit of voltage (p.u.) considered acceptable for the purposes of DVMS."
    upper_percentile: float = Field(alias="upperPercentile")
    "The highest percentile of customers' voltages to consider when applying DVMS."


class DvmsRegulatorConfigInput(BaseModel):
    allow_push_to_limit: bool = Field(alias="allowPushToLimit")
    "If this is true, we allow the regulator to push some number of customers outside the specified limits for DVMS, with the limit of customers given by lowerPercentile and upperPercentile in DvmsConfig."
    max_tap_change_per_step: int = Field(alias="maxTapChangePerStep")
    "The maximum number of tap steps to move (in either direction) for each timestep."
    pu_deadband_percent: float = Field(alias="puDeadbandPercent")
    "Width of window of voltages considered acceptable for the average customer voltage, in %p.u."
    pu_target: float = Field(alias="puTarget")
    "Voltage p.u. to move the average customer voltage towards."


class FeederConfigInput(BaseModel):
    feeder: str
    "The mRIDs of feeder to solve as part of this work package. Each feeder will be solved independently."
    fixed_time: Optional["FixedTimeInput"] = Field(alias="fixedTime", default=None)
    "Fixed Time setting for load retrieval, can not be set with time period setting."
    scenarios: list[str]
    "The IDs of scenarios to solve for."
    time_period: Optional["TimePeriodInput"] = Field(alias="timePeriod", default=None)
    "Time period setting for load retrieval, can not be set with fixed time setting."
    years: list[int]
    "The years to solve for. This is primarily used for fetching scenario data and calculating load growth."


class FeederConfigsInput(BaseModel):
    configs: list["FeederConfigInput"]
    "The mRIDs of feeders to solve for this work package. Each feeder will be solved independently."


class FeederLoadAnalysisInput(BaseModel):
    aggregate_at_feeder_level: bool = Field(alias="aggregateAtFeederLevel")
    "Request for a report which aggregate all downstream load at the feeder level"
    end_date: str = Field(alias="endDate")
    "End date for this analysis"
    feeders: Optional[list[str]] = None
    "The mRIDs of feeders to solve for feeder load analysis."
    fetch_lv_network: bool = Field(alias="fetchLvNetwork")
    "Whether to stop analysis at distribution transformer"
    fla_forecast_config: Optional["FlaForecastConfigInput"] = Field(
        alias="flaForecastConfig", default=None
    )
    "Configuration for forecast FLA study"
    geographical_regions: Optional[list[str]] = Field(
        alias="geographicalRegions", default=None
    )
    "The mRIDs of Geographical Region to solve for feeder load analysis."
    output: Optional[str] = None
    "The file name of the resulting study"
    process_coincident_loads: bool = Field(alias="processCoincidentLoads")
    "Whether to include values corresponding to conductor event time points in the report"
    process_feeder_loads: bool = Field(alias="processFeederLoads")
    "Whether to include values corresponding to feeder event time points in the report"
    produce_conductor_report: bool = Field(alias="produceConductorReport")
    "Request for an extensive report"
    start_date: str = Field(alias="startDate")
    "Start date for this analysis"
    sub_geographical_regions: Optional[list[str]] = Field(
        alias="subGeographicalRegions", default=None
    )
    "The mRIDs of sub-Geographical Region to solve for feeder load analysis."
    substations: Optional[list[str]] = None
    "The mRIDs of substations to solve for feeder load analysis."


class FixedTimeInput(BaseModel):
    load_time: Any = Field(alias="loadTime")
    "The fixed time point to use for load retrieval."
    overrides: Optional[list["FixedTimeLoadOverrideInput"]] = None
    "The list of load override profiles."


class FixedTimeLoadOverrideInput(BaseModel):
    gen_var_override: Optional[list[float]] = Field(
        alias="genVarOverride", default=None
    )
    gen_watts_override: Optional[list[float]] = Field(
        alias="genWattsOverride", default=None
    )
    load_id: str = Field(alias="loadId")
    load_var_override: Optional[list[float]] = Field(
        alias="loadVarOverride", default=None
    )
    load_watts_override: Optional[list[float]] = Field(
        alias="loadWattsOverride", default=None
    )


class FlaForecastConfigInput(BaseModel):
    bess_upgrade_threshold: Optional[int] = Field(
        alias="bessUpgradeThreshold", default=None
    )
    "Watts threshold to indicate if a customer site will gain additional battery during scenario application"
    pv_upgrade_threshold: Optional[int] = Field(
        alias="pvUpgradeThreshold", default=None
    )
    "Watts threshold to indicate if a customer site will gain additional pv during scenario application"
    scenario_id: str = Field(alias="scenarioID")
    "The id of forecast scenario"
    seed: Optional[int] = None
    "Seed for scenario application"
    year: int
    "The year for forecast model"


class ForecastConfigInput(BaseModel):
    feeders: list[str]
    "The mRIDs of feeders to solve for this work package. Each feeder will be solved independently."
    fixed_time: Optional["FixedTimeInput"] = Field(alias="fixedTime", default=None)
    "Fixed Time setting for load retrieval, can not be set with time period setting."
    scenarios: list[str]
    "The IDs of scenarios to solve for."
    time_period: Optional["TimePeriodInput"] = Field(alias="timePeriod", default=None)
    "Time period setting for load retrieval, can not be set with fixed time setting."
    years: list[int]
    "The years to solve for. This is primarily used for fetching scenario data and calculating load growth."


class GeoJsonOverlayInput(BaseModel):
    data: Any
    source_properties: Optional[Any] = Field(alias="sourceProperties", default=None)
    styles: list[str]


class GetOpenDssModelsFilterInput(BaseModel):
    is_public: Optional[bool] = Field(alias="isPublic", default=None)
    name: Optional[str] = None
    state: Optional[list[str]] = None


class GetOpenDssModelsSortCriteriaInput(BaseModel):
    created_at: Optional[SortOrder] = Field(alias="createdAt", default=None)
    is_public: Optional[SortOrder] = Field(alias="isPublic", default=None)
    name: Optional[SortOrder] = None
    state: Optional[SortOrder] = None


class GetPowerFactoryModelTemplatesFilterInput(BaseModel):
    is_public: Optional[bool] = Field(alias="isPublic", default=None)
    name: Optional[str] = None


class GetPowerFactoryModelTemplatesSortCriteriaInput(BaseModel):
    created_at: Optional[SortOrder] = Field(alias="createdAt", default=None)
    is_public: Optional[SortOrder] = Field(alias="isPublic", default=None)
    name: Optional[SortOrder] = None


class GetPowerFactoryModelsFilterInput(BaseModel):
    is_public: Optional[bool] = Field(alias="isPublic", default=None)
    name: Optional[str] = None
    state: Optional[list[str]] = None


class GetPowerFactoryModelsSortCriteriaInput(BaseModel):
    created_at: Optional[SortOrder] = Field(alias="createdAt", default=None)
    is_public: Optional[SortOrder] = Field(alias="isPublic", default=None)
    name: Optional[SortOrder] = None
    state: Optional[SortOrder] = None


class GetSincalModelPresetsFilterInput(BaseModel):
    is_public: Optional[bool] = Field(alias="isPublic", default=None)
    name: Optional[str] = None


class GetSincalModelPresetsSortCriteriaInput(BaseModel):
    created_at: Optional[SortOrder] = Field(alias="createdAt", default=None)
    is_public: Optional[SortOrder] = Field(alias="isPublic", default=None)
    name: Optional[SortOrder] = None


class GetSincalModelsFilterInput(BaseModel):
    is_public: Optional[bool] = Field(alias="isPublic", default=None)
    name: Optional[str] = None
    state: Optional[list[str]] = None


class GetSincalModelsSortCriteriaInput(BaseModel):
    created_at: Optional[SortOrder] = Field(alias="createdAt", default=None)
    is_public: Optional[SortOrder] = Field(alias="isPublic", default=None)
    name: Optional[SortOrder] = None
    state: Optional[SortOrder] = None


class GetStudiesFilterInput(BaseModel):
    created_after: Optional[Any] = Field(alias="createdAfter", default=None)
    created_before: Optional[Any] = Field(alias="createdBefore", default=None)
    created_by: Optional[list[str]] = Field(alias="createdBy", default=None)
    id: Optional[str] = None
    name: Optional[str] = None
    tags: Optional[list[str]] = None


class GetStudiesSortCriteriaInput(BaseModel):
    created_at: Optional[SortOrder] = Field(alias="createdAt", default=None)
    created_by: Optional[SortOrder] = Field(alias="createdBy", default=None)
    description: Optional[SortOrder] = None
    name: Optional[SortOrder] = None


class GqlDistributionTransformerConfigInput(BaseModel):
    r_ground: float = Field(alias="rGround")
    x_ground: float = Field(alias="xGround")


class GqlLoadConfigInput(BaseModel):
    spread_max_demand: bool = Field(alias="spreadMaxDemand")


class GqlScenarioConfigInput(BaseModel):
    bess_upgrade_threshold: int = Field(alias="bessUpgradeThreshold")
    pv_upgrade_threshold: int = Field(alias="pvUpgradeThreshold")
    scenario_id: str = Field(alias="scenarioID")
    years: list[int]


class GqlSincalModelForecastSpecInput(BaseModel):
    scenario_id: str = Field(alias="scenarioId")
    year: int


class HcEnhancedMetricsConfigInput(BaseModel):
    calculate_co_2: Optional[bool] = Field(alias="calculateCO2", default=None)
    calculate_emerg_for_gen_thermal: Optional[bool] = Field(
        alias="calculateEmergForGenThermal", default=None
    )
    calculate_emerg_for_load_thermal: Optional[bool] = Field(
        alias="calculateEmergForLoadThermal", default=None
    )
    calculate_normal_for_gen_thermal: Optional[bool] = Field(
        alias="calculateNormalForGenThermal", default=None
    )
    calculate_normal_for_load_thermal: Optional[bool] = Field(
        alias="calculateNormalForLoadThermal", default=None
    )
    populate_constraints: Optional[bool] = Field(
        alias="populateConstraints", default=None
    )
    populate_duration_curves: Optional[bool] = Field(
        alias="populateDurationCurves", default=None
    )
    populate_enhanced_metrics: Optional[bool] = Field(
        alias="populateEnhancedMetrics", default=None
    )
    populate_enhanced_metrics_profile: Optional[bool] = Field(
        alias="populateEnhancedMetricsProfile", default=None
    )
    populate_weekly_reports: Optional[bool] = Field(
        alias="populateWeeklyReports", default=None
    )


class HcExecutorConfigInput(BaseModel):
    value: Optional[str] = None
    "Placeholder parameter, currently ignored."


class HcGeneratorConfigInput(BaseModel):
    model: Optional["HcModelConfigInput"] = None
    node_level_results: Optional["HcNodeLevelResultsConfigInput"] = Field(
        alias="nodeLevelResults", default=None
    )
    raw_results: Optional["HcRawResultsConfigInput"] = Field(
        alias="rawResults", default=None
    )
    solve: Optional["HcSolveConfigInput"] = None


class HcInverterControlConfigInput(BaseModel):
    after_cut_off_profile: Optional[str] = Field(
        alias="afterCutOffProfile", default=None
    )
    before_cut_off_profile: Optional[str] = Field(
        alias="beforeCutOffProfile", default=None
    )
    cut_off_date: Optional[Any] = Field(alias="cutOffDate", default=None)


class HcMeterPlacementConfigInput(BaseModel):
    dist_transformers: Optional[bool] = Field(alias="distTransformers", default=None)
    energy_consumer_meter_group: Optional[str] = Field(
        alias="energyConsumerMeterGroup", default=None
    )
    feeder_head: Optional[bool] = Field(alias="feederHead", default=None)
    switch_meter_placement_configs: Optional[
        list["HcSwitchMeterPlacementConfigInput"]
    ] = Field(alias="switchMeterPlacementConfigs", default=None)


class HcMetricsResultsConfigInput(BaseModel):
    calculate_performance_metrics: Optional[bool] = Field(
        alias="calculatePerformanceMetrics", default=None
    )


class HcModelConfigInput(BaseModel):
    calibration: Optional[bool] = None
    closed_loop_time_delay: Optional[int] = Field(
        alias="closedLoopTimeDelay", default=None
    )
    closed_loop_v_band: Optional[float] = Field(alias="closedLoopVBand", default=None)
    closed_loop_v_limit: Optional[float] = Field(alias="closedLoopVLimit", default=None)
    closed_loop_v_reg_enabled: Optional[bool] = Field(
        alias="closedLoopVRegEnabled", default=None
    )
    closed_loop_v_reg_replace_all: Optional[bool] = Field(
        alias="closedLoopVRegReplaceAll", default=None
    )
    closed_loop_v_reg_set_point: Optional[float] = Field(
        alias="closedLoopVRegSetPoint", default=None
    )
    collapse_lv_networks: Optional[bool] = Field(
        alias="collapseLvNetworks", default=None
    )
    collapse_negligible_impedances: Optional[bool] = Field(
        alias="collapseNegligibleImpedances", default=None
    )
    collapse_swer: Optional[bool] = Field(alias="collapseSWER", default=None)
    combine_common_impedances: Optional[bool] = Field(
        alias="combineCommonImpedances", default=None
    )
    ct_prim_scaling_factor: Optional[float] = Field(
        alias="ctPrimScalingFactor", default=None
    )
    default_gen_var: Optional[list[float]] = Field(alias="defaultGenVar", default=None)
    default_gen_watts: Optional[list[float]] = Field(
        alias="defaultGenWatts", default=None
    )
    default_load_var: Optional[list[float]] = Field(
        alias="defaultLoadVar", default=None
    )
    default_load_watts: Optional[list[float]] = Field(
        alias="defaultLoadWatts", default=None
    )
    default_tap_changer_band: Optional[float] = Field(
        alias="defaultTapChangerBand", default=None
    )
    default_tap_changer_set_point_pu: Optional[float] = Field(
        alias="defaultTapChangerSetPointPu", default=None
    )
    default_tap_changer_time_delay: Optional[int] = Field(
        alias="defaultTapChangerTimeDelay", default=None
    )
    emerg_amp_scaling: Optional[float] = Field(alias="emergAmpScaling", default=None)
    feeder_scenario_allocation_strategy: Optional[
        HcFeederScenarioAllocationStrategy
    ] = Field(alias="feederScenarioAllocationStrategy", default=None)
    fix_overloading_consumers: Optional[bool] = Field(
        alias="fixOverloadingConsumers", default=None
    )
    fix_single_phase_loads: Optional[bool] = Field(
        alias="fixSinglePhaseLoads", default=None
    )
    fix_undersized_service_lines: Optional[bool] = Field(
        alias="fixUndersizedServiceLines", default=None
    )
    gen_v_max_pu: Optional[float] = Field(alias="genVMaxPu", default=None)
    gen_v_min_pu: Optional[float] = Field(alias="genVMinPu", default=None)
    inverter_control_config: Optional["HcInverterControlConfigInput"] = Field(
        alias="inverterControlConfig", default=None
    )
    load_interval_length_hours: Optional[float] = Field(
        alias="loadIntervalLengthHours", default=None
    )
    load_model: Optional[int] = Field(alias="loadModel", default=None)
    load_placement: Optional[HcLoadPlacement] = Field(
        alias="loadPlacement", default=None
    )
    load_v_max_pu: Optional[float] = Field(alias="loadVMaxPu", default=None)
    load_v_min_pu: Optional[float] = Field(alias="loadVMinPu", default=None)
    max_gen_tx_ratio: Optional[float] = Field(alias="maxGenTxRatio", default=None)
    max_load_lv_line_ratio: Optional[float] = Field(
        alias="maxLoadLvLineRatio", default=None
    )
    max_load_service_line_ratio: Optional[float] = Field(
        alias="maxLoadServiceLineRatio", default=None
    )
    max_load_tx_ratio: Optional[float] = Field(alias="maxLoadTxRatio", default=None)
    max_single_phase_load: Optional[float] = Field(
        alias="maxSinglePhaseLoad", default=None
    )
    meter_placement_config: Optional["HcMeterPlacementConfigInput"] = Field(
        alias="meterPlacementConfig", default=None
    )
    p_factor_base_exports: Optional[float] = Field(
        alias="pFactorBaseExports", default=None
    )
    p_factor_base_imports: Optional[float] = Field(
        alias="pFactorBaseImports", default=None
    )
    p_factor_forecast_pv: Optional[float] = Field(
        alias="pFactorForecastPv", default=None
    )
    rating_threshold: Optional[float] = Field(alias="ratingThreshold", default=None)
    seed: Optional[int] = None
    simplify_network: Optional[bool] = Field(alias="simplifyNetwork", default=None)
    simplify_plsi_threshold: Optional[float] = Field(
        alias="simplifyPLSIThreshold", default=None
    )
    split_phase_default_load_loss_percentage: Optional[float] = Field(
        alias="splitPhaseDefaultLoadLossPercentage", default=None
    )
    split_phase_lvkv: Optional[float] = Field(alias="splitPhaseLVKV", default=None)
    swer_voltage_to_line_voltage: Optional[list[list[int]]] = Field(
        alias="swerVoltageToLineVoltage", default=None
    )
    transformer_tap_settings: Optional[str] = Field(
        alias="transformerTapSettings", default=None
    )
    use_span_level_threshold: Optional[bool] = Field(
        alias="useSpanLevelThreshold", default=None
    )
    vm_pu: Optional[float] = Field(alias="vmPu", default=None)


class HcNodeLevelResultsConfigInput(BaseModel):
    collect_all_conductors: Optional[bool] = Field(
        alias="collectAllConductors", default=None
    )
    collect_all_energy_consumers: Optional[bool] = Field(
        alias="collectAllEnergyConsumers", default=None
    )
    collect_all_switches: Optional[bool] = Field(
        alias="collectAllSwitches", default=None
    )
    collect_all_transformers: Optional[bool] = Field(
        alias="collectAllTransformers", default=None
    )
    collect_current: Optional[bool] = Field(alias="collectCurrent", default=None)
    collect_power: Optional[bool] = Field(alias="collectPower", default=None)
    collect_voltage: Optional[bool] = Field(alias="collectVoltage", default=None)
    mrids_to_collect: Optional[list[str]] = Field(alias="mridsToCollect", default=None)


class HcRawResultsConfigInput(BaseModel):
    energy_meter_voltages_raw: Optional[bool] = Field(
        alias="energyMeterVoltagesRaw", default=None
    )
    energy_meters_raw: Optional[bool] = Field(alias="energyMetersRaw", default=None)
    overloads_raw: Optional[bool] = Field(alias="overloadsRaw", default=None)
    results_per_meter: Optional[bool] = Field(alias="resultsPerMeter", default=None)
    voltage_exceptions_raw: Optional[bool] = Field(
        alias="voltageExceptionsRaw", default=None
    )


class HcResultProcessorConfigInput(BaseModel):
    metrics: Optional["HcMetricsResultsConfigInput"] = None
    stored_results: Optional["HcStoredResultsConfigInput"] = Field(
        alias="storedResults", default=None
    )
    writer_config: Optional["HcWriterConfigInput"] = Field(
        alias="writerConfig", default=None
    )


class HcScenarioConfigsFilterInput(BaseModel):
    id: Optional[str] = None
    "Search for scenario configurations by Id. Returns partial matches."
    name: Optional[str] = None
    "Search for scenario configurations by name. Returns partial matches."


class HcSolveConfigInput(BaseModel):
    base_frequency: Optional[int] = Field(alias="baseFrequency", default=None)
    emerg_v_max_pu: Optional[float] = Field(alias="emergVMaxPu", default=None)
    emerg_v_min_pu: Optional[float] = Field(alias="emergVMinPu", default=None)
    max_control_iter: Optional[int] = Field(alias="maxControlIter", default=None)
    max_iter: Optional[int] = Field(alias="maxIter", default=None)
    mode: Optional[HcSolveMode] = None
    norm_v_max_pu: Optional[float] = Field(alias="normVMaxPu", default=None)
    norm_v_min_pu: Optional[float] = Field(alias="normVMinPu", default=None)
    step_size_minutes: Optional[int] = Field(alias="stepSizeMinutes", default=None)
    voltage_bases: Optional[list[float]] = Field(alias="voltageBases", default=None)


class HcStoredResultsConfigInput(BaseModel):
    energy_meter_voltages_raw: Optional[bool] = Field(
        alias="energyMeterVoltagesRaw", default=None
    )
    energy_meters_raw: Optional[bool] = Field(alias="energyMetersRaw", default=None)
    overloads_raw: Optional[bool] = Field(alias="overloadsRaw", default=None)
    voltage_exceptions_raw: Optional[bool] = Field(
        alias="voltageExceptionsRaw", default=None
    )


class HcSwitchMeterPlacementConfigInput(BaseModel):
    meter_switch_class: HcSwitchClass = Field(alias="meterSwitchClass")
    name_pattern: str = Field(alias="namePattern")


class HcWorkPackagesFilterInput(BaseModel):
    created_by: Optional[list[str]] = Field(alias="createdBy", default=None)
    "Search for work package by the username or email of the User that created the work package."
    id: Optional[str] = None
    "Search for work package by Id."
    name: Optional[str] = None
    "Search for work package by name. Returns partial matches."
    search_text: Optional[str] = Field(alias="searchText", default=None)
    "Search for work package by user input text. Returns partial matches."


class HcWorkPackagesSortCriteriaInput(BaseModel):
    created_at: Optional[SortOrder] = Field(alias="createdAt", default=None)
    name: Optional[SortOrder] = None


class HcWriterConfigInput(BaseModel):
    output_writer_config: Optional["HcWriterOutputConfigInput"] = Field(
        alias="outputWriterConfig", default=None
    )
    writer_type: Optional[HcWriterType] = Field(alias="writerType", default=None)


class HcWriterOutputConfigInput(BaseModel):
    enhanced_metrics_config: Optional["HcEnhancedMetricsConfigInput"] = Field(
        alias="enhancedMetricsConfig", default=None
    )


class IngestorConfigInput(BaseModel):
    key: str
    value: str


class IngestorRunsFilterInput(BaseModel):
    """Include results based on filters. A logical AND is applied between the supplied filters"""

    completed: Optional[bool] = None
    "Filter results by whether they are in a completed state or not."
    container_runtime_type: Optional[list[IngestorRuntimeKind]] = Field(
        alias="containerRuntimeType", default=None
    )
    "Filter results by containerRunTimeType."
    id: Optional[str] = None
    "Filter results by Id."
    status: Optional[list[IngestorRunState]] = None
    "Filter results by the current status of the ingestor run."


class IngestorRunsSortCriteriaInput(BaseModel):
    completed_at: Optional[SortOrder] = Field(alias="completedAt", default=None)
    container_runtime_type: Optional[SortOrder] = Field(
        alias="containerRuntimeType", default=None
    )
    started_at: Optional[SortOrder] = Field(alias="startedAt", default=None)
    status: Optional[SortOrder] = None
    status_last_updated_at: Optional[SortOrder] = Field(
        alias="statusLastUpdatedAt", default=None
    )


class InterventionConfigInput(BaseModel):
    allocation_criteria: Optional[str] = Field(alias="allocationCriteria", default=None)
    "The ID of the set of criteria used to select an intervention instance for each candidate."
    allocation_limit_per_year: Optional[int] = Field(
        alias="allocationLimitPerYear", default=None
    )
    "The maximum number of interventions that can be applied per year. Defaults to 1 million."
    base_work_package_id: str = Field(alias="baseWorkPackageId")
    "ID of the work package that this intervention is based on. The new work package should process a subset of its feeders, scenarios, and years."
    candidate_generation: Optional["CandidateGenerationConfigInput"] = Field(
        alias="candidateGeneration", default=None
    )
    "The method of generating candidates for the intervention. This does not need to be specified for certain interventions, e.g. PHASE_REBALANCING."
    dvms: Optional["DvmsConfigInput"] = None
    "The config for DVMS. This must be specified if interventionType = DVMS."
    intervention_type: InterventionClass = Field(alias="interventionType")
    "The class of intervention to apply."
    phase_rebalance_proportions: Optional["PhaseRebalanceProportionsInput"] = Field(
        alias="phaseRebalanceProportions", default=None
    )
    "The proportions to use for phase rebalancing. If this is unspecified and interventionType = PHASE_REBALANCING, phases will be rebalanced to equal proportions."
    specific_allocation_instance: Optional[str] = Field(
        alias="specificAllocationInstance", default=None
    )
    "The specific instance of intervention to use for every allocation. If this is unspecified, all instances of the intervention class will be considered when choosing one for each candidate."
    year_range: Optional["YearRangeInput"] = Field(alias="yearRange", default=None)
    "The range of years to search for and apply interventions. All years within this range should be included in the work package. Defaults to 1AD to 9999AD."


class OpenDssCommonConfigInput(BaseModel):
    fixed_time: Optional["FixedTimeInput"] = Field(alias="fixedTime", default=None)
    time_period: Optional["TimePeriodInput"] = Field(alias="timePeriod", default=None)


class OpenDssModelGenerationSpecInput(BaseModel):
    model_options: "OpenDssModelOptionsInput" = Field(alias="modelOptions")
    modules_configuration: "OpenDssModulesConfigInput" = Field(
        alias="modulesConfiguration"
    )


class OpenDssModelInput(BaseModel):
    generation_spec: "OpenDssModelGenerationSpecInput" = Field(alias="generationSpec")
    is_public: Optional[bool] = Field(alias="isPublic", default=None)
    model_name: Optional[str] = Field(alias="modelName", default=None)


class OpenDssModelOptionsInput(BaseModel):
    feeder: str
    scenario: str
    year: int


class OpenDssModulesConfigInput(BaseModel):
    common: "OpenDssCommonConfigInput"
    generator: Optional["HcGeneratorConfigInput"] = None


class PhaseRebalanceProportionsInput(BaseModel):
    a: float
    b: float
    c: float


class PowerFactoryModelGenerationSpecInput(BaseModel):
    distribution_transformer_config: Optional[
        "GqlDistributionTransformerConfigInput"
    ] = Field(alias="distributionTransformerConfig", default=None)
    equipment_container_mrids: list[str] = Field(alias="equipmentContainerMrids")
    load_config: Optional["GqlLoadConfigInput"] = Field(
        alias="loadConfig", default=None
    )
    model_name: Optional[str] = Field(alias="modelName", default=None)
    scenario_config: Optional["GqlScenarioConfigInput"] = Field(
        alias="scenarioConfig", default=None
    )


class PowerFactoryModelInput(BaseModel):
    generation_spec: "PowerFactoryModelGenerationSpecInput" = Field(
        alias="generationSpec"
    )
    is_public: Optional[bool] = Field(alias="isPublic", default=None)
    name: Optional[str] = None


class ProcessedDiffFilterInput(BaseModel):
    type_: Optional[str] = Field(alias="type", default=None)
    "Search for processed diffs by whether its network metrics or network metrics enhanced."
    w_p_id: Optional[str] = Field(alias="wPId", default=None)
    "Search for processed diffs by work package Id."


class ProcessedDiffSortCriteriaInput(BaseModel):
    type_: Optional[SortOrder] = Field(alias="type", default=None)
    work_packaged_id_1: Optional[SortOrder] = Field(
        alias="workPackagedId1", default=None
    )


class ResultSectionInput(BaseModel):
    columns: Any
    data: Any
    description: str
    name: str
    type_: SectionType = Field(alias="type")


class SincalModelGenerationSpecInput(BaseModel):
    equipment_container_mrids: Optional[list[str]] = Field(
        alias="equipmentContainerMrids", default=None
    )
    forecast_spec: Optional["GqlSincalModelForecastSpecInput"] = Field(
        alias="forecastSpec", default=None
    )
    "Configuration for forecast models"
    frontend_config: str = Field(alias="frontendConfig")
    "JSON frontend export config."


class SincalModelInput(BaseModel):
    generation_spec: "SincalModelGenerationSpecInput" = Field(alias="generationSpec")
    is_public: Optional[bool] = Field(alias="isPublic", default=None)
    model_name: Optional[str] = Field(alias="modelName", default=None)


class StateOverlayInput(BaseModel):
    data: Any
    styles: list[str]


class StudyInput(BaseModel):
    description: str
    name: str
    results: list["StudyResultInput"]
    styles: list[Any]
    tags: list[str]


class StudyResultInput(BaseModel):
    geo_json_overlay: Optional["GeoJsonOverlayInput"] = Field(
        alias="geoJsonOverlay", default=None
    )
    name: str
    sections: list["ResultSectionInput"]
    state_overlay: Optional["StateOverlayInput"] = Field(
        alias="stateOverlay", default=None
    )


class TimePeriodInput(BaseModel):
    end_time: Any = Field(alias="endTime")
    "The ending time for load data retrieval."
    overrides: Optional[list["TimePeriodLoadOverrideInput"]] = None
    "The list of load override profiles."
    start_time: Any = Field(alias="startTime")
    "The starting time for load data retrieval."


class TimePeriodLoadOverrideInput(BaseModel):
    gen_var_override: Optional[list[float]] = Field(
        alias="genVarOverride", default=None
    )
    gen_watts_override: Optional[list[float]] = Field(
        alias="genWattsOverride", default=None
    )
    load_id: str = Field(alias="loadId")
    load_var_override: Optional[list[float]] = Field(
        alias="loadVarOverride", default=None
    )
    load_watts_override: Optional[list[float]] = Field(
        alias="loadWattsOverride", default=None
    )


class WorkPackageInput(BaseModel):
    executor_config: Optional["HcExecutorConfigInput"] = Field(
        alias="executorConfig", default=None
    )
    "Config exclusive to the OpenDSS executor."
    feeder_configs: Optional["FeederConfigsInput"] = Field(
        alias="feederConfigs", default=None
    )
    "The list of feeder configurations for this work package, can not be set if forecast configurations exists."
    forecast_config: Optional["ForecastConfigInput"] = Field(
        alias="forecastConfig", default=None
    )
    "The forecast configurations for this work package, can not be set if feeder configurations exists."
    generator_config: Optional["HcGeneratorConfigInput"] = Field(
        alias="generatorConfig", default=None
    )
    "Config exclusive to the OpenDSS model generator."
    intervention: Optional["InterventionConfigInput"] = None
    "An optional intervention to use for this work package. Interventions are applied per feeder-scenario."
    quality_assurance_processing: Optional[bool] = Field(
        alias="qualityAssuranceProcessing", default=None
    )
    "Fetch load from a single timestamp. This will result in a single timestamp of results."
    result_processor_config: Optional["HcResultProcessorConfigInput"] = Field(
        alias="resultProcessorConfig", default=None
    )
    "Config exclusive to the result processor."


class YearRangeInput(BaseModel):
    max_year: int = Field(alias="maxYear")
    "The maximum year in this range (inclusive)"
    min_year: int = Field(alias="minYear")
    "The minimum year in this range (inclusive)"


DvmsConfigInput.model_rebuild()
FeederConfigInput.model_rebuild()
FeederConfigsInput.model_rebuild()
FeederLoadAnalysisInput.model_rebuild()
FixedTimeInput.model_rebuild()
ForecastConfigInput.model_rebuild()
HcGeneratorConfigInput.model_rebuild()
HcMeterPlacementConfigInput.model_rebuild()
HcModelConfigInput.model_rebuild()
HcResultProcessorConfigInput.model_rebuild()
HcWriterConfigInput.model_rebuild()
HcWriterOutputConfigInput.model_rebuild()
InterventionConfigInput.model_rebuild()
OpenDssCommonConfigInput.model_rebuild()
OpenDssModelGenerationSpecInput.model_rebuild()
OpenDssModelInput.model_rebuild()
OpenDssModulesConfigInput.model_rebuild()
PowerFactoryModelGenerationSpecInput.model_rebuild()
PowerFactoryModelInput.model_rebuild()
SincalModelGenerationSpecInput.model_rebuild()
SincalModelInput.model_rebuild()
StudyInput.model_rebuild()
StudyResultInput.model_rebuild()
TimePeriodInput.model_rebuild()
WorkPackageInput.model_rebuild()
