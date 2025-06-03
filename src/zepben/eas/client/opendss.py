#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass
from typing import Union, Optional
from zepben.eas.client.work_package import GeneratorConfig, TimePeriod, FixedTime

__all__ = [
    "OpenDssConfig"
]

@dataclass
class OpenDssConfig:
    """ A data class representing the configuration for a opendss export """
    scenario: str
    year: int
    feeder: str
    load_time: Union[TimePeriod, FixedTime]
    generator_config: Optional[GeneratorConfig] = None
    model_name: Optional[str] = None
    is_public: Optional[bool] = None