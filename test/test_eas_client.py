#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import random
import ssl
import string
from datetime import datetime
from unittest import mock

import pytest
import trustme
from pytest_httpserver import HTTPServer
from zepben.auth import ZepbenTokenFetcher

from zepben.eas import EasClient, Study
from zepben.eas.client.study import Result
from zepben.eas.client.work_package import WorkPackageConfig, TimePeriod

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
            ["feeder"],
            [1],
            ["scenario"],
            TimePeriod(
                datetime(2022, 1, 1),
                datetime(2022, 1, 2))
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
                    ["feeder"],
                    [1],
                    ["scenario"],
                    TimePeriod(
                        datetime(2022, 1, 1),
                        datetime(2022, 1, 2))
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
                ["feeder"],
                [1],
                ["scenario"],
                TimePeriod(
                    datetime(2022, 1, 1),
                    datetime(2022, 1, 2))
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
