#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import ast
from ariadne_codegen import Plugin


gql_field_all_fields_ast = ast.parse("""
@classmethod
def all_fields(cls) -> "Generator[GraphQLField | MethodType, None, None]":
    \"\"\"
    returns a generator over all ``GraphQLField``s that a given class returns

    :param cls: class to check
    :return: generator over all GraphQLField's in a given class
    \"\"\"
    import inspect

    for k in dir(cls):
        # we only want "public" attrs.
        if k.startswith("_"):
            continue
        # obviously we don't want to return ourselves.
        if k == "all_fields":
            continue

        v = getattr(cls, k)
        if isinstance(v, GraphQLField):
            yield v
        elif inspect.ismethod(v):
            yield v().fields(*v().all_fields())
""").body[0]

class GqlAllFieldsPlugin(Plugin):

    def copy_code(self, copied_code: str) -> str:
        code_as_ast = ast.parse(copied_code)
        for b in code_as_ast.body:
            if isinstance(class_def := b, ast.ClassDef):
                if class_def.name == "GraphQLField":
                    class_def.body.append(gql_field_all_fields_ast)
        return ast.unparse(code_as_ast)

