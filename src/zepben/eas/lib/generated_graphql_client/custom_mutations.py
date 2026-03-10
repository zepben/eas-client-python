from typing import Any, Optional

from . import SincalFileType, VariantFileType
from .custom_fields import (
    DiffResultFields,
    RemoveAppOptionResultFields,
    UserCustomerListColumnConfigFields,
)
from .custom_typing_fields import GraphQLField
from .input_types import (
    AppOptionsInput,
    FeederLoadAnalysisInput,
    HcGeneratorConfigInput,
    IngestorConfigInput,
    OpenDssModelInput,
    PowerFactoryModelGenerationSpecInput,
    PowerFactoryModelInput,
    SincalModelGenerationSpecInput,
    SincalModelInput,
    StudyInput,
    WorkPackageInput,
)


class Mutation:
    @classmethod
    def add_studies(cls, studies: list[StudyInput]) -> GraphQLField:
        """Add new studies to the database and return their IDs"""
        arguments: dict[str, dict[str, Any]] = {
            "studies": {"type": "[StudyInput!]!", "value": studies}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(field_name="addStudies", arguments=cleared_arguments)

    @classmethod
    def delete_studies(cls, ids: list[str]) -> GraphQLField:
        """Delete studies by their IDs and return the IDs of deleted studies"""
        arguments: dict[str, dict[str, Any]] = {"ids": {"type": "[ID!]!", "value": ids}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(field_name="deleteStudies", arguments=cleared_arguments)

    @classmethod
    def create_power_factory_model(cls, input: PowerFactoryModelInput) -> GraphQLField:
        """Creates a new powerFactoryModel and returns its ID"""
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "PowerFactoryModelInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="createPowerFactoryModel", arguments=cleared_arguments
        )

    @classmethod
    def create_power_factory_model_template(
        cls, input: PowerFactoryModelInput
    ) -> GraphQLField:
        """Creates a new powerFactoryModel template and returns its ID"""
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "PowerFactoryModelInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="createPowerFactoryModelTemplate", arguments=cleared_arguments
        )

    @classmethod
    def delete_power_factory_model(cls, model_id: str) -> GraphQLField:
        """Deletes powerFactoryModel with ID and returns said ID"""
        arguments: dict[str, dict[str, Any]] = {
            "modelId": {"type": "ID!", "value": model_id}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="deletePowerFactoryModel", arguments=cleared_arguments
        )

    @classmethod
    def delete_power_factory_model_template(cls, template_id: str) -> GraphQLField:
        """Deletes powerFactoryModel template with ID and returns its ID"""
        arguments: dict[str, dict[str, Any]] = {
            "templateId": {"type": "ID!", "value": template_id}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="deletePowerFactoryModelTemplate", arguments=cleared_arguments
        )

    @classmethod
    def update_power_factory_model_template(
        cls, template_id: str, generation_spec: PowerFactoryModelGenerationSpecInput
    ) -> GraphQLField:
        """Updates powerFactoryModel template with ID and returns its ID"""
        arguments: dict[str, dict[str, Any]] = {
            "templateId": {"type": "ID!", "value": template_id},
            "generationSpec": {
                "type": "PowerFactoryModelGenerationSpecInput!",
                "value": generation_spec,
            },
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="updatePowerFactoryModelTemplate", arguments=cleared_arguments
        )

    @classmethod
    def cancel_work_package(cls, work_package_id: str) -> GraphQLField:
        """Cancels a hosting capacity work package and returns its ID."""
        arguments: dict[str, dict[str, Any]] = {
            "workPackageId": {"type": "ID!", "value": work_package_id}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(field_name="cancelWorkPackage", arguments=cleared_arguments)

    @classmethod
    def delete_work_package(cls, work_package_ids: list[str]) -> GraphQLField:
        """Delete one or more hosting capacity work package(s). Returns the list of successfully deleted work package IDs, throws if none can be deleted."""
        arguments: dict[str, dict[str, Any]] = {
            "workPackageIds": {"type": "[String!]!", "value": work_package_ids}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(field_name="deleteWorkPackage", arguments=cleared_arguments)

    @classmethod
    def edit_diff_package(
        cls,
        diff_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> GraphQLField:
        """Edits a hosting capacity diff package and return boolean. Returns "true" on successful update"""
        arguments: dict[str, dict[str, Any]] = {
            "diffId": {"type": "ID!", "value": diff_id},
            "name": {"type": "String", "value": name},
            "description": {"type": "String", "value": description},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(field_name="editDiffPackage", arguments=cleared_arguments)

    @classmethod
    def edit_work_package(
        cls,
        work_package_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> GraphQLField:
        """Edits a hosting capacity work package and return boolean. Returns "true" on successful update"""
        arguments: dict[str, dict[str, Any]] = {
            "workPackageId": {"type": "ID!", "value": work_package_id},
            "name": {"type": "String", "value": name},
            "description": {"type": "String", "value": description},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(field_name="editWorkPackage", arguments=cleared_arguments)

    @classmethod
    def generate_enhanced_network_performance_diff(
        cls,
        diff_id: str,
        work_package_id_1: str,
        work_package_id_2: str,
        *,
        diff_name: Optional[str] = None,
        scenario: Optional[str] = None,
        feeder: Optional[str] = None,
        year: Optional[int] = None,
        season: Optional[str] = None,
        time_of_day: Optional[str] = None
    ) -> DiffResultFields:
        """Generate and store the differences of enhanced network performance metrics between two work packages and returns the number of entries generated with the ID of this diff package."""
        arguments: dict[str, dict[str, Any]] = {
            "diffId": {"type": "ID!", "value": diff_id},
            "diffName": {"type": "String", "value": diff_name},
            "workPackageId1": {"type": "ID!", "value": work_package_id_1},
            "workPackageId2": {"type": "ID!", "value": work_package_id_2},
            "scenario": {"type": "String", "value": scenario},
            "feeder": {"type": "String", "value": feeder},
            "year": {"type": "Int", "value": year},
            "season": {"type": "String", "value": season},
            "timeOfDay": {"type": "String", "value": time_of_day},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return DiffResultFields(
            field_name="generateEnhancedNetworkPerformanceDiff",
            arguments=cleared_arguments,
        )

    @classmethod
    def generate_network_performance_diff(
        cls,
        diff_id: str,
        work_package_id_1: str,
        work_package_id_2: str,
        *,
        diff_name: Optional[str] = None,
        scenario: Optional[str] = None,
        feeder: Optional[str] = None,
        year: Optional[int] = None
    ) -> DiffResultFields:
        """Generate and store the differences of network performance metrics between two work packages and returns the number of entries generated with the ID of this diff package."""
        arguments: dict[str, dict[str, Any]] = {
            "diffId": {"type": "ID!", "value": diff_id},
            "diffName": {"type": "String", "value": diff_name},
            "workPackageId1": {"type": "ID!", "value": work_package_id_1},
            "workPackageId2": {"type": "ID!", "value": work_package_id_2},
            "scenario": {"type": "String", "value": scenario},
            "feeder": {"type": "String", "value": feeder},
            "year": {"type": "Int", "value": year},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return DiffResultFields(
            field_name="generateNetworkPerformanceDiff", arguments=cleared_arguments
        )

    @classmethod
    def process_input_database(cls, file_path: str) -> GraphQLField:
        """Processes the input database specified by the given filepath."""
        arguments: dict[str, dict[str, Any]] = {
            "filePath": {"type": "String!", "value": file_path}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="processInputDatabase", arguments=cleared_arguments
        )

    @classmethod
    def run_calibration(
        cls,
        calibration_name: str,
        *,
        calibration_time_local: Optional[Any] = None,
        feeders: Optional[list[str]] = None,
        generator_config: Optional[HcGeneratorConfigInput] = None
    ) -> GraphQLField:
        """Runs a calibration and returns a run ID."""
        arguments: dict[str, dict[str, Any]] = {
            "calibrationName": {"type": "String!", "value": calibration_name},
            "calibrationTimeLocal": {
                "type": "LocalDateTime",
                "value": calibration_time_local,
            },
            "feeders": {"type": "[String!]", "value": feeders},
            "generatorConfig": {
                "type": "HcGeneratorConfigInput",
                "value": generator_config,
            },
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(field_name="runCalibration", arguments=cleared_arguments)

    @classmethod
    def run_work_package(
        cls, input: WorkPackageInput, work_package_name: str
    ) -> GraphQLField:
        """Runs a hosting capacity work package and returns its ID."""
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "WorkPackageInput!", "value": input},
            "workPackageName": {"type": "String!", "value": work_package_name},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(field_name="runWorkPackage", arguments=cleared_arguments)

    @classmethod
    def lock_network_model_database(cls) -> GraphQLField:
        """Lock EWB to the currently loaded network-model date."""
        return GraphQLField(field_name="lockNetworkModelDatabase")

    @classmethod
    def switch_network_model_database(cls, date: str) -> GraphQLField:
        """Lock EWB to the provided network-model date and reload the EWB server."""
        arguments: dict[str, dict[str, Any]] = {
            "date": {"type": "String!", "value": date}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="switchNetworkModelDatabase", arguments=cleared_arguments
        )

    @classmethod
    def unlock_network_model_database(cls) -> GraphQLField:
        """Unlock EWB network-model date (Note: This does not reload the EWB server)."""
        return GraphQLField(field_name="unlockNetworkModelDatabase")

    @classmethod
    def create_sincal_model(cls, input: SincalModelInput) -> GraphQLField:
        """Launches Sincal Exporter with specified config. Returns ID of model."""
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "SincalModelInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(field_name="createSincalModel", arguments=cleared_arguments)

    @classmethod
    def create_sincal_model_preset(cls, input: SincalModelInput) -> GraphQLField:
        """Creates a new sincalModel preset and returns its ID"""
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "SincalModelInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="createSincalModelPreset", arguments=cleared_arguments
        )

    @classmethod
    def delete_sincal_model(cls, model_id: str) -> GraphQLField:
        """Deletes sincalModel with ID and returns said ID"""
        arguments: dict[str, dict[str, Any]] = {
            "modelId": {"type": "ID!", "value": model_id}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(field_name="deleteSincalModel", arguments=cleared_arguments)

    @classmethod
    def delete_sincal_model_preset(cls, preset_id: str) -> GraphQLField:
        """Deletes sincalModel preset with ID and returns its ID"""
        arguments: dict[str, dict[str, Any]] = {
            "presetId": {"type": "ID!", "value": preset_id}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="deleteSincalModelPreset", arguments=cleared_arguments
        )

    @classmethod
    def update_sincal_model_config_file_path(
        cls, file_path: str, file_type: SincalFileType
    ) -> GraphQLField:
        """Updates the file path of one of the sincalModel input files. Returns true on success."""
        arguments: dict[str, dict[str, Any]] = {
            "filePath": {"type": "String!", "value": file_path},
            "fileType": {"type": "SincalFileType!", "value": file_type},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="updateSincalModelConfigFilePath", arguments=cleared_arguments
        )

    @classmethod
    def update_sincal_model_preset(
        cls, preset_id: str, generation_spec: SincalModelGenerationSpecInput
    ) -> GraphQLField:
        """Updates sincalModel preset with ID and returns its ID"""
        arguments: dict[str, dict[str, Any]] = {
            "presetId": {"type": "ID!", "value": preset_id},
            "generationSpec": {
                "type": "SincalModelGenerationSpecInput!",
                "value": generation_spec,
            },
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="updateSincalModelPreset", arguments=cleared_arguments
        )

    @classmethod
    def execute_ingestor(
        cls, *, run_config: Optional[list[IngestorConfigInput]] = None
    ) -> GraphQLField:
        """Start ingestor job."""
        arguments: dict[str, dict[str, Any]] = {
            "runConfig": {"type": "[IngestorConfigInput!]", "value": run_config}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(field_name="executeIngestor", arguments=cleared_arguments)

    @classmethod
    def run_feeder_load_analysis(cls, input: FeederLoadAnalysisInput) -> GraphQLField:
        """Runs a feeder load analysis job."""
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "FeederLoadAnalysisInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="runFeederLoadAnalysis", arguments=cleared_arguments
        )

    @classmethod
    def create_open_dss_model(cls, input: OpenDssModelInput) -> GraphQLField:
        """Launches OpenDSS Exporter with specified config. Returns ID of model."""
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "OpenDssModelInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="createOpenDssModel", arguments=cleared_arguments
        )

    @classmethod
    def delete_open_dss_model(cls, model_id: str) -> GraphQLField:
        """Deletes openDSS model with ID and returns said ID"""
        arguments: dict[str, dict[str, Any]] = {
            "modelId": {"type": "ID!", "value": model_id}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="deleteOpenDssModel", arguments=cleared_arguments
        )

    @classmethod
    def save_user_customer_list_column_config(
        cls, columns: list[str]
    ) -> UserCustomerListColumnConfigFields:
        """Update user's column configuration for the customer list to customize displayed columns."""
        arguments: dict[str, dict[str, Any]] = {
            "columns": {"type": "[String!]!", "value": columns}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UserCustomerListColumnConfigFields(
            field_name="saveUserCustomerListColumnConfig", arguments=cleared_arguments
        )

    @classmethod
    def clear_app_option(cls, name: str) -> RemoveAppOptionResultFields:
        """Reset an application option to its default value"""
        arguments: dict[str, dict[str, Any]] = {
            "name": {"type": "String!", "value": name}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RemoveAppOptionResultFields(
            field_name="clearAppOption", arguments=cleared_arguments
        )

    @classmethod
    def set_app_option(cls, app_options: AppOptionsInput) -> GraphQLField:
        """Set an application option"""
        arguments: dict[str, dict[str, Any]] = {
            "appOptions": {"type": "AppOptionsInput!", "value": app_options}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(field_name="setAppOption", arguments=cleared_arguments)

    @classmethod
    def finalize_variant_processing(
        cls, variant_upload_id: str, submitted_variants: list[str]
    ) -> GraphQLField:
        """Finalize variant processing with the specified file by supplying a list of finalized variants"""
        arguments: dict[str, dict[str, Any]] = {
            "variantUploadId": {"type": "String!", "value": variant_upload_id},
            "submittedVariants": {"type": "[String!]!", "value": submitted_variants},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="finalizeVariantProcessing", arguments=cleared_arguments
        )

    @classmethod
    def start_variant_processing(
        cls, prefix: str, file_type: VariantFileType
    ) -> GraphQLField:
        """Start variant processing with the specified file. Returns an ID which can be used to track progress of the processing"""
        arguments: dict[str, dict[str, Any]] = {
            "prefix": {"type": "String!", "value": prefix},
            "fileType": {"type": "VariantFileType!", "value": file_type},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(
            field_name="startVariantProcessing", arguments=cleared_arguments
        )
