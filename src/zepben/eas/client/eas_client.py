#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["EasClient"]

import importlib
import ssl
from http import HTTPStatus
from typing import Any, TYPE_CHECKING, TypeVar, cast

import httpx
from graphql import OperationType

from zepben.eas.lib.sync import (
    Client as SyncClient,
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQLClientInvalidResponseError,
)
from zepben.eas.lib.sync.base_operation import GraphQLField

AsyncClient = importlib.import_module("zepben.eas.lib.async").Client

if TYPE_CHECKING:
    from zepben.eas import GraphQLQuery

T = TypeVar("T")
R = TypeVar("R")


class _EasClientMeta(type):
    """Select the generated client implementation without exposing it publicly."""

    def __call__(cls, *args, **kwargs):
        if cls is EasClient:
            implementation = (
                _AsyncEasClient if kwargs.get("asynchronous", False) else _SyncEasClient
            )
            return type.__call__(implementation, *args, **kwargs)
        return super().__call__(*args, **kwargs)


class EasClient(metaclass=_EasClientMeta):
    """A client for the Evolve App Server.

    ``asynchronous=False`` returns results directly. With ``asynchronous=True``,
    the same methods return awaitables. The generated backing client is selected
    internally and is not part of this public API.
    """

    def __init__(
        self,
        *,
        host: str,
        port: int,
        protocol: str = "https",
        access_token: str | None = None,
        verify_certificate: bool = True,
        ca_filename: str | None = None,
        asynchronous: bool = False,
    ):
        self._asynchronous = asynchronous
        self._protocol = protocol
        self._host = host
        self._port = port
        self._base_url = f"{protocol}://{host}:{port}"

        verify: ssl.SSLContext | bool = False
        if verify_certificate:
            try:
                verify = ssl.create_default_context(cafile=ca_filename)
            except ssl.SSLError:
                verify = ssl.create_default_context(capath=ca_filename)

        super().__init__(
            f"{self._base_url}/api/graphql",
            http_client=self._http_client(access_token, verify),
        )

    def _http_client(self, access_token: str | None, verify: ssl.SSLContext | bool):
        raise NotImplementedError

    def get_data(self, response: httpx.Response) -> dict[str, Any]:
        """Return the complete GraphQL response, including its ``data`` key."""
        if not response.is_success:
            raise GraphQLClientHttpError(
                status_code=response.status_code, response=response
            )
        try:
            response_json = response.json()
        except ValueError as exc:
            raise GraphQLClientInvalidResponseError(response=response) from exc

        try:
            errors = response_json.get("errors")
        except AttributeError:
            errors = None
        if errors:
            raise GraphQLClientGraphQLMultiError.from_errors_dicts(
                errors_dicts=errors, data=response_json
            )
        return cast(dict[str, Any], response_json)

    # These declarations keep the complete public API discoverable on EasClient.
    # Concrete implementations below supply synchronous or asynchronous behavior.
    def close(self):
        raise NotImplementedError

    def query(
        self, query: GraphQLQuery[T, R], *returned_fields: R, operation_name: str = None
    ) -> T:
        raise NotImplementedError

    def mutation(
        self, *fields: GraphQLField, operation_name: str = None
    ) -> dict[str, Any]:
        raise NotImplementedError

    def execute_custom_operation(
        self,
        *fields: GraphQLField,
        operation_type: OperationType,
        operation_name: str = None,
    ) -> dict[str, Any]:
        raise NotImplementedError

    def get_opendss_model_download_url(self, run_id: int):
        raise NotImplementedError


class _SyncEasClient(EasClient, SyncClient):
    def _http_client(self, access_token, verify):
        return httpx.Client(
            headers={"authorization": f"Bearer {access_token}"}
            if access_token
            else None,
            verify=verify,
        )

    def close(self):
        self.http_client.close()

    def query(
        self, query: GraphQLQuery[T, R], *returned_fields: R, operation_name: str = None
    ) -> T:
        query = query.fields(*returned_fields) if hasattr(query, "fields") else query
        return super(EasClient, self).query(query, operation_name=operation_name)

    def mutation(
        self, *fields: GraphQLField, operation_name: str = None
    ) -> dict[str, Any]:
        return super(EasClient, self).mutation(*fields, operation_name=operation_name)

    def execute_custom_operation(
        self,
        *fields: GraphQLField,
        operation_type: OperationType,
        operation_name: str = None,
    ) -> dict[str, Any]:
        return super(EasClient, self).execute_custom_operation(
            *fields,
            operation_type=operation_type,
            operation_name=operation_name or "-".join(f._field_name for f in fields),
        )

    def get_opendss_model_download_url(self, run_id: int):
        response = self.http_client.get(
            f"{self._base_url}/api/opendss-model/{run_id}",
            headers=self.headers,
            follow_redirects=False,
        )
        if response.status_code == HTTPStatus.FOUND:
            return response.headers["Location"]
        if not response.is_success:
            response.raise_for_status()


class _AsyncEasClient(EasClient, AsyncClient):
    def _http_client(self, access_token, verify):
        return httpx.AsyncClient(
            headers={"authorization": f"Bearer {access_token}"}
            if access_token
            else None,
            verify=verify,
        )

    async def close(self):
        await self.http_client.aclose()

    async def query(
        self, query: GraphQLQuery[T, R], *returned_fields: R, operation_name: str = None
    ) -> T:
        query = query.fields(*returned_fields) if hasattr(query, "fields") else query
        return await super(EasClient, self).query(query, operation_name=operation_name)

    async def mutation(
        self, *fields: GraphQLField, operation_name: str = None
    ) -> dict[str, Any]:
        return await super(EasClient, self).mutation(
            *fields, operation_name=operation_name
        )

    async def execute_custom_operation(
        self,
        *fields: GraphQLField,
        operation_type: OperationType,
        operation_name: str = None,
    ) -> dict[str, Any]:
        return await super(EasClient, self).execute_custom_operation(
            *fields,
            operation_type=operation_type,
            operation_name=operation_name or "-".join(f._field_name for f in fields),
        )

    async def get_opendss_model_download_url(self, run_id: int):
        response = await self.http_client.get(
            f"{self._base_url}/api/opendss-model/{run_id}",
            headers=self.headers,
            follow_redirects=False,
        )
        if response.status_code == HTTPStatus.FOUND:
            return response.headers["Location"]
        if not response.is_success:
            response.raise_for_status()
