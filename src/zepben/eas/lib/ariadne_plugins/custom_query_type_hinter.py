#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import ast
from _ast import ClassDef

from ariadne_codegen.plugins.base import Plugin

class CustomQueryTypeHinterPlugin(Plugin):

    def generate_custom_module(self, module: ast.Module) -> ast.Module:
        for b in module.body:
            if isinstance((class_def := b), ClassDef):
                if class_def.name == "Query":
                    for method in class_def.body:
                        injected_type = method.returns.id.replace("Fields", "GraphQLField")
                        method.returns = ast.Name(
                            f'\"GraphQLQuery[{method.returns.id}, {injected_type}]\"'
                        )
                        module.body.extend(
                            [
                                ast.ImportFrom('.custom_typing_fields', [ast.alias(injected_type)], level=0),
                                ast.ImportFrom('zepben.eas.lib.ariadne_plugins.types', [
                                    ast.alias('GraphQLQuery')
                                ], level=0)
                            ]
                        )

        return module

