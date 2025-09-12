#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass
from typing import Optional

__all__ = [
    "FlaForecastConfig"
]


@dataclass
class FlaForecastConfig:
    """ A data class representing the configuration for a forecast portion of a feeder load analysis study """

    scenario_id: str
    """The id of forecast scenario"""

    year: int
    """The year for forecast model"""

    pv_upgrade_threshold: Optional[int] = 5000
    """Watts threshold to indicate if a customer site will gain additional pv during scenario application (Default to 5000)."""

    bess_upgrade_threshold: Optional[int] = 5000
    """Watts threshold to indicate if a customer site will gain additional battery during scenario application (Default to 5000)."""

    seed: Optional[int] = 123
    """Seed for scenario application (Default to 123)."""
