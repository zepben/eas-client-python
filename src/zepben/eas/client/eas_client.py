#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import warnings

import requests
from urllib3.exceptions import InsecureRequestWarning
from zepben.eas.client.util import construct_url

from zepben.eas.client.study import Study
from zepben.auth.client import AuthMethod, ZepbenTokenFetcher, create_token_fetcher
from hashlib import sha256
from typing import Optional

__all__ = ["EasClient"]


class EasClient:
    """
    A class used to represent a client to the Evolve App Server, with methods that represent requests to its API.
    """

    def __init__(
            self,
            host: str,
            port: int,
            client_id: Optional[str] = None,
            token_fetcher: Optional[ZepbenTokenFetcher] = None,
            client_secret: Optional[str] = None,
            username: Optional[str] = None,
            password: Optional[str] = None,
            protocol: str = "https",
            verify_certificate: bool = False,
            ca_filename: Optional[str] = None
    ):
        """
        :param host: The host string of the Evolve App Server, including the protocol, e.g."https://evolve.local"
        :param port: The port on which to make requests to the Evolve App Server, e.g. 7624
        :param verify_certificate: Set this to False to disable SSH certificate verification
        """
        self._protocol = protocol
        self._host = host
        self._port = port
        self._verify_certificate = verify_certificate
        self._ca_filename = ca_filename
        if token_fetcher is not None:
            self._token_fetcher = token_fetcher
        elif client_id is not None:
            self._token_fetcher = create_token_fetcher(
                conf_address=construct_url(
                    protocol=protocol,
                    host=self._host,
                    port=self._port,
                    path="/api/config/auth"
                ),
                verify_certificates=self._verify_certificate,
                auth_type_field="configType",
                audience_field="audience",
                issuer_domain_field="issuerDomain"
            )
            if self._token_fetcher is not None:
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
                if username is not None and password is not None:
                    self._token_fetcher.token_request_data.update({
                        'grant_type': 'password',
                        'username': username,
                        'password':
                            sha256(password.encode('utf-8')).hexdigest()
                            if self._token_fetcher.auth_method is AuthMethod.SELF
                            else password
                    })
                    if client_secret is not None:
                        self._token_fetcher.token_request_data.update({'client_secret': client_secret})
                elif client_secret is not None:
                    self._token_fetcher.token_request_data.update({
                        'grant_type': 'client_credentials',
                        'client_secret': client_secret
                    })
                else:
                    raise ValueError(
                        "Incompatible arguments passed to connect to secured Evolve App Server. "
                        "You must specify at least (username, password) or (client_secret) for a secure connection "
                        "with token based auth.")
        else:
            self._token_fetcher = None

    def _get_request_headers(self, content_type: str = "application/json") -> dict:
        headers = {"content-type": content_type}
        if self._token_fetcher is None:
            return headers
        else:
            headers["authorization"] = self._token_fetcher.fetch_token()
        return headers

    def upload_study(
            self,
            study: Study
    ) -> requests.Response:
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
            return requests.post(
                construct_url(
                    protocol=self._protocol,
                    host=self._host,
                    port=self._port,
                    path="/api/graphql"
                ),
                headers=self._get_request_headers(),
                json=json,
                verify=self._verify_certificate and (self._ca_filename or True)
            )
