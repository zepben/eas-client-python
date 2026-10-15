#!/usr/bin/env python3
#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Remove schema files duplicated by the async Ariadne Codegen invocation."""

from pathlib import Path


ASYNC_PACKAGE = Path("src/zepben/eas/lib/async")
SCHEMA_MODULES = (
    "base_model.py",
    "base_operation.py",
    "custom_fields.py",
    "custom_mutations.py",
    "custom_queries.py",
    "custom_typing_fields.py",
    "enums.py",
    "exceptions.py",
    "input_types.py",
    "types.py",
)


for module in SCHEMA_MODULES:
    (ASYNC_PACKAGE / module).unlink(missing_ok=True)
