#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import ast
from ariadne_codegen import Plugin


class MissedImportCheckerPlugin(Plugin):

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
