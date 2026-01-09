#  Copyright 2025 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.eas.client.feeder_load_analysis_input import FeederLoadAnalysisInput
from zepben.eas.client.fla_forecast_config import FlaForecastConfig


def test_feeder_load_analysis_constructor():
    feeder_load_analysis_input = FeederLoadAnalysisInput(
        feeders=["feeder123"],
        substations=["sub1"],
        sub_geographical_regions=["sgr1"],
        geographical_regions=["gr1"],
        start_date="2022-04-01",
        end_date="2022-12-31",
        fetch_lv_network=True,
        process_feeder_loads=True,
        process_coincident_loads=True,
        aggregate_at_feeder_level=False,
        output="Test",
        fla_forecast_config=FlaForecastConfig(
            scenario_id="1",
            year=2030,
            pv_upgrade_threshold=8000,
            bess_upgrade_threshold=8000,
            seed=64513
        )
    )

    assert feeder_load_analysis_input is not None
    assert feeder_load_analysis_input.feeders == ["feeder123"]
    assert feeder_load_analysis_input.substations == ["sub1"]
    assert feeder_load_analysis_input.sub_geographical_regions == ["sgr1"]
    assert feeder_load_analysis_input.geographical_regions == ["gr1"]
    assert feeder_load_analysis_input.start_date == "2022-04-01"
    assert feeder_load_analysis_input.end_date == "2022-12-31"
    assert feeder_load_analysis_input.fetch_lv_network == True
    assert feeder_load_analysis_input.process_feeder_loads == True
    assert feeder_load_analysis_input.process_coincident_loads == True
    assert feeder_load_analysis_input.aggregate_at_feeder_level == False
    assert feeder_load_analysis_input.output == "Test"
    assert feeder_load_analysis_input.fla_forecast_config.scenario_id == "1"
    assert feeder_load_analysis_input.fla_forecast_config.year == 2030
    assert feeder_load_analysis_input.fla_forecast_config.pv_upgrade_threshold == 8000
    assert feeder_load_analysis_input.fla_forecast_config.bess_upgrade_threshold == 8000
    assert feeder_load_analysis_input.fla_forecast_config.seed == 64513
