#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Generic, TypeVar, Optional

from zepben.eas import IngestionRunGraphQLField, IngestionRunFields, IngestorRunsFilterInput, IngestorRunsSortCriteriaInput

TGraphQLQueryField = TypeVar("TGraphQLQueryField")
TGraphQLField = TypeVar("TGraphQLField")


class GraphQLQuery(Generic[TGraphQLQueryField, TGraphQLField]):
    ...

    def fields(self, *fields: TGraphQLField):
        ...


class Query:

    @classmethod
    def list_ingestor_runs(
            cls,
            *,
            filter_: Optional[IngestorRunsFilterInput] = None,
            sort: Optional[IngestorRunsSortCriteriaInput] = None
    ) -> GraphQLQuery[IngestionRunFields, IngestionRunGraphQLField]:
        ...
