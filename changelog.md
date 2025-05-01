# EAS Python client
## [0.18.0] - UNRELEASED
### Breaking Changes
* None.

### New Features
* Update `ModelConfig` to contain an optional `transformer_tap_settings` field to specify a set of distribution transformer tap settings to be applied by the model-processor.

### Enhancements
* Added work package config documentation.

### Fixes
* None.

### Notes
* None.

## [0.17.0] - 2025-03-10
### Breaking Changes
* None.

### New Features
* Update `ModelConfig` to contain four optional list of values which makes up the default load profile for hosting capacity model generation.
  * `default_load_watts` Note: expects same size list of values as `default_load_var` 
  * `default_gen_watts` Note: expects same size list of values as `default_gen_var`
  * `default_load_var`
  * `default_gen_var`

### Enhancements
* None.

### Fixes
* None.

### Notes
* None.

## [0.16.0] - 2024-12-02
### Breaking Changes
* Updated `WorkPackageConfig` constructor to reorder the parameters and no longer provide a default value for `name`. A `name` must now be provided by the user.

### New Features
* Support specifying a `seed` in `ModelConfig` to allow reproducible scenarios
* Support for using access tokens for authentication that takes advantage of the new EAS personal access token authentication system. You can now pass an access_token to `EasClient` which is an EAS provisioned JWT.

### Enhancements
* Update requests restrictions to support all version 2 minor versions.
* Removed check that prevented passing a `client_secret` for "password" grant_type.

### Fixes
* Update to released version of zepben.auth (0.12.1) to support up to requests v3.0.0.

### Notes
* None.

## [0.7.0]
### Breaking Changes
* Updated work package data classes to account for latest changes to hosting capacity work package configuration.
* Updated the WorkPackageConfig to include ResultsConfig
* The ModelConfig in a WorkPackageConfig is not optional anymore
* The ModelConfig now includes load time information
* The ModelConfig now includes a flag to signal the model is a calibration model

### New Features

* Added basic client method to run hosting capacity work packages
* Added basic client method to cancel hosting capacity work packages
* Added basic client method to request hosting capacity work packages progress
* Added options to WorkPackageaConfig for:
    - Configuring load/export power factor.
    - Configuring running of NetworkFixer steps
* Added 'collapse_lv_networks' field to ModelConfig
* Added 'feeder_scenario_allocation_strategy' field to ModelConfig
* Added 'include_energy_consumer_meter_group' field to ModelConfig
* Added support for specifying a work package name in the `WorkPackageConfig`.
* Now support auth with Entra ID, including Azure managed identities


### Enhancements

* None.

### Fixes

* None.

### Notes

* None.
