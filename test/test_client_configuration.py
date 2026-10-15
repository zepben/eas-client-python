#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import ssl

import httpx
import pytest

from zepben.eas import EasClient


class _RecordingSyncClient:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def close(self):
        pass


class _RecordingAsyncClient:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    async def aclose(self):
        pass


def test_sync_client_configures_authentication_and_tls(monkeypatch):
    monkeypatch.setattr(httpx, "Client", _RecordingSyncClient)

    client = EasClient(host="example.test", port=443, access_token="token")

    assert client.http_client.kwargs["headers"] == {"authorization": "Bearer token"}
    assert isinstance(client.http_client.kwargs["verify"], ssl.SSLContext)
    client.close()


@pytest.mark.asyncio
async def test_async_client_configures_authentication_and_tls(monkeypatch):
    monkeypatch.setattr(httpx, "AsyncClient", _RecordingAsyncClient)

    client = EasClient(
        host="example.test", port=443, access_token="token", asynchronous=True
    )

    assert client.http_client.kwargs["headers"] == {"authorization": "Bearer token"}
    assert isinstance(client.http_client.kwargs["verify"], ssl.SSLContext)
    await client.close()
