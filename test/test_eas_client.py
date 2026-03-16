#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import random
import ssl
import string
from datetime import datetime
from http import HTTPStatus

import httpx
import pytest
import trustme
from pytest_httpserver import HTTPServer
from werkzeug import Response

from zepben.eas import EasClient
from zepben.eas.client.enums import OpenDssModelState
from zepben.eas.lib.generated_graphql_client import WorkPackageInput, ForecastConfigInput, TimePeriodInput, \
    FeederConfigInput, FeederConfigsInput, FixedTimeInput, FixedTimeLoadOverrideInput, TimePeriodLoadOverrideInput, \
    StudyInput, StudyResultInput, InterventionConfigInput, YearRangeInput, InterventionClass, \
    CandidateGenerationConfigInput, CandidateGenerationType, HcGeneratorConfigInput, HcModelConfigInput, \
    HcSolveConfigInput, GetOpenDssModelsFilterInput, GetOpenDssModelsSortCriteriaInput, SortOrder, IngestorConfigInput, \
    IngestorRunsFilterInput, IngestorRunState, IngestorRuntimeKind, IngestorRunsSortCriteriaInput, OpenDssModelInput, \
    OpenDssModelGenerationSpecInput, OpenDssModelOptionsInput, OpenDssModulesConfigInput, OpenDssCommonConfigInput, \
    HcFeederScenarioAllocationStrategy, HcLoadPlacement, HcMeterPlacementConfigInput, HcSwitchMeterPlacementConfigInput, \
    HcSwitchClass, HcInverterControlConfigInput, HcSolveMode, HcRawResultsConfigInput, HcNodeLevelResultsConfigInput

mock_host = ''.join(random.choices(string.ascii_lowercase, k=10))
mock_port = random.randrange(1024)
mock_client_id = ''.join(random.choices(string.ascii_lowercase, k=10))
mock_client_secret = ''.join(random.choices(string.ascii_lowercase, k=10))
mock_username = ''.join(random.choices(string.ascii_lowercase, k=10))
mock_password = ''.join(random.choices(string.ascii_lowercase, k=10))
mock_protocol = ''.join(random.choices(string.ascii_lowercase, k=10))
mock_access_token = ''.join(random.choices(string.ascii_lowercase, k=10))
mock_verify_certificate = bool(random.getrandbits(1))

mock_audience = ''.join(random.choices(string.ascii_lowercase, k=10))

LOCALHOST = "127.0.0.1"


class MockResponse:
    def __init__(self, json_data, status_code, reason="", text=""):
        self.json_data = json_data
        self.status_code = status_code
        self.ok = status_code < 400
        self.reason = reason
        self.text = text

    def json(self):
        if not self.json_data:
            raise ValueError()
        return self.json_data


def test_create_eas_client_success():
    eas_client = EasClient(
        host=mock_host,
        port=mock_port,
        protocol=mock_protocol,
        verify_certificate=mock_verify_certificate
    )

    assert eas_client is not None
    assert eas_client._host == mock_host
    assert eas_client._port == mock_port
    assert eas_client._protocol == mock_protocol


def test_get_request_headers_adds_access_token_in_auth_header():
    eas_client = EasClient(
        host=mock_host,
        port=mock_port,
        access_token=mock_access_token,
    )

    headers = eas_client.http_client.headers
    assert headers["authorization"] == f"Bearer {mock_access_token}"


@pytest.fixture(scope="session")
def ca():
    return trustme.CA()


@pytest.fixture(scope="session")
def localhost_cert(ca):
    return ca.issue_cert(LOCALHOST)


@pytest.fixture(scope="session")
def httpserver_ssl_context(localhost_cert):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    crt = localhost_cert.cert_chain_pems[0]
    key = localhost_cert.private_key_pem
    with crt.tempfile() as crt_file, key.tempfile() as key_file:
        context.load_cert_chain(crt_file, key_file)

    return context


def test_get_work_package_cost_estimation_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
        {"data": {"getWorkPackageCostEstimation": "123.45"}})
    res = eas_client.get_work_package_cost_estimation(
        WorkPackageInput(
            #"wp_name",
            forecastConfig=ForecastConfigInput(
                feeders=["feeder"],
                years=[1],
                scenarios=["scenario"],
                timePeriod=TimePeriodInput(
                    startTime=datetime(2022, 1, 1, 10),
                    endTime=datetime(2022, 1, 2, 12),
                    overrides=None
                )
            )
        )
    )
    httpserver.check_assertions()
    assert res == {"data": {"getWorkPackageCostEstimation": "123.45"}}


def test_get_work_package_cost_estimation_invalid_certificate_failure(httpserver: HTTPServer):
    eas_client = _invalid_ca(httpserver.port)

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
        {"data": {"getWorkPackageCostEstimation": "123.45"}})
    with pytest.raises(httpx.ConnectError):
        eas_client.get_work_package_cost_estimation(
            WorkPackageInput(
                forecastConfig=ForecastConfigInput(
                    feeders=["feeder"],
                    years=[1],
                    scenarios=["scenario"],
                    timePeriod=TimePeriodInput(
                        startTime=datetime(2022, 1, 1, 10),
                        endTime=datetime(2022, 1, 2, 12),
                        overrides=None
                    )
                )
            )
        )


def test_get_work_package_cost_estimation_valid_certificate_success(httpserver: HTTPServer, ca: trustme.CA):
    eas_client = _valid_ca(httpserver.port, ca)

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
        {"data": {"getWorkPackageCostEstimation": "123.45"}})
    res = eas_client.get_work_package_cost_estimation(
        WorkPackageInput(
            feederConfigs=FeederConfigsInput(
                configs=[
                    FeederConfigInput(
                        feeder="feeder",
                        years=[1],
                        scenarios=["scenario"],
                        fixedTime=FixedTimeInput(
                            loadTime=datetime(2022, 1, 1),
                            overrides=[
                                FixedTimeLoadOverrideInput(
                                    loadId="meter",
                                    genVarOverride=[1],
                                    genWattsOverride=[2],
                                    loadVarOverride=[3],
                                    loadWattsOverride=[4]
                                )
                            ]
                        )
                    )
                ]
            )
        )
    )

    httpserver.check_assertions()
    assert res == {"data": {"getWorkPackageCostEstimation": "123.45"}}


def test_run_hosting_capacity_work_package_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json({"data": {"runWorkPackage": "workPackageId"}})
    res = eas_client.run_hosting_capacity_work_package(
        WorkPackageInput(
            forecastConfig=ForecastConfigInput(
                feeders=["feeder"],
                years=[1],
                scenarios=["scenario"],
                timePeriod=TimePeriodInput(
                    startTime=datetime(2022, 1, 1),
                    endTime=datetime(2022, 1, 2),
                    overrides=None
                )
            )
        ), work_package_name="wp_name",
    )
    httpserver.check_assertions()
    assert res == {"data": {"runWorkPackage": "workPackageId"}}


def test_run_hosting_capacity_work_package_invalid_certificate_failure(httpserver: HTTPServer):
    eas_client = _invalid_ca(httpserver.port)

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
        {"data": {"runWorkPackage": "workPackageId"}})
    with pytest.raises(httpx.ConnectError):
        eas_client.run_hosting_capacity_work_package(
            WorkPackageInput(
                forecastConfig=ForecastConfigInput(
                    feeders=["feeder"],
                    years=[1],
                    scenarios=["scenario"],
                    timePeriod=TimePeriodInput(
                        startTime=datetime(2022, 1, 1),
                        endTime=datetime(2022, 1, 2),
                        overrides=None
                    )
                )
            ), work_package_name="wp_name",
        )


def test_run_hosting_capacity_work_package_valid_certificate_success(httpserver: HTTPServer, ca: trustme.CA):
    eas_client = _valid_ca(httpserver.port, ca)

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
        {"data": {"runWorkPackage": "workPackageId"}})
    res = eas_client.run_hosting_capacity_work_package(
        WorkPackageInput(
            forecastConfig=ForecastConfigInput(
                feeders=["feeder"],
                years=[1],
                scenarios=["scenario"],
                timePeriod=TimePeriodInput(
                    startTime=datetime(2022, 1, 1),
                    endTime=datetime(2022, 1, 2),
                    overrides=[
                        TimePeriodLoadOverrideInput(
                            loadId="meter1",
                            loadWattsOverride=[1.0],
                            genWattsOverride=[2.0],
                            loadVarOverride=[3.0],
                            genVarOverride=[4.0]
                        )
                    ]
                )
            )
        ), work_package_name="wp_name",
    )
    httpserver.check_assertions()
    assert res == {"data": {"runWorkPackage": "workPackageId"}}


def test_cancel_hosting_capacity_work_package_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
        {"data": {"cancelHostingCapacity": "workPackageId"}}
    )
    res = eas_client.cancel_hosting_capacity_work_package(work_package_id="workPackageId")
    httpserver.check_assertions()
    assert res == {"data": {"cancelHostingCapacity": "workPackageId"}}


def test_cancel_hosting_capacity_work_package_invalid_certificate_failure(httpserver: HTTPServer):
    eas_client = _invalid_ca(httpserver.port)

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
        {"data": {"cancelWorkPackage": "workPackageId"}})
    with pytest.raises(httpx.ConnectError):
        eas_client.cancel_hosting_capacity_work_package("workPackageId")


def test_cancel_hosting_capacity_work_package_valid_certificate_success(httpserver: HTTPServer, ca: trustme.CA):
    eas_client = _valid_ca(httpserver.port, ca)

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
        {"data": {"cancelWorkPackage": "workPackageId"}})
    res = eas_client.cancel_hosting_capacity_work_package("workPackageId")
    httpserver.check_assertions()
    assert res == {"data": {"cancelWorkPackage": "workPackageId"}}


def test_get_hosting_capacity_work_package_progress_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
        {"data": {"getWorkPackageProgress": {}}}
    )
    res = eas_client.get_hosting_capacity_work_packages_progress()
    httpserver.check_assertions()
    assert res == {"data": {"getWorkPackageProgress": {}}}


def test_get_hosting_capacity_work_package_progress_invalid_certificate_failure(httpserver: HTTPServer):
    eas_client = _invalid_ca(httpserver.port)

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
        {"data": {"getWorkPackageProgress": {}}})
    with pytest.raises(httpx.ConnectError):
        eas_client.get_hosting_capacity_work_packages_progress()


def test_get_hosting_capacity_work_package_progress_valid_certificate_success(httpserver: HTTPServer, ca: trustme.CA):
    eas_client = _valid_ca(httpserver.port, ca)

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
        {"data": {"getWorkPackageProgress": {}}})
    res = eas_client.get_hosting_capacity_work_packages_progress()
    httpserver.check_assertions()
    assert res == {"data": {"getWorkPackageProgress": {}}}


def test_upload_study_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json({"result": "success"})
    res = eas_client.upload_study(
        StudyInput(
            name="Test study",
            description="description",
            tags=["tag"],
            results=[StudyResultInput(name="Huge success", sections=[])],
            styles=[]
        )
    )
    httpserver.check_assertions()
    assert res == {"result": "success"}


def test_upload_study_invalid_certificate_failure(httpserver: HTTPServer):
    eas_client = _invalid_ca(httpserver.port)

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json({"result": "success"})
    with pytest.raises(httpx.ConnectError):
        eas_client.upload_study(StudyInput(name="Test study", description="description", tags=["tag"], results=[StudyResultInput(name="Huge success", sections=[])], styles=[]))


def test_upload_study_valid_certificate_success(httpserver: HTTPServer, ca: trustme.CA):
    eas_client = _valid_ca(httpserver.port, ca)

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json({"result": "success"})
    res = eas_client.upload_study(StudyInput(name="Test study", description="description", tags=["tag"], results=[StudyResultInput(name="Huge success", sections=[])], styles=[]))
    httpserver.check_assertions()
    assert res == {"result": "success"}


def hosting_capacity_run_calibration_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == "mutation runCalibration($calibrationName_0: String!, $calibrationTimeLocal_0: LocalDateTime) { runCalibration( calibrationName: $calibrationName_0 calibrationTimeLocal: $calibrationTimeLocal_0 ) }"
    assert actual_body['variables'] == {"calibrationName_0": "TEST CALIBRATION",
                                        "calibrationTimeLocal_0": datetime(2025, month=7, day=12).isoformat(),
                                        }

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_run_hosting_capacity_calibration_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        hosting_capacity_run_calibration_request_handler)
    res = eas_client.run_hosting_capacity_calibration("TEST CALIBRATION", datetime(2025, month=7, day=12))
    httpserver.check_assertions()
    assert res == {"result": "success"}


def test_run_hosting_capacity_calibration_invalid_certificate_failure(httpserver: HTTPServer):
    eas_client = _invalid_ca(httpserver.port)

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json({"result": "success"})
    with pytest.raises(httpx.ConnectError):
        eas_client.run_hosting_capacity_calibration("TEST CALIBRATION", datetime(2025, month=7, day=12))


def test_run_hosting_capacity_calibration_valid_certificate_success(httpserver: HTTPServer, ca: trustme.CA):
    eas_client = _valid_ca(httpserver.port, ca)

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        hosting_capacity_run_calibration_request_handler)
    res = eas_client.run_hosting_capacity_calibration("TEST CALIBRATION", datetime(2025, month=7, day=12))
    httpserver.check_assertions()
    assert res == {"result": "success"}


def get_hosting_capacity_run_calibration_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == ("query getCalibrationRun($id_0: ID!) { getCalibrationRun(id: $id_0) { id name "
                     "workflowId runId calibrationTimeLocal startAt completedAt status feeders "
                     "calibrationWorkPackageConfig } }")
    assert actual_body['variables'] == {"id_0": "calibration-id"}

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_get_hosting_capacity_calibration_run_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        get_hosting_capacity_run_calibration_request_handler)
    res = eas_client.get_hosting_capacity_calibration_run("calibration-id")
    httpserver.check_assertions()
    assert res == {"result": "success"}


def test_get_hosting_capacity_calibration_run_invalid_certificate_failure(httpserver: HTTPServer):
    eas_client = _invalid_ca(httpserver.port)

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json({"result": "success"})
    with pytest.raises(httpx.ConnectError):
        eas_client.get_hosting_capacity_calibration_run("calibration-id")


def test_get_hosting_capacity_calibration_run_valid_certificate_success(httpserver: HTTPServer, ca: trustme.CA):
    eas_client = _valid_ca(httpserver.port, ca)

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        get_hosting_capacity_run_calibration_request_handler)
    res = eas_client.get_hosting_capacity_calibration_run("calibration-id")
    httpserver.check_assertions()
    assert res == {"result": "success"}


def hosting_capacity_run_calibration_with_calibration_time_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == "mutation runCalibration($calibrationName_0: String!, $calibrationTimeLocal_0: LocalDateTime, $feeders_0: [String!], $generatorConfig_0: HcGeneratorConfigInput) { runCalibration( calibrationName: $calibrationName_0 calibrationTimeLocal: $calibrationTimeLocal_0 feeders: $feeders_0 generatorConfig: $generatorConfig_0 ) }"
    assert actual_body['variables'] == {"calibrationName_0": "TEST CALIBRATION",
                                        "calibrationTimeLocal_0": datetime(1902, month=1, day=28, hour=0, minute=0,
                                                                         second=20).isoformat(),
                                        "feeders_0": ["one", "two"],
                                        "generatorConfig_0": {
                                            'model': {
                                                'transformerTapSettings': 'test_tap_settings'
                                            },
                                        }
                                    }

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_run_hosting_capacity_calibration_with_calibration_time_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        hosting_capacity_run_calibration_with_calibration_time_request_handler)
    res = eas_client.run_hosting_capacity_calibration("TEST CALIBRATION",
                                                      datetime(1902, month=1, day=28, hour=0, minute=0, second=20),
                                                      ["one", "two"],
                                                      generator_config=HcGeneratorConfigInput(model=HcModelConfigInput(
                                                          transformerTapSettings="test_tap_settings"
                                                      ))
                                                      )
    httpserver.check_assertions()
    assert res == {"result": "success"}


def test_run_hosting_capacity_calibration_with_explicit_transformer_tap_settings_no_generator_config(
        httpserver: HTTPServer
):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        hosting_capacity_run_calibration_with_calibration_time_request_handler)
    res = eas_client.run_hosting_capacity_calibration("TEST CALIBRATION",
                                                      datetime(1902, month=1, day=28, hour=0, minute=0, second=20),
                                                      ["one", "two"],
                                                      transformer_tap_settings="test_tap_settings"
                                                      )
    httpserver.check_assertions()
    assert res == {"result": "success"}


def hosting_capacity_run_calibration_with_generator_config_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == "mutation runCalibration($calibrationName_0: String!, $calibrationTimeLocal_0: LocalDateTime, $feeders_0: [String!], $generatorConfig_0: HcGeneratorConfigInput) { runCalibration( calibrationName: $calibrationName_0 calibrationTimeLocal: $calibrationTimeLocal_0 feeders: $feeders_0 generatorConfig: $generatorConfig_0 ) }"
    assert actual_body['variables'] == {"calibrationName_0": "TEST CALIBRATION",
                                        "calibrationTimeLocal_0": datetime(1902, month=1, day=28, hour=0, minute=0,
                                                                         second=20).isoformat(),
                                        "feeders_0": ["one", "two"],
                                        "generatorConfig_0": {
                                            'model': {
                                                'transformerTapSettings': 'test_tap_settings',
                                            },
                                            'solve': {
                                                'normVMaxPu': 23.9,
                                            }
                                        }
                                        }

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_run_hosting_capacity_calibration_with_explicit_transformer_tap_settings_partial_generator_config(
        httpserver: HTTPServer
):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        hosting_capacity_run_calibration_with_generator_config_request_handler)
    res = eas_client.run_hosting_capacity_calibration("TEST CALIBRATION",
                                                      datetime(1902, month=1, day=28, hour=0, minute=0, second=20),
                                                      ["one", "two"],
                                                      transformer_tap_settings="test_tap_settings",
                                                      generator_config=HcGeneratorConfigInput(
                                                          solve=HcSolveConfigInput(normVMaxPu=23.9))
                                                      )
    httpserver.check_assertions()
    assert res == {"result": "success"}


def hosting_capacity_run_calibration_with_partial_model_config_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == "mutation runCalibration($calibrationName_0: String!, $calibrationTimeLocal_0: LocalDateTime, $feeders_0: [String!], $generatorConfig_0: HcGeneratorConfigInput) { runCalibration( calibrationName: $calibrationName_0 calibrationTimeLocal: $calibrationTimeLocal_0 feeders: $feeders_0 generatorConfig: $generatorConfig_0 ) }"
    assert actual_body['variables'] == {"calibrationName_0": "TEST CALIBRATION",
                                        "calibrationTimeLocal_0": datetime(1902, month=1, day=28, hour=0, minute=0,
                                                                         second=20).isoformat(),
                                        "feeders_0": ["one", "two"],
                                        "generatorConfig_0": {
                                            'model': {
                                                'transformerTapSettings': 'test_tap_settings',
                                                'vmPu': 123.4
                                            },
                                        }
                                        }

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_run_hosting_capacity_calibration_with_explicit_transformer_tap_settings_partial_model_config(
        httpserver: HTTPServer
):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        hosting_capacity_run_calibration_with_partial_model_config_request_handler)
    res = eas_client.run_hosting_capacity_calibration("TEST CALIBRATION",
                                                      datetime(1902, month=1, day=28, hour=0, minute=0, second=20),
                                                      ["one", "two"],
                                                      transformer_tap_settings="test_tap_settings",
                                                      generator_config=HcGeneratorConfigInput(model=HcModelConfigInput(vmPu=123.4))
                                                      )
    httpserver.check_assertions()
    assert res == {"result": "success"}


def test_run_hosting_capacity_calibration_with_explicit_transformer_tap_settings(httpserver: HTTPServer):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        hosting_capacity_run_calibration_with_calibration_time_request_handler)
    res = eas_client.run_hosting_capacity_calibration("TEST CALIBRATION",
                                                      datetime(1902, month=1, day=28, hour=0, minute=0, second=20),
                                                      ["one", "two"],
                                                      transformer_tap_settings="test_tap_settings",
                                                      generator_config=HcGeneratorConfigInput(model=HcModelConfigInput(
                                                          transformerTapSettings="this_should_be_over_written"
                                                      ))
                                                      )
    httpserver.check_assertions()
    assert res == {"result": "success"}


def get_hosting_capacity_calibration_sets_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = actual_body['query'].replace('\n', '')

    assert query == "query getCalibrationSets {  getCalibrationSets}"

    return Response(json.dumps(["one", "two", "three"]), status=200, content_type="application/json")


def test_get_hosting_capacity_calibration_sets_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        get_hosting_capacity_calibration_sets_request_handler)
    res = eas_client.get_hosting_capacity_calibration_sets()
    httpserver.check_assertions()
    assert res == ["one", "two", "three"]


def run_opendss_export_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == "mutation createOpenDssModel($input_0: OpenDssModelInput!) { createOpenDssModel(input: $input_0) }"
    assert actual_body['variables'] == {
        "input_0": {
            "modelName": "TEST OPENDSS MODEL 1",
            "isPublic": True,
            "generationSpec": {
                "modelOptions": {
                    "feeder": "feeder1",
                    "scenario": "scenario1",
                    "year": 2024
                },
                "modulesConfiguration": {
                    "common": {
                        "fixedTime": {
                            "loadTime": "2022-04-01T00:00:00",
                            "overrides": [{
                                'loadId': 'meter1',
                                'loadWattsOverride': [4.0],
                                'genWattsOverride': [2.0],
                                'loadVarOverride': [3.0],
                                'genVarOverride': [1.0]
                            }]
                        },
                        "timePeriod": {
                               "startTime": "2022-04-01T10:13:00",
                               "endTime": "2023-04-01T12:14:00",
                               "overrides": [{
                                   'loadId': 'meter1',
                                   'loadWattsOverride': [4.0],
                                   'genWattsOverride': [2.0],
                                   'loadVarOverride': [3.0],
                                   'genVarOverride': [1.0]
                           }]
                        }
                    },
                    "generator": {
                        "model": {
                            "vmPu": 1.0,
                            "loadVMinPu": 0.80,
                            "loadVMaxPu": 1.15,
                            "genVMinPu": 0.50,
                            "genVMaxPu": 2.00,
                            "loadModel": 1,
                            "collapseSWER": False,
                            "calibration": False,
                            "pFactorBaseExports": 0.95,
                            "pFactorBaseImports": 0.90,
                            "pFactorForecastPv": 1.0,
                            "fixSinglePhaseLoads": True,
                            "maxSinglePhaseLoad": 30000.0,
                            "fixOverloadingConsumers": True,
                            "maxLoadTxRatio": 3.0,
                            "maxGenTxRatio": 10.0,
                            "fixUndersizedServiceLines": True,
                            "maxLoadServiceLineRatio": 1.5,
                            "maxLoadLvLineRatio": 2.0,
                            "simplifyNetwork": False,
                            "collapseLvNetworks": False,
                            "collapseNegligibleImpedances": False,
                            "combineCommonImpedances": False,
                            "feederScenarioAllocationStrategy": "ADDITIVE",
                            "closedLoopVRegEnabled": True,
                            "closedLoopVRegReplaceAll": True,
                            "closedLoopVRegSetPoint": 0.985,
                            "closedLoopVBand": 2.0,
                            "closedLoopTimeDelay": 100,
                            "closedLoopVLimit": 1.1,
                            "defaultTapChangerTimeDelay": 100,
                            "defaultTapChangerSetPointPu": 1.0,
                            "defaultTapChangerBand": 2.0,
                            "splitPhaseDefaultLoadLossPercentage": 0.4,
                            "splitPhaseLVKV": 0.25,
                            "swerVoltageToLineVoltage": [
                                [230, 400],
                                [240, 415],
                                [250, 433],
                                [6350, 11000],
                                [6400, 11000],
                                [12700, 22000],
                                [19100, 33000]
                            ],
                            "loadPlacement": "PER_USAGE_POINT",
                            "loadIntervalLengthHours": 0.5,
                            "meterPlacementConfig": {
                                "feederHead": True,
                                "distTransformers": True,
                                "switchMeterPlacementConfigs": [
                                    {
                                        "meterSwitchClass": "LOAD_BREAK_SWITCH",
                                        "namePattern": ".*"
                                    }
                                ],
                                "energyConsumerMeterGroup": "meter group 1"
                            },
                            "seed": 42,
                            "defaultLoadWatts": [100.0, 200.0, 300.0],
                            "defaultGenWatts": [50.0, 150.0, 250.0],
                            "defaultLoadVar": [10.0, 20.0, 30.0],
                            "defaultGenVar": [5.0, 15.0, 25.0],
                            "transformerTapSettings": "tap-3",
                            "ctPrimScalingFactor": 2.0,
                            "useSpanLevelThreshold": True,
                            "ratingThreshold": 20.0,
                            "simplifyPLSIThreshold": 20.0,
                            "emergAmpScaling": 1.8,
                            'inverterControlConfig': {
                                'afterCutOffProfile': 'afterProfile',
                                'beforeCutOffProfile': 'beforeProfile',
                                'cutOffDate': '2024-04-12T11:42:00'
                            },
                        },
                        "solve": {
                            "normVMinPu": 0.9,
                            "normVMaxPu": 1.054,
                            "emergVMinPu": 0.8,
                            "emergVMaxPu": 1.1,
                            "baseFrequency": 50,
                            "voltageBases": [0.4, 0.433, 6.6, 11.0, 22.0, 33.0, 66.0, 132.0],
                            "maxIter": 25,
                            "maxControlIter": 20,
                            "mode": "YEARLY",
                            "stepSizeMinutes": 60
                        },
                        "rawResults": {
                            "energyMeterVoltagesRaw": True,
                            "energyMetersRaw": True,
                            "resultsPerMeter": True,
                            "overloadsRaw": True,
                            "voltageExceptionsRaw": True
                        },
                        "nodeLevelResults": {
                            "collectVoltage": True,
                            "collectCurrent": False,
                            "collectPower": True,
                            "mridsToCollect": ["mrid_one", "mrid_two"],
                            "collectAllSwitches": False,
                            "collectAllTransformers": True,
                            "collectAllConductors": False,
                            "collectAllEnergyConsumers": True
                        }
                    }
                }
            }
        }
    }

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")

OPENDSS_CONFIG = OpenDssModelInput(
    modelName="TEST OPENDSS MODEL 1",
    isPublic=True,
    generationSpec=OpenDssModelGenerationSpecInput(
        modelOptions=OpenDssModelOptionsInput(
            scenario="scenario1",
            year=2024,
            feeder="feeder1",
        ),
        modulesConfiguration=OpenDssModulesConfigInput(
            common=OpenDssCommonConfigInput(
                fixedTime= FixedTimeInput(
                    loadTime=datetime(2022, 4, 1),
                    overrides=[
                        FixedTimeLoadOverrideInput(
                            loadId="meter1",
                            genVarOverride=[1.0],
                            genWattsOverride=[2.0],
                            loadVarOverride=[3.0],
                            loadWattsOverride=[4.0]
                        )
                    ]
                ),
                timePeriod=TimePeriodInput(
                    startTime=datetime(2022, 4, 1, 10, 13),
                    endTime=datetime(2023, 4, 1, 12, 14),
                    overrides=[
                        TimePeriodLoadOverrideInput(
                            loadId="meter1",
                            genVarOverride=[1.0],
                            genWattsOverride=[2.0],
                            loadVarOverride=[3.0],
                            loadWattsOverride=[4.0]
                        )
                    ]
                ),
            ),
            generator=HcGeneratorConfigInput(
                model=HcModelConfigInput(
                    vmPu=1.0,
                    loadVMinPu=0.80,
                    loadVMaxPu=1.15,
                    genVMinPu=0.50,
                    genVMaxPu=2.00,
                    loadModel=1,
                    collapse_swer=False,
                    calibration=False,
                    p_factor_base_exports=0.95,
                    p_factor_base_imports=0.90,
                    p_factor_forecast_pv=1.0,
                    fix_single_phase_loads=True,
                    max_single_phase_load=30000.0,
                    fix_overloading_consumers=True,
                    max_load_tx_ratio=3.0,
                    max_gen_tx_ratio=10.0,
                    fix_undersized_service_lines=True,
                    max_load_service_line_ratio=1.5,
                    max_load_lv_line_ratio=2.0,
                    simplify_network=False,
                    collapse_lv_networks=False,
                    collapse_negligible_impedances=False,
                    combine_common_impedances=False,
                    feeder_scenario_allocation_strategy=HcFeederScenarioAllocationStrategy.ADDITIVE,
                    closed_loop_v_reg_enabled=True,
                    closed_loop_v_reg_replace_all=True,
                    closed_loop_v_reg_set_point=0.985,
                    closed_loop_v_band=2.0,
                    closed_loop_time_delay=100,
                    closed_loop_v_limit=1.1,
                    default_tap_changer_time_delay=100,
                    default_tap_changer_set_point_pu=1.0,
                    default_tap_changer_band=2.0,
                    split_phase_default_load_loss_percentage=0.4,
                    splitPhaseLVKV=0.25,
                    swer_voltage_to_line_voltage=[
                        [230, 400],
                        [240, 415],
                        [250, 433],
                        [6350, 11000],
                        [6400, 11000],
                        [12700, 22000],
                        [19100, 33000]
                    ],
                    load_placement=HcLoadPlacement.PER_USAGE_POINT,
                    loadIntervalLengthHours=0.5,
                    meter_placement_config=HcMeterPlacementConfigInput(
                        feederHead=True,
                        distTransformers=True,
                        switchMeterPlacementConfigs=[
                            HcSwitchMeterPlacementConfigInput(
                                meterSwitchClass=HcSwitchClass.LOAD_BREAK_SWITCH,
                                namePattern=".*"
                            )
                        ],
                        energyConsumerMeterGroup="meter group 1"
                    ),
                    seed=42,
                    default_load_watts=[100.0, 200.0, 300.0],
                    default_gen_watts=[50.0, 150.0, 250.0],
                    default_load_var=[10.0, 20.0, 30.0],
                    default_gen_var=[5.0, 15.0, 25.0],
                    transformer_tap_settings="tap-3",
                    ct_prim_scaling_factor=2.0,
                    use_span_level_threshold=True,
                    rating_threshold=20.0,
                    simplify_plsi_threshold=20.0,
                    emerg_amp_scaling=1.8,
                    inverter_control_config=HcInverterControlConfigInput(
                        cut_off_date=datetime(2024, 4, 12, 11, 42),
                        before_cut_off_profile="beforeProfile",
                        after_cut_off_profile="afterProfile"
                    )
                ),
                solve=HcSolveConfigInput(
                    normVMinPu=0.9,
                    normVMaxPu=1.054,
                    emergVMinPu=0.8,
                    emergVMaxPu=1.1,
                    base_frequency=50,
                    voltage_bases=[0.4, 0.433, 6.6, 11.0, 22.0, 33.0, 66.0, 132.0],
                    max_iter=25,
                    max_control_iter=20,
                    mode=HcSolveMode.YEARLY,
                    step_size_minutes=60
                ),
                rawResults=HcRawResultsConfigInput(
                    energy_meter_voltages_raw=True,
                    energy_meters_raw=True,
                    results_per_meter=True,
                    overloads_raw=True,
                    voltage_exceptions_raw=True
                ),
                nodeLevelResults=HcNodeLevelResultsConfigInput(
                    collect_voltage=True,
                    collect_current=False,
                    collect_power=True,
                    mrids_to_collect=["mrid_one", "mrid_two"],
                    collect_all_switches=False,
                    collect_all_transformers=True,
                    collect_all_conductors=False,
                    collect_all_energy_consumers=True
                )

            )
        )
    ),
)


def test_run_opendss_export_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(run_opendss_export_request_handler)
    res = eas_client.run_opendss_export(OPENDSS_CONFIG)
    httpserver.check_assertions()
    assert res == {"result": "success"}


def test_run_opendss_export_invalid_certificate_failure(httpserver: HTTPServer):
    eas_client = _invalid_ca(httpserver.port)

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json({"result": "success"})
    with pytest.raises(httpx.ConnectError):
        eas_client.run_opendss_export(OPENDSS_CONFIG)


def test_run_opendss_export_valid_certificate_success(httpserver: HTTPServer, ca: trustme.CA):
    eas_client = _valid_ca(httpserver.port, ca)

    dss_conf = OPENDSS_CONFIG.model_copy()
    dss_conf.generation_spec.modules_configuration.common.fixed_time = FixedTimeInput(load_time=datetime(2022, 4, 1),
                                         overrides=[
                                             FixedTimeLoadOverrideInput(
                                                 loadId="meter1",
                                                 genVarOverride=[1.0],
                                                 genWattsOverride=[2.0],
                                                 loadVarOverride=[3.0],
                                                 loadWattsOverride=[4.0]
                                             )
                                         ])
    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(run_opendss_export_request_handler)
    res = eas_client.run_opendss_export(dss_conf)
    httpserver.check_assertions()
    assert res == {"result": "success"}


get_paged_opendss_models_query = ("query pagedOpenDssModels($limit_0: Int, $offset_0: Long, $filter_0: "
                                  "GetOpenDssModelsFilterInput, $sort_0: GetOpenDssModelsSortCriteriaInput) { "
                                  "pagedOpenDssModels( limit: $limit_0 offset: $offset_0 filter: $filter_0 "
                                  "sort: $sort_0 ) { totalCount offset models { id name createdAt state "
                                  "downloadUrl isPublic errors generationSpec } } }")


def get_paged_opendss_models_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == " ".join(line.strip() for line in get_paged_opendss_models_query.strip().splitlines())
    assert actual_body['variables'] == {
        "limit_0": 5,
        "offset_0": 0,
        "filter_0": {
            "name": "TEST OPENDSS MODEL 1",
            "isPublic": True,
            "state": ["COMPLETED"],
        },
        "sort_0": {
            "state": "ASC",
        }
    }

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_get_paged_opendss_models_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        get_paged_opendss_models_request_handler)
    res = eas_client.get_paged_opendss_models(
        5, 0, GetOpenDssModelsFilterInput(name="TEST OPENDSS MODEL 1", isPublic=True, state=[OpenDssModelState.COMPLETED.name]),
        GetOpenDssModelsSortCriteriaInput(state=SortOrder.ASC))
    httpserver.check_assertions()
    assert res == {"result": "success"}


def test_get_paged_opendss_models_invalid_certificate_failure(httpserver: HTTPServer):
    eas_client = _invalid_ca(httpserver.port)

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json({"result": "success"})
    with pytest.raises(httpx.ConnectError):
        eas_client.get_paged_opendss_models()


def get_paged_opendss_models_no_param_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == ('query pagedOpenDssModels { pagedOpenDssModels { totalCount offset models { id name createdAt '
                     'state downloadUrl isPublic errors generationSpec } } }')
    assert actual_body['variables'] == {}

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_get_paged_opendss_models_valid_certificate_success(httpserver: HTTPServer, ca: trustme.CA):
    eas_client = _valid_ca(httpserver.port, ca)

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        get_paged_opendss_models_no_param_request_handler)
    res = eas_client.get_paged_opendss_models()
    httpserver.check_assertions()
    assert res == {"result": "success"}


def test_get_opendss_model_download_url_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/opendss-model/1", method="GET").respond_with_response(Response(
        status=HTTPStatus.FOUND,
        headers={"Location": "https://example.com/download/1"}
    ))
    res = eas_client.get_opendss_model_download_url(1)
    httpserver.check_assertions()
    assert res == "https://example.com/download/1"


def test_get_opendss_model_download_url_invalid_certificate_failure(httpserver: HTTPServer):
    eas_client = _invalid_ca(httpserver.port)

    httpserver.expect_oneshot_request("/api/opendss-model/1", method="GET").respond_with_response(Response(
        status=HTTPStatus.FOUND,
        headers={"Location": "https://example.com/download/1"}
    ))
    with pytest.raises(httpx.ConnectError):
        eas_client.get_opendss_model_download_url(1)


def test_get_opendss_model_download_url_valid_certificate_success(httpserver: HTTPServer, ca: trustme.CA):
    eas_client = _valid_ca(httpserver.port, ca)

    httpserver.expect_oneshot_request("/api/opendss-model/1", method="GET").respond_with_response(Response(
        status=HTTPStatus.FOUND,
        headers={"Location": "https://example.com/download/1"}
    ))
    res = eas_client.get_opendss_model_download_url(1)
    httpserver.check_assertions()
    assert res == "https://example.com/download/1"


def run_ingestor_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == "mutation executeIngestor($runConfig_0: [IngestorConfigInput!]) { executeIngestor(runConfig: $runConfig_0) }"
    assert actual_body['variables'] == {'runConfig_0': [{'key': 'random.config', 'value': 'random.value'},
                                                      {'key': 'dataStorePath', 'value': '/some/place/with/data'}]}

    return Response(json.dumps({"executeIngestor": 5}), status=200, content_type="application/json")


def test_run_ingestor_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        run_ingestor_request_handler)
    res = eas_client.run_ingestor([IngestorConfigInput(key="random.config", value="random.value"),
                                   IngestorConfigInput(key="dataStorePath", value="/some/place/with/data")])
    httpserver.check_assertions()
    assert res == {"executeIngestor": 5}


def get_ingestor_run_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == ("query getIngestorRun($id_0: Int!) { getIngestorRun(id: $id_0) { id "
                     "containerRuntimeType payload token status startedAt statusLastUpdatedAt "
                     "completedAt } }")
    assert actual_body['variables'] == {"id_0": 1}

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_get_ingestor_run_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(get_ingestor_run_request_handler)
    res = eas_client.get_ingestor_run(1)
    httpserver.check_assertions()
    assert res == {"result": "success"}


def get_ingestor_run_list_request_empty_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    get_ingestor_run_list_query = ("query listIngestorRuns { listIngestorRuns { id containerRuntimeType payload "
                                   "token status startedAt statusLastUpdatedAt completedAt } }")
    assert query == " ".join(line.strip() for line in get_ingestor_run_list_query.strip().splitlines())
    assert actual_body['variables'] == {}

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_get_ingestor_run_list_empty_filter_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(get_ingestor_run_list_request_empty_handler)
    res = eas_client.get_ingestor_run_list()
    httpserver.check_assertions()
    assert res == {"result": "success"}


def get_ingestor_run_list_request_complete_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    get_ingestor_run_list_query = ("query listIngestorRuns($filter_0: IngestorRunsFilterInput, $sort_0: "
                                   "IngestorRunsSortCriteriaInput) { listIngestorRuns(filter: $filter_0, sort: "
                                   "$sort_0) { id containerRuntimeType payload token status startedAt "
                                   "statusLastUpdatedAt completedAt } }")
    assert query == " ".join(line.strip() for line in get_ingestor_run_list_query.strip().splitlines())
    assert actual_body['variables'] == {
        "filter_0": {
            "id": '4',
            "status": ["SUCCESS", "STARTED", "FAILED_TO_START"],
            "completed": True,
            "containerRuntimeType": ["TEMPORAL_KUBERNETES", "AZURE_CONTAINER_APP_JOB"]
        },
        "sort_0": {
            "status": "ASC",
            "startedAt": "DESC",
            "statusLastUpdatedAt": "ASC",
            "completedAt": "DESC",
            "containerRuntimeType": "ASC",
        }
    }

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_get_ingestor_run_list_all_filters_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        host=LOCALHOST,
        port=httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        get_ingestor_run_list_request_complete_handler)
    res = eas_client.get_ingestor_run_list(
        query_filter=IngestorRunsFilterInput(
            id='4',
            status=[IngestorRunState.SUCCESS, IngestorRunState.STARTED, IngestorRunState.FAILED_TO_START],
            completed=True,
            containerRuntimeType=[IngestorRuntimeKind.TEMPORAL_KUBERNETES,
                                    IngestorRuntimeKind.AZURE_CONTAINER_APP_JOB]
        ),
        query_sort=IngestorRunsSortCriteriaInput(
            status=SortOrder.ASC,
            startedAt=SortOrder.DESC,
            statusLastUpdatedAt=SortOrder.ASC,
            completedAt=SortOrder.DESC,
            containerRuntimeType=SortOrder.ASC
        )
    )
    httpserver.check_assertions()
    assert res == {"result": "success"}


def test_work_package_config_to_json_omits_server_defaulted_fields_if_unspecified():

    wp_config = WorkPackageInput(
        feederConfigs=FeederConfigsInput(configs=[]),
        intervention=InterventionConfigInput(
            baseWorkPackageId="abc",
            interventionType=InterventionClass.COMMUNITY_BESS
        )
    )
    json_config = wp_config.model_dump_json(by_alias=True, exclude_defaults=True)

    assert json.loads(json_config)['intervention'] == {
        "baseWorkPackageId": "abc",
        "interventionType": "COMMUNITY_BESS",
    }

def test_work_package_config_to_json_includes_server_defaulted_fields_if_specified():

    wp_config = WorkPackageInput(
        feederConfigs=FeederConfigsInput(configs=[]),
        intervention=InterventionConfigInput(
            baseWorkPackageId="abc",
            yearRange=YearRangeInput(minYear=2020, maxYear=2025),
            interventionType=InterventionClass.COMMUNITY_BESS,
            allocationLimitPerYear=5
        )
    )
    json_config = wp_config.model_dump_json(by_alias=True)

    assert json.loads(json_config)['intervention'] == {
        "baseWorkPackageId": "abc",
        "yearRange": {
            "maxYear": 2025,
            "minYear": 2020
        },
        "interventionType": "COMMUNITY_BESS",
        "candidateGeneration": None,
        "allocationCriteria": None,
        "specificAllocationInstance": None,
        "phaseRebalanceProportions": None,
        "dvms": None,
        "allocationLimitPerYear": 5
    }

def test_work_package_config_to_json_for_tap_optimization():
    wp_config = WorkPackageInput(
        feederConfigs=FeederConfigsInput(configs=[]),
        intervention=InterventionConfigInput(
            baseWorkPackageId="abc",
            yearRange=YearRangeInput(minYear=2020, maxYear=2025),
            interventionType=InterventionClass.DISTRIBUTION_TAP_OPTIMIZATION,
            allocationLimitPerYear=5,
            candidateGeneration=CandidateGenerationConfigInput(
                type=CandidateGenerationType.TAP_OPTIMIZATION,
                averageVoltageSpreadThreshold=40,
                voltageUnderLimitHoursThreshold=1,
                voltageOverLimitHoursThreshold=2,
                tapWeightingFactorLowerThreshold=-0.3,
                tapWeightingFactorUpperThreshold=0.4
            )
        )
    )
    json_config = wp_config.model_dump_json(by_alias=True)

    assert json.loads(json_config) == {
        "executorConfig": None,
        "feederConfigs": {"configs": []},
        "forecastConfig": None,
        "generatorConfig": None,
        "intervention": {
            "baseWorkPackageId": "abc",
            "yearRange": {
                "maxYear": 2025,
                "minYear": 2020
            },
            "interventionType": "DISTRIBUTION_TAP_OPTIMIZATION",
            "candidateGeneration": {
                "type": "TAP_OPTIMIZATION",
                "interventionCriteriaName": None,
                "averageVoltageSpreadThreshold": 40,
                "voltageUnderLimitHoursThreshold": 1,
                "voltageOverLimitHoursThreshold": 2,
                "tapWeightingFactorLowerThreshold": -0.3,
                "tapWeightingFactorUpperThreshold": 0.4,
            },
            "allocationCriteria": None,
            "specificAllocationInstance": None,
            "phaseRebalanceProportions": None,
            "dvms": None,
            "allocationLimitPerYear": 5
        },
        "qualityAssuranceProcessing": None,
        "resultProcessorConfig": None,
    }


def _invalid_ca(port):
    with trustme.Blob(b"invalid ca").tempfile() as ca_filename:
        return EasClient(
            host=LOCALHOST,
            port=port,
            verify_certificate=True,
            ca_filename=ca_filename
        )


def _valid_ca(port, ca: trustme.CA):
    with ca.cert_pem.tempfile() as ca_filename:
        return EasClient(
            host=LOCALHOST,
            port=port,
            verify_certificate=True,
            ca_filename=ca_filename
        )
