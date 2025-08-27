#  Copyright 2025 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["construct_url", "snake_to_camel", "HostingCapacityDataclass"]

import inspect
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Union, Any, Generator, Tuple


def construct_url(protocol, host, path, port: Union[str, int] = None) -> str:
    return f"{protocol}://{host}{f':{port}' if port else ''}{path}"

def snake_to_camel(snake_str):
    """
    Converts a snake_case string to camelCase.

    :param snake_str: The string in snake_case format (e.g., "my_variable_name").
    :returns: The string in camelCase format (e.g., "myVariableName").
    """
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

@dataclass
class HostingCapacityDataclass(ABC):  # TODO: Another terrible name
    _snake_to_camel_overrides = dict(
        load_vmin_pu = 'loadVMinPu',
        load_vmax_pu = 'loadVMaxPu',
        gen_vmin_pu = 'genVMinPu',
        gen_vmax_pu = 'genVMaxPu',
        collapse_swer = 'collapseSWER',
        split_phase_lv_kv = 'splitPhaseLVKV',
        norm_vmin_pu = 'normVMinPu',
        norm_vmax_pu = 'normVMaxPu',
        emerg_vmin_pu = 'emergVMinPu',
        emerg_vmax_pu = 'emergVMaxPu',
        calculate_co2 = 'calculateCO2'
    )

    def to_json(self) -> Any:
        def _process_value(_value):
            if isinstance(_value, HostingCapacityDataclass):
                return _value.to_json()
            elif isinstance(_value, Enum):
                return _value.value
            elif isinstance(_value, datetime):
                return _value.isoformat()
            elif isinstance(_value, list):
                return [_process_value(i) for i in _value]
            elif isinstance(_value, dict):
                return {k: _process_value(v) for k, v in _value.items()}
            elif isinstance(_value, (str, int, float)):
                return _value
            elif _value is None:
                return None
            else:
                raise TypeError(f"Unsupported value type: {_value}")
        return {self._snake_to_camel_overrides.get(k, snake_to_camel(k)): _process_value(v) for k, v in self._public_attrs()}

    @classmethod
    def build_gql_query_object_model(cls):
        def _process_value(_value):
            """
            This is required for nested types, eg: Optional[MyClass]
            """
            try:
                try:
                    clazz = _value.__args__[0]
                except AttributeError:
                    return None
                if issubclass(clazz, HostingCapacityDataclass):
                    return clazz.build_gql_query_object_model()
            except TypeError:
                # This handles recursive nested types: Optional[List[MyClass]]
                try:
                    if clazz._name == 'List':
                        return _process_value(clazz)
                except AttributeError:
                    pass
            return None

        def _get_str(k, v):
            _rv = cls._snake_to_camel_overrides.get(k, snake_to_camel(k))
            _pv = _process_value(v)
            if _pv is None:
                return _rv
            return _rv + " { " + _pv + " }"

        # Iterate over all object attrs, convert them into camel case space delimited strings, if the hinted type of the
        #  attr is a subclass of HostingCapacityDataclass, then we want to process it and return the desired string.
        return ' '.join(_get_str(k, v) for k, v in inspect.get_annotations(cls).items() if not k.startswith("_"))

    def _public_attrs(self) -> Generator[Tuple[str, Any], None, None]:
        for k, v in self.__dict__.items():
            if not k.startswith("_"):
                yield k, v

