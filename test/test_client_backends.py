#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import httpx
import pytest
from graphql import OperationType

from zepben.eas import (
    EasClient,
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQLClientInvalidResponseError,
    Mutation,
    Query,
)


def _response(request: httpx.Request) -> httpx.Response:
    assert request.url.path == "/api/graphql"
    return httpx.Response(200, json={"data": {"activeWorkPackages": []}})


def test_sync_client_returns_a_result():
    client = EasClient(host="example.test", port=443, verify_certificate=False)
    client.close()
    client.http_client = httpx.Client(transport=httpx.MockTransport(_response))

    assert client.query(Query.get_active_work_packages()) == {
        "data": {"activeWorkPackages": []}
    }
    client.close()


@pytest.mark.asyncio
async def test_async_client_returns_an_awaitable_result():
    client = EasClient(
        host="example.test", port=443, verify_certificate=False, asynchronous=True
    )
    await client.close()
    client.http_client = httpx.AsyncClient(transport=httpx.MockTransport(_response))

    assert await client.query(Query.get_active_work_packages()) == {
        "data": {"activeWorkPackages": []}
    }
    await client.close()


def test_sync_mutation_and_custom_operation_return_results():
    client = EasClient(host="example.test", port=443, verify_certificate=False)
    client.close()
    client.http_client = httpx.Client(transport=httpx.MockTransport(_response))

    assert client.mutation(Mutation.delete_studies(["study-id"])) == {
        "data": {"activeWorkPackages": []}
    }
    assert client.execute_custom_operation(
        Query.get_active_work_packages(), operation_type=OperationType.QUERY
    ) == {"data": {"activeWorkPackages": []}}
    client.close()


@pytest.mark.asyncio
async def test_async_mutation_and_custom_operation_return_results():
    client = EasClient(
        host="example.test", port=443, verify_certificate=False, asynchronous=True
    )
    await client.close()
    client.http_client = httpx.AsyncClient(transport=httpx.MockTransport(_response))

    assert await client.mutation(Mutation.delete_studies(["study-id"])) == {
        "data": {"activeWorkPackages": []}
    }
    assert await client.execute_custom_operation(
        Query.get_active_work_packages(), operation_type=OperationType.QUERY
    ) == {"data": {"activeWorkPackages": []}}
    await client.close()


def test_sync_context_manager_and_opendss_download_url():
    def redirect(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/opendss-model/42"
        return httpx.Response(302, headers={"location": "https://download.test/model"})

    client = EasClient(host="example.test", port=443, verify_certificate=False)
    client.close()
    with client:
        client.http_client = httpx.Client(transport=httpx.MockTransport(redirect))
        assert (
            client.get_opendss_model_download_url(42) == "https://download.test/model"
        )


@pytest.mark.asyncio
async def test_async_context_manager_and_opendss_download_url():
    def redirect(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/opendss-model/42"
        return httpx.Response(302, headers={"location": "https://download.test/model"})

    client = EasClient(
        host="example.test", port=443, verify_certificate=False, asynchronous=True
    )
    await client.close()
    async with client:
        client.http_client = httpx.AsyncClient(transport=httpx.MockTransport(redirect))
        assert await client.get_opendss_model_download_url(42) == (
            "https://download.test/model"
        )


@pytest.mark.parametrize(
    ("response", "exception"),
    [
        (httpx.Response(500), GraphQLClientHttpError),
        (httpx.Response(200, content=b"not json"), GraphQLClientInvalidResponseError),
        (
            httpx.Response(200, json={"errors": [{"message": "invalid query"}]}),
            GraphQLClientGraphQLMultiError,
        ),
    ],
)
def test_response_errors_are_exposed_consistently(response, exception):
    client = EasClient(host="example.test", port=443, verify_certificate=False)
    with pytest.raises(exception):
        client.get_data(response)
    client.close()
