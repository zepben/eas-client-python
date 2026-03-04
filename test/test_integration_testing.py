#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import asyncio

from zepben.eas import EasClient


def test_can_connect_to_local_eas_non_async():
    client = EasClient(
        host="localhost",
        port=7654,
        protocol="http",
        verify_certificate=False,
        asynchronous=False,
    )
    assert client.get_ingestor_run_list() == {'data': {'listIngestorRuns': []}}


def test_can_connect_to_local_eas_async():
    client = EasClient(
        host="localhost",
        port=7654,
        protocol="http",
        verify_certificate=False,
        asynchronous=True
    )
    assert asyncio.run(client.get_ingestor_run_list()) == {'data': {'listIngestorRuns': []}}
