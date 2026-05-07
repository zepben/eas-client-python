#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import asyncio
from typing import TYPE_CHECKING

import pytest

from zepben.eas import (
    EasClient,
    OpenDssModelInput,
    OpenDssModelGenerationSpecInput,
    OpenDssModelOptionsInput,
    OpenDssModulesConfigInput,
    OpenDssCommonConfigInput,
    Query,
    IngestionRunFields,
    IngestionJobFields,
)

if TYPE_CHECKING:
    from zepben.eas import GraphQLQuery


@pytest.mark.skip("Local testing if you really want it...")
def test_can_connect_to_local_eas_non_async():
    client = EasClient(
        host="localhost",
        port=7654,
        protocol="http",
        verify_certificate=False,
        asynchronous=False,
        enable_legacy_methods=True,
    )
    assert client.get_ingestor_run_list() == {"data": {"listIngestorRuns": []}}


@pytest.mark.skip("Local testing if you really want it...")
def test_can_connect_to_local_eas_async_asyncio_run_calling():
    client = EasClient(
        host="localhost",
        port=7654,
        protocol="http",
        verify_certificate=False,
        asynchronous=True,
        enable_legacy_methods=True,
    )
    assert asyncio.run(client.get_ingestor_run_list()) == {
        "data": {"listIngestorRuns": []}
    }


@pytest.mark.skip("Local testing if you really want it...")
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
    assert await client.get_ingestor_run_list() == {"data": {"listIngestorRuns": []}}
    print(
        await client.run_opendss_export(
            OpenDssModelInput(
                generationSpec=OpenDssModelGenerationSpecInput(
                    modelOptions=OpenDssModelOptionsInput(
                        feeder="feeder", scenario="foo", year=1
                    ),
                    modulesConfiguration=OpenDssModulesConfigInput(
                        common=OpenDssCommonConfigInput()
                    ),
                )
            )
        )
    )


@pytest.mark.skip("only displays type hinting in client.query call")
@pytest.mark.asyncio
async def test_do_things():
    client = EasClient(host="localhost", port=7654, asynchronous=True)
    try:
        await client.query(
            Query.list_ingestor_runs(filter_=None, sort=None),
            IngestionRunFields.completed_at,
            IngestionRunFields.status,
        )
        await client.query(
            Query.list_ingestor_runs(filter_=None, sort=None),
            IngestionJobFields.application,
            1,
        )
    except:
        pass
    # my_query(Query.list_ingestor_runs(filter_=None, sort=None))
