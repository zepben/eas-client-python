#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import ast
from _ast import ImportFrom
from typing import Callable, Any

from ariadne_codegen.plugins.base import Plugin

class CustomQueryTypeHinterPlugin(Plugin):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._current_class = None

    def generate_custom_method(self, method: ast.FunctionDef) -> ast.FunctionDef:
        return method

    def generate_custom_module(self, imports: list[ImportFrom], type_imports: list[ImportFrom], class_defs: list[ast.ClassDef]) -> tuple[list[ImportFrom], list[ImportFrom], list[ast.ClassDef]]:
        # 1. Target a specific class (e.g., the root 'Query' result)
        if class_defs[0].name == "Query":
            for method in class_defs[0].body:
                injected_type = method.returns.id.replace("Fields", "GraphQLField")
                method.returns = ast.Name(
                    f'\"GraphQLQuery[{method.returns.id}, {injected_type}]\"'
                )
                imports.extend(
                    [
                        ImportFrom('.custom_typing_fields', [ast.alias(injected_type)], level=0),
                        ImportFrom('zepben.eas.lib.ariadne_plugins.types', [
                            ast.alias('GraphQLQuery')
                        ], level=0)
                    ]
                )

        return imports, type_imports, class_defs

    def generate_client_import(self, import_: ast.ImportFrom) -> ast.ImportFrom:
        if (iname := import_.names[0].name) in (
                'SincalFileType',
                'VariantFileType',
                'ContainerType',
                'HostingCapacityFileType',
                'WorkflowStatus',
        ):
            if import_.module is None:
                print(f"[ZBEX] Assuming class import {iname} is from module 'enums.py'")
                import_.module = 'enums'
        return import_

