#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import httpx
import pytest

from zepben.eas import EasClient, Query


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
