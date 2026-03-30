#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from _typeshed import Incomplete
from types import MethodType
from typing import Generator, Any

def __getattr__(name) -> Incomplete: ...

class GraphQLField:
    def __getattr__(self, name: str) -> Incomplete: ...

    @classmethod
    def all_fields(cls) -> Generator[GraphQLField | MethodType, None, None]:
        """
        Returns a generator over all ``GraphQLField``s that a given class returns

        :param cls: class to check
        :return: generator over all GraphQLField's in a given class
        """
