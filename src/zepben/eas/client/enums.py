#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["OpenDssModelState"]

from enum import Enum

__doc__ = """
    This file should ONLY contain enums that the gql generator misses.
    Ideally it should be non existent.
"""

class OpenDssModelState(Enum):
    COULD_NOT_START = 'COULD_NOT_START'
    CREATION = 'CREATION'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
