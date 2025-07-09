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


@dataclass
class FeederLoadAnalysisInput:
    """ A data class representing the configuration for a feeder load analysis study """

    feeders: Optional[List[str]]
    """The mRIDs of feeders to solve for feeder load analysis"""

    substations: Optional[List[str]]
    """The mRIDs of substations to solve for feeder load analysis"""

    subGeographicalRegions: Optional[List[str]]
    """The mRIDs of sub-Geographical Region to solve for feeder load analysis"""

    geographicalRegions: Optional[List[str]]
    """The mRIDs of Geographical Region to solve for feeder load analysis"""

    startDate: str
    """Start date for this analysis"""

    endDate: str
    """End date for this analysis"""

    fetchLvNetwork: bool
    """Whether to stop analysis at distribution transformer"""

    processFeederLoads: bool
    """Whether to include values corresponding to feeder event time points in the report"""

    processCoincidentLoads: bool
    """Whether to include values corresponding to conductor event time points in the report"""

    produceBasicReport: bool
    """Request for a basic report"""

    produceConductorReport: bool
    """Request for an extensive report"""

    aggregateAtFeederLevel: bool
    """Request for a report which aggregate all downstream load at the feeder level"""

    output: str
    """The file name of the resulting study"""
