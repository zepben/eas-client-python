#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import ssl
import warnings
from asyncio import get_event_loop
from hashlib import sha256
from json import dumps
from typing import Optional

import aiohttp
from aiohttp import ClientSession
from urllib3.exceptions import InsecureRequestWarning
from zepben.auth import AuthMethod, ZepbenTokenFetcher, create_token_fetcher, create_token_fetcher_managed_identity

from zepben.eas.client.study import Study
from zepben.eas.client.util import construct_url
from zepben.eas.client.work_package import WorkPackageConfig, FixedTime, TimePeriod

__all__ = ["EasClient"]


class EasClient:
    """
    A class used to represent a client to the Evolve App Server, with methods that represent requests to its API.
    """

    def __init__(
            self,
            host: str,
            port: int,
            protocol: str = "https",
            client_id: Optional[str] = None,
            username: Optional[str] = None,
            password: Optional[str] = None,
            client_secret: Optional[str] = None,
            token_fetcher: Optional[ZepbenTokenFetcher] = None,
            verify_certificate: bool = True,
            ca_filename: Optional[str] = None,
            session: ClientSession = None,
            json_serialiser=None
    ):
        """
        Construct a client for the Evolve App Server. If the server is HTTPS, authentication may be configured.
        Authentication may be configured in one of two ways:
            - Specifying the client ID of the Auth0 application via the client_id parameter, plus one of the following:
                - A username and password pair via the username and password parameters (account authentication)
                - The client secret via the client_secret parameter (M2M authentication)
              If this method is used, the auth configuration will be fetched from the Evolve App Server at the path
              "/api/config/auth".
            - Specifying a ZepbenTokenFetcher directly via the token_fetcher parameter

        Address parameters:
        :param host: The domain of the Evolve App Server, e.g. "evolve.local"
        :param port: The port on which to make requests to the Evolve App Server, e.g. 7624
        :param protocol: The protocol of the Evolve App Server. Should be either "http" or "https". Must be "https" if
                         auth is configured. (Defaults to "https")

        Authentication parameters:
        :param client_id: The Auth0 client ID used to specify to the auth server which application to request a token
                          for. (Optional)
        :param username: The username used for account authentication. (Optional)
        :param password: The password used for account authentication. (Optional)
        :param client_secret: The Auth0 client secret used for M2M authentication. (Optional)
        :param token_fetcher: A ZepbenTokenFetcher used to fetch auth tokens for access to the Evolve App Server.
                              (Optional)

        HTTP/HTTPS parameters:
        :param verify_certificate: Set this to False to disable certificate verification. This will also apply to the
                                   auth provider if auth is initialised via client id + username + password or
                                   client_id + client_secret. (Defaults to True)
        :param ca_filename: Path to CA file to use for verification. (Optional)
        :param session: aiohttp ClientSession to use, if not provided a new session will be created for you. You should
                        typically only use one aiohttp session per application.
        :param json_serialiser: JSON serialiser to use for requests e.g. ujson.dumps. (Defaults to json.dumps)
        """
        self._protocol = protocol
        self._host = host
        self._port = port
        self._verify_certificate = verify_certificate
        self._ca_filename = ca_filename
        if protocol != "https" and (token_fetcher or client_id):
            raise ValueError(
                "Incompatible arguments passed to connect to secured Evolve App Server. "
                "Authentication tokens must be sent via https. "
                "To resolve this issue, exclude the \"protocol\" argument when initialising the EasClient.")

        if token_fetcher and (client_id or client_secret or username or password):
            raise ValueError(
                "Incompatible arguments passed to connect to secured Evolve App Server. "
                "You cannot provide both a token_fetcher and credentials, "
                "please provide either client_id, client_id + client_secret, username + password, or token_fetcher."
            )

        if client_secret and (username or password):
            raise ValueError(
                "Incompatible arguments passed to connect to secured Evolve App Server. "
                "You cannot provide both a client_secret and username/password, "
                "please provide either client_id + client_secret or client_id + username + password."
            )

        if client_id:
            self._token_fetcher = create_token_fetcher(
                conf_address=f"{self._protocol}://{self._host}:{self._port}/api/config/auth",
                verify_conf=self._verify_certificate,
            )
            if self._token_fetcher:
                self._token_fetcher.token_request_data.update({
                    'client_id': client_id,
                    'scope':
                        'trusted' if self._token_fetcher.auth_method is AuthMethod.SELF
                        else 'offline_access openid profile email0'
                })
                self._token_fetcher.refresh_request_data.update({
                    "grant_type": "refresh_token",
                    'client_id': client_id,
                    'scope':
                        'trusted' if self._token_fetcher.auth_method is AuthMethod.SELF
                        else 'offline_access openid profile email0'
                })
                if username and password:
                    self._token_fetcher.token_request_data.update({
                        'grant_type': 'password',
                        'username': username,
                        'password':
                            sha256(password.encode('utf-8')).hexdigest()
                            if self._token_fetcher.auth_method is AuthMethod.SELF
                            else password
                    })
                    if client_secret:
                        self._token_fetcher.token_request_data.update({'client_secret': client_secret})
                elif client_secret:
                    self._token_fetcher.token_request_data.update({
                        'grant_type': 'client_credentials',
                        'client_secret': client_secret
                    })
                else:
                    # Attempt azure managed identity (what a hack)
                    url = "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01"
                    self._token_fetcher = create_token_fetcher_managed_identity(
                        identity_url=f"{url}&resource={client_id}",
                        verify_auth=self._verify_certificate
                    )
        elif token_fetcher:
            self._token_fetcher = token_fetcher
        else:
            self._token_fetcher = None

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
        if self._token_fetcher is None:
            return headers
        else:
            headers["authorization"] = self._token_fetcher.fetch_token()
        return headers

    def run_hosting_capacity_work_package(self, work_package: WorkPackageConfig):
        """
        Send request to hosting capacity service to run work package

        :param work_package: An instance of the `WorkPackageConfig` data class representing the work package configuration for the run
        :return: The HTTP response received from the Evolve App Server after attempting to run work package
        """
        return get_event_loop().run_until_complete(self.async_run_hosting_capacity_work_package(work_package))

    async def async_run_hosting_capacity_work_package(self, work_package: WorkPackageConfig):
        """
        Send asynchronous request to hosting capacity service to run work package

        :param work_package: An instance of the `WorkPackageConfig` data class representing the work package configuration for the run
        :return: The HTTP response received from the Evolve App Server after attempting to run work package
        """
        with warnings.catch_warnings():
            if not self._verify_certificate:
                warnings.filterwarnings("ignore", category=InsecureRequestWarning)
            json = {
                "query": """
                    mutation runWorkPackage($input: WorkPackageInput!, $workPackageName: String!) {
                        runWorkPackage(input: $input, workPackageName: $workPackageName)
                    }
                """,
                "variables": {
                    "workPackageName": work_package.name,
                    "input": {
                        "feeders": work_package.feeders,
                        "years": work_package.years,
                        "scenarios": work_package.scenarios,
                        "fixedTime": work_package.load_time.time.isoformat()
                        if isinstance(work_package.load_time, FixedTime) else None,
                        "timePeriod": {
                            "startTime": work_package.load_time.start_time.isoformat(),
                            "endTime": work_package.load_time.end_time.isoformat(),
                        } if isinstance(work_package.load_time, TimePeriod) else None,
                        "qualityAssuranceProcessing": work_package.quality_assurance_processing,
                        "generatorConfig": {
                            "model": {
                                "vmPu": work_package.generator_config.model.vm_pu,
                                "vMinPu": work_package.generator_config.model.vmin_pu,
                                "vMaxPu": work_package.generator_config.model.vmax_pu,
                                "loadModel": work_package.generator_config.model.load_model,
                                "collapseSWER": work_package.generator_config.model.collapse_swer,
                                "calibration": work_package.generator_config.model.calibration,
                                "pFactorBaseExports": work_package.generator_config.model.p_factor_base_exports,
                                "pFactorForecastPv": work_package.generator_config.model.p_factor_forecast_pv,
                                "pFactorBaseImports": work_package.generator_config.model.p_factor_base_imports,
                                "fixSinglePhaseLoads": work_package.generator_config.model.fix_single_phase_loads,
                                "maxSinglePhaseLoad": work_package.generator_config.model.max_single_phase_load,
                                "fixOverloadingConsumers": work_package.generator_config.model.fix_overloading_consumers,
                                "maxLoadTxRatio": work_package.generator_config.model.max_load_tx_ratio,
                                "maxGenTxRatio": work_package.generator_config.model.max_gen_tx_ratio,
                                "fixUndersizedServiceLines": work_package.generator_config.model.fix_undersized_service_lines,
                                "maxLoadServiceLineRatio": work_package.generator_config.model.max_load_service_line_ratio,
                                "maxLoadLvLineRatio": work_package.generator_config.model.max_load_lv_line_ratio,
                                "collapseLvNetworks": work_package.generator_config.model.collapse_lv_networks,
                                "feederScenarioAllocationStrategy": work_package.generator_config.model.feeder_scenario_allocation_strategy.name if work_package.generator_config.model.feeder_scenario_allocation_strategy is not None else None,
                                "closedLoopVRegEnabled": work_package.generator_config.model.closed_loop_v_reg_enabled,
                                "closedLoopVRegReplaceAll": work_package.generator_config.model.closed_loop_v_reg_replace_all,
                                "closedLoopVRegSetPoint": work_package.generator_config.model.closed_loop_v_reg_set_point,
                                "closedLoopVBand": work_package.generator_config.model.closed_loop_v_band,
                                "closedLoopTimeDelay": work_package.generator_config.model.closed_loop_time_delay,
                                "closedLoopVLimit": work_package.generator_config.model.closed_loop_v_limit,
                                "defaultTapChangerTimeDelay": work_package.generator_config.model.default_tap_changer_time_delay,
                                "defaultTapChangerSetPointPu": work_package.generator_config.model.default_tap_changer_set_point_pu,
                                "defaultTapChangerBand": work_package.generator_config.model.default_tap_changer_band,
                                "splitPhaseDefaultLoadLossPercentage": work_package.generator_config.model.split_phase_default_load_loss_percentage,
                                "splitPhaseLVKV": work_package.generator_config.model.split_phase_lv_kv,
                                "swerVoltageToLineVoltage": work_package.generator_config.model.swer_voltage_to_line_voltage,
                                "loadPlacement": work_package.generator_config.model.load_placement.name if work_package.generator_config.model.load_placement is not None else None,
                                "loadIntervalLengthHours": work_package.generator_config.model.load_interval_length_hours,
                                "meterPlacementConfig": {
                                    "feederHead": work_package.generator_config.model.meter_placement_config.feeder_head,
                                    "distTransformers": work_package.generator_config.model.meter_placement_config.dist_transformers,
                                    "switchMeterPlacementConfigs": [{
                                        "meterSwitchClass": spc.meter_switch_class.name if spc.meter_switch_class is not None else None,
                                        "namePattern": spc.name_pattern
                                    } for spc in
                                        work_package.generator_config.model.meter_placement_config.switch_meter_placement_configs] if work_package.generator_config.model.meter_placement_config.switch_meter_placement_configs is not None else None,
                                    "energyConsumerMeterGroup": work_package.generator_config.model.meter_placement_config.energy_consumer_meter_group
                                } if work_package.generator_config.model.meter_placement_config is not None else None
                            } if work_package.generator_config.model is not None else None,
                            "solve": {
                                "normVMinPu": work_package.generator_config.solve.norm_vmin_pu,
                                "normVMaxPu": work_package.generator_config.solve.norm_vmax_pu,
                                "emergVMinPu": work_package.generator_config.solve.emerg_vmin_pu,
                                "emergVMaxPu": work_package.generator_config.solve.emerg_vmax_pu,
                                "baseFrequency": work_package.generator_config.solve.base_frequency,
                                "voltageBases": work_package.generator_config.solve.voltage_bases,
                                "maxIter": work_package.generator_config.solve.max_iter,
                                "maxControlIter": work_package.generator_config.solve.max_control_iter,
                                "mode": work_package.generator_config.solve.mode.name if work_package.generator_config.solve.mode is not None else None,
                                "stepSizeMinutes": work_package.generator_config.solve.step_size_minutes
                            } if work_package.generator_config.solve is not None else None,
                            "rawResults": {
                                "energyMeterVoltagesRaw": work_package.generator_config.raw_results.energy_meter_voltages_raw,
                                "energyMetersRaw": work_package.generator_config.raw_results.energy_meters_raw,
                                "resultsPerMeter": work_package.generator_config.raw_results.results_per_meter,
                                "overloadsRaw": work_package.generator_config.raw_results.overloads_raw,
                                "voltageExceptionsRaw": work_package.generator_config.raw_results.voltage_exceptions_raw
                            } if work_package.generator_config.raw_results is not None else None
                        } if work_package.generator_config is not None else None,
                        "executorConfig": {},
                        "resultProcessorConfig": {
                            "storedResults": {
                                "energyMeterVoltagesRaw": work_package.result_processor_config.stored_results.energy_meter_voltages_raw,
                                "energyMetersRaw": work_package.result_processor_config.stored_results.energy_meters_raw,
                                "overloadsRaw": work_package.result_processor_config.stored_results.overloads_raw,
                                "voltageExceptionsRaw": work_package.result_processor_config.stored_results.voltage_exceptions_raw,
                            } if work_package.result_processor_config.stored_results is not None else None,
                            "metrics": {
                                "calculatePerformanceMetrics": work_package.result_processor_config.metrics.calculate_performance_metrics
                            } if work_package.result_processor_config.metrics is not None else None,
                            "writerConfig": {
                                "writerType": work_package.result_processor_config.writer_config.writer_type.name if work_package.result_processor_config.writer_config.writer_type is not None else None,
                                "outputWriterConfig": {
                                    "enhancedMetricsConfig": {
                                        "populateEnhancedMetrics": work_package.result_processor_config.writer_config.output_writer_config.enhanced_metrics_config.populate_enhanced_metrics,
                                        "populateEnhancedMetricsProfile": work_package.result_processor_config.writer_config.output_writer_config.enhanced_metrics_config.populate_enhanced_metrics_profile,
                                        "populateDurationCurves": work_package.result_processor_config.writer_config.output_writer_config.enhanced_metrics_config.populate_duration_curves,
                                        "populateConstraints": work_package.result_processor_config.writer_config.output_writer_config.enhanced_metrics_config.populate_constraints,
                                        "populateWeeklyReports": work_package.result_processor_config.writer_config.output_writer_config.enhanced_metrics_config.populate_weekly_reports,
                                        "calculateNormalForLoadThermal": work_package.result_processor_config.writer_config.output_writer_config.enhanced_metrics_config.calculate_normal_for_load_thermal,
                                        "calculateEmergForLoadThermal": work_package.result_processor_config.writer_config.output_writer_config.enhanced_metrics_config.calculate_emerg_for_load_thermal,
                                        "calculateNormalForGenThermal": work_package.result_processor_config.writer_config.output_writer_config.enhanced_metrics_config.calculate_normal_for_gen_thermal,
                                        "calculateEmergForGenThermal": work_package.result_processor_config.writer_config.output_writer_config.enhanced_metrics_config.calculate_emerg_for_gen_thermal,
                                        "calculateCO2": work_package.result_processor_config.writer_config.output_writer_config.enhanced_metrics_config.calculate_co2
                                    } if work_package.result_processor_config.writer_config.output_writer_config.enhanced_metrics_config is not None else None
                                } if work_package.result_processor_config.writer_config.output_writer_config is not None else None
                            } if work_package.result_processor_config.writer_config is not None else None
                        } if work_package.result_processor_config is not None else None
                    }
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
                    response = await response.json()
                else:
                    response = await response.text()
                return response

    def cancel_hosting_capacity_work_package(self, work_package_id: str):
        """
        Send request to hosting capacity service to cancel a running work package

        :param work_package_id: The id of the running work package to cancel
        :return: The HTTP response received from the Evolve App Server after attempting to cancel work package
        """
        return get_event_loop().run_until_complete(self.async_cancel_hosting_capacity_work_package(work_package_id))

    async def async_cancel_hosting_capacity_work_package(self, work_package_id: str):
        """
        Send asynchronous request to hosting capacity service to cancel a running work package

        :param work_package_id: The id of the running work package to cancel
        :return: The HTTP response received from the Evolve App Server after attempting to cancel work package
        """
        with warnings.catch_warnings():
            if not self._verify_certificate:
                warnings.filterwarnings("ignore", category=InsecureRequestWarning)
            json = {
                "query": """
                    mutation cancelWorkPackage($workPackageId: ID!) {
                        cancelWorkPackage(workPackageId: $workPackageId)
                    }
                """,
                "variables": {"workPackageId": work_package_id}
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
                    response = await response.json()
                else:
                    response = await response.text()
                return response

    def get_hosting_capacity_work_packages_progress(self):
        """
        Retrieve running work packages progress information from hosting capacity service

        :return: The HTTP response received from the Evolve App Server after requesting work packages progress info
        """
        return get_event_loop().run_until_complete(self.async_get_hosting_capacity_work_packages_progress())

    async def async_get_hosting_capacity_work_packages_progress(self):
        """
        Asynchronously retrieve running work packages progress information from hosting capacity service

        :return: The HTTP response received from the Evolve App Server after requesting work packages progress info
        """
        with warnings.catch_warnings():
            if not self._verify_certificate:
                warnings.filterwarnings("ignore", category=InsecureRequestWarning)
            json = {
                "query": """
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
                    }
                """,
                "variables": {}
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
                    response = await response.json()
                else:
                    response = await response.text()
                return response

    def upload_study(self, study: Study):
        """
        Uploads a new study to the Evolve App Server
        :param study: An instance of a data class representing a new study
        """
        return get_event_loop().run_until_complete(self.async_upload_study(study))

    async def async_upload_study(self, study: Study):
        """
        Uploads a new study to the Evolve App Server
        :param study: An instance of a data class representing a new study
        :return: The HTTP response received from the Evolve App Server after attempting to upload the study
        """
        with warnings.catch_warnings():
            if not self._verify_certificate:
                warnings.filterwarnings("ignore", category=InsecureRequestWarning)
            json = {
                "query": """
                    mutation uploadStudy($study: StudyInput!) {
                        addStudies(studies: [$study])
                    }
                """,
                "variables": {
                    "study": {
                        "name": study.name,
                        "description": study.description,
                        "tags": study.tags,
                        "styles": study.styles,
                        "results": [{
                            "name": result.name,
                            "geoJsonOverlay": {
                                "data": result.geo_json_overlay.data,
                                "sourceProperties": result.geo_json_overlay.source_properties,
                                "styles": result.geo_json_overlay.styles
                            } if result.geo_json_overlay else None,
                            "stateOverlay": {
                                "data": result.state_overlay.data,
                                "styles": result.state_overlay.styles
                            } if result.state_overlay else None,
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
                    response = await response.json()
                else:
                    response = await response.text()
                return response
