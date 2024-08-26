## [0.7.0]

##### Breaking Changes
* Updated work package data classes to account for latest changes to hosting capacity work package configuration.
* Updated the WorkPackageConfig to include ResultsConfig
* The ModelConfig in a WorkPackageConfig is not optional anymore
* The ModelConfig now includes load time information
* The ModelConfig now includes a flag to signal the model is a calibration model

##### New Features

* Added basic client method to run hosting capacity work packages
* Added basic client method to cancel hosting capacity work packages
* Added basic client method to request hosting capacity work packages progress
* Added options to WorkPackageaConfig for:
    - Configuring load/export power factor.
    - Configuring running of NetworkFixer steps
* Added 'collapse_lv_networks' field to ModelConfig
* Added 'feeder_scenario_allocation_strategy' field to ModelConfig
* Added 'include_energy_consumer_meter_group' field to ModelConfig

##### Enhancements

* None.

##### Fixes

* None.

##### Notes

* None.
