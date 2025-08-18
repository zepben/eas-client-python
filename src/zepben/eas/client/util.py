#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["construct_url", "snake_to_camel"]

from typing import Union


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
