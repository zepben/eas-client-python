#  Copyright 2022 Zeppelin Bend Pty Ltd
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
from unittest import mock

import pytest
import trustme
from pytest_httpserver import HTTPServer
from werkzeug import Response
from zepben.auth import ZepbenTokenFetcher

from zepben.eas import EasClient, Study, SolveConfig
from zepben.eas import FeederConfig, ForecastConfig, FixedTimeLoadOverride
from zepben.eas.client.ingestor import IngestorConfigInput, IngestorRunsSortCriteriaInput, IngestorRunsFilterInput, \
    IngestorRunState, IngestorRuntimeKind
from zepben.eas.client.opendss import OpenDssConfig, GetOpenDssModelsFilterInput, OpenDssModelState, \
    GetOpenDssModelsSortCriteriaInput, \
    Order
from zepben.eas.client.study import Result
from zepben.eas.client.work_package import FeederConfigs, TimePeriodLoadOverride, \
    FixedTime, NodeLevelResultsConfig
from zepben.eas.client.work_package import WorkPackageConfig, TimePeriod, GeneratorConfig, ModelConfig, \
    FeederScenarioAllocationStrategy, LoadPlacement, MeterPlacementConfig, SwitchMeterPlacementConfig, SwitchClass, \
    SolveMode, RawResultsConfig

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
        mock_host,
        mock_port,
        protocol=mock_protocol,
        verify_certificate=mock_verify_certificate
    )

    assert eas_client is not None
    assert eas_client._host == mock_host
    assert eas_client._port == mock_port
    assert eas_client._protocol == mock_protocol
    assert eas_client._verify_certificate == mock_verify_certificate


def test_create_eas_client_with_access_token_success():
    eas_client = EasClient(
        mock_host,
        mock_port,
        access_token=mock_access_token,
    )

    assert eas_client is not None
    assert eas_client._host == mock_host
    assert eas_client._port == mock_port
    assert eas_client._access_token == mock_access_token


def test_get_request_headers_adds_access_token_in_auth_header():
    eas_client = EasClient(
        mock_host,
        mock_port,
        access_token=mock_access_token,
    )

    headers = eas_client._get_request_headers()
    assert headers["authorization"] == f"Bearer {mock_access_token}"


@mock.patch("zepben.auth.client.zepben_token_fetcher.ZepbenTokenFetcher.fetch_token", return_value="test_token3")
def test_get_request_headers_adds_token_from_token_fetcher_in_auth_header(_):
    eas_client = EasClient(
        mock_host,
        mock_port,
        token_fetcher=ZepbenTokenFetcher(audience="fake", token_endpoint="unused")
    )

    assert eas_client is not None
    assert eas_client._token_fetcher is not None
    headers = eas_client._get_request_headers()
    assert headers["authorization"] == "test_token3"


@mock.patch("zepben.auth.client.zepben_token_fetcher.requests.get", side_effect=lambda *args, **kwargs: MockResponse(
    {"authType": "AUTH0", "audience": mock_audience, "issuer": "test_issuer"}, 200))
def test_create_eas_client_with_password_success(_):
    eas_client = EasClient(
        mock_host,
        mock_port,
        client_id=mock_client_id,
        username=mock_username,
        password=mock_password,
        verify_certificate=mock_verify_certificate
    )

    assert eas_client is not None
    assert eas_client._token_fetcher is not None
    assert eas_client._token_fetcher.token_request_data["grant_type"] == "password"
    assert eas_client._token_fetcher.token_request_data["client_id"] == mock_client_id
    assert eas_client._token_fetcher.token_request_data["username"] == mock_username
    assert eas_client._token_fetcher.token_request_data["password"] == mock_password
    assert eas_client._host == mock_host
    assert eas_client._port == mock_port
    assert eas_client._verify_certificate == mock_verify_certificate


@mock.patch("zepben.auth.client.zepben_token_fetcher.requests.get", side_effect=lambda *args, **kwargs: MockResponse(
    {"authType": "AUTH0", "audience": mock_audience, "issuer": "test_issuer"}, 200))
def test_create_eas_client_with_client_secret_success(_):
    eas_client = EasClient(
        mock_host,
        mock_port,
        client_id=mock_client_id,
        client_secret=mock_client_secret,
        verify_certificate=mock_verify_certificate
    )

    assert eas_client is not None
    assert eas_client._token_fetcher is not None
    assert eas_client._token_fetcher.token_request_data["grant_type"] == "client_credentials"
    assert eas_client._token_fetcher.token_request_data["client_secret"] == mock_client_secret
    assert eas_client._host == mock_host
    assert eas_client._port == mock_port
    assert eas_client._verify_certificate == mock_verify_certificate


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
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
        {"data": {"getWorkPackageCostEstimation": "123.45"}})
    res = eas_client.get_work_package_cost_estimation(
        WorkPackageConfig(
            "wp_name",
            ForecastConfig(
                ["feeder"],
                [1],
                ["scenario"],
                TimePeriod(
                    datetime(2022, 1, 1),
                    datetime(2022, 1, 2),
                    None
                )
            )
        )
    )
    httpserver.check_assertions()
    assert res == {"data": {"getWorkPackageCostEstimation": "123.45"}}


def test_get_work_package_cost_estimation_invalid_certificate_failure(ca: trustme.CA, httpserver: HTTPServer):
    with trustme.Blob(b"invalid ca").tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
            {"data": {"getWorkPackageCostEstimation": "123.45"}})
        with pytest.raises(ssl.SSLError):
            eas_client.get_work_package_cost_estimation(
                WorkPackageConfig(
                    "wp_name",
                    ForecastConfig(
                        ["feeder"],
                        [1],
                        ["scenario"],
                        TimePeriod(
                            datetime(2022, 1, 1),
                            datetime(2022, 1, 2),
                            None
                        )
                    )
                )
            )


def test_get_work_package_cost_estimation_valid_certificate_success(ca: trustme.CA, httpserver: HTTPServer):
    with ca.cert_pem.tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
            {"data": {"getWorkPackageCostEstimation": "123.45"}})
        res = eas_client.get_work_package_cost_estimation(
            WorkPackageConfig(
                "wp_name",
                FeederConfigs(
                    [FeederConfig(
                        "feeder",
                        [1],
                        ["scenario"],
                        FixedTime(
                            datetime(2022, 1, 1),
                            {"meter": FixedTimeLoadOverride(1, 2, 3, 4)}
                        )
                    )]
                )
            )
        )
        httpserver.check_assertions()
        assert res == {"data": {"getWorkPackageCostEstimation": "123.45"}}


def test_run_hosting_capacity_work_package_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json({"data": {"runWorkPackage": "workPackageId"}})
    res = eas_client.run_hosting_capacity_work_package(
        WorkPackageConfig(
            "wp_name",
            ForecastConfig(
                ["feeder"],
                [1],
                ["scenario"],
                TimePeriod(
                    datetime(2022, 1, 1),
                    datetime(2022, 1, 2),
                    None
                )
            )
        )
    )
    httpserver.check_assertions()
    assert res == {"data": {"runWorkPackage": "workPackageId"}}


def test_run_hosting_capacity_work_package_invalid_certificate_failure(ca: trustme.CA, httpserver: HTTPServer):
    with trustme.Blob(b"invalid ca").tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
            {"data": {"runWorkPackage": "workPackageId"}})
        with pytest.raises(ssl.SSLError):
            eas_client.run_hosting_capacity_work_package(
                WorkPackageConfig(
                    "wp_name",
                    ForecastConfig(
                        ["feeder"],
                        [1],
                        ["scenario"],
                        TimePeriod(
                            datetime(2022, 1, 1),
                            datetime(2022, 1, 2),
                            None
                        )
                    )
                )
            )


def test_run_hosting_capacity_work_package_valid_certificate_success(ca: trustme.CA, httpserver: HTTPServer):
    with ca.cert_pem.tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
            {"data": {"runWorkPackage": "workPackageId"}})
        res = eas_client.run_hosting_capacity_work_package(
            WorkPackageConfig(
                "wp_name",
                ForecastConfig(
                    ["feeder"],
                    [1],
                    ["scenario"],
                    TimePeriod(
                        datetime(2022, 1, 1),
                        datetime(2022, 1, 2),
                        {"meter1": TimePeriodLoadOverride([1.0], [2.0], [3.0], [4.0])}
                    )
                )
            )
        )
        httpserver.check_assertions()
        assert res == {"data": {"runWorkPackage": "workPackageId"}}


def test_cancel_hosting_capacity_work_package_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
        {"data": {"cancelHostingCapacity": "workPackageId"}}
    )
    res = eas_client.cancel_hosting_capacity_work_package(work_package_id="workPackageId")
    httpserver.check_assertions()
    assert res == {"data": {"cancelHostingCapacity": "workPackageId"}}


def test_cancel_hosting_capacity_work_package_invalid_certificate_failure(ca: trustme.CA, httpserver: HTTPServer):
    with trustme.Blob(b"invalid ca").tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
            {"data": {"cancelWorkPackage": "workPackageId"}})
        with pytest.raises(ssl.SSLError):
            eas_client.cancel_hosting_capacity_work_package("workPackageId")


def test_cancel_hosting_capacity_work_package_valid_certificate_success(ca: trustme.CA, httpserver: HTTPServer):
    with ca.cert_pem.tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
            {"data": {"cancelWorkPackage": "workPackageId"}})
        res = eas_client.cancel_hosting_capacity_work_package("workPackageId")
        httpserver.check_assertions()
        assert res == {"data": {"cancelWorkPackage": "workPackageId"}}


def test_get_hosting_capacity_work_package_progress_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
        {"data": {"getWorkPackageProgress": {}}}
    )
    res = eas_client.get_hosting_capacity_work_packages_progress()
    httpserver.check_assertions()
    assert res == {"data": {"getWorkPackageProgress": {}}}


def test_get_hosting_capacity_work_package_progress_invalid_certificate_failure(ca: trustme.CA, httpserver: HTTPServer):
    with trustme.Blob(b"invalid ca").tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
            {"data": {"getWorkPackageProgress": {}}})
        with pytest.raises(ssl.SSLError):
            eas_client.get_hosting_capacity_work_packages_progress()


def test_get_hosting_capacity_work_package_progress_valid_certificate_success(ca: trustme.CA, httpserver: HTTPServer):
    with ca.cert_pem.tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_json(
            {"data": {"getWorkPackageProgress": {}}})
        res = eas_client.get_hosting_capacity_work_packages_progress()
        httpserver.check_assertions()
        assert res == {"data": {"getWorkPackageProgress": {}}}


def test_upload_study_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_json({"result": "success"})
    res = eas_client.upload_study(Study("Test study", "description", ["tag"], [Result("Huge success")], []))
    httpserver.check_assertions()
    assert res == {"result": "success"}


def test_upload_study_invalid_certificate_failure(ca: trustme.CA, httpserver: HTTPServer):
    with trustme.Blob(b"invalid ca").tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_json({"result": "success"})
        with pytest.raises(ssl.SSLError):
            eas_client.upload_study(Study("Test study", "description", ["tag"], [Result("Huge success")], []))


def test_upload_study_valid_certificate_success(ca: trustme.CA, httpserver: HTTPServer):
    with ca.cert_pem.tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_json({"result": "success"})
        res = eas_client.upload_study(Study("Test study", "description", ["tag"], [Result("Huge success")], []))
        httpserver.check_assertions()
        assert res == {"result": "success"}


def test_raises_error_if_auth_configured_with_http_server(httpserver: HTTPServer):
    with pytest.raises(ValueError):
        EasClient(
            LOCALHOST,
            httpserver.port,
            protocol="http",
            client_id=mock_client_id,
            username=mock_username,
            password=mock_password
        )


def test_raises_error_if_token_fetcher_and_creds_configured(httpserver: HTTPServer):
    with pytest.raises(ValueError, match="You cannot provide both a token_fetcher and credentials"):
        EasClient(
            LOCALHOST,
            httpserver.port,
            protocol="https",
            client_id=mock_client_id,
            username=mock_username,
            password=mock_password,
            token_fetcher=ZepbenTokenFetcher(audience="test", auth_method="test", token_endpoint="some-endpoint")
        )

    with pytest.raises(ValueError, match="You cannot provide both a token_fetcher and credentials"):
        EasClient(
            LOCALHOST,
            httpserver.port,
            protocol="https",
            client_id=mock_client_id,
            client_secret=mock_client_secret,
            token_fetcher=ZepbenTokenFetcher(audience="test", auth_method="test", token_endpoint="test")
        )


@mock.patch("zepben.auth.client.zepben_token_fetcher.requests.get", side_effect=lambda *args, **kwargs: MockResponse(
    {"authType": "AUTH0", "audience": mock_audience, "issuer": "test_issuer"}, 200))
def test_allows_secret_and_creds_configured(httpserver: HTTPServer):
    eas_client = EasClient(
        mock_host,
        mock_port,
        protocol="https",
        client_id=mock_client_id,
        client_secret=mock_client_secret,
        username=mock_username,
        password=mock_password
    )
    assert eas_client is not None
    assert eas_client._token_fetcher is not None
    assert eas_client._token_fetcher.token_request_data["grant_type"] == "password"
    assert eas_client._token_fetcher.token_request_data["client_id"] == mock_client_id
    assert eas_client._token_fetcher.token_request_data["username"] == mock_username
    assert eas_client._token_fetcher.token_request_data["password"] == mock_password
    assert eas_client._token_fetcher.token_request_data["client_secret"] == mock_client_secret
    assert eas_client._host == mock_host
    assert eas_client._port == mock_port


def test_raises_error_if_access_token_and_creds_configured(httpserver: HTTPServer):
    with pytest.raises(ValueError) as error_message_for_username:
        EasClient(
            LOCALHOST,
            httpserver.port,
            protocol="https",
            access_token=mock_access_token,
            username=mock_username,
        )
    assert "Incompatible arguments passed to connect to secured Evolve App Server. You cannot provide multiple types of authentication. When using an access_token, do not provide client_id, client_secret, username, password, or token_fetcher." in str(
        error_message_for_username.value)

    with pytest.raises(ValueError) as error_message_for_password:
        EasClient(
            LOCALHOST,
            httpserver.port,
            protocol="https",
            access_token=mock_access_token,
            password=mock_password,
        )
    assert "Incompatible arguments passed to connect to secured Evolve App Server. You cannot provide multiple types of authentication. When using an access_token, do not provide client_id, client_secret, username, password, or token_fetcher." in str(
        error_message_for_password.value)


def test_raises_error_if_access_token_and_token_fetcher_configured(httpserver: HTTPServer):
    with pytest.raises(ValueError) as error_message_for_username:
        EasClient(
            LOCALHOST,
            httpserver.port,
            protocol="https",
            access_token=mock_access_token,
            token_fetcher=ZepbenTokenFetcher(audience="test", auth_method="test", token_endpoint="test")
        )
    assert "Incompatible arguments passed to connect to secured Evolve App Server. You cannot provide multiple types of authentication. When using an access_token, do not provide client_id, client_secret, username, password, or token_fetcher." in str(
        error_message_for_username.value)


def test_raises_error_if_access_token_and_client_id_configured(httpserver: HTTPServer):
    with pytest.raises(ValueError) as error_message_for_username:
        EasClient(
            LOCALHOST,
            httpserver.port,
            protocol="https",
            access_token=mock_access_token,
            client_id=mock_client_id
        )
    assert "Incompatible arguments passed to connect to secured Evolve App Server. You cannot provide multiple types of authentication. When using an access_token, do not provide client_id, client_secret, username, password, or token_fetcher." in str(
        error_message_for_username.value)


def test_raises_error_if_access_token_and_client_secret_configured(httpserver: HTTPServer):
    with pytest.raises(ValueError) as error_message_for_username:
        EasClient(
            LOCALHOST,
            httpserver.port,
            protocol="https",
            access_token=mock_access_token,
            client_secret=mock_client_secret
        )
    assert "Incompatible arguments passed to connect to secured Evolve App Server. You cannot provide multiple types of authentication. When using an access_token, do not provide client_id, client_secret, username, password, or token_fetcher." in str(
        error_message_for_username.value)


def hosting_capacity_run_calibration_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == "mutation runCalibration($calibrationName: String!, $calibrationTimeLocal: LocalDateTime, $feeders: [String!], $generatorConfig: HcGeneratorConfigInput) { runCalibration(calibrationName: $calibrationName, calibrationTimeLocal: $calibrationTimeLocal, feeders: $feeders, generatorConfig: $generatorConfig) }"
    assert actual_body['variables'] == {"calibrationName": "TEST CALIBRATION",
                                        "calibrationTimeLocal": datetime(2025, month=7, day=12).isoformat(),
                                        "feeders": None, 'generatorConfig': None
                                        }

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_run_hosting_capacity_calibration_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(hosting_capacity_run_calibration_request_handler)
    res = eas_client.run_hosting_capacity_calibration("TEST CALIBRATION", datetime(2025, month=7, day=12))
    httpserver.check_assertions()
    assert res == {"result": "success"}


def test_run_hosting_capacity_calibration_invalid_certificate_failure(ca: trustme.CA, httpserver: HTTPServer):
    with trustme.Blob(b"invalid ca").tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_json({"result": "success"})
        with pytest.raises(ssl.SSLError):
            eas_client.run_hosting_capacity_calibration("TEST CALIBRATION", datetime(2025, month=7, day=12))


def test_run_hosting_capacity_calibration_valid_certificate_success(ca: trustme.CA, httpserver: HTTPServer):
    with ca.cert_pem.tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
            hosting_capacity_run_calibration_request_handler)
        res = eas_client.run_hosting_capacity_calibration("TEST CALIBRATION", datetime(2025, month=7, day=12))
        httpserver.check_assertions()
        assert res == {"result": "success"}


def get_hosting_capacity_run_calibration_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == "query getCalibrationRun($id: ID!) { getCalibrationRun(id: $id) { id name workflowId runId calibrationTimeLocal startAt completedAt status feeders calibrationWorkPackageConfig } }"
    assert actual_body['variables'] == {"id": "calibration-id"}

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_get_hosting_capacity_calibration_run_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        get_hosting_capacity_run_calibration_request_handler)
    res = eas_client.get_hosting_capacity_calibration_run("calibration-id")
    httpserver.check_assertions()
    assert res == {"result": "success"}


def test_get_hosting_capacity_calibration_run_invalid_certificate_failure(ca: trustme.CA, httpserver: HTTPServer):
    with trustme.Blob(b"invalid ca").tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_json({"result": "success"})
        with pytest.raises(ssl.SSLError):
            eas_client.get_hosting_capacity_calibration_run("calibration-id")


def test_get_hosting_capacity_calibration_run_valid_certificate_success(ca: trustme.CA, httpserver: HTTPServer):
    with ca.cert_pem.tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
            get_hosting_capacity_run_calibration_request_handler)
        res = eas_client.get_hosting_capacity_calibration_run("calibration-id")
        httpserver.check_assertions()
        assert res == {"result": "success"}


def hosting_capacity_run_calibration_with_calibration_time_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == "mutation runCalibration($calibrationName: String!, $calibrationTimeLocal: LocalDateTime, $feeders: [String!], $generatorConfig: HcGeneratorConfigInput) { runCalibration(calibrationName: $calibrationName, calibrationTimeLocal: $calibrationTimeLocal, feeders: $feeders, generatorConfig: $generatorConfig) }"
    assert actual_body['variables'] == {"calibrationName": "TEST CALIBRATION",
                                        "calibrationTimeLocal": datetime(1902, month=1, day=28, hour=0, minute=0,
                                                                         second=20).isoformat(),
                                        "feeders": ["one", "two"],
                                        "generatorConfig": {
                                            'model': {
                                                'calibration': None,
                                                'closedLoopTimeDelay': None,
                                                'closedLoopVBand': None,
                                                'closedLoopVLimit': None,
                                                'closedLoopVRegEnabled': None,
                                                'closedLoopVRegReplaceAll': None,
                                                'closedLoopVRegSetPoint': None,
                                                'collapseLvNetworks': None,
                                                'collapseNegligibleImpedances': None,
                                                'collapseSWER': None,
                                                'combineCommonImpedances': None,
                                                'ctPrimScalingFactor': None,
                                                'defaultGenVar': None,
                                                'defaultGenWatts': None,
                                                'defaultLoadVar': None,
                                                'defaultLoadWatts': None,
                                                'defaultTapChangerBand': None,
                                                'defaultTapChangerSetPointPu': None,
                                                'defaultTapChangerTimeDelay': None,
                                                'feederScenarioAllocationStrategy': None,
                                                'fixOverloadingConsumers': None,
                                                'fixSinglePhaseLoads': None,
                                                'fixUndersizedServiceLines': None,
                                                'genVMaxPu': None,
                                                'genVMinPu': None,
                                                'loadIntervalLengthHours': None,
                                                'loadModel': None,
                                                'loadPlacement': None,
                                                'loadVMaxPu': None,
                                                'loadVMinPu': None,
                                                'maxGenTxRatio': None,
                                                'maxLoadLvLineRatio': None,
                                                'maxLoadServiceLineRatio': None,
                                                'maxLoadTxRatio': None,
                                                'maxSinglePhaseLoad': None,
                                                'meterPlacementConfig': None,
                                                'pFactorBaseExports': None,
                                                'pFactorBaseImports': None,
                                                'pFactorForecastPv': None,
                                                'seed': None,
                                                'simplifyNetwork': None,
                                                'useSpanLevelThreshold': False,
                                                'ratingThreshold': None,
                                                'simplifyPLSIThreshold': None,
                                                'emergAmpScaling': None,
                                                'splitPhaseDefaultLoadLossPercentage': None,
                                                'splitPhaseLVKV': None,
                                                'swerVoltageToLineVoltage': None,
                                                'transformerTapSettings': 'test_tap_settings',
                                                'vmPu': None},
                                            'rawResults': None,
                                            'nodeLevelResults': None,
                                            'solve': None}
                                        }

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_run_hosting_capacity_calibration_with_calibration_time_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        hosting_capacity_run_calibration_with_calibration_time_request_handler)
    res = eas_client.run_hosting_capacity_calibration("TEST CALIBRATION",
                                                      datetime(1902, month=1, day=28, hour=0, minute=0, second=20),
                                                      ["one", "two"],
                                                      generator_config=GeneratorConfig(model=ModelConfig(
                                                          transformer_tap_settings="test_tap_settings"
                                                      ))
                                                      )
    httpserver.check_assertions()
    assert res == {"result": "success"}


def test_run_hosting_capacity_calibration_with_explicit_transformer_tap_settings_no_generator_config(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
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

    assert query == "mutation runCalibration($calibrationName: String!, $calibrationTimeLocal: LocalDateTime, $feeders: [String!], $generatorConfig: HcGeneratorConfigInput) { runCalibration(calibrationName: $calibrationName, calibrationTimeLocal: $calibrationTimeLocal, feeders: $feeders, generatorConfig: $generatorConfig) }"
    assert actual_body['variables'] == {"calibrationName": "TEST CALIBRATION",
                                        "calibrationTimeLocal": datetime(1902, month=1, day=28, hour=0, minute=0,
                                                                         second=20).isoformat(),
                                        "feeders": ["one", "two"],
                                        "generatorConfig": {
                                            'model': {
                                                'calibration': None,
                                                'closedLoopTimeDelay': None,
                                                'closedLoopVBand': None,
                                                'closedLoopVLimit': None,
                                                'closedLoopVRegEnabled': None,
                                                'closedLoopVRegReplaceAll': None,
                                                'closedLoopVRegSetPoint': None,
                                                'collapseLvNetworks': None,
                                                'collapseNegligibleImpedances': None,
                                                'collapseSWER': None,
                                                'combineCommonImpedances': None,
                                                'ctPrimScalingFactor': None,
                                                'defaultGenVar': None,
                                                'defaultGenWatts': None,
                                                'defaultLoadVar': None,
                                                'defaultLoadWatts': None,
                                                'defaultTapChangerBand': None,
                                                'defaultTapChangerSetPointPu': None,
                                                'defaultTapChangerTimeDelay': None,
                                                'feederScenarioAllocationStrategy': None,
                                                'fixOverloadingConsumers': None,
                                                'fixSinglePhaseLoads': None,
                                                'fixUndersizedServiceLines': None,
                                                'genVMaxPu': None,
                                                'genVMinPu': None,
                                                'loadIntervalLengthHours': None,
                                                'loadModel': None,
                                                'loadPlacement': None,
                                                'loadVMaxPu': None,
                                                'loadVMinPu': None,
                                                'maxGenTxRatio': None,
                                                'maxLoadLvLineRatio': None,
                                                'maxLoadServiceLineRatio': None,
                                                'maxLoadTxRatio': None,
                                                'maxSinglePhaseLoad': None,
                                                'meterPlacementConfig': None,
                                                'pFactorBaseExports': None,
                                                'pFactorBaseImports': None,
                                                'pFactorForecastPv': None,
                                                'seed': None,
                                                'simplifyNetwork': None,
                                                'useSpanLevelThreshold': False,
                                                'ratingThreshold': None,
                                                'simplifyPLSIThreshold': None,
                                                'emergAmpScaling': None,
                                                'splitPhaseDefaultLoadLossPercentage': None,
                                                'splitPhaseLVKV': None,
                                                'swerVoltageToLineVoltage': None,
                                                'transformerTapSettings': 'test_tap_settings',
                                                'vmPu': None
                                            },
                                            'nodeLevelResults': None,
                                            'rawResults': None,
                                            'solve': {
                                                'baseFrequency': None,
                                                'emergVMaxPu': None,
                                                'emergVMinPu': None,
                                                'maxControlIter': None,
                                                'maxIter': None,
                                                'mode': None,
                                                'normVMaxPu': 23.9,
                                                'normVMinPu': None,
                                                'stepSizeMinutes': None,
                                                'voltageBases': None
                                                }
                                            }
                                        }

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_run_hosting_capacity_calibration_with_explicit_transformer_tap_settings_partial_generator_config(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        hosting_capacity_run_calibration_with_generator_config_request_handler)
    res = eas_client.run_hosting_capacity_calibration("TEST CALIBRATION",
                                                      datetime(1902, month=1, day=28, hour=0, minute=0, second=20),
                                                      ["one", "two"],
                                                      transformer_tap_settings="test_tap_settings",
                                                      generator_config=GeneratorConfig(solve=SolveConfig(norm_vmax_pu=23.9))
                                                      )
    httpserver.check_assertions()
    assert res == {"result": "success"}


def hosting_capacity_run_calibration_with_partial_model_config_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == "mutation runCalibration($calibrationName: String!, $calibrationTimeLocal: LocalDateTime, $feeders: [String!], $generatorConfig: HcGeneratorConfigInput) { runCalibration(calibrationName: $calibrationName, calibrationTimeLocal: $calibrationTimeLocal, feeders: $feeders, generatorConfig: $generatorConfig) }"
    assert actual_body['variables'] == {"calibrationName": "TEST CALIBRATION",
                                        "calibrationTimeLocal": datetime(1902, month=1, day=28, hour=0, minute=0,
                                                                         second=20).isoformat(),
                                        "feeders": ["one", "two"],
                                        "generatorConfig": {
                                            'model': {
                                                'calibration': None,
                                                'closedLoopTimeDelay': None,
                                                'closedLoopVBand': None,
                                                'closedLoopVLimit': None,
                                                'closedLoopVRegEnabled': None,
                                                'closedLoopVRegReplaceAll': None,
                                                'closedLoopVRegSetPoint': None,
                                                'collapseLvNetworks': None,
                                                'collapseNegligibleImpedances': None,
                                                'collapseSWER': None,
                                                'combineCommonImpedances': None,
                                                'ctPrimScalingFactor': None,
                                                'defaultGenVar': None,
                                                'defaultGenWatts': None,
                                                'defaultLoadVar': None,
                                                'defaultLoadWatts': None,
                                                'defaultTapChangerBand': None,
                                                'defaultTapChangerSetPointPu': None,
                                                'defaultTapChangerTimeDelay': None,
                                                'feederScenarioAllocationStrategy': None,
                                                'fixOverloadingConsumers': None,
                                                'fixSinglePhaseLoads': None,
                                                'fixUndersizedServiceLines': None,
                                                'genVMaxPu': None,
                                                'genVMinPu': None,
                                                'loadIntervalLengthHours': None,
                                                'loadModel': None,
                                                'loadPlacement': None,
                                                'loadVMaxPu': None,
                                                'loadVMinPu': None,
                                                'maxGenTxRatio': None,
                                                'maxLoadLvLineRatio': None,
                                                'maxLoadServiceLineRatio': None,
                                                'maxLoadTxRatio': None,
                                                'maxSinglePhaseLoad': None,
                                                'meterPlacementConfig': None,
                                                'pFactorBaseExports': None,
                                                'pFactorBaseImports': None,
                                                'pFactorForecastPv': None,
                                                'seed': None,
                                                'simplifyNetwork': None,
                                                'useSpanLevelThreshold': False,
                                                'ratingThreshold': None,
                                                'simplifyPLSIThreshold': None,
                                                'emergAmpScaling': None,
                                                'splitPhaseDefaultLoadLossPercentage': None,
                                                'splitPhaseLVKV': None,
                                                'swerVoltageToLineVoltage': None,
                                                'transformerTapSettings': 'test_tap_settings',
                                                'vmPu': 123.4
                                                },
                                            'nodeLevelResults': None,
                                            'rawResults': None,
                                            'solve': None
                                            }
                                        }

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_run_hosting_capacity_calibration_with_explicit_transformer_tap_settings_partial_model_config(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        hosting_capacity_run_calibration_with_partial_model_config_request_handler)
    res = eas_client.run_hosting_capacity_calibration("TEST CALIBRATION",
                                                      datetime(1902, month=1, day=28, hour=0, minute=0, second=20),
                                                      ["one", "two"],
                                                      transformer_tap_settings="test_tap_settings",
                                                      generator_config=GeneratorConfig(model=ModelConfig(vm_pu=123.4))
                                                      )
    httpserver.check_assertions()
    assert res == {"result": "success"}


def test_run_hosting_capacity_calibration_with_explicit_transformer_tap_settings(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        hosting_capacity_run_calibration_with_calibration_time_request_handler)
    res = eas_client.run_hosting_capacity_calibration("TEST CALIBRATION",
                                                      datetime(1902, month=1, day=28, hour=0, minute=0, second=20),
                                                      ["one", "two"],
                                                      transformer_tap_settings="test_tap_settings",
                                                      generator_config=GeneratorConfig(model=ModelConfig(
                                                          transformer_tap_settings="this_should_be_over_written"
                                                      ))
                                                      )
    httpserver.check_assertions()
    assert res == {"result": "success"}


def get_hosting_capacity_calibration_sets_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == "query { getCalibrationSets }"

    assert "variables" not in actual_body

    return Response(json.dumps(["one", "two", "three"]), status=200, content_type="application/json")


def test_get_hosting_capacity_calibration_sets_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
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

    assert query == "mutation createOpenDssModel($input: OpenDssModelInput!) { createOpenDssModel(input: $input) }"
    assert actual_body['variables'] == {
        "input": {
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
                        **({"fixedTime": {
                            "loadTime": "2022-04-01T00:00:00",
                            "overrides": [{
                                'loadId': 'meter1',
                                'loadWattsOverride': [1.0],
                                'genWattsOverride': [2.0],
                                'loadVarOverride': [3.0],
                                'genVarOverride': [4.0]
                            }]
                        }} if isinstance(OPENDSS_CONFIG.load_time, FixedTime) else
                           {"timePeriod": {
                               "startTime": "2022-04-01T00:00:00",
                               "endTime": "2023-04-01T00:00:00",
                               "overrides": [{
                                   'loadId': 'meter1',
                                   'loadWattsOverride': [1.0],
                                   'genWattsOverride': [2.0],
                                   'loadVarOverride': [3.0],
                                   'genVarOverride': [4.0]
                               }]
                           }})
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
                            "emergAmpScaling": 1.8
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


OPENDSS_CONFIG = OpenDssConfig(
    scenario="scenario1",
    year=2024,
    feeder="feeder1",
    load_time=TimePeriod(
        datetime(2022, 4, 1),
        datetime(2023, 4, 1),
        {"meter1": TimePeriodLoadOverride([1.0], [2.0], [3.0], [4.0])}
    ),
    model_name="TEST OPENDSS MODEL 1",
    generator_config=GeneratorConfig(
        ModelConfig(
            vm_pu=1.0,
            load_vmin_pu=0.80,
            load_vmax_pu=1.15,
            gen_vmin_pu=0.50,
            gen_vmax_pu=2.00,
            load_model=1,
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
            feeder_scenario_allocation_strategy=FeederScenarioAllocationStrategy.ADDITIVE,
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
            split_phase_lv_kv=0.25,
            swer_voltage_to_line_voltage=[
                [230, 400],
                [240, 415],
                [250, 433],
                [6350, 11000],
                [6400, 11000],
                [12700, 22000],
                [19100, 33000]
            ],
            load_placement=LoadPlacement.PER_USAGE_POINT,
            load_interval_length_hours=0.5,
            meter_placement_config=MeterPlacementConfig(
                True,
                True,
                [SwitchMeterPlacementConfig(SwitchClass.LOAD_BREAK_SWITCH, ".*")],
                "meter group 1"),
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
            emerg_amp_scaling= 1.8
        ),
        SolveConfig(
            norm_vmin_pu=0.9,
            norm_vmax_pu=1.054,
            emerg_vmin_pu=0.8,
            emerg_vmax_pu=1.1,
            base_frequency=50,
            voltage_bases=[0.4, 0.433, 6.6, 11.0, 22.0, 33.0, 66.0, 132.0],
            max_iter=25,
            max_control_iter=20,
            mode=SolveMode.YEARLY,
            step_size_minutes=60
        ),
        RawResultsConfig(
            energy_meter_voltages_raw=True,
            energy_meters_raw=True,
            results_per_meter=True,
            overloads_raw=True,
            voltage_exceptions_raw=True
        ),
        NodeLevelResultsConfig(
            collect_voltage=True,
            collect_current=False,
            collect_power=True,
            mrids_to_collect=["mrid_one", "mrid_two"],
            collect_all_switches=False,
            collect_all_transformers=True,
            collect_all_conductors=False,
            collect_all_energy_consumers=True
        )
    ),
    is_public=True)


def test_run_opendss_export_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(run_opendss_export_request_handler)
    res = eas_client.run_opendss_export(OPENDSS_CONFIG)
    httpserver.check_assertions()
    assert res == {"result": "success"}


def test_run_opendss_export_invalid_certificate_failure(ca: trustme.CA, httpserver: HTTPServer):
    with trustme.Blob(b"invalid ca").tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_json({"result": "success"})
        with pytest.raises(ssl.SSLError):
            eas_client.run_opendss_export(OPENDSS_CONFIG)


def test_run_opendss_export_valid_certificate_success(ca: trustme.CA, httpserver: HTTPServer):
    with ca.cert_pem.tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        OPENDSS_CONFIG.load_time = FixedTime(datetime(2022, 4, 1), {"meter1": FixedTimeLoadOverride([1.0], [2.0], [3.0], [4.0])})
        httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(run_opendss_export_request_handler)
        res = eas_client.run_opendss_export(OPENDSS_CONFIG)
        httpserver.check_assertions()
        assert res == {"result": "success"}


get_paged_opendss_models_query = """
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
                                    simplifyNetwork
                                    collapseLvNetworks
                                    collapseNegligibleImpedances
                                    combineCommonImpedances
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
                                    useSpanLevelThreshold
                                    ratingThreshold
                                    simplifyPLSIThreshold
                                    emergAmpScaling
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
                                nodeLevelResults {
                                    collectVoltage
                                    collectCurrent
                                    collectPower
                                    mridsToCollect
                                    collectAllSwitches
                                    collectAllTransformers
                                    collectAllConductors
                                    collectAllEnergyConsumers
                                }
                            }
                        }
                    }
                }
            }
        }
    """


def get_paged_opendss_models_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == " ".join(line.strip() for line in get_paged_opendss_models_query.strip().splitlines())
    assert actual_body['variables'] == {
        "limit": 5,
        "offset": 0,
        "filter": {
            "name": "TEST OPENDSS MODEL 1",
            "isPublic": True,
            "state": ["COMPLETED"],
        },
        "sort": {
            "state": "ASC",
            "createdAt": None,
            "name": None,
            "isPublic": None
        }
    }

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_get_paged_opendss_models_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        get_paged_opendss_models_request_handler)
    res = eas_client.get_paged_opendss_models(
        5, 0, GetOpenDssModelsFilterInput("TEST OPENDSS MODEL 1", True, [OpenDssModelState.COMPLETED]),
        GetOpenDssModelsSortCriteriaInput(state=Order.ASC))
    httpserver.check_assertions()
    assert res == {"result": "success"}


def test_get_paged_opendss_models_invalid_certificate_failure(ca: trustme.CA, httpserver: HTTPServer):
    with trustme.Blob(b"invalid ca").tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_json({"result": "success"})
        with pytest.raises(ssl.SSLError):
            eas_client.get_paged_opendss_models()


def get_paged_opendss_models_no_param_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == " ".join(line.strip() for line in get_paged_opendss_models_query.strip().splitlines())
    assert actual_body['variables'] == {}

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_get_paged_opendss_models_valid_certificate_success(ca: trustme.CA, httpserver: HTTPServer):
    with ca.cert_pem.tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
            get_paged_opendss_models_no_param_request_handler)
        res = eas_client.get_paged_opendss_models()
        httpserver.check_assertions()
        assert res == {"result": "success"}


def test_get_opendss_model_download_url_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/opendss-model/1", method="GET").respond_with_response(Response(
        status=HTTPStatus.FOUND,
        headers={"Location": "https://example.com/download/1"}
    ))
    res = eas_client.get_opendss_model_download_url(1)
    httpserver.check_assertions()
    assert res == "https://example.com/download/1"


def test_get_opendss_model_download_url_invalid_certificate_failure(ca: trustme.CA, httpserver: HTTPServer):
    with trustme.Blob(b"invalid ca").tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/opendss-model/1", method="GET").respond_with_response(Response(
            status=HTTPStatus.FOUND,
            headers={"Location": "https://example.com/download/1"}
        ))
        with pytest.raises(ssl.SSLError):
            eas_client.get_opendss_model_download_url(1)


def test_get_opendss_model_download_url_valid_certificate_success(ca: trustme.CA, httpserver: HTTPServer):
    with ca.cert_pem.tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

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

    assert query == "mutation executeIngestor($runConfig: [IngestorConfigInput!]) { executeIngestor(runConfig: $runConfig) }"
    assert actual_body['variables'] == {'runConfig': [{'key': 'random.config', 'value': 'random.value'},
                                                      {'key': 'dataStorePath', 'value': '/some/place/with/data'}]}

    return Response(json.dumps({"executeIngestor": 5}), status=200, content_type="application/json")


def test_run_ingestor_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(
        run_ingestor_request_handler)
    res = eas_client.run_ingestor([IngestorConfigInput("random.config", "random.value"),
                                   IngestorConfigInput("dataStorePath", "/some/place/with/data")])
    httpserver.check_assertions()
    assert res == {"executeIngestor": 5}


def get_ingestor_run_request_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    assert query == "query getIngestorRun($id: Int!) { getIngestorRun(id: $id) { id containerRuntimeType, payload, token, status, startedAt, statusLastUpdatedAt, completedAt } }"
    assert actual_body['variables'] == {"id": 1}

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_get_ingestor_run_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(get_ingestor_run_request_handler)
    res = eas_client.get_ingestor_run(1)
    httpserver.check_assertions()
    assert res == {"result": "success"}


def get_ingestor_run_list_request_empty_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    get_ingestor_run_list_query = """
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
            """
    assert query == " ".join(line.strip() for line in get_ingestor_run_list_query.strip().splitlines())
    assert actual_body['variables'] == {}

    return Response(json.dumps({"result": "success"}), status=200, content_type="application/json")


def test_get_ingestor_run_list_empty_filter_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(get_ingestor_run_list_request_empty_handler)
    res = eas_client.get_ingestor_run_list()
    httpserver.check_assertions()
    assert res == {"result": "success"}


def get_ingestor_run_list_request_complete_handler(request):
    actual_body = json.loads(request.data.decode())
    query = " ".join(actual_body['query'].split())

    get_ingestor_run_list_query = """
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
            """
    assert query == " ".join(line.strip() for line in get_ingestor_run_list_query.strip().splitlines())
    assert actual_body['variables'] == {
        "filter": {
            "id": 4,
            "status": ["SUCCESS", "STARTED", "FAILED_TO_START"],
            "completed": True,
            "containerRuntimeType": ["TEMPORAL_KUBERNETES", "AZURE_CONTAINER_APP_JOB"]
        },
        "sort": {
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
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_handler(get_ingestor_run_list_request_complete_handler)
    res = eas_client.get_ingestor_run_list(
        query_filter=IngestorRunsFilterInput(
            id=4,
            status=[IngestorRunState.SUCCESS, IngestorRunState.STARTED, IngestorRunState.FAILED_TO_START],
            completed=True,
            container_runtime_type=[IngestorRuntimeKind.TEMPORAL_KUBERNETES,
                                    IngestorRuntimeKind.AZURE_CONTAINER_APP_JOB]
        ),
        query_sort=IngestorRunsSortCriteriaInput(
            status=Order.ASC,
            started_at=Order.DESC,
            status_last_updated_at=Order.ASC,
            completed_at=Order.DESC,
            container_runtime_type=Order.ASC
        )
    )
    httpserver.check_assertions()
    assert res == {"result": "success"}
