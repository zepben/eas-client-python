from typing import Any, Optional, Union

from . import SerializationType
from .base_operation import GraphQLField
from .custom_typing_fields import (
    AppOptionsGraphQLField,
    ColumnGraphQLField,
    CoordinateGraphQLField,
    CustomerDetailsGraphQLField,
    CustomerDetailsResponseGraphQLField,
    CustomerListColumnConfigGraphQLField,
    DiffResultGraphQLField,
    DurationCurveByTerminalGraphQLField,
    DurationCurveGraphQLField,
    DurationCurvePointGraphQLField,
    EquipmentGraphQLField,
    FeederLoadAnalysisReportGraphQLField,
    FeederLoadAnalysisSpecGraphQLField,
    GeoJsonFeatureGraphQLField,
    GeoJsonGeometryGraphQLField,
    GeoJsonOverlayGraphQLField,
    GeoJsonPropertiesGraphQLField,
    GqlDistributionTransformerConfigGraphQLField,
    GqlLoadConfigGraphQLField,
    GqlScenarioConfigGraphQLField,
    GqlTxTapRecordGraphQLField,
    GqlUserGraphQLField,
    GqlUserResponseGraphQLField,
    HcCalibrationGraphQLField,
    HcModelGraphQLField,
    HcScenarioConfigsPageGraphQLField,
    HcWorkPackageGraphQLField,
    HcWorkPackagePageGraphQLField,
    IngestionJobGraphQLField,
    IngestionRunGraphQLField,
    IngestorRunPageGraphQLField,
    JobSourceGraphQLField,
    MachineUserGraphQLField,
    MetricGraphQLField,
    NetworkModelGraphQLField,
    NetworkModelsGraphQLField,
    OpenDssModelGraphQLField,
    OpenDssModelPageGraphQLField,
    OpportunitiesByYearGraphQLField,
    OpportunityGraphQLField,
    OpportunityLocationGraphQLField,
    PowerFactoryModelGenerationSpecGraphQLField,
    PowerFactoryModelGraphQLField,
    PowerFactoryModelPageGraphQLField,
    PowerFactoryModelTemplateGraphQLField,
    PowerFactoryModelTemplatePageGraphQLField,
    ProcessedDiffGraphQLField,
    ProcessedDiffPageGraphQLField,
    RemoveAppOptionResultGraphQLField,
    ResultSectionGraphQLField,
    ScenarioConfigurationGraphQLField,
    SincalConfigFileGraphQLField,
    SincalGlobalInputsConfigGraphQLField,
    SincalModelGenerationSpecGraphQLField,
    SincalModelGraphQLField,
    SincalModelPageGraphQLField,
    SincalModelPresetGraphQLField,
    SincalModelPresetPageGraphQLField,
    StateOverlayGraphQLField,
    StudyGraphQLField,
    StudyPageGraphQLField,
    StudyResultGraphQLField,
    TableSectionGraphQLField,
    UploadUrlResponseGraphQLField,
    UserCustomerListColumnConfigGraphQLField,
    VariantGraphQLField,
    VariantWorkPackageGraphQLField,
    WorkPackageModelGroupingsGraphQLField,
    WorkPackageModelTotalsGraphQLField,
    WorkPackageProgressDetailsGraphQLField,
    WorkPackageTreeGraphQLField,
)


class AppOptionsFields(GraphQLField):
    """Application configuration option."""

    asset_name_format: "AppOptionsGraphQLField" = AppOptionsGraphQLField(
        "assetNameFormat"
    )
    pole_string_format: "AppOptionsGraphQLField" = AppOptionsGraphQLField(
        "poleStringFormat"
    )

    def fields(self, *subfields: AppOptionsGraphQLField) -> "AppOptionsFields":
        """Subfields should come from the AppOptionsFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AppOptionsFields":
        self._alias = alias
        return self


class ColumnFields(GraphQLField):
    key: "ColumnGraphQLField" = ColumnGraphQLField("key")
    name: "ColumnGraphQLField" = ColumnGraphQLField("name")

    def fields(self, *subfields: ColumnGraphQLField) -> "ColumnFields":
        """Subfields should come from the ColumnFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ColumnFields":
        self._alias = alias
        return self


class CoordinateFields(GraphQLField):
    latitude: "CoordinateGraphQLField" = CoordinateGraphQLField("latitude")
    longitude: "CoordinateGraphQLField" = CoordinateGraphQLField("longitude")

    def fields(self, *subfields: CoordinateGraphQLField) -> "CoordinateFields":
        """Subfields should come from the CoordinateFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CoordinateFields":
        self._alias = alias
        return self


class CustomerDetailsFields(GraphQLField):
    """Detailed customer information including both customer-specific and network-specific fields."""

    customer_mrid: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField(
        "customerMrid"
    )
    customer_type: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField(
        "customerType"
    )
    distributor: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField(
        "distributor"
    )
    dlf: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField("dlf")
    feeder: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField("feeder")
    first_name: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField("firstName")
    is_embedded_network: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField(
        "isEmbeddedNetwork"
    )
    is_energy_feedback: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField(
        "isEnergyFeedback"
    )
    last_name: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField("lastName")
    lv_feeder: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField("lvFeeder")
    meter_number: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField(
        "meterNumber"
    )
    mobile_number: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField(
        "mobileNumber"
    )
    move_in_date: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField(
        "moveInDate"
    )
    nmi: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField("nmi")
    nmi_class: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField("nmiClass")
    phone_number: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField(
        "phoneNumber"
    )
    postal_address: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField(
        "postalAddress"
    )
    sensitivity_category: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField(
        "sensitivityCategory"
    )
    service_address: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField(
        "serviceAddress"
    )
    service_provision_status: "CustomerDetailsGraphQLField" = (
        CustomerDetailsGraphQLField("serviceProvisionStatus")
    )
    supply_point_id: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField(
        "supplyPointId"
    )
    tariff: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField("tariff")
    tni: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField("tni")
    transformer_description: "CustomerDetailsGraphQLField" = (
        CustomerDetailsGraphQLField("transformerDescription")
    )
    transformer_id: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField(
        "transformerId"
    )
    zone_substation: "CustomerDetailsGraphQLField" = CustomerDetailsGraphQLField(
        "zoneSubstation"
    )

    def fields(
        self, *subfields: CustomerDetailsGraphQLField
    ) -> "CustomerDetailsFields":
        """Subfields should come from the CustomerDetailsFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CustomerDetailsFields":
        self._alias = alias
        return self


class CustomerDetailsResponseFields(GraphQLField):
    @classmethod
    def customer_details(cls) -> "CustomerDetailsFields":
        return CustomerDetailsFields("customerDetails")

    def fields(
        self,
        *subfields: Union[CustomerDetailsResponseGraphQLField, "CustomerDetailsFields"]
    ) -> "CustomerDetailsResponseFields":
        """Subfields should come from the CustomerDetailsResponseFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CustomerDetailsResponseFields":
        self._alias = alias
        return self


class CustomerListColumnConfigFields(GraphQLField):
    """Defines a column available for configuration in the customer list table."""

    column_name: "CustomerListColumnConfigGraphQLField" = (
        CustomerListColumnConfigGraphQLField("columnName")
    )
    "The unique name of the column."
    group: "CustomerListColumnConfigGraphQLField" = (
        CustomerListColumnConfigGraphQLField("group")
    )
    "The group this column belongs to (e.g., PII, NON_PII)."

    def fields(
        self, *subfields: CustomerListColumnConfigGraphQLField
    ) -> "CustomerListColumnConfigFields":
        """Subfields should come from the CustomerListColumnConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CustomerListColumnConfigFields":
        self._alias = alias
        return self


class DiffResultFields(GraphQLField):
    entries: "DiffResultGraphQLField" = DiffResultGraphQLField("entries")
    id: "DiffResultGraphQLField" = DiffResultGraphQLField("id")

    def fields(self, *subfields: DiffResultGraphQLField) -> "DiffResultFields":
        """Subfields should come from the DiffResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DiffResultFields":
        self._alias = alias
        return self


class DurationCurveFields(GraphQLField):
    @classmethod
    def points(cls) -> "DurationCurvePointFields":
        return DurationCurvePointFields("points")

    def fields(
        self, *subfields: Union[DurationCurveGraphQLField, "DurationCurvePointFields"]
    ) -> "DurationCurveFields":
        """Subfields should come from the DurationCurveFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DurationCurveFields":
        self._alias = alias
        return self


class DurationCurveByTerminalFields(GraphQLField):
    """The duration curve for a terminal of a conducting equipment."""

    @classmethod
    def duration_curve(cls) -> "DurationCurveFields":
        return DurationCurveFields("durationCurve")

    terminal_sequence_number: "DurationCurveByTerminalGraphQLField" = (
        DurationCurveByTerminalGraphQLField("terminalSequenceNumber")
    )

    def fields(
        self,
        *subfields: Union[DurationCurveByTerminalGraphQLField, "DurationCurveFields"]
    ) -> "DurationCurveByTerminalFields":
        """Subfields should come from the DurationCurveByTerminalFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DurationCurveByTerminalFields":
        self._alias = alias
        return self


class DurationCurvePointFields(GraphQLField):
    conducting_equipment: "DurationCurvePointGraphQLField" = (
        DurationCurvePointGraphQLField("conductingEquipment")
    )
    feeder: "DurationCurvePointGraphQLField" = DurationCurvePointGraphQLField("feeder")
    kw: "DurationCurvePointGraphQLField" = DurationCurvePointGraphQLField("kw")
    measurement_zone_type: "DurationCurvePointGraphQLField" = (
        DurationCurvePointGraphQLField("measurementZoneType")
    )
    percentage_of_time: "DurationCurvePointGraphQLField" = (
        DurationCurvePointGraphQLField("percentageOfTime")
    )
    scenario: "DurationCurvePointGraphQLField" = DurationCurvePointGraphQLField(
        "scenario"
    )
    terminal_sequence_number: "DurationCurvePointGraphQLField" = (
        DurationCurvePointGraphQLField("terminalSequenceNumber")
    )
    timestamp: "DurationCurvePointGraphQLField" = DurationCurvePointGraphQLField(
        "timestamp"
    )
    v_base: "DurationCurvePointGraphQLField" = DurationCurvePointGraphQLField("vBase")
    work_package_id: "DurationCurvePointGraphQLField" = DurationCurvePointGraphQLField(
        "workPackageId"
    )

    def fields(
        self, *subfields: DurationCurvePointGraphQLField
    ) -> "DurationCurvePointFields":
        """Subfields should come from the DurationCurvePointFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DurationCurvePointFields":
        self._alias = alias
        return self


class EquipmentFields(GraphQLField):
    m_rid: "EquipmentGraphQLField" = EquipmentGraphQLField("mRID")

    @classmethod
    def location(cls) -> "CoordinateFields":
        return CoordinateFields("location")

    def fields(
        self, *subfields: Union[EquipmentGraphQLField, "CoordinateFields"]
    ) -> "EquipmentFields":
        """Subfields should come from the EquipmentFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "EquipmentFields":
        self._alias = alias
        return self


class FeederLoadAnalysisReportFields(GraphQLField):
    completed_at: "FeederLoadAnalysisReportGraphQLField" = (
        FeederLoadAnalysisReportGraphQLField("completedAt")
    )
    created_at: "FeederLoadAnalysisReportGraphQLField" = (
        FeederLoadAnalysisReportGraphQLField("createdAt")
    )
    created_by: "FeederLoadAnalysisReportGraphQLField" = (
        FeederLoadAnalysisReportGraphQLField("createdBy")
    )
    errors: "FeederLoadAnalysisReportGraphQLField" = (
        FeederLoadAnalysisReportGraphQLField("errors")
    )

    @classmethod
    def generation_spec(cls) -> "FeederLoadAnalysisSpecFields":
        return FeederLoadAnalysisSpecFields("generationSpec")

    id: "FeederLoadAnalysisReportGraphQLField" = FeederLoadAnalysisReportGraphQLField(
        "id"
    )
    name: "FeederLoadAnalysisReportGraphQLField" = FeederLoadAnalysisReportGraphQLField(
        "name"
    )
    state: "FeederLoadAnalysisReportGraphQLField" = (
        FeederLoadAnalysisReportGraphQLField("state")
    )

    def fields(
        self,
        *subfields: Union[
            FeederLoadAnalysisReportGraphQLField, "FeederLoadAnalysisSpecFields"
        ]
    ) -> "FeederLoadAnalysisReportFields":
        """Subfields should come from the FeederLoadAnalysisReportFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "FeederLoadAnalysisReportFields":
        self._alias = alias
        return self


class FeederLoadAnalysisSpecFields(GraphQLField):
    aggregate_at_feeder_level: "FeederLoadAnalysisSpecGraphQLField" = (
        FeederLoadAnalysisSpecGraphQLField("aggregateAtFeederLevel")
    )
    "Request for a report which aggregate all downstream load at the feeder level"
    end_date: "FeederLoadAnalysisSpecGraphQLField" = FeederLoadAnalysisSpecGraphQLField(
        "endDate"
    )
    "End date for this analysis"
    feeders: "FeederLoadAnalysisSpecGraphQLField" = FeederLoadAnalysisSpecGraphQLField(
        "feeders"
    )
    "The mRIDs of feeders to solve for feeder load analysis."
    fetch_lv_network: "FeederLoadAnalysisSpecGraphQLField" = (
        FeederLoadAnalysisSpecGraphQLField("fetchLvNetwork")
    )
    "Whether to stop analysis at distribution transformer"
    geographical_regions: "FeederLoadAnalysisSpecGraphQLField" = (
        FeederLoadAnalysisSpecGraphQLField("geographicalRegions")
    )
    "The mRIDs of Geographical Region to solve for feeder load analysis."
    output: "FeederLoadAnalysisSpecGraphQLField" = FeederLoadAnalysisSpecGraphQLField(
        "output"
    )
    "The file name of the resulting study"
    process_coincident_loads: "FeederLoadAnalysisSpecGraphQLField" = (
        FeederLoadAnalysisSpecGraphQLField("processCoincidentLoads")
    )
    "Whether to include values corresponding to conductor event time points in the report"
    process_feeder_loads: "FeederLoadAnalysisSpecGraphQLField" = (
        FeederLoadAnalysisSpecGraphQLField("processFeederLoads")
    )
    "Whether to include values corresponding to feeder event time points in the report"
    produce_basic_report: "FeederLoadAnalysisSpecGraphQLField" = (
        FeederLoadAnalysisSpecGraphQLField("produceBasicReport")
    )
    "Request for a basic report"
    produce_conductor_report: "FeederLoadAnalysisSpecGraphQLField" = (
        FeederLoadAnalysisSpecGraphQLField("produceConductorReport")
    )
    "Request for an extensive report"
    start_date: "FeederLoadAnalysisSpecGraphQLField" = (
        FeederLoadAnalysisSpecGraphQLField("startDate")
    )
    "Start date for this analysis"
    sub_geographical_regions: "FeederLoadAnalysisSpecGraphQLField" = (
        FeederLoadAnalysisSpecGraphQLField("subGeographicalRegions")
    )
    "The mRIDs of sub-Geographical Region to solve for feeder load analysis."
    substations: "FeederLoadAnalysisSpecGraphQLField" = (
        FeederLoadAnalysisSpecGraphQLField("substations")
    )
    "The mRIDs of substations to solve for feeder load analysis."

    def fields(
        self, *subfields: FeederLoadAnalysisSpecGraphQLField
    ) -> "FeederLoadAnalysisSpecFields":
        """Subfields should come from the FeederLoadAnalysisSpecFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "FeederLoadAnalysisSpecFields":
        self._alias = alias
        return self


class GeoJsonFeatureFields(GraphQLField):
    @classmethod
    def geometry(cls) -> "GeoJsonGeometryFields":
        return GeoJsonGeometryFields("geometry")

    @classmethod
    def properties(cls) -> "GeoJsonPropertiesFields":
        return GeoJsonPropertiesFields("properties")

    type_: "GeoJsonFeatureGraphQLField" = GeoJsonFeatureGraphQLField("type")

    def fields(
        self,
        *subfields: Union[
            GeoJsonFeatureGraphQLField,
            "GeoJsonGeometryFields",
            "GeoJsonPropertiesFields",
        ]
    ) -> "GeoJsonFeatureFields":
        """Subfields should come from the GeoJsonFeatureFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GeoJsonFeatureFields":
        self._alias = alias
        return self


class GeoJsonGeometryFields(GraphQLField):
    @classmethod
    def coordinates(cls) -> "CoordinateFields":
        return CoordinateFields("coordinates")

    type_: "GeoJsonGeometryGraphQLField" = GeoJsonGeometryGraphQLField("type")

    def fields(
        self, *subfields: Union[GeoJsonGeometryGraphQLField, "CoordinateFields"]
    ) -> "GeoJsonGeometryFields":
        """Subfields should come from the GeoJsonGeometryFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GeoJsonGeometryFields":
        self._alias = alias
        return self


class GeoJsonOverlayFields(GraphQLField):
    styles: "GeoJsonOverlayGraphQLField" = GeoJsonOverlayGraphQLField("styles")
    id: "GeoJsonOverlayGraphQLField" = GeoJsonOverlayGraphQLField("id")
    data: "GeoJsonOverlayGraphQLField" = GeoJsonOverlayGraphQLField("data")
    source_properties: "GeoJsonOverlayGraphQLField" = GeoJsonOverlayGraphQLField(
        "sourceProperties"
    )

    def fields(self, *subfields: GeoJsonOverlayGraphQLField) -> "GeoJsonOverlayFields":
        """Subfields should come from the GeoJsonOverlayFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GeoJsonOverlayFields":
        self._alias = alias
        return self


class GeoJsonPropertiesFields(GraphQLField):
    detail: "GeoJsonPropertiesGraphQLField" = GeoJsonPropertiesGraphQLField("detail")
    properties: "GeoJsonPropertiesGraphQLField" = GeoJsonPropertiesGraphQLField(
        "properties"
    )

    def fields(
        self, *subfields: GeoJsonPropertiesGraphQLField
    ) -> "GeoJsonPropertiesFields":
        """Subfields should come from the GeoJsonPropertiesFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GeoJsonPropertiesFields":
        self._alias = alias
        return self


class GqlDistributionTransformerConfigFields(GraphQLField):
    r_ground: "GqlDistributionTransformerConfigGraphQLField" = (
        GqlDistributionTransformerConfigGraphQLField("rGround")
    )
    x_ground: "GqlDistributionTransformerConfigGraphQLField" = (
        GqlDistributionTransformerConfigGraphQLField("xGround")
    )

    def fields(
        self, *subfields: GqlDistributionTransformerConfigGraphQLField
    ) -> "GqlDistributionTransformerConfigFields":
        """Subfields should come from the GqlDistributionTransformerConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GqlDistributionTransformerConfigFields":
        self._alias = alias
        return self


class GqlLoadConfigFields(GraphQLField):
    spread_max_demand: "GqlLoadConfigGraphQLField" = GqlLoadConfigGraphQLField(
        "spreadMaxDemand"
    )

    def fields(self, *subfields: GqlLoadConfigGraphQLField) -> "GqlLoadConfigFields":
        """Subfields should come from the GqlLoadConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GqlLoadConfigFields":
        self._alias = alias
        return self


class GqlScenarioConfigFields(GraphQLField):
    bess_upgrade_threshold: "GqlScenarioConfigGraphQLField" = (
        GqlScenarioConfigGraphQLField("bessUpgradeThreshold")
    )
    pv_upgrade_threshold: "GqlScenarioConfigGraphQLField" = (
        GqlScenarioConfigGraphQLField("pvUpgradeThreshold")
    )
    scenario_id: "GqlScenarioConfigGraphQLField" = GqlScenarioConfigGraphQLField(
        "scenarioID"
    )
    years: "GqlScenarioConfigGraphQLField" = GqlScenarioConfigGraphQLField("years")

    def fields(
        self, *subfields: GqlScenarioConfigGraphQLField
    ) -> "GqlScenarioConfigFields":
        """Subfields should come from the GqlScenarioConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GqlScenarioConfigFields":
        self._alias = alias
        return self


class GqlTxTapRecordFields(GraphQLField):
    control_enabled: "GqlTxTapRecordGraphQLField" = GqlTxTapRecordGraphQLField(
        "controlEnabled"
    )
    high_step: "GqlTxTapRecordGraphQLField" = GqlTxTapRecordGraphQLField("highStep")
    id: "GqlTxTapRecordGraphQLField" = GqlTxTapRecordGraphQLField("id")
    low_step: "GqlTxTapRecordGraphQLField" = GqlTxTapRecordGraphQLField("lowStep")
    nominal_tap_num: "GqlTxTapRecordGraphQLField" = GqlTxTapRecordGraphQLField(
        "nominalTapNum"
    )
    step_voltage_increment: "GqlTxTapRecordGraphQLField" = GqlTxTapRecordGraphQLField(
        "stepVoltageIncrement"
    )
    tap_position: "GqlTxTapRecordGraphQLField" = GqlTxTapRecordGraphQLField(
        "tapPosition"
    )

    def fields(self, *subfields: GqlTxTapRecordGraphQLField) -> "GqlTxTapRecordFields":
        """Subfields should come from the GqlTxTapRecordFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GqlTxTapRecordFields":
        self._alias = alias
        return self


class GqlUserFields(GraphQLField):
    email: "GqlUserGraphQLField" = GqlUserGraphQLField("email")
    identity_provider: "GqlUserGraphQLField" = GqlUserGraphQLField("identityProvider")
    username: "GqlUserGraphQLField" = GqlUserGraphQLField("username")
    id: "GqlUserGraphQLField" = GqlUserGraphQLField("id")

    def fields(self, *subfields: GqlUserGraphQLField) -> "GqlUserFields":
        """Subfields should come from the GqlUserFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GqlUserFields":
        self._alias = alias
        return self


class GqlUserResponseFields(GraphQLField):
    email: "GqlUserResponseGraphQLField" = GqlUserResponseGraphQLField("email")
    id: "GqlUserResponseGraphQLField" = GqlUserResponseGraphQLField("id")
    identity_provider: "GqlUserResponseGraphQLField" = GqlUserResponseGraphQLField(
        "identityProvider"
    )
    permissions: "GqlUserResponseGraphQLField" = GqlUserResponseGraphQLField(
        "permissions"
    )
    username: "GqlUserResponseGraphQLField" = GqlUserResponseGraphQLField("username")

    def fields(
        self, *subfields: GqlUserResponseGraphQLField
    ) -> "GqlUserResponseFields":
        """Subfields should come from the GqlUserResponseFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GqlUserResponseFields":
        self._alias = alias
        return self


class HcCalibrationFields(GraphQLField):
    calibration_time_local: "HcCalibrationGraphQLField" = HcCalibrationGraphQLField(
        "calibrationTimeLocal"
    )
    calibration_work_package_config: "HcCalibrationGraphQLField" = (
        HcCalibrationGraphQLField("calibrationWorkPackageConfig")
    )
    completed_at: "HcCalibrationGraphQLField" = HcCalibrationGraphQLField("completedAt")
    feeders: "HcCalibrationGraphQLField" = HcCalibrationGraphQLField("feeders")
    name: "HcCalibrationGraphQLField" = HcCalibrationGraphQLField("name")
    run_id: "HcCalibrationGraphQLField" = HcCalibrationGraphQLField("runId")
    run_info: "HcCalibrationGraphQLField" = HcCalibrationGraphQLField("runInfo")
    start_at: "HcCalibrationGraphQLField" = HcCalibrationGraphQLField("startAt")
    status: "HcCalibrationGraphQLField" = HcCalibrationGraphQLField("status")
    workflow_id: "HcCalibrationGraphQLField" = HcCalibrationGraphQLField("workflowId")
    id: "HcCalibrationGraphQLField" = HcCalibrationGraphQLField("id")

    def fields(self, *subfields: HcCalibrationGraphQLField) -> "HcCalibrationFields":
        """Subfields should come from the HcCalibrationFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "HcCalibrationFields":
        self._alias = alias
        return self


class HcModelFields(GraphQLField):
    """HC model representation"""

    feeder: "HcModelGraphQLField" = HcModelGraphQLField("feeder")
    scenario: "HcModelGraphQLField" = HcModelGraphQLField("scenario")
    year: "HcModelGraphQLField" = HcModelGraphQLField("year")

    def fields(self, *subfields: HcModelGraphQLField) -> "HcModelFields":
        """Subfields should come from the HcModelFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "HcModelFields":
        self._alias = alias
        return self


class HcScenarioConfigsPageFields(GraphQLField):
    offset: "HcScenarioConfigsPageGraphQLField" = HcScenarioConfigsPageGraphQLField(
        "offset"
    )

    @classmethod
    def scenario_configs(cls) -> "ScenarioConfigurationFields":
        return ScenarioConfigurationFields("scenarioConfigs")

    total_count: "HcScenarioConfigsPageGraphQLField" = (
        HcScenarioConfigsPageGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            HcScenarioConfigsPageGraphQLField, "ScenarioConfigurationFields"
        ]
    ) -> "HcScenarioConfigsPageFields":
        """Subfields should come from the HcScenarioConfigsPageFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "HcScenarioConfigsPageFields":
        self._alias = alias
        return self


class HcWorkPackageFields(GraphQLField):
    completed_at: "HcWorkPackageGraphQLField" = HcWorkPackageGraphQLField("completedAt")
    created_at: "HcWorkPackageGraphQLField" = HcWorkPackageGraphQLField("createdAt")

    @classmethod
    def created_by(cls) -> "GqlUserFields":
        return GqlUserFields("createdBy")

    feeders: "HcWorkPackageGraphQLField" = HcWorkPackageGraphQLField("feeders")
    is_deleted: "HcWorkPackageGraphQLField" = HcWorkPackageGraphQLField("isDeleted")
    load_type: "HcWorkPackageGraphQLField" = HcWorkPackageGraphQLField("loadType")
    name: "HcWorkPackageGraphQLField" = HcWorkPackageGraphQLField("name")
    parent_id: "HcWorkPackageGraphQLField" = HcWorkPackageGraphQLField("parentId")

    @classmethod
    def progress_details(cls) -> "WorkPackageProgressDetailsFields":
        return WorkPackageProgressDetailsFields("progressDetails")

    scenarios: "HcWorkPackageGraphQLField" = HcWorkPackageGraphQLField("scenarios")
    status: "HcWorkPackageGraphQLField" = HcWorkPackageGraphQLField("status")
    time_period_end: "HcWorkPackageGraphQLField" = HcWorkPackageGraphQLField(
        "timePeriodEnd"
    )
    time_period_start: "HcWorkPackageGraphQLField" = HcWorkPackageGraphQLField(
        "timePeriodStart"
    )
    years: "HcWorkPackageGraphQLField" = HcWorkPackageGraphQLField("years")
    id: "HcWorkPackageGraphQLField" = HcWorkPackageGraphQLField("id")
    config: "HcWorkPackageGraphQLField" = HcWorkPackageGraphQLField("config")
    description: "HcWorkPackageGraphQLField" = HcWorkPackageGraphQLField("description")
    updated_at: "HcWorkPackageGraphQLField" = HcWorkPackageGraphQLField("updatedAt")

    def fields(
        self,
        *subfields: Union[
            HcWorkPackageGraphQLField,
            "GqlUserFields",
            "WorkPackageProgressDetailsFields",
        ]
    ) -> "HcWorkPackageFields":
        """Subfields should come from the HcWorkPackageFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "HcWorkPackageFields":
        self._alias = alias
        return self


class HcWorkPackagePageFields(GraphQLField):
    all_users: "HcWorkPackagePageGraphQLField" = HcWorkPackagePageGraphQLField(
        "allUsers"
    )
    offset: "HcWorkPackagePageGraphQLField" = HcWorkPackagePageGraphQLField("offset")
    total_count: "HcWorkPackagePageGraphQLField" = HcWorkPackagePageGraphQLField(
        "totalCount"
    )

    @classmethod
    def work_packages(cls) -> "HcWorkPackageFields":
        return HcWorkPackageFields("workPackages")

    def fields(
        self, *subfields: Union[HcWorkPackagePageGraphQLField, "HcWorkPackageFields"]
    ) -> "HcWorkPackagePageFields":
        """Subfields should come from the HcWorkPackagePageFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "HcWorkPackagePageFields":
        self._alias = alias
        return self


class IngestionJobFields(GraphQLField):
    application: "IngestionJobGraphQLField" = IngestionJobGraphQLField("application")
    application_version: "IngestionJobGraphQLField" = IngestionJobGraphQLField(
        "applicationVersion"
    )
    id: "IngestionJobGraphQLField" = IngestionJobGraphQLField("id")
    source: "IngestionJobGraphQLField" = IngestionJobGraphQLField("source")
    start_time: "IngestionJobGraphQLField" = IngestionJobGraphQLField("startTime")

    def fields(self, *subfields: IngestionJobGraphQLField) -> "IngestionJobFields":
        """Subfields should come from the IngestionJobFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "IngestionJobFields":
        self._alias = alias
        return self


class IngestionRunFields(GraphQLField):
    completed_at: "IngestionRunGraphQLField" = IngestionRunGraphQLField("completedAt")
    container_runtime_type: "IngestionRunGraphQLField" = IngestionRunGraphQLField(
        "containerRuntimeType"
    )
    payload: "IngestionRunGraphQLField" = IngestionRunGraphQLField("payload")
    started_at: "IngestionRunGraphQLField" = IngestionRunGraphQLField("startedAt")
    status: "IngestionRunGraphQLField" = IngestionRunGraphQLField("status")
    status_last_updated_at: "IngestionRunGraphQLField" = IngestionRunGraphQLField(
        "statusLastUpdatedAt"
    )
    token: "IngestionRunGraphQLField" = IngestionRunGraphQLField("token")
    id: "IngestionRunGraphQLField" = IngestionRunGraphQLField("id")

    def fields(self, *subfields: IngestionRunGraphQLField) -> "IngestionRunFields":
        """Subfields should come from the IngestionRunFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "IngestionRunFields":
        self._alias = alias
        return self


class IngestorRunPageFields(GraphQLField):
    @classmethod
    def ingestor_runs(cls) -> "IngestionRunFields":
        return IngestionRunFields("ingestorRuns")

    offset: "IngestorRunPageGraphQLField" = IngestorRunPageGraphQLField("offset")
    total_count: "IngestorRunPageGraphQLField" = IngestorRunPageGraphQLField(
        "totalCount"
    )

    def fields(
        self, *subfields: Union[IngestorRunPageGraphQLField, "IngestionRunFields"]
    ) -> "IngestorRunPageFields":
        """Subfields should come from the IngestorRunPageFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "IngestorRunPageFields":
        self._alias = alias
        return self


class JobSourceFields(GraphQLField):
    file_hash: "JobSourceGraphQLField" = JobSourceGraphQLField("fileHash")
    name: "JobSourceGraphQLField" = JobSourceGraphQLField("name")
    timestamp: "JobSourceGraphQLField" = JobSourceGraphQLField("timestamp")

    def fields(self, *subfields: JobSourceGraphQLField) -> "JobSourceFields":
        """Subfields should come from the JobSourceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "JobSourceFields":
        self._alias = alias
        return self


class MachineUserFields(GraphQLField):
    display_name: "MachineUserGraphQLField" = MachineUserGraphQLField("displayName")
    username: "MachineUserGraphQLField" = MachineUserGraphQLField("username")

    def fields(self, *subfields: MachineUserGraphQLField) -> "MachineUserFields":
        """Subfields should come from the MachineUserFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "MachineUserFields":
        self._alias = alias
        return self


class MetricFields(GraphQLField):
    name: "MetricGraphQLField" = MetricGraphQLField("name")
    value: "MetricGraphQLField" = MetricGraphQLField("value")

    def fields(self, *subfields: MetricGraphQLField) -> "MetricFields":
        """Subfields should come from the MetricFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "MetricFields":
        self._alias = alias
        return self


class NetworkModelFields(GraphQLField):
    database_name: "NetworkModelGraphQLField" = NetworkModelGraphQLField("databaseName")
    source_data_date: "NetworkModelGraphQLField" = NetworkModelGraphQLField(
        "sourceDataDate"
    )

    def fields(self, *subfields: NetworkModelGraphQLField) -> "NetworkModelFields":
        """Subfields should come from the NetworkModelFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "NetworkModelFields":
        self._alias = alias
        return self


class NetworkModelsFields(GraphQLField):
    @classmethod
    def available_network_models(cls) -> "NetworkModelFields":
        return NetworkModelFields("availableNetworkModels")

    currently_loaded_network_model: "NetworkModelsGraphQLField" = (
        NetworkModelsGraphQLField("currentlyLoadedNetworkModel")
    )
    network_date_locked: "NetworkModelsGraphQLField" = NetworkModelsGraphQLField(
        "networkDateLocked"
    )

    def fields(
        self, *subfields: Union[NetworkModelsGraphQLField, "NetworkModelFields"]
    ) -> "NetworkModelsFields":
        """Subfields should come from the NetworkModelsFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "NetworkModelsFields":
        self._alias = alias
        return self


class OpenDssModelFields(GraphQLField):
    created_at: "OpenDssModelGraphQLField" = OpenDssModelGraphQLField("createdAt")
    created_by: "OpenDssModelGraphQLField" = OpenDssModelGraphQLField("createdBy")
    download_url: "OpenDssModelGraphQLField" = OpenDssModelGraphQLField("downloadUrl")
    errors: "OpenDssModelGraphQLField" = OpenDssModelGraphQLField("errors")
    generation_spec: "OpenDssModelGraphQLField" = OpenDssModelGraphQLField(
        "generationSpec"
    )
    id: "OpenDssModelGraphQLField" = OpenDssModelGraphQLField("id")
    is_public: "OpenDssModelGraphQLField" = OpenDssModelGraphQLField("isPublic")
    name: "OpenDssModelGraphQLField" = OpenDssModelGraphQLField("name")
    state: "OpenDssModelGraphQLField" = OpenDssModelGraphQLField("state")

    def fields(self, *subfields: OpenDssModelGraphQLField) -> "OpenDssModelFields":
        """Subfields should come from the OpenDssModelFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "OpenDssModelFields":
        self._alias = alias
        return self


class OpenDssModelPageFields(GraphQLField):
    @classmethod
    def models(cls) -> "OpenDssModelFields":
        return OpenDssModelFields("models")

    offset: "OpenDssModelPageGraphQLField" = OpenDssModelPageGraphQLField("offset")
    total_count: "OpenDssModelPageGraphQLField" = OpenDssModelPageGraphQLField(
        "totalCount"
    )

    def fields(
        self, *subfields: Union[OpenDssModelPageGraphQLField, "OpenDssModelFields"]
    ) -> "OpenDssModelPageFields":
        """Subfields should come from the OpenDssModelPageFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "OpenDssModelPageFields":
        self._alias = alias
        return self


class OpportunitiesByYearFields(GraphQLField):
    """Opportunities available for a specific year."""

    @classmethod
    def available_opportunities(cls) -> "OpportunityFields":
        return OpportunityFields("availableOpportunities")

    year: "OpportunitiesByYearGraphQLField" = OpportunitiesByYearGraphQLField("year")

    def fields(
        self, *subfields: Union[OpportunitiesByYearGraphQLField, "OpportunityFields"]
    ) -> "OpportunitiesByYearFields":
        """Subfields should come from the OpportunitiesByYearFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "OpportunitiesByYearFields":
        self._alias = alias
        return self


class OpportunityFields(GraphQLField):
    annual_deferral_value: "OpportunityGraphQLField" = OpportunityGraphQLField(
        "annualDeferralValue"
    )

    @classmethod
    def conducting_equipment(cls) -> "EquipmentFields":
        return EquipmentFields("conductingEquipment")

    connection_voltage_level: "OpportunityGraphQLField" = OpportunityGraphQLField(
        "connectionVoltageLevel"
    )
    constraint_primary_driver: "OpportunityGraphQLField" = OpportunityGraphQLField(
        "constraintPrimaryDriver"
    )
    days_required: "OpportunityGraphQLField" = OpportunityGraphQLField("daysRequired")
    downstream_customers: "OpportunityGraphQLField" = OpportunityGraphQLField(
        "downstreamCustomers"
    )
    est_annual_hours: "OpportunityGraphQLField" = OpportunityGraphQLField(
        "estAnnualHours"
    )
    est_duration_per_event: "OpportunityGraphQLField" = OpportunityGraphQLField(
        "estDurationPerEvent"
    )
    est_number_of_events: "OpportunityGraphQLField" = OpportunityGraphQLField(
        "estNumberOfEvents"
    )
    id: "OpportunityGraphQLField" = OpportunityGraphQLField("id")
    min_capacity: "OpportunityGraphQLField" = OpportunityGraphQLField("minCapacity")
    need_direction: "OpportunityGraphQLField" = OpportunityGraphQLField("needDirection")
    peak_demand: "OpportunityGraphQLField" = OpportunityGraphQLField("peakDemand")
    time_required: "OpportunityGraphQLField" = OpportunityGraphQLField("timeRequired")
    title: "OpportunityGraphQLField" = OpportunityGraphQLField("title")
    year: "OpportunityGraphQLField" = OpportunityGraphQLField("year")

    @classmethod
    def polygon(cls) -> "GeoJsonFeatureFields":
        return GeoJsonFeatureFields("polygon")

    def fields(
        self,
        *subfields: Union[
            OpportunityGraphQLField, "EquipmentFields", "GeoJsonFeatureFields"
        ]
    ) -> "OpportunityFields":
        """Subfields should come from the OpportunityFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "OpportunityFields":
        self._alias = alias
        return self


class OpportunityLocationFields(GraphQLField):
    @classmethod
    def coordinates(cls) -> "CoordinateFields":
        return CoordinateFields("coordinates")

    m_rid: "OpportunityLocationGraphQLField" = OpportunityLocationGraphQLField("mRID")

    def fields(
        self, *subfields: Union[OpportunityLocationGraphQLField, "CoordinateFields"]
    ) -> "OpportunityLocationFields":
        """Subfields should come from the OpportunityLocationFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "OpportunityLocationFields":
        self._alias = alias
        return self


class PowerFactoryModelFields(GraphQLField):
    created_at: "PowerFactoryModelGraphQLField" = PowerFactoryModelGraphQLField(
        "createdAt"
    )
    errors: "PowerFactoryModelGraphQLField" = PowerFactoryModelGraphQLField("errors")

    @classmethod
    def generation_spec(cls) -> "PowerFactoryModelGenerationSpecFields":
        return PowerFactoryModelGenerationSpecFields("generationSpec")

    id: "PowerFactoryModelGraphQLField" = PowerFactoryModelGraphQLField("id")
    is_public: "PowerFactoryModelGraphQLField" = PowerFactoryModelGraphQLField(
        "isPublic"
    )
    name: "PowerFactoryModelGraphQLField" = PowerFactoryModelGraphQLField("name")
    state: "PowerFactoryModelGraphQLField" = PowerFactoryModelGraphQLField("state")

    def fields(
        self,
        *subfields: Union[
            PowerFactoryModelGraphQLField, "PowerFactoryModelGenerationSpecFields"
        ]
    ) -> "PowerFactoryModelFields":
        """Subfields should come from the PowerFactoryModelFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "PowerFactoryModelFields":
        self._alias = alias
        return self


class PowerFactoryModelGenerationSpecFields(GraphQLField):
    @classmethod
    def distribution_transformer_config(
        cls,
    ) -> "GqlDistributionTransformerConfigFields":
        return GqlDistributionTransformerConfigFields("distributionTransformerConfig")

    equipment_container_mrids: "PowerFactoryModelGenerationSpecGraphQLField" = (
        PowerFactoryModelGenerationSpecGraphQLField("equipmentContainerMrids")
    )

    @classmethod
    def load_config(cls) -> "GqlLoadConfigFields":
        return GqlLoadConfigFields("loadConfig")

    @classmethod
    def scenario_config(cls) -> "GqlScenarioConfigFields":
        return GqlScenarioConfigFields("scenarioConfig")

    def fields(
        self,
        *subfields: Union[
            PowerFactoryModelGenerationSpecGraphQLField,
            "GqlDistributionTransformerConfigFields",
            "GqlLoadConfigFields",
            "GqlScenarioConfigFields",
        ]
    ) -> "PowerFactoryModelGenerationSpecFields":
        """Subfields should come from the PowerFactoryModelGenerationSpecFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "PowerFactoryModelGenerationSpecFields":
        self._alias = alias
        return self


class PowerFactoryModelPageFields(GraphQLField):
    offset: "PowerFactoryModelPageGraphQLField" = PowerFactoryModelPageGraphQLField(
        "offset"
    )

    @classmethod
    def power_factory_models(cls) -> "PowerFactoryModelFields":
        return PowerFactoryModelFields("powerFactoryModels")

    total_count: "PowerFactoryModelPageGraphQLField" = (
        PowerFactoryModelPageGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[PowerFactoryModelPageGraphQLField, "PowerFactoryModelFields"]
    ) -> "PowerFactoryModelPageFields":
        """Subfields should come from the PowerFactoryModelPageFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "PowerFactoryModelPageFields":
        self._alias = alias
        return self


class PowerFactoryModelTemplateFields(GraphQLField):
    created_at: "PowerFactoryModelTemplateGraphQLField" = (
        PowerFactoryModelTemplateGraphQLField("createdAt")
    )

    @classmethod
    def generation_spec(cls) -> "PowerFactoryModelGenerationSpecFields":
        return PowerFactoryModelGenerationSpecFields("generationSpec")

    id: "PowerFactoryModelTemplateGraphQLField" = PowerFactoryModelTemplateGraphQLField(
        "id"
    )
    is_public: "PowerFactoryModelTemplateGraphQLField" = (
        PowerFactoryModelTemplateGraphQLField("isPublic")
    )
    name: "PowerFactoryModelTemplateGraphQLField" = (
        PowerFactoryModelTemplateGraphQLField("name")
    )

    def fields(
        self,
        *subfields: Union[
            PowerFactoryModelTemplateGraphQLField,
            "PowerFactoryModelGenerationSpecFields",
        ]
    ) -> "PowerFactoryModelTemplateFields":
        """Subfields should come from the PowerFactoryModelTemplateFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "PowerFactoryModelTemplateFields":
        self._alias = alias
        return self


class PowerFactoryModelTemplatePageFields(GraphQLField):
    offset: "PowerFactoryModelTemplatePageGraphQLField" = (
        PowerFactoryModelTemplatePageGraphQLField("offset")
    )

    @classmethod
    def templates(cls) -> "PowerFactoryModelTemplateFields":
        return PowerFactoryModelTemplateFields("templates")

    total_count: "PowerFactoryModelTemplatePageGraphQLField" = (
        PowerFactoryModelTemplatePageGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            PowerFactoryModelTemplatePageGraphQLField, "PowerFactoryModelTemplateFields"
        ]
    ) -> "PowerFactoryModelTemplatePageFields":
        """Subfields should come from the PowerFactoryModelTemplatePageFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "PowerFactoryModelTemplatePageFields":
        self._alias = alias
        return self


class ProcessedDiffFields(GraphQLField):
    description: "ProcessedDiffGraphQLField" = ProcessedDiffGraphQLField("description")
    diff_id: "ProcessedDiffGraphQLField" = ProcessedDiffGraphQLField("diffId")
    feeder: "ProcessedDiffGraphQLField" = ProcessedDiffGraphQLField("feeder")
    name: "ProcessedDiffGraphQLField" = ProcessedDiffGraphQLField("name")
    scenario: "ProcessedDiffGraphQLField" = ProcessedDiffGraphQLField("scenario")
    type_: "ProcessedDiffGraphQLField" = ProcessedDiffGraphQLField("type")

    @classmethod
    def w_p_id_1(cls) -> "HcWorkPackageFields":
        return HcWorkPackageFields("wPId1")

    @classmethod
    def w_p_id_2(cls) -> "HcWorkPackageFields":
        return HcWorkPackageFields("wPId2")

    year: "ProcessedDiffGraphQLField" = ProcessedDiffGraphQLField("year")

    def fields(
        self, *subfields: Union[ProcessedDiffGraphQLField, "HcWorkPackageFields"]
    ) -> "ProcessedDiffFields":
        """Subfields should come from the ProcessedDiffFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProcessedDiffFields":
        self._alias = alias
        return self


class ProcessedDiffPageFields(GraphQLField):
    offset: "ProcessedDiffPageGraphQLField" = ProcessedDiffPageGraphQLField("offset")

    @classmethod
    def processed_diff(cls) -> "ProcessedDiffFields":
        return ProcessedDiffFields("processedDiff")

    total_count: "ProcessedDiffPageGraphQLField" = ProcessedDiffPageGraphQLField(
        "totalCount"
    )

    def fields(
        self, *subfields: Union[ProcessedDiffPageGraphQLField, "ProcessedDiffFields"]
    ) -> "ProcessedDiffPageFields":
        """Subfields should come from the ProcessedDiffPageFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProcessedDiffPageFields":
        self._alias = alias
        return self


class RemoveAppOptionResultFields(GraphQLField):
    """Result of removing an application option"""

    name: "RemoveAppOptionResultGraphQLField" = RemoveAppOptionResultGraphQLField(
        "name"
    )
    removed: "RemoveAppOptionResultGraphQLField" = RemoveAppOptionResultGraphQLField(
        "removed"
    )

    def fields(
        self, *subfields: RemoveAppOptionResultGraphQLField
    ) -> "RemoveAppOptionResultFields":
        """Subfields should come from the RemoveAppOptionResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "RemoveAppOptionResultFields":
        self._alias = alias
        return self


class ResultSectionInterface(GraphQLField):
    name: "ResultSectionGraphQLField" = ResultSectionGraphQLField("name")
    type_: "ResultSectionGraphQLField" = ResultSectionGraphQLField("type")
    id: "ResultSectionGraphQLField" = ResultSectionGraphQLField("id")
    description: "ResultSectionGraphQLField" = ResultSectionGraphQLField("description")

    def fields(self, *subfields: ResultSectionGraphQLField) -> "ResultSectionInterface":
        """Subfields should come from the ResultSectionInterface class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ResultSectionInterface":
        self._alias = alias
        return self

    def on(self, type_name: str, *subfields: GraphQLField) -> "ResultSectionInterface":
        self._inline_fragments[type_name] = subfields
        return self


class ScenarioConfigurationFields(GraphQLField):
    bess_allocation_id: "ScenarioConfigurationGraphQLField" = (
        ScenarioConfigurationGraphQLField("bessAllocationId")
    )
    bess_forecast_level: "ScenarioConfigurationGraphQLField" = (
        ScenarioConfigurationGraphQLField("bessForecastLevel")
    )
    bess_forecasts_scenario: "ScenarioConfigurationGraphQLField" = (
        ScenarioConfigurationGraphQLField("bessForecastsScenario")
    )
    demand_forecast_level: "ScenarioConfigurationGraphQLField" = (
        ScenarioConfigurationGraphQLField("demandForecastLevel")
    )
    demand_forecast_poe: "ScenarioConfigurationGraphQLField" = (
        ScenarioConfigurationGraphQLField("demandForecastPoe")
    )
    demand_forecasts_scenario: "ScenarioConfigurationGraphQLField" = (
        ScenarioConfigurationGraphQLField("demandForecastsScenario")
    )
    ev_allocation_id: "ScenarioConfigurationGraphQLField" = (
        ScenarioConfigurationGraphQLField("evAllocationId")
    )
    ev_forecast_level: "ScenarioConfigurationGraphQLField" = (
        ScenarioConfigurationGraphQLField("evForecastLevel")
    )
    ev_forecasts_scenario: "ScenarioConfigurationGraphQLField" = (
        ScenarioConfigurationGraphQLField("evForecastsScenario")
    )
    pv_allocation_id: "ScenarioConfigurationGraphQLField" = (
        ScenarioConfigurationGraphQLField("pvAllocationId")
    )
    pv_forecast_level: "ScenarioConfigurationGraphQLField" = (
        ScenarioConfigurationGraphQLField("pvForecastLevel")
    )
    pv_forecasts_scenario: "ScenarioConfigurationGraphQLField" = (
        ScenarioConfigurationGraphQLField("pvForecastsScenario")
    )
    scenario_name: "ScenarioConfigurationGraphQLField" = (
        ScenarioConfigurationGraphQLField("scenarioName")
    )
    id: "ScenarioConfigurationGraphQLField" = ScenarioConfigurationGraphQLField("id")

    def fields(
        self, *subfields: ScenarioConfigurationGraphQLField
    ) -> "ScenarioConfigurationFields":
        """Subfields should come from the ScenarioConfigurationFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ScenarioConfigurationFields":
        self._alias = alias
        return self


class SincalConfigFileFields(GraphQLField):
    file_type: "SincalConfigFileGraphQLField" = SincalConfigFileGraphQLField("fileType")
    original_filename: "SincalConfigFileGraphQLField" = SincalConfigFileGraphQLField(
        "originalFilename"
    )
    raw_filename: "SincalConfigFileGraphQLField" = SincalConfigFileGraphQLField(
        "rawFilename"
    )
    standard_name: "SincalConfigFileGraphQLField" = SincalConfigFileGraphQLField(
        "standardName"
    )

    def fields(
        self, *subfields: SincalConfigFileGraphQLField
    ) -> "SincalConfigFileFields":
        """Subfields should come from the SincalConfigFileFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SincalConfigFileFields":
        self._alias = alias
        return self


class SincalGlobalInputsConfigFields(GraphQLField):
    @classmethod
    def backend_config(cls) -> "SincalConfigFileFields":
        return SincalConfigFileFields("backendConfig")

    @classmethod
    def frontend_config(cls) -> "SincalConfigFileFields":
        return SincalConfigFileFields("frontendConfig")

    @classmethod
    def in_feeder_mapping_database(cls) -> "SincalConfigFileFields":
        return SincalConfigFileFields("inFeederMappingDatabase")

    @classmethod
    def local_standard_database(cls) -> "SincalConfigFileFields":
        return SincalConfigFileFields("localStandardDatabase")

    @classmethod
    def protection_standard_database(cls) -> "SincalConfigFileFields":
        return SincalConfigFileFields("protectionStandardDatabase")

    @classmethod
    def template(cls) -> "SincalConfigFileFields":
        return SincalConfigFileFields("template")

    def fields(
        self,
        *subfields: Union[
            SincalGlobalInputsConfigGraphQLField, "SincalConfigFileFields"
        ]
    ) -> "SincalGlobalInputsConfigFields":
        """Subfields should come from the SincalGlobalInputsConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SincalGlobalInputsConfigFields":
        self._alias = alias
        return self


class SincalModelFields(GraphQLField):
    created_at: "SincalModelGraphQLField" = SincalModelGraphQLField("createdAt")
    created_by: "SincalModelGraphQLField" = SincalModelGraphQLField("createdBy")
    errors: "SincalModelGraphQLField" = SincalModelGraphQLField("errors")

    @classmethod
    def generation_spec(cls) -> "SincalModelGenerationSpecFields":
        """JSON exporter generation spec (auth tokens withheld)"""
        return SincalModelGenerationSpecFields("generationSpec")

    id: "SincalModelGraphQLField" = SincalModelGraphQLField("id")
    is_public: "SincalModelGraphQLField" = SincalModelGraphQLField("isPublic")
    name: "SincalModelGraphQLField" = SincalModelGraphQLField("name")
    state: "SincalModelGraphQLField" = SincalModelGraphQLField("state")

    def fields(
        self,
        *subfields: Union[SincalModelGraphQLField, "SincalModelGenerationSpecFields"]
    ) -> "SincalModelFields":
        """Subfields should come from the SincalModelFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SincalModelFields":
        self._alias = alias
        return self


class SincalModelGenerationSpecFields(GraphQLField):
    config: "SincalModelGenerationSpecGraphQLField" = (
        SincalModelGenerationSpecGraphQLField("config")
    )
    "JSON export config."
    equipment_container_mrids: "SincalModelGenerationSpecGraphQLField" = (
        SincalModelGenerationSpecGraphQLField("equipmentContainerMrids")
    )

    def fields(
        self, *subfields: SincalModelGenerationSpecGraphQLField
    ) -> "SincalModelGenerationSpecFields":
        """Subfields should come from the SincalModelGenerationSpecFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SincalModelGenerationSpecFields":
        self._alias = alias
        return self


class SincalModelPageFields(GraphQLField):
    offset: "SincalModelPageGraphQLField" = SincalModelPageGraphQLField("offset")

    @classmethod
    def sincal_models(cls) -> "SincalModelFields":
        return SincalModelFields("sincalModels")

    total_count: "SincalModelPageGraphQLField" = SincalModelPageGraphQLField(
        "totalCount"
    )

    def fields(
        self, *subfields: Union[SincalModelPageGraphQLField, "SincalModelFields"]
    ) -> "SincalModelPageFields":
        """Subfields should come from the SincalModelPageFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SincalModelPageFields":
        self._alias = alias
        return self


class SincalModelPresetFields(GraphQLField):
    created_at: "SincalModelPresetGraphQLField" = SincalModelPresetGraphQLField(
        "createdAt"
    )
    created_by: "SincalModelPresetGraphQLField" = SincalModelPresetGraphQLField(
        "createdBy"
    )

    @classmethod
    def generation_spec(cls) -> "SincalModelGenerationSpecFields":
        return SincalModelGenerationSpecFields("generationSpec")

    id: "SincalModelPresetGraphQLField" = SincalModelPresetGraphQLField("id")
    is_public: "SincalModelPresetGraphQLField" = SincalModelPresetGraphQLField(
        "isPublic"
    )
    name: "SincalModelPresetGraphQLField" = SincalModelPresetGraphQLField("name")

    def fields(
        self,
        *subfields: Union[
            SincalModelPresetGraphQLField, "SincalModelGenerationSpecFields"
        ]
    ) -> "SincalModelPresetFields":
        """Subfields should come from the SincalModelPresetFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SincalModelPresetFields":
        self._alias = alias
        return self


class SincalModelPresetPageFields(GraphQLField):
    offset: "SincalModelPresetPageGraphQLField" = SincalModelPresetPageGraphQLField(
        "offset"
    )

    @classmethod
    def presets(cls) -> "SincalModelPresetFields":
        return SincalModelPresetFields("presets")

    total_count: "SincalModelPresetPageGraphQLField" = (
        SincalModelPresetPageGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[SincalModelPresetPageGraphQLField, "SincalModelPresetFields"]
    ) -> "SincalModelPresetPageFields":
        """Subfields should come from the SincalModelPresetPageFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SincalModelPresetPageFields":
        self._alias = alias
        return self


class StateOverlayFields(GraphQLField):
    styles: "StateOverlayGraphQLField" = StateOverlayGraphQLField("styles")
    id: "StateOverlayGraphQLField" = StateOverlayGraphQLField("id")
    data: "StateOverlayGraphQLField" = StateOverlayGraphQLField("data")

    def fields(self, *subfields: StateOverlayGraphQLField) -> "StateOverlayFields":
        """Subfields should come from the StateOverlayFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "StateOverlayFields":
        self._alias = alias
        return self


class StudyFields(GraphQLField):
    created_at: "StudyGraphQLField" = StudyGraphQLField("createdAt")
    name: "StudyGraphQLField" = StudyGraphQLField("name")
    tags: "StudyGraphQLField" = StudyGraphQLField("tags")
    id: "StudyGraphQLField" = StudyGraphQLField("id")

    @classmethod
    def created_by(cls) -> "GqlUserFields":
        return GqlUserFields("createdBy")

    description: "StudyGraphQLField" = StudyGraphQLField("description")

    @classmethod
    def results(cls) -> "StudyResultFields":
        return StudyResultFields("results")

    styles: "StudyGraphQLField" = StudyGraphQLField("styles")

    def fields(
        self, *subfields: Union[StudyGraphQLField, "GqlUserFields", "StudyResultFields"]
    ) -> "StudyFields":
        """Subfields should come from the StudyFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "StudyFields":
        self._alias = alias
        return self


class StudyPageFields(GraphQLField):
    all_tags: "StudyPageGraphQLField" = StudyPageGraphQLField("allTags")
    all_users: "StudyPageGraphQLField" = StudyPageGraphQLField("allUsers")
    offset: "StudyPageGraphQLField" = StudyPageGraphQLField("offset")

    @classmethod
    def studies(cls) -> "StudyFields":
        return StudyFields("studies")

    total_count: "StudyPageGraphQLField" = StudyPageGraphQLField("totalCount")

    def fields(
        self, *subfields: Union[StudyPageGraphQLField, "StudyFields"]
    ) -> "StudyPageFields":
        """Subfields should come from the StudyPageFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "StudyPageFields":
        self._alias = alias
        return self


class StudyResultFields(GraphQLField):
    name: "StudyResultGraphQLField" = StudyResultGraphQLField("name")
    id: "StudyResultGraphQLField" = StudyResultGraphQLField("id")

    @classmethod
    def geo_json_overlay(cls) -> "GeoJsonOverlayFields":
        return GeoJsonOverlayFields("geoJsonOverlay")

    @classmethod
    def sections(cls) -> "ResultSectionInterface":
        return ResultSectionInterface("sections")

    @classmethod
    def state_overlay(cls) -> "StateOverlayFields":
        return StateOverlayFields("stateOverlay")

    def fields(
        self,
        *subfields: Union[
            StudyResultGraphQLField,
            "GeoJsonOverlayFields",
            "ResultSectionInterface",
            "StateOverlayFields",
        ]
    ) -> "StudyResultFields":
        """Subfields should come from the StudyResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "StudyResultFields":
        self._alias = alias
        return self


class TableSectionFields(GraphQLField):
    id: "TableSectionGraphQLField" = TableSectionGraphQLField("id")
    name: "TableSectionGraphQLField" = TableSectionGraphQLField("name")
    type_: "TableSectionGraphQLField" = TableSectionGraphQLField("type")

    @classmethod
    def columns(cls) -> "ColumnFields":
        return ColumnFields("columns")

    @classmethod
    def data(
        cls, *, serialization: Optional[SerializationType] = None
    ) -> "TableSectionGraphQLField":
        arguments: dict[str, dict[str, Any]] = {
            "serialization": {"type": "SerializationType", "value": serialization}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return TableSectionGraphQLField("data", arguments=cleared_arguments)

    description: "TableSectionGraphQLField" = TableSectionGraphQLField("description")

    def fields(
        self, *subfields: Union[TableSectionGraphQLField, "ColumnFields"]
    ) -> "TableSectionFields":
        """Subfields should come from the TableSectionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TableSectionFields":
        self._alias = alias
        return self


class UploadUrlResponseFields(GraphQLField):
    file_path: "UploadUrlResponseGraphQLField" = UploadUrlResponseGraphQLField(
        "filePath"
    )
    upload_url: "UploadUrlResponseGraphQLField" = UploadUrlResponseGraphQLField(
        "uploadUrl"
    )

    def fields(
        self, *subfields: UploadUrlResponseGraphQLField
    ) -> "UploadUrlResponseFields":
        """Subfields should come from the UploadUrlResponseFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UploadUrlResponseFields":
        self._alias = alias
        return self


class UserCustomerListColumnConfigFields(GraphQLField):
    """User-specific column configuration for the customer list table."""

    @classmethod
    def columns(cls) -> "CustomerListColumnConfigFields":
        """List of columns configured by the user to display in the customer list table."""
        return CustomerListColumnConfigFields("columns")

    def fields(
        self,
        *subfields: Union[
            UserCustomerListColumnConfigGraphQLField, "CustomerListColumnConfigFields"
        ]
    ) -> "UserCustomerListColumnConfigFields":
        """Subfields should come from the UserCustomerListColumnConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UserCustomerListColumnConfigFields":
        self._alias = alias
        return self


class VariantFields(GraphQLField):
    conducting_equipment_count: "VariantGraphQLField" = VariantGraphQLField(
        "conductingEquipmentCount"
    )
    m_rid: "VariantGraphQLField" = VariantGraphQLField("mRID")
    name: "VariantGraphQLField" = VariantGraphQLField("name")
    network_database_location: "VariantGraphQLField" = VariantGraphQLField(
        "networkDatabaseLocation"
    )
    new_parent: "VariantGraphQLField" = VariantGraphQLField("newParent")
    new_variant: "VariantGraphQLField" = VariantGraphQLField("newVariant")
    parent: "VariantGraphQLField" = VariantGraphQLField("parent")
    parent_mrid: "VariantGraphQLField" = VariantGraphQLField("parentMRID")
    status: "VariantGraphQLField" = VariantGraphQLField("status")

    def fields(self, *subfields: VariantGraphQLField) -> "VariantFields":
        """Subfields should come from the VariantFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "VariantFields":
        self._alias = alias
        return self


class VariantWorkPackageFields(GraphQLField):
    status: "VariantWorkPackageGraphQLField" = VariantWorkPackageGraphQLField("status")

    @classmethod
    def variants(cls) -> "VariantFields":
        return VariantFields("variants")

    def fields(
        self, *subfields: Union[VariantWorkPackageGraphQLField, "VariantFields"]
    ) -> "VariantWorkPackageFields":
        """Subfields should come from the VariantWorkPackageFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "VariantWorkPackageFields":
        self._alias = alias
        return self


class WorkPackageModelGroupingsFields(GraphQLField):
    @classmethod
    def cancelled(cls) -> "HcModelFields":
        return HcModelFields("cancelled")

    @classmethod
    def execution(cls) -> "HcModelFields":
        return HcModelFields("execution")

    @classmethod
    def failed(cls) -> "HcModelFields":
        return HcModelFields("failed")

    @classmethod
    def generation(cls) -> "HcModelFields":
        return HcModelFields("generation")

    @classmethod
    def pending(cls) -> "HcModelFields":
        return HcModelFields("pending")

    @classmethod
    def result_processing(cls) -> "HcModelFields":
        return HcModelFields("resultProcessing")

    @classmethod
    def succeeded(cls) -> "HcModelFields":
        return HcModelFields("succeeded")

    @classmethod
    def timed_out(cls) -> "HcModelFields":
        return HcModelFields("timedOut")

    def fields(
        self, *subfields: Union[WorkPackageModelGroupingsGraphQLField, "HcModelFields"]
    ) -> "WorkPackageModelGroupingsFields":
        """Subfields should come from the WorkPackageModelGroupingsFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "WorkPackageModelGroupingsFields":
        self._alias = alias
        return self


class WorkPackageModelTotalsFields(GraphQLField):
    total_cancelled: "WorkPackageModelTotalsGraphQLField" = (
        WorkPackageModelTotalsGraphQLField("totalCancelled")
    )
    total_failed: "WorkPackageModelTotalsGraphQLField" = (
        WorkPackageModelTotalsGraphQLField("totalFailed")
    )
    total_models: "WorkPackageModelTotalsGraphQLField" = (
        WorkPackageModelTotalsGraphQLField("totalModels")
    )
    total_pending: "WorkPackageModelTotalsGraphQLField" = (
        WorkPackageModelTotalsGraphQLField("totalPending")
    )
    total_running: "WorkPackageModelTotalsGraphQLField" = (
        WorkPackageModelTotalsGraphQLField("totalRunning")
    )
    total_succeeded: "WorkPackageModelTotalsGraphQLField" = (
        WorkPackageModelTotalsGraphQLField("totalSucceeded")
    )
    total_timed_out: "WorkPackageModelTotalsGraphQLField" = (
        WorkPackageModelTotalsGraphQLField("totalTimedOut")
    )

    def fields(
        self, *subfields: WorkPackageModelTotalsGraphQLField
    ) -> "WorkPackageModelTotalsFields":
        """Subfields should come from the WorkPackageModelTotalsFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "WorkPackageModelTotalsFields":
        self._alias = alias
        return self


class WorkPackageProgressDetailsFields(GraphQLField):
    @classmethod
    def model_groupings(cls) -> "WorkPackageModelGroupingsFields":
        return WorkPackageModelGroupingsFields("modelGroupings")

    @classmethod
    def model_totals(cls) -> "WorkPackageModelTotalsFields":
        return WorkPackageModelTotalsFields("modelTotals")

    def fields(
        self,
        *subfields: Union[
            WorkPackageProgressDetailsGraphQLField,
            "WorkPackageModelGroupingsFields",
            "WorkPackageModelTotalsFields",
        ]
    ) -> "WorkPackageProgressDetailsFields":
        """Subfields should come from the WorkPackageProgressDetailsFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "WorkPackageProgressDetailsFields":
        self._alias = alias
        return self


class WorkPackageTreeFields(GraphQLField):
    @classmethod
    def ancestors(cls) -> "HcWorkPackageFields":
        return HcWorkPackageFields("ancestors")

    @classmethod
    def children(cls) -> "HcWorkPackageFields":
        return HcWorkPackageFields("children")

    def fields(
        self, *subfields: Union[WorkPackageTreeGraphQLField, "HcWorkPackageFields"]
    ) -> "WorkPackageTreeFields":
        """Subfields should come from the WorkPackageTreeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "WorkPackageTreeFields":
        self._alias = alias
        return self
