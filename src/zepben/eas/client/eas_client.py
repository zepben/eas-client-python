#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import ssl
import warnings
from asyncio import get_event_loop
from hashlib import sha256
from typing import Optional

import aiohttp
from aiohttp import ClientSession
from urllib3.exceptions import InsecureRequestWarning
from zepben.auth import AuthMethod, ZepbenTokenFetcher, create_token_fetcher

from zepben.eas.client.study import Study
from zepben.eas.client.util import construct_url

__all__ = ["EasClient"]


class EasClient:
    """
    A class used to represent a client to the Evolve App Server, with methods that represent requests to its API.
    """

    def __init__(
        self,
        host: str,
        port: int,
        protocol: str = "https",
        client_id: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        client_secret: Optional[str] = None,
        token_fetcher: Optional[ZepbenTokenFetcher] = None,
        verify_certificate: bool = True,
        ca_filename: Optional[str] = None,
        session: ClientSession = None,
        json_serialiser = None
    ):
        """
        Construct a client for the Evolve App Server. If the server is HTTPS, authentication may be configured.
        Authentication may be configured in one of two ways:
            - Specifying the client ID of the Auth0 application via the client_id parameter, plus one of the following:
                - A username and password pair via the username and password parameters (account authentication)
                - The client secret via the client_secret parameter (M2M authentication)
              If this method is used, the auth configuration will be fetched from the Evolve App Server at the path
              "/api/config/auth".
            - Specifying a ZepbenTokenFetcher directly via the token_fetcher parameter

        Address parameters:
        :param host: The domain of the Evolve App Server, e.g. "evolve.local"
        :param port: The port on which to make requests to the Evolve App Server, e.g. 7624
        :param protocol: The protocol of the Evolve App Server. Should be either "http" or "https". Must be "https" if
                         auth is configured. (Defaults to "https")

        Authentication parameters:
        :param client_id: The Auth0 client ID used to specify to the auth server which application to request a token
                          for. (Optional)
        :param username: The username used for account authentication. (Optional)
        :param password: The password used for account authentication. (Optional)
        :param client_secret: The Auth0 client secret used for M2M authentication. (Optional)
        :param token_fetcher: A ZepbenTokenFetcher used to fetch auth tokens for access to the Evolve App Server.
                              (Optional)

        HTTP/HTTPS parameters:
        :param verify_certificate: Set this to False to disable certificate verification. This will also apply to the
                                   auth provider if auth is initialised via client id + username + password or
                                   client_id + client_secret. (Defaults to True)
        :param ca_filename: Path to CA file to use for verification. (Optional)
        :param session: aiohttp ClientSession to use, if not provided a new session will be created for you. You should
                        typically only use one aiohttp session per application.
        :param json_serialiser: JSON serialiser to use for requests e.g. ujson.dumps. (Defaults to json.dumps)
        """
        self._protocol = protocol
        self._host = host
        self._port = port
        self._verify_certificate = verify_certificate
        self._ca_filename = ca_filename
        if protocol != "https" and (token_fetcher or client_id):
            raise ValueError(
                "Incompatible arguments passed to connect to secured Evolve App Server. "
                "Authentication tokens must be sent via https. "
                "To resolve this issue, exclude the \"protocol\" argument when initialising the EasClient.")

        if token_fetcher and (client_id or client_secret or username or password):
            raise ValueError(
                "Incompatible arguments passed to connect to secured Evolve App Server. "
                "You cannot provide both a token_fetcher and credentials, "
                "please provide either client_id + client_secret, username + password, or token_fetcher."
            )

        if client_secret and (username or password):
            raise ValueError(
                "Incompatible arguments passed to connect to secured Evolve App Server. "
                "You cannot provide both a client_secret and username/password, "
                "please provide either client_id + client_secret or client_id + username + password."
            )

        if client_id:
            self._token_fetcher = create_token_fetcher(
                conf_address=f"{self._protocol}://{self._host}:{self._port}/api/config/auth",
                verify_conf=self._verify_certificate,
                auth_type_field="configType",
                audience_field="audience",
                issuer_domain_field="issuerDomain"
            )
            if self._token_fetcher:
                self._token_fetcher.token_request_data.update({
                    'client_id': client_id,
                    'scope':
                        'trusted' if self._token_fetcher.auth_method is AuthMethod.SELF
                        else 'offline_access openid profile email0'
                })
                self._token_fetcher.refresh_request_data.update({
                    "grant_type": "refresh_token",
                    'client_id': client_id,
                    'scope':
                        'trusted' if self._token_fetcher.auth_method is AuthMethod.SELF
                        else 'offline_access openid profile email0'
                })
                if username and password:
                    self._token_fetcher.token_request_data.update({
                        'grant_type': 'password',
                        'username': username,
                        'password':
                            sha256(password.encode('utf-8')).hexdigest()
                            if self._token_fetcher.auth_method is AuthMethod.SELF
                            else password
                    })
                    if client_secret:
                        self._token_fetcher.token_request_data.update({'client_secret': client_secret})
                elif client_secret:
                    self._token_fetcher.token_request_data.update({
                        'grant_type': 'client_credentials',
                        'client_secret': client_secret
                    })
                else:
                    raise ValueError(
                        "Incompatible arguments passed to connect to secured Evolve App Server. "
                        "You must specify at least (username, password) or (client_secret) for a secure connection "
                        "with token based auth.")
        elif token_fetcher:
            self._token_fetcher = token_fetcher
        else:
            self._token_fetcher = None

        if session is None:
            conn = aiohttp.TCPConnector(limit=200, limit_per_host=0)
            timeout = aiohttp.ClientTimeout(total=60)
            self.session = aiohttp.ClientSession(json_serialize=json_serialiser or json.dumps, connector=conn, timeout=timeout)
        else:
            self.session = session

    def close(self):
        return get_event_loop().run_until_complete(self.aclose())

    async def aclose(self):
        await self.session.close()

    def _get_request_headers(self, content_type: str = "application/json") -> dict:
        headers = {"content-type": content_type}
        if self._token_fetcher is None:
            return headers
        else:
            headers["authorization"] = self._token_fetcher.fetch_token()
        return headers

    def upload_study(self, study: Study):
        """
        Uploads a new study to the Evolve App Server
        :param study: An instance of a data class representing a new study
        """
        return get_event_loop().run_until_complete(self.async_upload_study(study))

    async def async_upload_study(self, study: Study):
        """
        Uploads a new study to the Evolve App Server
        :param study: An instance of a data class representing a new study
        :return: The HTTP response received from the Evolve App Server after attempting to upload the study
        """
        with warnings.catch_warnings():
            if not self._verify_certificate:
                warnings.filterwarnings("ignore", category=InsecureRequestWarning)
            json = {
                "query": """
                    mutation uploadStudy($study: StudyInput!) {
                        addStudies(studies: [$study])
                    }
                """,
                "variables": {
                    "study": {
                        "name": study.name,
                        "description": study.description,
                        "tags": study.tags,
                        "styles": study.styles,
                        "results": [{
                            "name": result.name,
                            "geoJsonOverlay": {
                                "data": result.geo_json_overlay.data,
                                "sourceProperties": result.geo_json_overlay.source_properties,
                                "styles": result.geo_json_overlay.styles
                            } if result.geo_json_overlay else None,
                            "stateOverlay": {
                                "data": result.state_overlay.data,
                                "styles": result.state_overlay.styles
                            } if result.state_overlay else None,
                            "sections": [{
                                "type": section.type,
                                "name": section.name,
                                "description": section.description,
                                "columns": section.columns,
                                "data": section.data
                            } for section in result.sections]
                        } for result in study.results]
                    }
                }
            }
            if self._verify_certificate:
                sslcontext = ssl.create_default_context(cafile=self._ca_filename)

            async with self.session.post(
                    construct_url(protocol=self._protocol, host=self._host, port=self._port, path="/api/graphql"),
                    headers=self._get_request_headers(),
                    json=json,
                    ssl=sslcontext if self._verify_certificate else False
            ) as response:
                if response.ok:
                    response = await response.json()
                else:
                    response = await response.text()
                return response
