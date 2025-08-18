#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["EasClient"]

import ssl
import warnings
from asyncio import get_event_loop
from http import HTTPStatus
from json import dumps
from typing import Optional, List
from dataclasses import asdict

import aiohttp
from aiohttp import ClientSession, ClientResponse
from urllib3.exceptions import InsecureRequestWarning

from zepben.eas.client.auth_method import BaseAuthMethod, TokenAuth
from zepben.eas.client.decorators import catch_warnings
from zepben.eas.client.feeder_load_analysis_input import FeederLoadAnalysisInput
from zepben.eas.client.opendss import OpenDssConfig, GetOpenDssModelsFilterInput, GetOpenDssModelsSortCriteriaInput
from zepben.eas.client.study import Study
from zepben.eas.client.ingestor import IngestorConfigInput, IngestorRunsFilterInput, IngestorRunsSortCriteriaInput
from zepben.eas.client.util import construct_url
from zepben.eas.client.work_package import WorkPackageConfig


class EasClient:
    """
    A class used to represent a client to the Evolve App Server, with methods that represent requests to its API.
    """

    def __init__(
        self,
        auth: BaseAuthMethod = None,
        ca_filename: Optional[str] = None,
        session: ClientSession = None,
        json_serialiser = None
    ):
        """
        Construct a client for the Evolve App Server. If the server is HTTPS, authentication may be configured.

        Address parameters:

        :param auth: Auth method to use for connection. (Optional)

        HTTP/HTTPS parameters:
        :param ca_filename: Path to CA file to use for verification. (Optional)
        :param session: aiohttp ClientSession to use, if not provided a new session will be created for you. You should
                        typically only use one aiohttp session per application.
        :param json_serialiser: JSON serialiser to use for requests e.g. ujson.dumps. (Defaults to json.dumps)
        """
        self._ca_filename = ca_filename
        self._verify_certificate = auth.verify_certificate
        self._auth = auth

        if session is None:
            conn = aiohttp.TCPConnector(limit=200, limit_per_host=0)
            timeout = aiohttp.ClientTimeout(total=60)
            self.session = aiohttp.ClientSession(json_serialize=json_serialiser or dumps, connector=conn,
                                                 timeout=timeout)
        else:
            self.session = session

    def close(self):
        return get_event_loop().run_until_complete(self.aclose())

    async def aclose(self):
        await self.session.close()

    def _get_request_headers(self, content_type: str = "application/json") -> dict:
        headers = {"content-type": content_type}
        if isinstance(self._auth, TokenAuth):
            if token := self._auth.token:
                headers["authorization"] = token
        return headers

    @staticmethod
    def build_request(query: str, variables: Optional[Any] = None) -> dict:
        _json = {"query": query}
        if variables is not None:
            _json.update({"variables": variables})
        return _json

    def run_hosting_capacity_work_package(self, work_package: WorkPackageConfig):
        """
        Send request to hosting capacity service to run work package

        :param work_package: An instance of the `WorkPackageConfig` data class representing the work package
            configuration for the run
        :return: The HTTP response received from the Evolve App Server after attempting to run work package
        """
        return get_event_loop().run_until_complete(self.async_run_hosting_capacity_work_package(work_package))

    def get_work_package_cost_estimation(self, work_package: WorkPackageConfig):
        """
        Send request to hosting capacity service to get an estimate cost of supplied work package

        :param work_package: An instance of the `WorkPackageConfig` data class representing the work package
            configuration for the run
        :return: The HTTP response received from the Evolve App Server after attempting to run work package
        """
        return get_event_loop().run_until_complete(self.async_get_work_package_cost_estimation(work_package))

    @catch_warnings
    async def async_get_work_package_cost_estimation(self, work_package: WorkPackageConfig):
        """
        Send asynchronous request to hosting capacity service to get an estimate cost of supplied work package

        :param work_package: An instance of the `WorkPackageConfig` data class representing the work package
            configuration for the run
        :return: The HTTP response received from the Evolve App Server after attempting to run work package
        """
        return await self.do_post_request(
            self.build_request("""
                query getWorkPackageCostEstimation($input: WorkPackageInput!) {
                    getWorkPackageCostEstimation(input: $input)
                }""", work_package.to_json()
            )
        )

    @catch_warnings
    async def async_run_hosting_capacity_work_package(self, work_package: WorkPackageConfig):
        """
        Send asynchronous request to hosting capacity service to run work package

        :param work_package: An instance of the `WorkPackageConfig` data class representing the work package
            configuration for the run
        :return: The HTTP response received from the Evolve App Server after attempting to run work package
        """
        return await self.do_post_request(
            self.build_request("""
                mutation runWorkPackage($input: WorkPackageInput!, $workPackageName: String!) {
                    runWorkPackage(input: $input, workPackageName: $workPackageName)
                }""", work_package.to_json()
            )
        )

    def cancel_hosting_capacity_work_package(self, work_package_id: str):
        """
        Send request to hosting capacity service to cancel a running work package

        :param work_package_id: The id of the running work package to cancel
        :return: The HTTP response received from the Evolve App Server after attempting to cancel work package
        """
        return get_event_loop().run_until_complete(self.async_cancel_hosting_capacity_work_package(work_package_id))

    @catch_warnings
    async def async_cancel_hosting_capacity_work_package(self, work_package_id: str):
        """
        Send asynchronous request to hosting capacity service to cancel a running work package

        :param work_package_id: The id of the running work package to cancel
        :return: The HTTP response received from the Evolve App Server after attempting to cancel work package
        """
        return await self.do_post_request(
            self.build_request("""
                mutation cancelWorkPackage($workPackageId: ID!) {
                    cancelWorkPackage(workPackageId: $workPackageId)
                }""",{'workPackageId': work_package_id}
            )
        )

    def get_hosting_capacity_work_packages_progress(self):
        """
        Retrieve running work packages progress information from hosting capacity service

        :return: The HTTP response received from the Evolve App Server after requesting work packages progress info
        """
        return get_event_loop().run_until_complete(self.async_get_hosting_capacity_work_packages_progress())

    @catch_warnings
    async def async_get_hosting_capacity_work_packages_progress(self):
        """
        Asynchronously retrieve running work packages progress information from hosting capacity service

        :return: The HTTP response received from the Evolve App Server after requesting work packages progress info
        """
        return await self.do_post_request(
            self.build_request("""
                query getWorkPackageProgress {
                    getWorkPackageProgress {
                        pending
                        inProgress {
                           id
                           progressPercent
                           pending
                           generation
                           execution
                           resultProcessing
                           failureProcessing
                           complete
                        }
                    }
                }"""
            )
        )

    def run_feeder_load_analysis_report(self, feeder_load_analysis_input: FeederLoadAnalysisInput):
        """
        Send request to evolve app server to run a feeder load analysis study

        :param feeder_load_analysis_input:: An instance of the `FeederLoadAnalysisConfig` data class representing the
            configuration for the run
        :return: The HTTP response received from the Evolve App Server after attempting to run work package
        """
        return get_event_loop().run_until_complete(
            self.async_run_feeder_load_analysis_report(feeder_load_analysis_input))

    @catch_warnings
    async def async_run_feeder_load_analysis_report(self, feeder_load_analysis_input: FeederLoadAnalysisInput):
        """
        Asynchronously send request to evolve app server to run a feeder load analysis study

        :return: The HTTP response received from the Evolve App Server after requesting a feeder load analysis report
        """
        return await self.do_post_request(
            self.build_request("""
                mutation runFeederLoadAnalysis($input: FeederLoadAnalysisInput!) {
                    runFeederLoadAnalysis(input: $input)
                }
                """,{
                    "input": {
                        "feeders": feeder_load_analysis_input.feeders,
                        "substations": feeder_load_analysis_input.substations,
                        "subGeographicalRegions": feeder_load_analysis_input.sub_geographical_regions,
                        "geographicalRegions": feeder_load_analysis_input.feeders,
                        "startDate": feeder_load_analysis_input.start_date,
                        "endDate": feeder_load_analysis_input.end_date,
                        "fetchLvNetwork": feeder_load_analysis_input.fetch_lv_network,
                        "processFeederLoads": feeder_load_analysis_input.process_feeder_loads,
                        "processCoincidentLoads": feeder_load_analysis_input.process_coincident_loads,
                        "produceConductorReport": True, # We currently only support conductor report
                        "aggregateAtFeederLevel": feeder_load_analysis_input.aggregate_at_feeder_level,
                        "output": feeder_load_analysis_input.output
                    }
                }
            )
        )

    def upload_study(self, study: Study):
        """
        Uploads a new study to the Evolve App Server
        :param study: An instance of a data class representing a new study
        """
        return get_event_loop().run_until_complete(self.async_upload_study(study))

    @catch_warnings
    async def async_upload_study(self, study: Study):
        """
        Uploads a new study to the Evolve App Server
        :param study: An instance of a data class representing a new study
        :return: The HTTP response received from the Evolve App Server after attempting to upload the study
        """
        return await self.do_post_request(
            self.build_request("""
                mutation uploadStudy($study: StudyInput!) {
                    addStudies(studies: [$study])
                }""", {
                    "study": {
                        "name": study.name,
                        "description": study.description,
                        "tags": study.tags,
                        "styles": study.styles,
                        "results": [{
                            "name": result.name,
                            "geoJsonOverlay": result.geo_json_overlay and {
                                "data": result.geo_json_overlay.data,
                                "sourceProperties": result.geo_json_overlay.source_properties,
                                "styles": result.geo_json_overlay.styles
                            },
                            "stateOverlay": result.state_overlay and {
                                "data": result.state_overlay.data,
                                "styles": result.state_overlay.styles
                            },
                            "sections": [{
                                "type": section.type,
                                "name": section.name,
                                "description": section.description,
                                "columns": section.columns,
                                "data": section.data
                            } for section in result.sections]
                        } for result in study.results]
                    }
                }
            )
        )

    def run_ingestor(self, run_config: List[IngestorConfigInput]):
        """
        Send request to perform an ingestor run
        :param run_config: A list of IngestorConfigInput
        :return: The HTTP response received from the Evolve App Server after attempting to run the ingestor
        """
        return get_event_loop().run_until_complete(
            self.async_run_ingestor(run_config))

    async def async_run_ingestor(self, run_config: List[IngestorConfigInput]):
        """
        Send asynchronous request to perform an ingestor run
        :param run_config: A list of IngestorConfigInput
        :return: The HTTP response received from the Evolve App Server after attempting to run the ingestor
        """
        with warnings.catch_warnings():
            if not self._verify_certificate:
                warnings.filterwarnings("ignore", category=InsecureRequestWarning)
            json = {
                "query": """
                    mutation executeIngestor($runConfig: [IngestorConfigInput!]) {
                        executeIngestor(runConfig: $runConfig)
                    }
                """,
                "variables": {
                    "runConfig": [asdict(x) for x in run_config],
                }
            }

            if self._verify_certificate:
                sslcontext = ssl.create_default_context(cafile=self._ca_filename)

            async with self.session.post(
                construct_url(protocol=self._protocol, host=self._host, port=self._port, path="/api/graphql"),
                headers=self._get_request_headers(),
                json=json,
                ssl=sslcontext if self._verify_certificate else False
            ) as response:
                if response.ok:
                    return await response.json()
                else:
                    response.raise_for_status()

    def get_ingestor_run(self, ingestor_run_id: int):
        """
        Send request to retrieve the record of a particular ingestor run.
        :param ingestor_run_id: The ID of the ingestor run to retrieve execution information about.
        :return: The HTTP response received from the Evolve App Server including the ingestor run information (if found).
        """
        return get_event_loop().run_until_complete(
            self.async_get_ingestor_run(ingestor_run_id))

    async def async_get_ingestor_run(self, ingestor_run_id: int):
        """
        Send asynchronous request to retrieve the record of a particular ingestor run.
        :param ingestor_run_id: The ID of the ingestor run to retrieve execution information about.
        :return: The HTTP response received from the Evolve App Server including the ingestor run information (if found).
        """
        with warnings.catch_warnings():
            if not self._verify_certificate:
                warnings.filterwarnings("ignore", category=InsecureRequestWarning)
            json = {
                "query": """
                    query getIngestorRun($id: Int!) {
                        getIngestorRun(id: $id) {
                        id
                        containerRuntimeType,
                        payload,
                        token,
                        status,
                        startedAt,
                        statusLastUpdatedAt,
                        completedAt
                        }
                    }
                """,
                "variables": {
                    "id": ingestor_run_id,
                }
            }

            if self._verify_certificate:
                sslcontext = ssl.create_default_context(cafile=self._ca_filename)

            async with self.session.post(
                    construct_url(protocol=self._protocol, host=self._host, port=self._port, path="/api/graphql"),
                    headers=self._get_request_headers(),
                    json=json,
                    ssl=sslcontext if self._verify_certificate else False
            ) as response:
                if response.ok:
                    return await response.json()
                else:
                    raise response.raise_for_status()

    def get_ingestor_run_list(self, query_filter: Optional[IngestorRunsFilterInput] = None,
                              query_sort: Optional[IngestorRunsSortCriteriaInput] = None):
        """
        Send request to retrieve a list of ingestor run records matching the provided filter parameters.
        :param query_filter: An `IngestorRunsFilterInput` object. Only records matching the provided values will be returned.
            If not supplied all records will be returned. (Optional)
        :param query_sort: An `IngestorRunsSortCriteriaInput` that can control the order of the returned record based on a number of fields. (Optional)
        :return: The HTTP response received from the Evolve App Server including all matching ingestor records found.
        """
        return get_event_loop().run_until_complete(
            self.async_get_ingestor_run_list(query_filter, query_sort))

    async def async_get_ingestor_run_list(self, query_filter: Optional[IngestorRunsFilterInput] = None,
                                          query_sort: Optional[IngestorRunsSortCriteriaInput] = None):
        """
        Send asynchronous request to retrieve a list of ingestor run records matching the provided filter parameters.
        :param query_filter: An `IngestorRunsFilterInput` object. Only records matching the provided values will be returned.
            If not supplied all records will be returned. (Optional)
        :param query_sort: An `IngestorRunsSortCriteriaInput` that can control the order of the returned record based on a number of fields. (Optional)
        :return: The HTTP response received from the Evolve App Server including all matching ingestor records found.
        """

        with warnings.catch_warnings():
            if not self._verify_certificate:
                warnings.filterwarnings("ignore", category=InsecureRequestWarning)
            json = {
                "query": """
                    query listIngestorRuns($filter: IngestorRunsFilterInput, $sort: IngestorRunsSortCriteriaInput) {
                        listIngestorRuns(filter: $filter, sort: $sort) {
                        id
                        containerRuntimeType,
                        payload,
                        token,
                        status,
                        startedAt,
                        statusLastUpdatedAt,
                        completedAt
                        }
                    }
                """,
                "variables": {
                    **({"filter": {
                        "id": query_filter.id,
                        "status": query_filter.status and [state.name for state in query_filter.status],
                        "completed": query_filter.completed,
                        "containerRuntimeType": query_filter.container_runtime_type and [runtime.name for runtime in
                                                                                         query_filter.container_runtime_type]
                    }} if query_filter else {}),
                    **({"sort": {
                        "status": query_sort.status and query_sort.status.name,
                        "startedAt": query_sort.started_at and query_sort.started_at.name,
                        "statusLastUpdatedAt": query_sort.status_last_updated_at and query_sort.status_last_updated_at.name,
                        "completedAt": query_sort.completed_at and query_sort.completed_at.name,
                        "containerRuntimeType": query_sort.container_runtime_type and query_sort.container_runtime_type.name,
                    }} if query_sort else {})
                }
            }

            if self._verify_certificate:
                sslcontext = ssl.create_default_context(cafile=self._ca_filename)

            async with self.session.post(
                    construct_url(protocol=self._protocol, host=self._host, port=self._port, path="/api/graphql"),
                    headers=self._get_request_headers(),
                    json=json,
                    ssl=sslcontext if self._verify_certificate else False
            ) as response:
                if response.ok:
                    return await response.json()
                else:
                    raise response.raise_for_status()

    def run_hosting_capacity_calibration(self, calibration_name: str, local_calibration_time: datetime,
                                         feeders: Optional[List[str]] = None,
                                         transformer_tap_settings: Optional[str] = None,
                                         generator_config: Optional[GeneratorConfig] = None):
        """
        Send request to run hosting capacity calibration
        :param calibration_name: A string representation of the calibration name
        :param local_calibration_time: A datetime representation of the calibration time, in the timezone of your pqv data ("model time").
        :param feeders: A list of feeder ID's to run the calibration over. If not supplied then the calibration is run over all feeders in the network.
        :param transformer_tap_settings: A set of transformer tap settings to apply before running the calibration work package.
                If provided, this will take precedence over any 'transformer_tap_settings' supplied in via the generator_config parameter
        :param generator_config: A `GeneratorConfig` object that overrides the default values in the `WorkPackageConfig` used by calibration.
                Note: The following fields cannot be overridden during calibration: generator_config.model.calibration, generator_config.model.meter_placement_config, generator_config.solve.step_size_minutes, and generator_config.raw_results.

        :return: The HTTP response received from the Evolve App Server after attempting to run the calibration
        """
        return get_event_loop().run_until_complete(
            self.async_run_hosting_capacity_calibration(calibration_name, local_calibration_time, feeders,
                                                        transformer_tap_settings,
                                                        generator_config))

    @catch_warnings
    async def async_run_hosting_capacity_calibration(self, calibration_name: str,
                                                     calibration_time_local: datetime,
                                                     feeders: Optional[List[str]] = None,
                                                     transformer_tap_settings: Optional[str] = None,
                                                     generator_config: Optional[GeneratorConfig] = None):
        """
        Send asynchronous request to run hosting capacity calibration
        :param calibration_name: A string representation of the calibration name
        :param calibration_time_local: A datetime representation of the calibration time, in the timezone of your pqv data ("model time").
        :param feeders: A list of feeder ID's to run the calibration over. If not supplied then the calibration is run over all feeders in the network.
        :param transformer_tap_settings: A set of transformer tap settings to apply before running the calibration work package.
                If provided, this will take precedence over any 'transformer_tap_settings' supplied in via the generator_config parameter
        :param generator_config: A `GeneratorConfig` object that overrides the default values in the `WorkPackageConfig` used by calibration.
                Note: The following fields cannot be overridden during calibration: generator_config.model.calibration, generator_config.model.meter_placement_config, generator_config.solve.step_size_minutes, and generator_config.raw_results.

        :return: The HTTP response received from the Evolve App Server after attempting to run the calibration
        """
        parsed_time = calibration_time_local.replace(microsecond=0, tzinfo=None)
        if transformer_tap_settings:
            if generator_config:
                if generator_config.model:
                    generator_config.model.transformer_tap_settings = transformer_tap_settings
                else:
                    generator_config.model = ModelConfig(transformer_tap_settings=transformer_tap_settings)
            else:
                generator_config = GeneratorConfig(model=ModelConfig(transformer_tap_settings=transformer_tap_settings))

        return await self.do_post_request(
            self.build_request("""
                mutation runCalibration($calibrationName: String!, $calibrationTimeLocal: LocalDateTime, $feeders: [String!]) {
                    runCalibration(calibrationName: $calibrationName, calibrationTimeLocal: $calibrationTimeLocal, feeders: $feeders)
                }""", {
                    "calibrationName": calibration_name,
                    "calibrationTimeLocal": parsed_time.isoformat(),
                    "feeders": feeders,
                    "generatorConfig": generator_config and {
                        "model": generator_config.model and {
                            "vmPu": generator_config.model.vm_pu,
                            "loadVMinPu": generator_config.model.load_vmin_pu,
                            "loadVMaxPu": generator_config.model.load_vmax_pu,
                            "genVMinPu": generator_config.model.gen_vmin_pu,
                            "genVMaxPu": generator_config.model.gen_vmax_pu,
                            "loadModel": generator_config.model.load_model,
                            "collapseSWER": generator_config.model.collapse_swer,
                            "calibration": generator_config.model.calibration,
                            "pFactorBaseExports": generator_config.model.p_factor_base_exports,
                            "pFactorForecastPv": generator_config.model.p_factor_forecast_pv,
                            "pFactorBaseImports": generator_config.model.p_factor_base_imports,
                            "fixSinglePhaseLoads": generator_config.model.fix_single_phase_loads,
                            "maxSinglePhaseLoad": generator_config.model.max_single_phase_load,
                            "fixOverloadingConsumers": generator_config.model.fix_overloading_consumers,
                            "maxLoadTxRatio": generator_config.model.max_load_tx_ratio,
                            "maxGenTxRatio": generator_config.model.max_gen_tx_ratio,
                            "fixUndersizedServiceLines": generator_config.model.fix_undersized_service_lines,
                            "maxLoadServiceLineRatio": generator_config.model.max_load_service_line_ratio,
                            "maxLoadLvLineRatio": generator_config.model.max_load_lv_line_ratio,
                            "collapseLvNetworks": generator_config.model.collapse_lv_networks,
                            "feederScenarioAllocationStrategy": generator_config.model.feeder_scenario_allocation_strategy and generator_config.model.feeder_scenario_allocation_strategy.name,
                            "closedLoopVRegEnabled": generator_config.model.closed_loop_v_reg_enabled,
                            "closedLoopVRegReplaceAll": generator_config.model.closed_loop_v_reg_replace_all,
                            "closedLoopVRegSetPoint": generator_config.model.closed_loop_v_reg_set_point,
                            "closedLoopVBand": generator_config.model.closed_loop_v_band,
                            "closedLoopTimeDelay": generator_config.model.closed_loop_time_delay,
                            "closedLoopVLimit": generator_config.model.closed_loop_v_limit,
                            "defaultTapChangerTimeDelay": generator_config.model.default_tap_changer_time_delay,
                            "defaultTapChangerSetPointPu": generator_config.model.default_tap_changer_set_point_pu,
                            "defaultTapChangerBand": generator_config.model.default_tap_changer_band,
                            "splitPhaseDefaultLoadLossPercentage": generator_config.model.split_phase_default_load_loss_percentage,
                            "splitPhaseLVKV": generator_config.model.split_phase_lv_kv,
                            "swerVoltageToLineVoltage": generator_config.model.swer_voltage_to_line_voltage,
                            "loadPlacement": generator_config.model.load_placement and generator_config.model.load_placement.name,
                            "loadIntervalLengthHours": generator_config.model.load_interval_length_hours,
                            "meterPlacementConfig": generator_config.model.meter_placement_config and {
                                "feederHead": generator_config.model.meter_placement_config.feeder_head,
                                "distTransformers": generator_config.model.meter_placement_config.dist_transformers,
                                "switchMeterPlacementConfigs": generator_config.model.meter_placement_config.switch_meter_placement_configs and [
                                    {
                                        "meterSwitchClass": spc.meter_switch_class and spc.meter_switch_class.name,
                                        "namePattern": spc.name_pattern
                                    } for spc in
                                    generator_config.model.meter_placement_config.switch_meter_placement_configs
                                ],
                                "energyConsumerMeterGroup": generator_config.model.meter_placement_config.energy_consumer_meter_group
                            },
                            "seed": generator_config.model.seed,
                            "defaultLoadWatts": generator_config.model.default_load_watts,
                            "defaultGenWatts": generator_config.model.default_gen_watts,
                            "defaultLoadVar": generator_config.model.default_load_var,
                            "defaultGenVar": generator_config.model.default_gen_var,
                            "transformerTapSettings": generator_config.model.transformer_tap_settings,
                            "ctPrimScalingFactor": generator_config.model.ct_prim_scaling_factor,
                        },
                        "solve": generator_config.solve and {
                            "normVMinPu": generator_config.solve.norm_vmin_pu,
                            "normVMaxPu": generator_config.solve.norm_vmax_pu,
                            "emergVMinPu": generator_config.solve.emerg_vmin_pu,
                            "emergVMaxPu": generator_config.solve.emerg_vmax_pu,
                            "baseFrequency": generator_config.solve.base_frequency,
                            "voltageBases": generator_config.solve.voltage_bases,
                            "maxIter": generator_config.solve.max_iter,
                            "maxControlIter": generator_config.solve.max_control_iter,
                            "mode": generator_config.solve.mode and generator_config.solve.mode.name,
                            "stepSizeMinutes": generator_config.solve.step_size_minutes
                        },
                        "rawResults": generator_config.raw_results and {
                            "energyMeterVoltagesRaw": generator_config.raw_results.energy_meter_voltages_raw,
                            "energyMetersRaw": generator_config.raw_results.energy_meters_raw,
                            "resultsPerMeter": generator_config.raw_results.results_per_meter,
                            "overloadsRaw": generator_config.raw_results.overloads_raw,
                            "voltageExceptionsRaw": generator_config.raw_results.voltage_exceptions_raw
                        }
                    }
                }
            )
        )

    def get_hosting_capacity_calibration_run(self, id_: str):
        """
        Retrieve information of a hosting capacity calibration run
        :param id_: The calibration ID
        :return: The HTTP response received from the Evolve App Server after requesting calibration run info
        """
        return get_event_loop().run_until_complete(self.async_get_hosting_capacity_calibration_run(id_))

    @catch_warnings
    async def async_get_hosting_capacity_calibration_run(self, id_: str):
        """
        Retrieve information of a hosting capacity calibration run
        :param id_: The calibration ID
        :return: The HTTP response received from the Evolve App Server after requesting calibration run info
        """
        return await self.do_post_request(
            self.build_request("""
                query getCalibrationRun($id: ID!) {
                    getCalibrationRun(id: $id) {
                        id
                        name
                        workflowId
                        runId
                        calibrationTimeLocal
                        startAt
                        completedAt
                        status
                        feeders
                        calibrationWorkPackageConfig
                    }
                }""", {"id": id_}
            )
        )

    def get_hosting_capacity_calibration_sets(self):
        """
        Retrieve a list of all completed calibration runs initiated through Evolve App Server
        :return: The HTTP response received from the Evolve App Server after requesting completed calibration runs
        """
        return get_event_loop().run_until_complete(self.async_get_hosting_capacity_calibration_sets())

    @catch_warnings
    async def async_get_hosting_capacity_calibration_sets(self):
        """
        Retrieve a list of all completed calibration runs initiated through Evolve App Server
        :return: The HTTP response received from the Evolve App Server after requesting completed calibration runs
        """
        return await self.do_post_request(
            self.build_request("""
                query { 
                    getCalibrationSets
                }"""
            )
        )

    def get_transformer_tap_settings(self, calibration_id: str, feeder: Optional[str] = None,
                                     transformer_mrid: Optional[str] = None):
        """
        Retrieve distribution transformer tap settings from a calibration set in the hosting capacity input database.
        :return: The HTTP response received from the Evolve App Server after requesting transformer tap settings for the calibration id
        """
        return get_event_loop().run_until_complete(
            self.async_get_transformer_tap_settings(calibration_id, feeder, transformer_mrid))

    async def async_get_transformer_tap_settings(self, calibration_id: str, feeder: Optional[str] = None,
                                                 transformer_mrid: Optional[str] = None):
        """
        Retrieve distribution transformer tap settings from a calibration set in the hosting capacity input database.
        :return: The HTTP response received from the Evolve App Server after requesting transformer tap settings for the calibration id
        """
        with warnings.catch_warnings():
            if not self._verify_certificate:
                warnings.filterwarnings("ignore", category=InsecureRequestWarning)
            json = {
                "query": """
                    query getTransformerTapSettings($calibrationName: String!, $feeder: String, $transformerMrid: String) {
                        getTransformerTapSettings(calibrationName: $calibrationName, feeder: $feeder, transformerMrid: $transformerMrid) {
                            id
                            highStep
                            lowStep
                            nominalTapNum
                            tapPosition
                            controlEnabled
                            stepVoltageIncrement
                        }
                     }
                """,
                "variables": {
                    "calibrationName": calibration_id,
                    "feeder": feeder,
                    "transformerMrid": transformer_mrid
                }
            }
            if self._verify_certificate:
                sslcontext = ssl.create_default_context(cafile=self._ca_filename)

            async with self.session.post(
                construct_url(protocol=self._protocol, host=self._host, port=self._port, path="/api/graphql"),
                headers=self._get_request_headers(),
                json=json,
                ssl=sslcontext if self._verify_certificate else False
            ) as response:
                if response.ok:
                    return await response.json()
                else:
                    response.raise_for_status()

    def run_opendss_export(self, config: OpenDssConfig):
        """
        Send request to run an opendss export
        :param config: The OpenDssConfig for running the export
        :return: The HTTP response received from the Evolve App Server after attempting to run the opendss export
        """
        return get_event_loop().run_until_complete(self.async_run_opendss_export(config))

    @catch_warnings
    async def async_run_opendss_export(self, config: OpenDssConfig):
        """
        Send asynchronous request to run an opendss export
        :param config: The OpenDssConfig for running the export
        :return: The HTTP response received from the Evolve App Server after attempting to run the opendss export
        """
        return await self.do_post_request(
            self.build_request("""
                mutation createOpenDssModel($input: OpenDssModelInput!) {
                    createOpenDssModel(input: $input)
                }""", {
                    "input": config.to_json()
                }
            )
        )

    def get_paged_opendss_models(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        query_filter: Optional[GetOpenDssModelsFilterInput] = None,
        query_sort: Optional[GetOpenDssModelsSortCriteriaInput] = None):
        """
        Retrieve a paginated opendss export run information
        :param limit: The number of opendss export runs to retrieve
        :param offset: The number of opendss export runs to skip
        :param query_filter: The filter to apply to the query
        :param query_sort: The sorting to apply to the query
        :return: The HTTP response received from the Evolve App Server after requesting opendss export run information
        """
        return get_event_loop().run_until_complete(
            self.async_get_paged_opendss_models(limit, offset, query_filter, query_sort))

    @catch_warnings
    async def async_get_paged_opendss_models(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        query_filter: Optional[GetOpenDssModelsFilterInput] = None,
        query_sort: Optional[GetOpenDssModelsSortCriteriaInput] = None) -> dict:
        """
        Retrieve a paginated opendss export run information
        :param limit: The number of opendss export runs to retrieve
        :param offset: The number of opendss export runs to skip
        :param query_filter: The filter to apply to the query
        :param query_sort: The sorting to apply to the query
        :return: The HTTP response received from the Evolve App Server after requesting opendss export run information
        """
        json = {
            "query": """
                query pagedOpenDssModels($limit: Int, $offset: Long, $filter: GetOpenDssModelsFilterInput, $sort: GetOpenDssModelsSortCriteriaInput) {
                pagedOpenDssModels(limit: $limit, offset: $offset, filter: $filter,sort: $sort) {
                    totalCount
                    offset,
                    models {
                        id
                        name
                        createdAt
                        createdBy
                        state
                        downloadUrl
                        isPublic
                        errors
                        generationSpec {
                            modelOptions{
                                scenario
                                year
                                feeder
                            }
                            modulesConfiguration {
                                common {
                                    fixedTime{
                                        loadTime
                                        overrides {
                                            loadId
                                            loadWattsOverride
                                            genWattsOverride
                                            loadVarOverride
                                            genVarOverride
                                        }
                                    }
                                    timePeriod {
                                        startTime
                                        endTime
                                        overrides {
                                            loadId
                                            loadWattsOverride
                                            genWattsOverride
                                            loadVarOverride
                                            genVarOverride
                                        }
                                    }
                                }
                                generator {
                                    model {
                                        vmPu
                                        loadVMinPu
                                        loadVMaxPu
                                        genVMinPu
                                        genVMaxPu
                                        loadModel
                                        collapseSWER
                                        calibration
                                        pFactorBaseExports
                                        pFactorForecastPv
                                        pFactorBaseImports
                                        fixSinglePhaseLoads
                                        maxSinglePhaseLoad
                                        fixOverloadingConsumers
                                        maxLoadTxRatio
                                        maxGenTxRatio
                                        fixUndersizedServiceLines
                                        maxLoadServiceLineRatio
                                        maxLoadLvLineRatio
                                        collapseLvNetworks
                                        feederScenarioAllocationStrategy
                                        closedLoopVRegEnabled
                                        closedLoopVRegReplaceAll
                                        closedLoopVRegSetPoint
                                        closedLoopVBand
                                        closedLoopTimeDelay
                                        closedLoopVLimit
                                        defaultTapChangerTimeDelay
                                        defaultTapChangerSetPointPu
                                        defaultTapChangerBand
                                        splitPhaseDefaultLoadLossPercentage
                                        splitPhaseLVKV
                                        swerVoltageToLineVoltage
                                        loadPlacement
                                        loadIntervalLengthHours
                                        meterPlacementConfig {
                                            feederHead
                                            distTransformers
                                            switchMeterPlacementConfigs {
                                              meterSwitchClass
                                              namePattern
                                            }
                                            energyConsumerMeterGroup
                                        }
                                        seed
                                        defaultLoadWatts
                                        defaultGenWatts
                                        defaultLoadVar
                                        defaultGenVar
                                        transformerTapSettings
                                        ctPrimScalingFactor
                                    }
                                    solve {
                                        normVMinPu
                                        normVMaxPu
                                        emergVMinPu
                                        emergVMaxPu
                                        baseFrequency
                                        voltageBases
                                        maxIter
                                        maxControlIter
                                        mode
                                        stepSizeMinutes
                                    }
                                    rawResults {
                                        energyMeterVoltagesRaw
                                        energyMetersRaw
                                        resultsPerMeter
                                        overloadsRaw
                                        voltageExceptionsRaw
                                    }
                                }
                            }
                        }
                    }
                }
            }
            """,
            "variables": {
                **({"limit": limit} if limit is not None else {}),
                **({"offset": offset} if offset is not None else {}),
                **({"filter": {
                    "name": query_filter.name,
                    "isPublic": query_filter.is_public,
                    "state": query_filter.state and [state.name for state in query_filter.state]
                }} if query_filter else {}),
                **({"sort": {
                    "name": query_sort.name and query_sort.name.name,
                    "createdAt": query_sort.created_at and query_sort.created_at.name,
                    "state": query_sort.state and query_sort.state.name,
                    "isPublic": query_sort.is_public and query_sort.is_public.name
                }} if query_sort else {})
            }
        }
        return await self.do_post_request(json)

    def get_opendss_model_download_url(self, run_id: int):
        """
        Retrieve a download url for the specified opendss export run id
        :param run_id: The opendss export run ID
        :return: The HTTP response received from the Evolve App Server after requesting opendss export model download url
        """
        return get_event_loop().run_until_complete(self.async_get_opendss_model_download_url(run_id))

    @catch_warnings
    async def async_get_opendss_model_download_url(self, run_id: int):
        """
        Retrieve a download url for the specified opendss export run id
        :param run_id: The opendss export run ID
        :return: The HTTP response received from the Evolve App Server after requesting opendss export model download url
        """
        return await self.do_get_request(run_id=run_id)

    async def do_post_request(self, json):
        self._do_request()
        async with self.session.post(
                construct_url(**self._auth.base_url_args, path="/api/graphql"),
                headers=self._get_request_headers(),
                json=json,
                ssl=self._get_ssl()
        ) as response:
            if response.ok:
                return await response.json()
            else:
                response.raise_for_status()

    async def do_get_request(self, *, run_id: int):  # TODO: Terrible name probably
        self._do_request()
        async with self.session.get(
                construct_url(**self._auth.base_url_args,
                              path=f"/api/opendss-model/{run_id}"),
                headers=self._get_request_headers(),
                ssl=self._get_ssl(),
                allow_redirects=False
            ) as response:
                if response.status == HTTPStatus.FOUND:
                    return response.headers["Location"]
                elif not response.ok:
                    response.raise_for_status()

    def _do_request(self):  # TODO: can this just be called once per run?
        if not self._verify_certificate:
            warnings.filterwarnings("ignore", category=InsecureRequestWarning)

    def _get_ssl(self):
        return ssl.create_default_context(cafile=self._ca_filename) if self._verify_certificate else False

    def get_opendss_model(self, model_id: int):
        """
        Retrieve information of a OpenDss model export
        :param model_id: The OpenDss model export ID
        :return: The HTTP response received from the Evolve App Server after requesting the openDss model info
        """
        return get_event_loop().run_until_complete(self.async_get_opendss_model(model_id))

    async def async_get_opendss_model(self, model_id: int):  # TODO: this logic should be hidden behind a generator
        """
        Retrieve information of a OpenDss model export
        :param model_id: The OpenDss model export ID
        :return: The HTTP response received from the Evolve App Server after requesting the openDss model info
        """

        offset = 0
        page_size = 20

        while True:
            response = await self.async_get_paged_opendss_models(page_size, offset)
            total_count = int(response["data"]["pagedOpenDssModels"]["totalCount"])
            page_count = len(response["data"]["pagedOpenDssModels"]["models"])
            for model in response["data"]["pagedOpenDssModels"]["models"]:
                if model["id"] == model_id:
                    return model
            offset += page_count

            if offset >= total_count:
                break

        raise ValueError(f"Model id:{model_id} was not found in EAS database.")
