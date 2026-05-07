#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import ast
import pytest


@pytest.mark.skip("deleteme")
@pytest.mark.asyncio
async def test_do_things():
    from zepben.eas.lib import custom_queries

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
                    extra_imports.append(
                        func.returns.id.replace("Fields", "GraphQLField")
                    )
                    func.returns = ast.Name(
                        f'"GraphQLQuery[{func.returns.id}, {func.returns.id.replace("Fields", "GraphQLField")}]"'
                    )

    orig_ast.body.insert(
        n,
        ast.parse(
            """
class GraphQLQuery(Generic[TGraphQLQueryField, TGraphQLField]):
def fields(self, *fields: TGraphQLField):  ...
    """
        ).body[0],
    )
    orig_ast.body.insert(
        n, ast.parse('TGraphQLField = TypeVar("TGraphQLField")').body[0]
    )
    orig_ast.body.insert(
        n, ast.parse('TGraphQLQueryField = TypeVar("TGraphQLQueryField")').body[0]
    )

    orig_ast.body.insert(n, ast.parse("from typing import Generic, TypeVar").body[0])
    orig_ast.body.insert(
        n, ast.parse(f"from zepben.eas import {', '.join(extra_imports)}").body[0]
    )

    with open(custom_queries.__file__ + "i", "w") as f:
        f.write(ast.unparse(orig_ast))
