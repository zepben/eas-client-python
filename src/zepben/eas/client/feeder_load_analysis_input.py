#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass
from typing import List, Optional

__all__ = [
    "FeederLoadAnalysisInput"
]

from zepben.eas.client.fla_forecast_config import FlaForecastConfig


@dataclass
class FeederLoadAnalysisInput:
    """ A data class representing the configuration for a feeder load analysis study """

    start_date: str
    """Start date for this analysis"""

    end_date: str
    """End date for this analysis"""

    fetch_lv_network: bool
    """Whether to stop analysis at distribution transformer"""

    process_feeder_loads: bool
    """Whether to include values corresponding to feeder event time points in the report"""

    process_coincident_loads: bool
    """Whether to include values corresponding to conductor event time points in the report"""

    aggregate_at_feeder_level: bool
    """Request for a report which aggregate all downstream load at the feeder level"""

    output: str
    """The file name of the resulting study"""

    feeders: Optional[List[str]] = None
    """The mRIDs of feeders to solve for feeder load analysis"""

    substations: Optional[List[str]] = None
    """The mRIDs of substations to solve for feeder load analysis"""

    sub_geographical_regions: Optional[List[str]] = None
    """The mRIDs of sub-Geographical Region to solve for feeder load analysis"""

    geographical_regions: Optional[List[str]] = None
    """The mRIDs of Geographical Region to solve for feeder load analysis"""

    fla_forecast_config: Optional[FlaForecastConfig] = None
    """The forecast configuration for this fla study"""
