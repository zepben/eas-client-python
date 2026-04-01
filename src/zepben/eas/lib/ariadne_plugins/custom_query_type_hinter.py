#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import ast
from ariadne_codegen.plugins.base import Plugin

class CustomQueryTypeHinterPlugin(Plugin):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._current_class = None
        self._all_imports = set()

    def generate_custom_method(self, method: ast.FunctionDef) -> ast.FunctionDef:
        return method

    def generate_custom_module(self, module: ast.Module, **kwargs) -> ast.Module:
        for b in module.body:
            if isinstance((class_def := b), ast.ClassDef):
                # 1. Target a specific class (e.g., the root 'Query' result)
                if class_def.name == "Query":
                    for method in class_def.body:
                        method.body = [ast.Pass()]
                        method.returns = ast.Name(
                            f'\"GraphQLQuery[{method.returns.id}, {method.returns.id.replace("Fields", "GraphQLField")}]\"'
                        )

        print(next(b for b in module.body if isinstance(b, ast.ClassDef)).name)
        return module

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
