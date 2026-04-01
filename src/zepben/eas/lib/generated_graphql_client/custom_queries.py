from typing import Any, Optional

from .custom_fields import (
    AppOptionsFields,
    CustomerDetailsResponseFields,
    DurationCurveByTerminalFields,
    FeederLoadAnalysisReportFields,
    GqlTxTapRecordFields,
    GqlUserFields,
    GqlUserResponseFields,
    HcCalibrationFields,
    HcScenarioConfigsPageFields,
    HcWorkPackageFields,
    HcWorkPackagePageFields,
    IngestionJobFields,
    IngestionRunFields,
    IngestorRunPageFields,
    JobSourceFields,
    MachineUserFields,
    MetricFields,
    NetworkModelsFields,
    OpenDssModelPageFields,
    OpportunitiesByYearFields,
    OpportunityFields,
    OpportunityLocationFields,
    PowerFactoryModelFields,
    PowerFactoryModelPageFields,
    PowerFactoryModelTemplateFields,
    PowerFactoryModelTemplatePageFields,
    ProcessedDiffFields,
    ProcessedDiffPageFields,
    SincalGlobalInputsConfigFields,
    SincalModelFields,
    SincalModelPageFields,
    SincalModelPresetFields,
    SincalModelPresetPageFields,
    StudyFields,
    StudyPageFields,
    StudyResultFields,
    UploadUrlResponseFields,
    UserCustomerListColumnConfigFields,
    VariantWorkPackageFields,
    WorkPackageTreeFields,
)
from .custom_typing_fields import GraphQLField
from .enums import (
    ContainerType,
    HostingCapacityFileType,
    SincalFileType,
    VariantFileType,
    WorkflowStatus,
)
from .input_types import (
    GetOpenDssModelsFilterInput,
    GetOpenDssModelsSortCriteriaInput,
    GetPowerFactoryModelsFilterInput,
    GetPowerFactoryModelsSortCriteriaInput,
    GetPowerFactoryModelTemplatesFilterInput,
    GetPowerFactoryModelTemplatesSortCriteriaInput,
    GetSincalModelPresetsFilterInput,
    GetSincalModelPresetsSortCriteriaInput,
    GetSincalModelsFilterInput,
    GetSincalModelsSortCriteriaInput,
    GetStudiesFilterInput,
    GetStudiesSortCriteriaInput,
    HcScenarioConfigsFilterInput,
    HcWorkPackagesFilterInput,
    HcWorkPackagesSortCriteriaInput,
    IngestorRunsFilterInput,
    IngestorRunsSortCriteriaInput,
    ProcessedDiffFilterInput,
    ProcessedDiffSortCriteriaInput,
    WorkPackageInput,
)


class Query:
    @classmethod
    def paged_studies(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[GetStudiesFilterInput] = None,
        sort: Optional[GetStudiesSortCriteriaInput] = None,
    ) -> "GraphQLQuery[StudyPageFields, StudyPageGraphQLField]":
        pass

    @classmethod
    def results_by_id(
        cls, ids: list[str]
    ) -> "GraphQLQuery[StudyResultFields, StudyResultGraphQLField]":
        pass

    @classmethod
    def studies(
        cls, *, filter_: Optional[GetStudiesFilterInput] = None
    ) -> "GraphQLQuery[StudyFields, StudyGraphQLField]":
        pass

    @classmethod
    def studies_by_id(
        cls, ids: list[str]
    ) -> "GraphQLQuery[StudyFields, StudyGraphQLField]":
        pass

    @classmethod
    def styles_by_id(cls, ids: list[str]) -> "GraphQLQuery[GraphQLField, GraphQLField]":
        pass

    @classmethod
    def current_user(
        cls,
    ) -> "GraphQLQuery[GqlUserResponseFields, GqlUserResponseGraphQLField]":
        pass

    @classmethod
    def paged_power_factory_model_templates(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[GetPowerFactoryModelTemplatesFilterInput] = None,
        sort: Optional[GetPowerFactoryModelTemplatesSortCriteriaInput] = None,
    ) -> "GraphQLQuery[PowerFactoryModelTemplatePageFields, PowerFactoryModelTemplatePageGraphQLField]":
        pass

    @classmethod
    def paged_power_factory_models(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[GetPowerFactoryModelsFilterInput] = None,
        sort: Optional[GetPowerFactoryModelsSortCriteriaInput] = None,
    ) -> "GraphQLQuery[PowerFactoryModelPageFields, PowerFactoryModelPageGraphQLField]":
        pass

    @classmethod
    def power_factory_model_by_id(
        cls, model_id: str
    ) -> "GraphQLQuery[PowerFactoryModelFields, PowerFactoryModelGraphQLField]":
        pass

    @classmethod
    def power_factory_model_template_by_id(
        cls, template_id: str
    ) -> "GraphQLQuery[PowerFactoryModelTemplateFields, PowerFactoryModelTemplateGraphQLField]":
        pass

    @classmethod
    def power_factory_model_templates_by_ids(
        cls, template_ids: list[str]
    ) -> "GraphQLQuery[PowerFactoryModelTemplateFields, PowerFactoryModelTemplateGraphQLField]":
        pass

    @classmethod
    def power_factory_models_by_ids(
        cls, model_ids: list[str]
    ) -> "GraphQLQuery[PowerFactoryModelFields, PowerFactoryModelGraphQLField]":
        pass

    @classmethod
    def get_active_work_packages(cls) -> "GraphQLQuery[GraphQLField, GraphQLField]":
        pass

    @classmethod
    def get_all_work_packages_authors(
        cls,
    ) -> "GraphQLQuery[GqlUserFields, GqlUserGraphQLField]":
        pass

    @classmethod
    def get_calibration_run(
        cls, id: str
    ) -> "GraphQLQuery[HcCalibrationFields, HcCalibrationGraphQLField]":
        pass

    @classmethod
    def get_calibration_sets(cls) -> "GraphQLQuery[GraphQLField, GraphQLField]":
        pass

    @classmethod
    def get_duration_curves(
        cls,
        work_package_id: str,
        scenario: str,
        feeder: str,
        year: int,
        conducting_equipment_mrid: str,
    ) -> "GraphQLQuery[DurationCurveByTerminalFields, DurationCurveByTerminalGraphQLField]":
        pass

    @classmethod
    def get_opportunities(
        cls, *, year: Optional[int] = None
    ) -> "GraphQLQuery[OpportunitiesByYearFields, OpportunitiesByYearGraphQLField]":
        pass

    @classmethod
    def get_opportunities_for_equipment(
        cls, m_rid: str
    ) -> "GraphQLQuery[OpportunityFields, OpportunityGraphQLField]":
        pass

    @classmethod
    def get_opportunity(
        cls, id: str
    ) -> "GraphQLQuery[OpportunityFields, OpportunityGraphQLField]":
        pass

    @classmethod
    def get_opportunity_locations(
        cls, *, year: Optional[int] = None
    ) -> "GraphQLQuery[OpportunityLocationFields, OpportunityLocationGraphQLField]":
        pass

    @classmethod
    def get_scenario_configurations(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[HcScenarioConfigsFilterInput] = None,
    ) -> "GraphQLQuery[HcScenarioConfigsPageFields, HcScenarioConfigsPageGraphQLField]":
        pass

    @classmethod
    def get_transformer_tap_settings(
        cls,
        calibration_name: str,
        *,
        feeder: Optional[str] = None,
        transformer_mrid: Optional[str] = None,
    ) -> "GraphQLQuery[GqlTxTapRecordFields, GqlTxTapRecordGraphQLField]":
        pass

    @classmethod
    def get_work_package_by_id(
        cls, id: str, *, with_groupings: Optional[bool] = None
    ) -> "GraphQLQuery[HcWorkPackageFields, HcWorkPackageGraphQLField]":
        pass

    @classmethod
    def get_work_package_cost_estimation(
        cls, input: WorkPackageInput
    ) -> "GraphQLQuery[GraphQLField, GraphQLField]":
        pass

    @classmethod
    def get_work_package_tree(
        cls, id: str
    ) -> "GraphQLQuery[WorkPackageTreeFields, WorkPackageTreeGraphQLField]":
        pass

    @classmethod
    def get_work_packages(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[HcWorkPackagesFilterInput] = None,
        sort: Optional[HcWorkPackagesSortCriteriaInput] = None,
        with_groupings: Optional[bool] = None,
    ) -> "GraphQLQuery[HcWorkPackagePageFields, HcWorkPackagePageGraphQLField]":
        pass

    @classmethod
    def hosting_capacity_file_upload_url(
        cls, filename: str, file_type: HostingCapacityFileType
    ) -> "GraphQLQuery[UploadUrlResponseFields, UploadUrlResponseGraphQLField]":
        pass

    @classmethod
    def list_calibration_runs(
        cls,
        *,
        name: Optional[str] = None,
        calibration_time: Optional[Any] = None,
        status: Optional[WorkflowStatus] = None,
    ) -> "GraphQLQuery[HcCalibrationFields, HcCalibrationGraphQLField]":
        pass

    @classmethod
    def get_processed_diff(
        cls, diff_id: str
    ) -> "GraphQLQuery[ProcessedDiffFields, ProcessedDiffGraphQLField]":
        pass

    @classmethod
    def get_processed_diffs(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[ProcessedDiffFilterInput] = None,
        sort: Optional[ProcessedDiffSortCriteriaInput] = None,
    ) -> "GraphQLQuery[ProcessedDiffPageFields, ProcessedDiffPageGraphQLField]":
        pass

    @classmethod
    def get_all_jobs(
        cls,
    ) -> "GraphQLQuery[IngestionJobFields, IngestionJobGraphQLField]":
        pass

    @classmethod
    def get_distinct_metric_names(
        cls, job_id: str
    ) -> "GraphQLQuery[GraphQLField, GraphQLField]":
        pass

    @classmethod
    def get_metrics(
        cls, job_id: str, container_type: ContainerType, container_id: str
    ) -> "GraphQLQuery[MetricFields, MetricGraphQLField]":
        pass

    @classmethod
    def get_newest_job(
        cls,
    ) -> "GraphQLQuery[IngestionJobFields, IngestionJobGraphQLField]":
        pass

    @classmethod
    def get_sources(
        cls, job_id: str
    ) -> "GraphQLQuery[JobSourceFields, JobSourceGraphQLField]":
        pass

    @classmethod
    def paged_sincal_model_presets(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[GetSincalModelPresetsFilterInput] = None,
        sort: Optional[GetSincalModelPresetsSortCriteriaInput] = None,
    ) -> "GraphQLQuery[SincalModelPresetPageFields, SincalModelPresetPageGraphQLField]":
        pass

    @classmethod
    def paged_sincal_models(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[GetSincalModelsFilterInput] = None,
        sort: Optional[GetSincalModelsSortCriteriaInput] = None,
    ) -> "GraphQLQuery[SincalModelPageFields, SincalModelPageGraphQLField]":
        pass

    @classmethod
    def sincal_model_by_id(
        cls, model_id: str
    ) -> "GraphQLQuery[SincalModelFields, SincalModelGraphQLField]":
        pass

    @classmethod
    def sincal_model_config_upload_url(
        cls, filename: str, file_type: SincalFileType
    ) -> "GraphQLQuery[UploadUrlResponseFields, UploadUrlResponseGraphQLField]":
        pass

    @classmethod
    def sincal_model_global_config(
        cls,
    ) -> "GraphQLQuery[SincalGlobalInputsConfigFields, SincalGlobalInputsConfigGraphQLField]":
        pass

    @classmethod
    def sincal_model_preset_by_id(
        cls, preset_id: str
    ) -> "GraphQLQuery[SincalModelPresetFields, SincalModelPresetGraphQLField]":
        pass

    @classmethod
    def sincal_model_presets_by_ids(
        cls, preset_ids: list[str]
    ) -> "GraphQLQuery[SincalModelPresetFields, SincalModelPresetGraphQLField]":
        pass

    @classmethod
    def sincal_models_by_ids(
        cls, model_ids: list[str]
    ) -> "GraphQLQuery[SincalModelFields, SincalModelGraphQLField]":
        pass

    @classmethod
    def create_machine_api_key(
        cls, roles: list[str], token_name: str
    ) -> "GraphQLQuery[GraphQLField, GraphQLField]":
        pass

    @classmethod
    def create_user_api_key(
        cls, roles: list[str], token_name: str
    ) -> "GraphQLQuery[GraphQLField, GraphQLField]":
        pass

    @classmethod
    def get_machine_tokens(
        cls,
    ) -> "GraphQLQuery[MachineUserFields, MachineUserGraphQLField]":
        pass

    @classmethod
    def get_public_geo_view_config(cls) -> "GraphQLQuery[GraphQLField, GraphQLField]":
        pass

    @classmethod
    def get_all_external_roles(cls) -> "GraphQLQuery[GraphQLField, GraphQLField]":
        pass

    @classmethod
    def get_network_models(
        cls,
    ) -> "GraphQLQuery[NetworkModelsFields, NetworkModelsGraphQLField]":
        pass

    @classmethod
    def get_feeder_load_analysis_report_status(
        cls, report_id: str, full_spec: bool
    ) -> "GraphQLQuery[FeederLoadAnalysisReportFields, FeederLoadAnalysisReportGraphQLField]":
        pass

    @classmethod
    def get_ingestor_run(
        cls, id: int
    ) -> "GraphQLQuery[IngestionRunFields, IngestionRunGraphQLField]":
        pass

    @classmethod
    def list_ingestor_runs(
        cls,
        *,
        filter_: Optional[IngestorRunsFilterInput] = None,
        sort: Optional[IngestorRunsSortCriteriaInput] = None,
    ) -> "GraphQLQuery[IngestionRunFields, IngestionRunGraphQLField]":
        pass

    @classmethod
    def list_ingestor_runs_paged(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[IngestorRunsFilterInput] = None,
        sort: Optional[IngestorRunsSortCriteriaInput] = None,
    ) -> "GraphQLQuery[IngestorRunPageFields, IngestorRunPageGraphQLField]":
        pass

    @classmethod
    def paged_open_dss_models(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[GetOpenDssModelsFilterInput] = None,
        sort: Optional[GetOpenDssModelsSortCriteriaInput] = None,
    ) -> "GraphQLQuery[OpenDssModelPageFields, OpenDssModelPageGraphQLField]":
        pass

    @classmethod
    def get_user_permitted_customer_list_column_config(
        cls,
    ) -> "GraphQLQuery[UserCustomerListColumnConfigFields, UserCustomerListColumnConfigGraphQLField]":
        pass

    @classmethod
    def get_user_saved_customer_list_column_config(
        cls,
    ) -> "GraphQLQuery[UserCustomerListColumnConfigFields, UserCustomerListColumnConfigGraphQLField]":
        pass

    @classmethod
    def get_customer_list(
        cls, m_ri_ds: list[str]
    ) -> "GraphQLQuery[CustomerDetailsResponseFields, CustomerDetailsResponseGraphQLField]":
        pass

    @classmethod
    def get_customer_list_by_nmis(
        cls, nmis: list[str]
    ) -> "GraphQLQuery[CustomerDetailsResponseFields, CustomerDetailsResponseGraphQLField]":
        pass

    @classmethod
    def get_app_options(
        cls,
    ) -> "GraphQLQuery[AppOptionsFields, AppOptionsGraphQLField]":
        pass

    @classmethod
    def get_presigned_upload_url_for_variant(
        cls, filename: str, file_type: VariantFileType
    ) -> "GraphQLQuery[UploadUrlResponseFields, UploadUrlResponseGraphQLField]":
        pass

    @classmethod
    def get_variant_upload_info(
        cls, job_id: str
    ) -> "GraphQLQuery[VariantWorkPackageFields, VariantWorkPackageGraphQLField]":
        pass
