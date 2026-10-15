#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Make the generated async transport reuse the synchronous schema package."""

import ast

from ariadne_codegen.plugins.base import Plugin


class SharedAsyncSchemaPlugin(Plugin):
    """Generate only the async transport surface in ``zepben.eas.lib.async``."""

    def generate_init_module(self, module: ast.Module) -> ast.Module:
        module.body = ast.parse(
            """
from .async_base_client import AsyncBaseClient
from .client import Client

__all__ = ["AsyncBaseClient", "Client"]
"""
        ).body
        return module

    def generate_client_module(self, module: ast.Module) -> ast.Module:
        for node in module.body:
            if (
                isinstance(node, ast.ImportFrom)
                and node.level == 1
                and node.module == "base_operation"
            ):
                node.level = 2
                node.module = "sync.base_operation"
        return module

    def copy_code(self, copied_code: str) -> str:
        return copied_code.replace(
            "from .base_model import", "from ..sync.base_model import"
        ).replace("from .exceptions import", "from ..sync.exceptions import")
