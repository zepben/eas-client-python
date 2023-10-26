#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.


__all__ = [
    "STORED_RESULTS_CONFIG_STORE_NONE",
    "STORED_RESULTS_CONFIG_STORE_ALL",
    "RAW_RESULTS_CONFIG_ALL_RAW_VALUES",
    "RAW_RESULTS_CONFIG_STANDARD",
    "RAW_RESULTS_CONFIG_BASIC",
    "METRICS_RESULTS_CONFIG_CALCULATE_PERFORMANCE_METRICS",
    "RESULTS_CONFIG_DEFAULT_RESULTS_CONFIG",
    "STANDARD_RESULTS_CONFIG",
    "BASIC_RESULTS_CONFIG",
]

from zepben.eas import StoredResultsConfig, RawResultsConfig, MetricsResultsConfig, ResultsConfig

STORED_RESULTS_CONFIG_STORE_NONE = StoredResultsConfig(
    energy_meters_raw=False,
    energy_meter_voltages_raw=False,
    over_loads_raw=False,
    voltage_exceptions_raw=False
)

STORED_RESULTS_CONFIG_STORE_ALL = StoredResultsConfig(
    energy_meters_raw=True,
    energy_meter_voltages_raw=True,
    over_loads_raw=True,
    voltage_exceptions_raw=True
)

RAW_RESULTS_CONFIG_ALL_RAW_VALUES = RawResultsConfig(
    energy_meters_raw=True,
    energy_meter_voltages_raw=True,
    results_per_meter=True,
    over_loads_raw=True,
    voltage_exceptions_raw=True
)

RAW_RESULTS_CONFIG_STANDARD = RawResultsConfig(
    energy_meters_raw=True,
    energy_meter_voltages_raw=True,
    results_per_meter=True,
    over_loads_raw=True,
    voltage_exceptions_raw=True
)

# BASIC everything in RawConfig to false.
# AT THE MOMENT it means that no raw results are going to be generated,
# however there's a task in the backlog to implement generating a summary
# for each meter; so even though raw results are not going to be produced, a
# message with a summary per meter will still be generated.
RAW_RESULTS_CONFIG_BASIC = RawResultsConfig()

METRICS_RESULTS_CONFIG_CALCULATE_PERFORMANCE_METRICS = MetricsResultsConfig(
    calculate_performance_metrics=True
)

RESULTS_CONFIG_DEFAULT_RESULTS_CONFIG = ResultsConfig(
    raw_config=RawResultsConfig(energy_meters_raw=True, energy_meter_voltages_raw=True),
    metrics_config=METRICS_RESULTS_CONFIG_CALCULATE_PERFORMANCE_METRICS,
    stored_results_config=STORED_RESULTS_CONFIG_STORE_NONE
)

STANDARD_RESULTS_CONFIG = ResultsConfig(
    raw_config=RAW_RESULTS_CONFIG_STANDARD,
    metrics_config=METRICS_RESULTS_CONFIG_CALCULATE_PERFORMANCE_METRICS,
    stored_results_config=StoredResultsConfig(voltage_exceptions_raw=True, over_loads_raw=True)
)

BASIC_RESULTS_CONFIG = ResultsConfig(
    raw_config=RAW_RESULTS_CONFIG_BASIC,
    metrics_config=METRICS_RESULTS_CONFIG_CALCULATE_PERFORMANCE_METRICS,
    stored_results_config=STORED_RESULTS_CONFIG_STORE_NONE
)
