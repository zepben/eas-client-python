from typing import Any, Optional

from . import HostingCapacityFileType, WorkflowStatus, ContainerType, SincalFileType, VariantFileType
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
        sort: Optional[GetStudiesSortCriteriaInput] = None
    ) -> StudyPageFields:
        """Retrieve a page of studies, with optional limit and offset, and optional filtering"""
        arguments: dict[str, dict[str, Any]] = {
            "limit": {"type": "Int", "value": limit},
            "offset": {"type": "Long", "value": offset},
            "filter": {"type": "GetStudiesFilterInput", "value": filter_},
            "sort": {"type": "GetStudiesSortCriteriaInput", "value": sort},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return StudyPageFields(field_name="pagedStudies", arguments=cleared_arguments)

    @classmethod
    def results_by_id(cls, ids: list[str]) -> StudyResultFields:
        """Retrieve a list of results by IDs"""
        arguments: dict[str, dict[str, Any]] = {"ids": {"type": "[ID!]!", "value": ids}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return StudyResultFields(field_name="resultsById", arguments=cleared_arguments)

    @classmethod
    def studies(cls, *, filter_: Optional[GetStudiesFilterInput] = None) -> StudyFields:
        """Retrieve a list of studies, with optional filtering"""
        arguments: dict[str, dict[str, Any]] = {
            "filter": {"type": "GetStudiesFilterInput", "value": filter_}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return StudyFields(field_name="studies", arguments=cleared_arguments)

    @classmethod
    def studies_by_id(cls, ids: list[str]) -> StudyFields:
        """Retrieve a list of studies by IDs"""
        arguments: dict[str, dict[str, Any]] = {"ids": {"type": "[ID!]!", "value": ids}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return StudyFields(field_name="studiesById", arguments=cleared_arguments)

    @classmethod
    def styles_by_id(cls, ids: list[str]) -> GraphQLField:
        """Retrieve a list of style layers by IDs"""
        arguments: dict[str, dict[str, Any]] = {"ids": {"type": "[ID!]!", "value": ids}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(field_name="stylesById", arguments=cleared_arguments)

    @classmethod
    def current_user(cls) -> GqlUserResponseFields:
        """Get information about the current user"""
        return GqlUserResponseFields(field_name="currentUser")

    @classmethod
    def paged_power_factory_model_templates(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[GetPowerFactoryModelTemplatesFilterInput] = None,
        sort: Optional[GetPowerFactoryModelTemplatesSortCriteriaInput] = None
    ) -> PowerFactoryModelTemplatePageFields:
        """Retrieve a page of powerFactoryModel templates, with optional limit and offset, and optional filtering"""
        arguments: dict[str, dict[str, Any]] = {
            "limit": {"type": "Int", "value": limit},
            "offset": {"type": "Long", "value": offset},
            "filter": {
                "type": "GetPowerFactoryModelTemplatesFilterInput",
                "value": filter_,
            },
            "sort": {
                "type": "GetPowerFactoryModelTemplatesSortCriteriaInput",
                "value": sort,
            },
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return PowerFactoryModelTemplatePageFields(
            field_name="pagedPowerFactoryModelTemplates", arguments=cleared_arguments
        )

    @classmethod
    def paged_power_factory_models(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[GetPowerFactoryModelsFilterInput] = None,
        sort: Optional[GetPowerFactoryModelsSortCriteriaInput] = None
    ) -> PowerFactoryModelPageFields:
        """Retrieve a page of powerFactoryModels, with optional limit and offset, and optional filtering"""
        arguments: dict[str, dict[str, Any]] = {
            "limit": {"type": "Int", "value": limit},
            "offset": {"type": "Long", "value": offset},
            "filter": {"type": "GetPowerFactoryModelsFilterInput", "value": filter_},
            "sort": {"type": "GetPowerFactoryModelsSortCriteriaInput", "value": sort},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return PowerFactoryModelPageFields(
            field_name="pagedPowerFactoryModels", arguments=cleared_arguments
        )

    @classmethod
    def power_factory_model_by_id(cls, model_id: str) -> PowerFactoryModelFields:
        """Retrieve a powerFactoryModel by ID"""
        arguments: dict[str, dict[str, Any]] = {
            "modelId": {"type": "ID!", "value": model_id}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return PowerFactoryModelFields(
            field_name="powerFactoryModelById", arguments=cleared_arguments
        )

    @classmethod
    def power_factory_model_template_by_id(
        cls, template_id: str
    ) -> PowerFactoryModelTemplateFields:
        """Retrieve a powerFactoryModel template by ID"""
        arguments: dict[str, dict[str, Any]] = {
            "templateId": {"type": "ID!", "value": template_id}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return PowerFactoryModelTemplateFields(
            field_name="powerFactoryModelTemplateById", arguments=cleared_arguments
        )

    @classmethod
    def power_factory_model_templates_by_ids(
        cls, template_ids: list[str]
    ) -> PowerFactoryModelTemplateFields:
        """Retrieve a list of powerFactoryModel templates by IDs"""
        arguments: dict[str, dict[str, Any]] = {
            "templateIds": {"type": "[ID!]!", "value": template_ids}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return PowerFactoryModelTemplateFields(
            field_name="powerFactoryModelTemplatesByIds", arguments=cleared_arguments
        )

    @classmethod
    def power_factory_models_by_ids(
        cls, model_ids: list[str]
    ) -> PowerFactoryModelFields:
        """Retrieve a list of powerFactoryModels by IDs"""
        arguments: dict[str, dict[str, Any]] = {
            "modelIds": {"type": "[ID!]!", "value": model_ids}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return PowerFactoryModelFields(
            field_name="powerFactoryModelsByIds", arguments=cleared_arguments
        )

    @classmethod
    def get_active_work_packages(cls) -> GraphQLField:
        """Retrieve a list of currently active (running, scheduled, pending) work packages"""
        return GraphQLField(field_name="getActiveWorkPackages")

    @classmethod
    def get_all_work_packages_authors(cls) -> GqlUserFields:
        """Retrieve all users that have created work packages."""
        return GqlUserFields(field_name="getAllWorkPackagesAuthors")

    @classmethod
    def get_calibration_run(cls, id: str) -> HcCalibrationFields:
        """Retrieve calibration run details by ID"""
        arguments: dict[str, dict[str, Any]] = {"id": {"type": "ID!", "value": id}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return HcCalibrationFields(
            field_name="getCalibrationRun", arguments=cleared_arguments
        )

    @classmethod
    def get_calibration_sets(cls) -> GraphQLField:
        """Retrieve available distribution transformer tap calibration sets."""
        return GraphQLField(field_name="getCalibrationSets")

    @classmethod
    def get_duration_curves(
        cls,
        work_package_id: str,
        scenario: str,
        feeder: str,
        year: int,
        conducting_equipment_mrid: str,
    ) -> DurationCurveByTerminalFields:
        """Retrieve duration curves for a single piece of equipment in a specific SYF."""
        arguments: dict[str, dict[str, Any]] = {
            "workPackageId": {"type": "String!", "value": work_package_id},
            "scenario": {"type": "String!", "value": scenario},
            "feeder": {"type": "String!", "value": feeder},
            "year": {"type": "Int!", "value": year},
            "conductingEquipmentMrid": {
                "type": "String!",
                "value": conducting_equipment_mrid,
            },
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return DurationCurveByTerminalFields(
            field_name="getDurationCurves", arguments=cleared_arguments
        )

    @classmethod
    def get_opportunities(
        cls, *, year: Optional[int] = None
    ) -> OpportunitiesByYearFields:
        """Retrieve all Opportunities available for a specific year."""
        arguments: dict[str, dict[str, Any]] = {"year": {"type": "Int", "value": year}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return OpportunitiesByYearFields(
            field_name="getOpportunities", arguments=cleared_arguments
        )

    @classmethod
    def get_opportunities_for_equipment(cls, m_rid: str) -> OpportunityFields:
        """Retrieve Opportunities by attached conducting equipment mRID."""
        arguments: dict[str, dict[str, Any]] = {
            "mRID": {"type": "String!", "value": m_rid}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return OpportunityFields(
            field_name="getOpportunitiesForEquipment", arguments=cleared_arguments
        )

    @classmethod
    def get_opportunity(cls, id: str) -> OpportunityFields:
        """Retrieve Opportunities by id."""
        arguments: dict[str, dict[str, Any]] = {"id": {"type": "String!", "value": id}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return OpportunityFields(
            field_name="getOpportunity", arguments=cleared_arguments
        )

    @classmethod
    def get_opportunity_locations(
        cls, *, year: Optional[int] = None
    ) -> OpportunityLocationFields:
        """Retrieve all opportunity locations available for a specific year."""
        arguments: dict[str, dict[str, Any]] = {"year": {"type": "Int", "value": year}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return OpportunityLocationFields(
            field_name="getOpportunityLocations", arguments=cleared_arguments
        )

    @classmethod
    def get_scenario_configurations(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[HcScenarioConfigsFilterInput] = None
    ) -> HcScenarioConfigsPageFields:
        """Retrieve a page scenario configurations from the hosting capacity input database."""
        arguments: dict[str, dict[str, Any]] = {
            "limit": {"type": "Int", "value": limit},
            "offset": {"type": "Long", "value": offset},
            "filter": {"type": "HcScenarioConfigsFilterInput", "value": filter_},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return HcScenarioConfigsPageFields(
            field_name="getScenarioConfigurations", arguments=cleared_arguments
        )

    @classmethod
    def get_transformer_tap_settings(
        cls,
        calibration_name: str,
        *,
        feeder: Optional[str] = None,
        transformer_mrid: Optional[str] = None
    ) -> GqlTxTapRecordFields:
        """Retrieve distribution transformer tap settings from a calibration set in the hosting capacity input database."""
        arguments: dict[str, dict[str, Any]] = {
            "calibrationName": {"type": "String!", "value": calibration_name},
            "feeder": {"type": "String", "value": feeder},
            "transformerMrid": {"type": "String", "value": transformer_mrid},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GqlTxTapRecordFields(
            field_name="getTransformerTapSettings", arguments=cleared_arguments
        )

    @classmethod
    def get_work_package_by_id(
        cls, id: str, *, with_groupings: Optional[bool] = None
    ) -> HcWorkPackageFields:
        """Retrieve a hosting capacity work package by ID, withGroupings: Whether to include model groupings in the work package progress details, default value is false"""
        arguments: dict[str, dict[str, Any]] = {
            "id": {"type": "ID!", "value": id},
            "withGroupings": {"type": "Boolean", "value": with_groupings},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return HcWorkPackageFields(
            field_name="getWorkPackageById", arguments=cleared_arguments
        )

    @classmethod
    def get_work_package_cost_estimation(cls, input: WorkPackageInput) -> GraphQLField:
        """Returns an estimated cost of the submitted hosting capacity work package."""
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "WorkPackageInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="getWorkPackageCostEstimation", arguments=cleared_arguments
        )

    @classmethod
    def get_work_package_tree(cls, id: str) -> WorkPackageTreeFields:
        """Retrieve a work package tree with its ancestors and immediate children."""
        arguments: dict[str, dict[str, Any]] = {"id": {"type": "ID!", "value": id}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return WorkPackageTreeFields(
            field_name="getWorkPackageTree", arguments=cleared_arguments
        )

    @classmethod
    def get_work_packages(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[HcWorkPackagesFilterInput] = None,
        sort: Optional[HcWorkPackagesSortCriteriaInput] = None,
        with_groupings: Optional[bool] = None
    ) -> HcWorkPackagePageFields:
        """Retrieve a page of hosting capacity work packages, with optional limit and offset, and optional filtering"""
        arguments: dict[str, dict[str, Any]] = {
            "limit": {"type": "Int", "value": limit},
            "offset": {"type": "Long", "value": offset},
            "filter": {"type": "HcWorkPackagesFilterInput", "value": filter_},
            "sort": {"type": "HcWorkPackagesSortCriteriaInput", "value": sort},
            "withGroupings": {"type": "Boolean", "value": with_groupings},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return HcWorkPackagePageFields(
            field_name="getWorkPackages", arguments=cleared_arguments
        )

    @classmethod
    def hosting_capacity_file_upload_url(
        cls, filename: str, file_type: HostingCapacityFileType
    ) -> UploadUrlResponseFields:
        """Generate a pre-signed URL to upload hosting capacity file to the storage location. Returns the pre-signed URL along with the final file path as it will be referenced by EAS"""
        arguments: dict[str, dict[str, Any]] = {
            "filename": {"type": "String!", "value": filename},
            "fileType": {"type": "HostingCapacityFileType!", "value": file_type},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UploadUrlResponseFields(
            field_name="hostingCapacityFileUploadUrl", arguments=cleared_arguments
        )

    @classmethod
    def list_calibration_runs(
        cls,
        *,
        name: Optional[str] = None,
        calibration_time: Optional[Any] = None,
        status: Optional[WorkflowStatus] = None
    ) -> HcCalibrationFields:
        """Retrieve all calibration runs initiated through EAS"""
        arguments: dict[str, dict[str, Any]] = {
            "name": {"type": "String", "value": name},
            "calibrationTime": {"type": "LocalDateTime", "value": calibration_time},
            "status": {"type": "WorkflowStatus", "value": status},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return HcCalibrationFields(
            field_name="listCalibrationRuns", arguments=cleared_arguments
        )

    @classmethod
    def get_processed_diff(cls, diff_id: str) -> ProcessedDiffFields:
        """Retrieve processed diff of hosting capacity work packages with diffId"""
        arguments: dict[str, dict[str, Any]] = {
            "diffId": {"type": "ID!", "value": diff_id}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ProcessedDiffFields(
            field_name="getProcessedDiff", arguments=cleared_arguments
        )

    @classmethod
    def get_processed_diffs(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[ProcessedDiffFilterInput] = None,
        sort: Optional[ProcessedDiffSortCriteriaInput] = None
    ) -> ProcessedDiffPageFields:
        """Retrieve a page of processed diffs, with optional limit and offset, and optional filtering"""
        arguments: dict[str, dict[str, Any]] = {
            "limit": {"type": "Int", "value": limit},
            "offset": {"type": "Long", "value": offset},
            "filter": {"type": "ProcessedDiffFilterInput", "value": filter_},
            "sort": {"type": "ProcessedDiffSortCriteriaInput", "value": sort},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ProcessedDiffPageFields(
            field_name="getProcessedDiffs", arguments=cleared_arguments
        )

    @classmethod
    def get_all_jobs(cls) -> IngestionJobFields:
        """Gets the ID and metadata of all ingestion jobs in reverse chronological order."""
        return IngestionJobFields(field_name="getAllJobs")

    @classmethod
    def get_distinct_metric_names(cls, job_id: str) -> GraphQLField:
        """Gets all possible values of metricName for a specific job."""
        arguments: dict[str, dict[str, Any]] = {
            "jobId": {"type": "String!", "value": job_id}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="getDistinctMetricNames", arguments=cleared_arguments
        )

    @classmethod
    def get_metrics(
        cls, job_id: str, container_type: ContainerType, container_id: str
    ) -> MetricFields:
        """Gets the metrics for a network container emitted in an ingestion job."""
        arguments: dict[str, dict[str, Any]] = {
            "jobId": {"type": "String!", "value": job_id},
            "containerType": {"type": "ContainerType!", "value": container_type},
            "containerId": {"type": "String!", "value": container_id},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return MetricFields(field_name="getMetrics", arguments=cleared_arguments)

    @classmethod
    def get_newest_job(cls) -> IngestionJobFields:
        """Gets the ID and metadata of the newest ingestion job. If no job exists, this returns null."""
        return IngestionJobFields(field_name="getNewestJob")

    @classmethod
    def get_sources(cls, job_id: str) -> JobSourceFields:
        """Gets the data sources used in an ingestion job."""
        arguments: dict[str, dict[str, Any]] = {
            "jobId": {"type": "String!", "value": job_id}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return JobSourceFields(field_name="getSources", arguments=cleared_arguments)

    @classmethod
    def paged_sincal_model_presets(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[GetSincalModelPresetsFilterInput] = None,
        sort: Optional[GetSincalModelPresetsSortCriteriaInput] = None
    ) -> SincalModelPresetPageFields:
        """Retrieve a page of sincalModel presets, with optional limit and offset, and optional filtering. A default preset with null ID will also be included in the response, which may result in the number of presets returned exceeding the desired page size (limit)."""
        arguments: dict[str, dict[str, Any]] = {
            "limit": {"type": "Int", "value": limit},
            "offset": {"type": "Long", "value": offset},
            "filter": {"type": "GetSincalModelPresetsFilterInput", "value": filter_},
            "sort": {"type": "GetSincalModelPresetsSortCriteriaInput", "value": sort},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return SincalModelPresetPageFields(
            field_name="pagedSincalModelPresets", arguments=cleared_arguments
        )

    @classmethod
    def paged_sincal_models(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[GetSincalModelsFilterInput] = None,
        sort: Optional[GetSincalModelsSortCriteriaInput] = None
    ) -> SincalModelPageFields:
        """Retrieve a page of sincalModels, with optional limit and offset, and optional filtering"""
        arguments: dict[str, dict[str, Any]] = {
            "limit": {"type": "Int", "value": limit},
            "offset": {"type": "Long", "value": offset},
            "filter": {"type": "GetSincalModelsFilterInput", "value": filter_},
            "sort": {"type": "GetSincalModelsSortCriteriaInput", "value": sort},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return SincalModelPageFields(
            field_name="pagedSincalModels", arguments=cleared_arguments
        )

    @classmethod
    def sincal_model_by_id(cls, model_id: str) -> SincalModelFields:
        """Retrieve a sincalModel by ID"""
        arguments: dict[str, dict[str, Any]] = {
            "modelId": {"type": "ID!", "value": model_id}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return SincalModelFields(
            field_name="sincalModelById", arguments=cleared_arguments
        )

    @classmethod
    def sincal_model_config_upload_url(
        cls, filename: str, file_type: SincalFileType
    ) -> UploadUrlResponseFields:
        """Generate a pre-signed URL to upload a sincal configuration file to the input storage location. Returns the pre-signed URL along with the final file path as it will be referenced by EAS. This does not update the sincal configuration. To make use of a newly uploaded configuration file, pass the `filePath` returned by this query to the `updateSincalModelConfigFilePath()` mutation."""
        arguments: dict[str, dict[str, Any]] = {
            "filename": {"type": "String!", "value": filename},
            "fileType": {"type": "SincalFileType!", "value": file_type},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UploadUrlResponseFields(
            field_name="sincalModelConfigUploadUrl", arguments=cleared_arguments
        )

    @classmethod
    def sincal_model_global_config(cls) -> SincalGlobalInputsConfigFields:
        """Retrieve the current sincalModel input file paths."""
        return SincalGlobalInputsConfigFields(field_name="sincalModelGlobalConfig")

    @classmethod
    def sincal_model_preset_by_id(cls, preset_id: str) -> SincalModelPresetFields:
        """Retrieve a sincalModel preset by ID"""
        arguments: dict[str, dict[str, Any]] = {
            "presetId": {"type": "ID!", "value": preset_id}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return SincalModelPresetFields(
            field_name="sincalModelPresetById", arguments=cleared_arguments
        )

    @classmethod
    def sincal_model_presets_by_ids(
        cls, preset_ids: list[str]
    ) -> SincalModelPresetFields:
        """Retrieve a list of sincalModel presets by IDs"""
        arguments: dict[str, dict[str, Any]] = {
            "presetIds": {"type": "[ID!]!", "value": preset_ids}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return SincalModelPresetFields(
            field_name="sincalModelPresetsByIds", arguments=cleared_arguments
        )

    @classmethod
    def sincal_models_by_ids(cls, model_ids: list[str]) -> SincalModelFields:
        """Retrieve a list of sincalModels by IDs"""
        arguments: dict[str, dict[str, Any]] = {
            "modelIds": {"type": "[ID!]!", "value": model_ids}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return SincalModelFields(
            field_name="sincalModelsByIds", arguments=cleared_arguments
        )

    @classmethod
    def create_machine_api_key(cls, roles: list[str], token_name: str) -> GraphQLField:
        """Create a new JWT auth token for a machine with the specified roles."""
        arguments: dict[str, dict[str, Any]] = {
            "roles": {"type": "[String!]!", "value": roles},
            "tokenName": {"type": "String!", "value": token_name},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="createMachineApiKey", arguments=cleared_arguments
        )

    @classmethod
    def create_user_api_key(cls, roles: list[str], token_name: str) -> GraphQLField:
        """Create the JWT auth token for the current user with specified roles."""
        arguments: dict[str, dict[str, Any]] = {
            "roles": {"type": "[String!]!", "value": roles},
            "tokenName": {"type": "String!", "value": token_name},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(field_name="createUserApiKey", arguments=cleared_arguments)

    @classmethod
    def get_machine_tokens(cls) -> MachineUserFields:
        """Gets all machine token users with their username and display name."""
        return MachineUserFields(field_name="getMachineTokens")

    @classmethod
    def get_public_geo_view_config(cls) -> GraphQLField:
        """Retrieve the GeoViewConfig used to config the EWB public map tile endpoint. Returns NUll if not enabled."""
        return GraphQLField(field_name="getPublicGeoViewConfig")

    @classmethod
    def get_all_external_roles(cls) -> GraphQLField:
        """Get all external roles from EAS."""
        return GraphQLField(field_name="getAllExternalRoles")

    @classmethod
    def get_network_models(cls) -> NetworkModelsFields:
        """Get all EWB network models"""
        return NetworkModelsFields(field_name="getNetworkModels")

    @classmethod
    def get_feeder_load_analysis_report_status(
        cls, report_id: str, full_spec: bool
    ) -> FeederLoadAnalysisReportFields:
        """Retrieve the status of a feeder load analysis job."""
        arguments: dict[str, dict[str, Any]] = {
            "reportId": {"type": "ID!", "value": report_id},
            "fullSpec": {"type": "Boolean!", "value": full_spec},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return FeederLoadAnalysisReportFields(
            field_name="getFeederLoadAnalysisReportStatus", arguments=cleared_arguments
        )

    @classmethod
    def get_ingestor_run(cls, id: int) -> IngestionRunFields:
        """Retrieve ingestor run details by ID"""
        arguments: dict[str, dict[str, Any]] = {"id": {"type": "Int!", "value": id}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return IngestionRunFields(
            field_name="getIngestorRun", arguments=cleared_arguments
        )

    @classmethod
    def list_ingestor_runs(
        cls,
        *,
        filter_: Optional[IngestorRunsFilterInput] = None,
        sort: Optional[IngestorRunsSortCriteriaInput] = None
    ) -> IngestionRunFields:
        """Retrieve all ingestor runs initiated through EAS"""
        arguments: dict[str, dict[str, Any]] = {
            "filter": {"type": "IngestorRunsFilterInput", "value": filter_},
            "sort": {"type": "IngestorRunsSortCriteriaInput", "value": sort},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return IngestionRunFields(
            field_name="listIngestorRuns", arguments=cleared_arguments
        )

    @classmethod
    def list_ingestor_runs_paged(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[IngestorRunsFilterInput] = None,
        sort: Optional[IngestorRunsSortCriteriaInput] = None
    ) -> IngestorRunPageFields:
        """Retrieve all ingestor runs initiated through EAS"""
        arguments: dict[str, dict[str, Any]] = {
            "limit": {"type": "Int", "value": limit},
            "offset": {"type": "Long", "value": offset},
            "filter": {"type": "IngestorRunsFilterInput", "value": filter_},
            "sort": {"type": "IngestorRunsSortCriteriaInput", "value": sort},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return IngestorRunPageFields(
            field_name="listIngestorRunsPaged", arguments=cleared_arguments
        )

    @classmethod
    def paged_open_dss_models(
        cls,
        *,
        limit: Optional[int] = None,
        offset: Optional[Any] = None,
        filter_: Optional[GetOpenDssModelsFilterInput] = None,
        sort: Optional[GetOpenDssModelsSortCriteriaInput] = None
    ) -> OpenDssModelPageFields:
        """Retrieve a page of OpenDSS models, with optional limit and offset, and optional filtering"""
        arguments: dict[str, dict[str, Any]] = {
            "limit": {"type": "Int", "value": limit},
            "offset": {"type": "Long", "value": offset},
            "filter": {"type": "GetOpenDssModelsFilterInput", "value": filter_},
            "sort": {"type": "GetOpenDssModelsSortCriteriaInput", "value": sort},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return OpenDssModelPageFields(
            field_name="pagedOpenDssModels", arguments=cleared_arguments
        )

    @classmethod
    def get_user_permitted_customer_list_column_config(
        cls,
    ) -> UserCustomerListColumnConfigFields:
        """Fetches the user permitted column configuration for the customer list view."""
        return UserCustomerListColumnConfigFields(
            field_name="getUserPermittedCustomerListColumnConfig"
        )

    @classmethod
    def get_user_saved_customer_list_column_config(
        cls,
    ) -> UserCustomerListColumnConfigFields:
        """Fetches the user's column configuration for the customer list view."""
        return UserCustomerListColumnConfigFields(
            field_name="getUserSavedCustomerListColumnConfig"
        )

    @classmethod
    def get_customer_list(cls, m_ri_ds: list[str]) -> CustomerDetailsResponseFields:
        """Retrieve the list of customers and their details."""
        arguments: dict[str, dict[str, Any]] = {
            "mRIDs": {"type": "[String!]!", "value": m_ri_ds}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return CustomerDetailsResponseFields(
            field_name="getCustomerList", arguments=cleared_arguments
        )

    @classmethod
    def get_customer_list_by_nmis(
        cls, nmis: list[str]
    ) -> CustomerDetailsResponseFields:
        """Retrieve customer details using NMIs as input."""
        arguments: dict[str, dict[str, Any]] = {
            "nmis": {"type": "[String!]!", "value": nmis}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return CustomerDetailsResponseFields(
            field_name="getCustomerListByNmis", arguments=cleared_arguments
        )

    @classmethod
    def get_app_options(cls) -> AppOptionsFields:
        """Get App Options"""
        return AppOptionsFields(field_name="getAppOptions")

    @classmethod
    def get_presigned_upload_url_for_variant(
        cls, filename: str, file_type: VariantFileType
    ) -> UploadUrlResponseFields:
        """Generate a pre-signed URL to upload variant files to the cloud storage. Returns the pre-signed URL along with the final file path as it will be referenced by EAS"""
        arguments: dict[str, dict[str, Any]] = {
            "filename": {"type": "String!", "value": filename},
            "fileType": {"type": "VariantFileType!", "value": file_type},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UploadUrlResponseFields(
            field_name="getPresignedUploadUrlForVariant", arguments=cleared_arguments
        )

    @classmethod
    def get_variant_upload_info(cls, job_id: str) -> VariantWorkPackageFields:
        """Retrieves status of a variant ingestion workflow"""
        arguments: dict[str, dict[str, Any]] = {
            "jobID": {"type": "String!", "value": job_id}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return VariantWorkPackageFields(
            field_name="getVariantUploadInfo", arguments=cleared_arguments
        )
