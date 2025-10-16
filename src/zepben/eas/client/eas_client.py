#  Copyright 2025 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["EasClient"]

import ssl
import warnings
from asyncio import get_event_loop
from dataclasses import asdict
from datetime import datetime
from http import HTTPStatus
from json import dumps
from typing import Optional, List, Any

import aiohttp
from aiohttp import ClientSession
from urllib3.exceptions import InsecureRequestWarning

from zepben.eas.client.auth_method import BaseAuthMethod, TokenAuth
from zepben.eas.client.decorators import catch_warnings
from zepben.eas.client.feeder_load_analysis_input import FeederLoadAnalysisInput
from zepben.eas.client.ingestor import IngestorConfigInput, IngestorRunsFilterInput, IngestorRunsSortCriteriaInput, IngestorRun
from zepben.eas.client.opendss import OpenDssConfig, GetOpenDssModelsFilterInput, GetOpenDssModelsSortCriteriaInput
from zepben.eas.client.study import Study
from zepben.eas.client.util import construct_url
from zepben.eas.client.work_package import WorkPackageConfig, GeneratorConfig, ModelConfig, WorkPackageProgress


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
        self._ca_filename: Optional[str] = ca_filename
        self._verify_certificate: bool = auth.verify_certificate
        self._auth: BaseAuthMethod = auth

        if session is None:
            conn = aiohttp.TCPConnector(limit=200, limit_per_host=0)
            timeout = aiohttp.ClientTimeout(total=60)
            self.session: ClientSession = aiohttp.ClientSession(
                json_serialize=json_serialiser or dumps,
                connector=conn,
                timeout=timeout
            )
        else:
            self.session = session

    def close(self):
        return get_event_loop().run_until_complete(self.aclose())

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

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

    def run_hosting_capacity_work_package(self, work_package: WorkPackageConfig) -> dict:
        """
        Send request to hosting capacity service to run work package

        :param work_package: An instance of the `WorkPackageConfig` data class representing the work package
            configuration for the run
        :return: The HTTP response received from the Evolve App Server after attempting to run work package
        """
        return get_event_loop().run_until_complete(self.async_run_hosting_capacity_work_package(work_package))

    def get_work_package_cost_estimation(self, work_package: WorkPackageConfig) -> dict:
        """
        Send request to hosting capacity service to get an estimate cost of supplied work package

        :param work_package: An instance of the `WorkPackageConfig` data class representing the work package
            configuration for the run
        :return: The HTTP response received from the Evolve App Server after attempting to run work package
        """
        return get_event_loop().run_until_complete(self.async_get_work_package_cost_estimation(work_package))

    async def async_get_work_package_cost_estimation(self, work_package: WorkPackageConfig) -> dict:
        """
        Send asynchronous request to hosting capacity service to get an estimate cost of supplied work package

        :param work_package: An instance of the `WorkPackageConfig` data class representing the work package
            configuration for the run
        :return: The HTTP response received from the Evolve App Server after attempting to run work package
        """
        return await self._do_post_request(
            self.build_request("""
                query getWorkPackageCostEstimation($input: WorkPackageInput!) {
                    getWorkPackageCostEstimation(input: $input)
                }""", work_package.to_json()
            )
        )

    async def async_run_hosting_capacity_work_package(self, work_package: WorkPackageConfig) -> dict:
        """
        Send asynchronous request to hosting capacity service to run work package

        :param work_package: An instance of the `WorkPackageConfig` data class representing the work package
            configuration for the run
        :return: The HTTP response received from the Evolve App Server after attempting to run work package
        """
        return await self._do_post_request(
            self.build_request("""
                mutation runWorkPackage($input: WorkPackageInput!, $workPackageName: String!) {
                    runWorkPackage(input: $input, workPackageName: $workPackageName)
                }""", work_package.to_json()
            )
        )

    def cancel_hosting_capacity_work_package(self, work_package_id: str) -> dict:
        """
        Send request to hosting capacity service to cancel a running work package

        :param work_package_id: The id of the running work package to cancel
        :return: The HTTP response received from the Evolve App Server after attempting to cancel work package
        """
        return get_event_loop().run_until_complete(self.async_cancel_hosting_capacity_work_package(work_package_id))

    async def async_cancel_hosting_capacity_work_package(self, work_package_id: str) -> dict:
        """
        Send asynchronous request to hosting capacity service to cancel a running work package

        :param work_package_id: The id of the running work package to cancel
        :return: The HTTP response received from the Evolve App Server after attempting to cancel work package
        """
        return await self._do_post_request(
            self.build_request("""
                mutation cancelWorkPackage($workPackageId: ID!) {
                    cancelWorkPackage(workPackageId: $workPackageId)
                }""",{
                    "workPackageId": work_package_id
                }
            )
        )

    def get_hosting_capacity_work_packages_progress(self) -> dict:
        """
        Retrieve running work packages progress information from hosting capacity service

        :return: The HTTP response received from the Evolve App Server after requesting work packages progress info
        """
        return get_event_loop().run_until_complete(self.async_get_hosting_capacity_work_packages_progress())

    async def async_get_hosting_capacity_work_packages_progress(self) -> dict:
        """
        Asynchronously retrieve running work packages progress information from hosting capacity service

        :return: The HTTP response received from the Evolve App Server after requesting work packages progress info
        """
        return await self._do_post_request(
            self.build_request("""
                query getWorkPackageProgress {
                    %s
                }""" % WorkPackageProgress.build_gql_query_object_model()
            )
        )

    def run_feeder_load_analysis_report(self, feeder_load_analysis_input: FeederLoadAnalysisInput) -> dict:
        """
        Send request to evolve app server to run a feeder load analysis study

        :param feeder_load_analysis_input:: An instance of the `FeederLoadAnalysisConfig` data class representing the
            configuration for the run
        :return: The HTTP response received from the Evolve App Server after attempting to run work package
        """
        return get_event_loop().run_until_complete(
            self.async_run_feeder_load_analysis_report(feeder_load_analysis_input))

    async def async_run_feeder_load_analysis_report(self, feeder_load_analysis_input: FeederLoadAnalysisInput) -> dict:
        """
        Asynchronously send request to evolve app server to run a feeder load analysis study

        :return: The HTTP response received from the Evolve App Server after requesting a feeder load analysis report
        """
        _json = feeder_load_analysis_input.to_json()
        _json['geographicalRegions'] = _json.get('feeders', None)
        return await self._do_post_request(
            self.build_request("""
                mutation runFeederLoadAnalysis($input: FeederLoadAnalysisInput!) {
                    runFeederLoadAnalysis(input: $input)
                }""",{
                    "input": _json
                }
            )
        )

    def upload_study(self, study: Study) -> dict:
        """
        Uploads a new study to the Evolve App Server

        :param study: An instance of a data class representing a new study
        """
        return get_event_loop().run_until_complete(self.async_upload_study(study))

    async def async_upload_study(self, study: Study) -> dict:
        """
        Uploads a new study to the Evolve App Server

        :param study: An instance of a data class representing a new study
        :return: The HTTP response received from the Evolve App Server after attempting to upload the study
        """
        return await self._do_post_request(
            self.build_request("""
                mutation uploadStudy($study: StudyInput!) {
                    addStudies(studies: [$study])
                }""", {
                    "study": study.to_json()
                }
            )
        )

    def run_ingestor(self, run_config: List[IngestorConfigInput]) -> dict:
        """
        Send request to perform an ingestor run

        :param run_config: A list of IngestorConfigInput
        :return: The HTTP response received from the Evolve App Server after attempting to run the ingestor
        """
        return get_event_loop().run_until_complete(
            self.async_run_ingestor(run_config))

    async def async_run_ingestor(self, run_config: List[IngestorConfigInput]) -> dict:
        """
        Send asynchronous request to perform an ingestor run

        :param run_config: A list of IngestorConfigInput
        :return: The HTTP response received from the Evolve App Server after attempting to run the ingestor
        """
        return await self._do_post_request(
            self.build_request("""
                mutation executeIngestor($runConfig: [IngestorConfigInput!]) {
                    executeIngestor(runConfig: $runConfig)
                }""", {
                    "runConfig": [asdict(x) for x in run_config],
                }
            )
        )

    def get_ingestor_run(self, ingestor_run_id: int) -> dict:
        """
        Send request to retrieve the record of a particular ingestor run.

        :param ingestor_run_id: The ID of the ingestor run to retrieve execution information about.
        :return: The HTTP response received from the Evolve App Server including the ingestor run information (if found).
        """
        return get_event_loop().run_until_complete(
            self.async_get_ingestor_run(ingestor_run_id))

    async def async_get_ingestor_run(self, ingestor_run_id: int) -> dict:
        """
        Send asynchronous request to retrieve the record of a particular ingestor run.

        :param ingestor_run_id: The ID of the ingestor run to retrieve execution information about.
        :return: The HTTP response received from the Evolve App Server including the ingestor run information (if found).
        """
        return await self._do_post_request(
            self.build_request("""
                query getIngestorRun($id: Int!) {
                    getIngestorRun(id: $id) {
                        %s
                    }
                }""" % IngestorRun.build_gql_query_object_model(), {
                    "id": ingestor_run_id,
                }
            )
        )

    def get_ingestor_run_list(
            self,
            query_filter: Optional[IngestorRunsFilterInput] = None,
            query_sort: Optional[IngestorRunsSortCriteriaInput] = None
    ) -> dict:
        """
        Send request to retrieve a list of ingestor run records matching the provided filter parameters.

        :param query_filter: An `IngestorRunsFilterInput` object. Only records matching the provided values will be returned.
            If not supplied all records will be returned. (Optional)
        :param query_sort: An `IngestorRunsSortCriteriaInput` that can control the order of the returned record based on a number of fields. (Optional)
        :return: The HTTP response received from the Evolve App Server including all matching ingestor records found.
        """
        return get_event_loop().run_until_complete(
            self.async_get_ingestor_run_list(query_filter, query_sort))

    async def async_get_ingestor_run_list(
            self,
            query_filter: Optional[IngestorRunsFilterInput] = None,
            query_sort: Optional[IngestorRunsSortCriteriaInput] = None
    ) -> dict:
        """
        Send asynchronous request to retrieve a list of ingestor run records matching the provided filter parameters.

        :param query_filter: An `IngestorRunsFilterInput` object. Only records matching the provided values will be returned.
            If not supplied all records will be returned. (Optional)
        :param query_sort: An `IngestorRunsSortCriteriaInput` that can control the order of the returned record based on a number of fields. (Optional)
        :return: The HTTP response received from the Evolve App Server including all matching ingestor records found.
        """
        _json = {}
        if query_filter is not None:
            _json['filter'] = query_filter.to_json()
        if query_sort is not None:
            _json['sort'] = query_sort.to_json()

        return await self._do_post_request(
            self.build_request("""
                query listIngestorRuns($filter: IngestorRunsFilterInput, $sort: IngestorRunsSortCriteriaInput) {
                    listIngestorRuns(filter: $filter, sort: $sort) {
                        %s
                    }
                }""" % IngestorRun.build_gql_query_object_model(), _json
            )
        )

    def run_hosting_capacity_calibration(
            self,
            calibration_name: str,
            local_calibration_time: datetime,
            feeders: Optional[List[str]] = None,
            transformer_tap_settings: Optional[str] = None,
            generator_config: Optional[GeneratorConfig] = None
    ) -> dict:
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

    async def async_run_hosting_capacity_calibration(
            self,
            calibration_name: str,
            calibration_time_local: datetime,
            feeders: Optional[List[str]] = None,
            transformer_tap_settings: Optional[str] = None,
            generator_config: Optional[GeneratorConfig] = None
    ) -> dict:
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

        return await self._do_post_request(
            self.build_request("""
                mutation runCalibration($calibrationName: String!, $calibrationTimeLocal: LocalDateTime, $feeders: [String!], $generatorConfig: HcGeneratorConfigInput) {
                    runCalibration(calibrationName: $calibrationName, calibrationTimeLocal: $calibrationTimeLocal, feeders: $feeders, generatorConfig: $generatorConfig)
                }""", {
                    "calibrationName": calibration_name,
                    "calibrationTimeLocal": parsed_time.isoformat(),
                    "feeders": feeders,
                    "generatorConfig": generator_config.to_json() if generator_config is not None else None,
                }
            )
        )

    def get_hosting_capacity_calibration_run(self, id_: str) -> dict:
        """
        Retrieve information of a hosting capacity calibration run

        :param id_: The calibration run ID
        :return: The HTTP response received from the Evolve App Server after requesting calibration run info
        """
        return get_event_loop().run_until_complete(self.async_get_hosting_capacity_calibration_run(id_))

    async def async_get_hosting_capacity_calibration_run(self, id_: str) -> dict:
        """
        Retrieve information of a hosting capacity calibration run

        :param id_: The calibration run ID
        :return: The HTTP response received from the Evolve App Server after requesting calibration run info
        """
        return await self._do_post_request(
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

    def get_hosting_capacity_calibration_sets(self) -> dict:
        """
        Retrieve a list of all completed calibration runs initiated through Evolve App Server

        :return: The HTTP response received from the Evolve App Server after requesting completed calibration runs
        """
        return get_event_loop().run_until_complete(self.async_get_hosting_capacity_calibration_sets())

    async def async_get_hosting_capacity_calibration_sets(self) -> dict:
        """
        Retrieve a list of all completed calibration runs initiated through Evolve App Server

        :return: The HTTP response received from the Evolve App Server after requesting completed calibration runs
        """
        return await self._do_post_request(
            self.build_request("""
                query { 
                    getCalibrationSets
                }"""
            )
        )

    def get_transformer_tap_settings(
            self,
            calibration_name: str,
            feeder: Optional[str] = None,
            transformer_mrid: Optional[str] = None
    ) -> dict:
        """
        Retrieve distribution transformer tap settings from a calibration set in the hosting capacity input database.

        :param calibration_name: The (user supplied) name of the calibration run to retrieve transformer tap settings from
        :param feeder: An optional filter to apply to the returned list of transformer tap settings
        :param transformer_mrid: An optional filter to return only the transformer tap settings for a particular transfomer mrid
        :return: The HTTP response received from the Evolve App Server after requesting transformer tap settings for the calibration id
        """
        return get_event_loop().run_until_complete(
            self.async_get_transformer_tap_settings(calibration_name, feeder, transformer_mrid))

    async def async_get_transformer_tap_settings(
            self,
            calibration_name: str,
            feeder: Optional[str] = None,
            transformer_mrid: Optional[str] = None
    ) -> dict:
        """
        Retrieve distribution transformer tap settings from a calibration set in the hosting capacity input database.

        :param calibration_name: The (user supplied) name of the calibration run to retrieve transformer tap settings from
        :param feeder: An optional filter to apply to the returned list of transformer tap settings
        :param transformer_mrid: An optional filter to return only the transformer tap settings for a particular transfomer mrid
        :return: The HTTP response received from the Evolve App Server after requesting transformer tap settings for the calibration id
        """
        return await self._do_post_request(
            self.build_request("""
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
                }""", {
                    "calibrationName": calibration_name,
                    "feeder": feeder,
                   "transformerMrid": transformer_mrid
                }
            )
        )

    def run_opendss_export(self, config: OpenDssConfig) -> dict:
        """
        Send request to run an opendss export

        :param config: The OpenDssConfig for running the export
        :return: The HTTP response received from the Evolve App Server after attempting to run the opendss export
        """
        return get_event_loop().run_until_complete(self.async_run_opendss_export(config))

    async def async_run_opendss_export(self, config: OpenDssConfig) -> dict:
        """
        Send asynchronous request to run an opendss export

        :param config: The OpenDssConfig for running the export
        :return: The HTTP response received from the Evolve App Server after attempting to run the opendss export
        """
        return await self._do_post_request(
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
        query_sort: Optional[GetOpenDssModelsSortCriteriaInput] = None
    ) -> dict:
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

    async def async_get_paged_opendss_models(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        query_filter: Optional[GetOpenDssModelsFilterInput] = None,
        query_sort: Optional[GetOpenDssModelsSortCriteriaInput] = None
    ) -> dict:
        """
        Retrieve a paginated opendss export run information

        :param limit: The number of opendss export runs to retrieve
        :param offset: The number of opendss export runs to skip
        :param query_filter: The filter to apply to the query
        :param query_sort: The sorting to apply to the query
        :return: The HTTP response received from the Evolve App Server after requesting opendss export run information
        """
        _json = {
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
                        generationSpec 
                    }
                }
            }
            """,
            "variables": {}
        }

        if limit is not None:
            _json['variables']['limit'] = limit
        if offset is not None:
            _json['variables']['offset'] = offset
        if query_filter is not None:
            _json['variables']['filter'] = query_filter.to_json()
        if query_sort is not None:
            _json['variables']['sort'] = query_sort.to_json()

        return await self._do_post_request(_json)

    def get_opendss_model_download_url(self, run_id: int) -> dict:
        """
        Retrieve a download url for the specified opendss export run id

        :param run_id: The opendss export run ID
        :return: The HTTP response received from the Evolve App Server after requesting opendss export model download url
        """
        return get_event_loop().run_until_complete(self.async_get_opendss_model_download_url(run_id))

    async def async_get_opendss_model_download_url(self, run_id: int) -> dict:
        """
        Retrieve a download url for the specified opendss export run id

        :param run_id: The opendss export run ID
        :return: The HTTP response received from the Evolve App Server after requesting opendss export model download url
        """
        return await self._do_get_request(run_id=run_id)

    @catch_warnings
    async def _do_post_request(self, _json):
        self._do_request()
        async with self.session.post(
                construct_url(**self._auth.base_url_args, path="/api/graphql"),
                headers=self._get_request_headers(),
                json=_json,
                ssl=self._get_ssl()
        ) as response:
            if response.ok:
                return await response.json()
            else:
                response.raise_for_status()

    @catch_warnings
    async def _do_get_request(self, *, run_id: int):  # TODO: Terrible name probably
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

    async def async_get_opendss_model(self, model_id: int) -> dict:  # TODO: this logic should be hidden behind a generator
        """
        Retrieve information of an OpenDss model export

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
