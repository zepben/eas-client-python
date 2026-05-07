#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["catch_warnings", "async_func", "opt_in"]

import asyncio
import functools
import warnings
from typing import Callable


def catch_warnings(func: Callable) -> Callable:
    """
    Wrap a function in `warnings.catch_warnings()
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            return func(*args, **kwargs)

    return wrapper


# Type hinting async_func will break the type hinting.
#
# from typing import ParamSpec, TypeVar
# P = ParamSpec("P")
# R = TypeVar("R")
# def async_func(func: Callable[P, R]) -> Callable[P, R]:
def async_func(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._asynchronous:
            return func(self, *args, **kwargs)

        try:
            return asyncio.get_running_loop().run_until_complete(
                func(self, *args, **kwargs)
            )
        except RuntimeError:
            return asyncio.run(func(self, *args, **kwargs))

    return wrapper


def opt_in(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._opt_in_legacy:
            return func(self, *args, **kwargs)
        raise AttributeError(
            f"'{func.__qualname__}' is a legacy function and must be explicitly opted into."
        )

    return wrapper
