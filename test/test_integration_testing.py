#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import asyncio
from typing import TypeVar

import pytest

from zepben.eas import EasClient, OpenDssModelInput, OpenDssModelGenerationSpecInput, OpenDssModelOptionsInput, \
    OpenDssModulesConfigInput, OpenDssCommonConfigInput, Query, IngestionRunFields, GraphQLQuery, IngestionJobFields


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
    assert client.get_ingestor_run_list() == {'data': {'listIngestorRuns': []}}


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
    assert asyncio.run(client.get_ingestor_run_list()) == {'data': {'listIngestorRuns': []}}


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
    assert await client.get_ingestor_run_list() == {'data': {'listIngestorRuns': []}}
    print(await client.run_opendss_export(
        OpenDssModelInput(
            generationSpec=OpenDssModelGenerationSpecInput(
                modelOptions=OpenDssModelOptionsInput(feeder='feeder', scenario='foo', year=1),
                modulesConfiguration=OpenDssModulesConfigInput(common=OpenDssCommonConfigInput()),
            )
        )
    ))


T = TypeVar("T")
R = TypeVar("R")


def my_query(query: GraphQLQuery[T, R], field: R, *additional_fields: R) -> T:
    return query.fields(field, *additional_fields)


def test_do_things():
    my_query(Query.list_ingestor_runs(filter_=None, sort=None), IngestionRunFields.completed_at, IngestionRunFields.status)
    my_query(Query.list_ingestor_runs(filter_=None, sort=None), IngestionJobFields.application, 1)
    my_query(Query.list_ingestor_runs(filter_=None, sort=None))
