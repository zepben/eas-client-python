#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import ast
import asyncio
from typing import TypeVar, TYPE_CHECKING

import pytest

from zepben.eas import EasClient, OpenDssModelInput, OpenDssModelGenerationSpecInput, OpenDssModelOptionsInput, \
    OpenDssModulesConfigInput, OpenDssCommonConfigInput, Query, IngestionRunFields, IngestionJobFields

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

@pytest.mark.asyncio
async def test_do_things():
    from zepben.eas.lib.generated_graphql_client import custom_queries
    with open(custom_queries.__file__) as f:
        orig_ast = ast.parse(
            f.read(),
        )
    n = None
    extra_imports = []

    for i, b in enumerate(orig_ast.body):
        if isinstance(b, ast.ClassDef):
            if n is None:
                n = i
            for func in b.body:
                if isinstance(func, ast.FunctionDef):
                    func.body = [ast.Pass()]
                    extra_imports.append(func.returns.id.replace("Fields", "GraphQLField"))
                    func.returns = ast.Name(f'\"GraphQLQuery[{func.returns.id}, {func.returns.id.replace("Fields", "GraphQLField")}]\"')

    orig_ast.body.insert(n, ast.parse(
            """
class GraphQLQuery(Generic[TGraphQLQueryField, TGraphQLField]):
    def fields(self, *fields: TGraphQLField):  ...
        """
    ).body[0])
    orig_ast.body.insert(n, ast.parse(
            'TGraphQLField = TypeVar("TGraphQLField")'
    ).body[0])
    orig_ast.body.insert(n, ast.parse(
        'TGraphQLQueryField = TypeVar("TGraphQLQueryField")'
    ).body[0])

    orig_ast.body.insert(n, ast.parse("from typing import Generic, TypeVar").body[0])
    orig_ast.body.insert(n, ast.parse(f"from zepben.eas import {', '.join(extra_imports)}").body[0])

    with open(custom_queries.__file__ + 'i', 'w') as f:
        f.write(ast.unparse(orig_ast))

    client = EasClient(
        host="localhost",
        port=7654,
        asynchronous=True
    )
    await client.do_query(Query.list_ingestor_runs(filter_=None, sort=None), IngestionRunFields.completed_at, IngestionRunFields.status)
    await client.do_query(Query.list_ingestor_runs(filter_=None, sort=None), IngestionJobFields.application, 1)
    # my_query(Query.list_ingestor_runs(filter_=None, sort=None))
