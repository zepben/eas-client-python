#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import random
import ssl
import string
from unittest import mock

import pytest
import requests.exceptions
from pytest_httpserver import HTTPServer
import trustme

from zepben.eas import EasClient, Study
from zepben.eas.client.study import Result

mock_host = ''.join(random.choices(string.ascii_lowercase, k=10))
mock_port = random.randrange(1024)
mock_client_id = ''.join(random.choices(string.ascii_lowercase, k=10))
mock_client_secret = ''.join(random.choices(string.ascii_lowercase, k=10))
mock_username = ''.join(random.choices(string.ascii_lowercase, k=10))
mock_password = ''.join(random.choices(string.ascii_lowercase, k=10))
mock_protocol = ''.join(random.choices(string.ascii_lowercase, k=10))
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


@mock.patch("zepben.auth.client.token_fetcher.requests.get", side_effect=lambda *args, **kwargs: MockResponse(
    {"configType": "AUTH0", "audience": mock_audience, "issuerDomain": "test_issuer"}, 200))
def test_create_eas_client_with_password_success(_):
    eas_client = EasClient(
        mock_host,
        mock_port,
        client_id=mock_client_id,
        username=mock_username,
        password=mock_password,
        protocol=mock_protocol,
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
    assert eas_client._protocol == mock_protocol
    assert eas_client._verify_certificate == mock_verify_certificate


@mock.patch("zepben.auth.client.token_fetcher.requests.get", side_effect=lambda *args, **kwargs: MockResponse(
    {"configType": "AUTH0", "audience": mock_audience, "issuerDomain": "test_issuer"}, 200))
def test_create_eas_client_with_client_secret_success(_):
    eas_client = EasClient(
        mock_host,
        mock_port,
        client_id=mock_client_id,
        client_secret=mock_client_secret,
        protocol=mock_protocol,
        verify_certificate=mock_verify_certificate
    )

    assert eas_client is not None
    assert eas_client._token_fetcher is not None
    assert eas_client._token_fetcher.token_request_data["grant_type"] == "client_credentials"
    assert eas_client._token_fetcher.token_request_data["client_secret"] == mock_client_secret
    assert eas_client._host == mock_host
    assert eas_client._port == mock_port
    assert eas_client._protocol == mock_protocol
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


def test_upload_study_no_verify_success(httpserver: HTTPServer):
    eas_client = EasClient(
        LOCALHOST,
        httpserver.port,
        verify_certificate=False
    )

    httpserver.expect_oneshot_request("/api/graphql").respond_with_data("OK")
    res = eas_client.upload_study(Study("Test study", "description", ["tag"], [Result("Huge success")], []))
    httpserver.check_assertions()
    assert res.status_code == 200
    assert res.text == "OK"


def test_upload_study_invalid_certificate_failure(ca: trustme.CA, httpserver: HTTPServer):
    with trustme.Blob(b"invalid ca").tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_data("OK")
        with pytest.raises(requests.exceptions.SSLError):
            eas_client.upload_study(Study("Test study", "description", ["tag"], [Result("Huge success")], []))


def test_upload_study_valid_certificate_success(ca: trustme.CA, httpserver: HTTPServer):
    with ca.cert_pem.tempfile() as ca_filename:
        eas_client = EasClient(
            LOCALHOST,
            httpserver.port,
            verify_certificate=True,
            ca_filename=ca_filename
        )

        httpserver.expect_oneshot_request("/api/graphql").respond_with_data("OK")
        res = eas_client.upload_study(Study("Test study", "description", ["tag"], [Result("Huge success")], []))
        httpserver.check_assertions()
        assert res.status_code == 200
        assert res.text == "OK"
