#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import asyncio

import pytest

from zepben.eas import EasClient, OpenDssModelInput, OpenDssModelGenerationSpecInput, OpenDssModelOptionsInput, \
    OpenDssModulesConfigInput, OpenDssCommonConfigInput


def test_can_connect_to_local_eas_non_async():
    client = EasClient(
        host="localhost",
        port=7654,
        protocol="http",
        verify_certificate=False,
        asynchronous=False,
        enable_legacy_methods=True,
    )
    assert client.get_ingestor_run_list() == {'data': {'listIngestorRuns': []}}


def test_can_connect_to_local_eas_async_asyncio_run_calling():
    client = EasClient(
        host="localhost",
        port=7654,
        protocol="http",
        verify_certificate=False,
        asynchronous=True,
        enable_legacy_methods = True,
    )
    assert asyncio.run(client.get_ingestor_run_list()) == {'data': {'listIngestorRuns': []}}


@pytest.mark.asyncio
async def test_can_connect_to_local_eas_async_calling_func():
    client = EasClient(
        host="localhost",
        port=7654,
        protocol="http",
        verify_certificate=False,
        asynchronous=True,
        enable_legacy_methods=True,
    )
    assert await client.get_ingestor_run_list() == {'data': {'listIngestorRuns': []}}
    print(await client.run_opendss_export(
        OpenDssModelInput(
            generationSpec=OpenDssModelGenerationSpecInput(
                modelOptions=OpenDssModelOptionsInput(feeder='feeder', scenario='foo', year=1),
                modulesConfiguration=OpenDssModulesConfigInput(common=OpenDssCommonConfigInput()),
            )
        )
    ))

