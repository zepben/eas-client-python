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
from zepben.auth import ZepbenAuthenticator, create_authenticator, AuthMethod
from hashlib import sha256
from typing import Optional

__all__ = ["EasClient"]


class EasClient:
    """
    A class used to represent a client to the Evolve App Server, with methods that represent requests to its API.
    """

    __protocol: str
    __host: str
    __port: int
    __authenticator: Optional[ZepbenAuthenticator]
    __verify_certificate: bool = True
    __access_token: str = None
    _authenticator = None

    def __init__(
            self,
            host: str,
            port: int,
            client_id: str,
            authenticator: Optional[ZepbenAuthenticator] = None,
            client_secret: Optional[str] = None,
            username: Optional[str] = None,
            password: Optional[str] = None,
            protocol: str = "https",
            verify_certificate: bool = True
    ):
        """
        :param host: The host string of the Evolve App Server, including the protocol, e.g."https://evolve.local"
        :param port: The port on which to make requests to the Evolve App Server, e.g. 7624
        :param verify_certificate: Set this to False to disable SSH certificate verification
        """
        self.__protocol = protocol
        self.__host = host
        self.__port = port
        self.__verify_certificate = verify_certificate
        if authenticator is not None:
            self.__authenticator = authenticator
        else:
            self.__authenticator = create_authenticator(
                conf_address=construct_url(
                    protocol="https",
                    host=self.__host,
                    port=self.__port,
                    path="/api/config/auth"
                ),
                verify_certificate=self.__verify_certificate,
                auth_type_field="configType",
                audience_field="audience",
                issuer_domain_field="issuerDomain"
            )
            if self.__authenticator is not None:
                if client_id is None:
                    raise ValueError(
                        "Incompatible arguments passed to connect to secured Evolve App Server. You must specify (client_id) "
                        "to establish a secure connection with token based auth.")
                self.__authenticator.token_request_data.update({
                    'client_id': client_id,
                    'scope': 'trusted' if self.__authenticator.auth_method is AuthMethod.SELF else 'offline_access openid profile email0'
                })
                self.__authenticator.refresh_request_data.update({
                    "grant_type": "refresh_token",
                    'client_id': client_id,
                    'scope': 'trusted' if self.__authenticator.auth_method is AuthMethod.SELF else 'offline_access openid profile email0'
                })
                if username is not None and password is not None:
                    self.__authenticator.token_request_data.update({
                        'grant_type': 'password',
                        'username': username,
                        'password': sha256(password.encode('utf-8')).hexdigest() if self.__authenticator.auth_method is AuthMethod.SELF else password
                    })
                    if client_secret is not None:
                        self.__authenticator.token_request_data.update({'client_secret': client_secret})
                elif client_secret is not None:
                    self.__authenticator.token_request_data.update({
                        'grant_type': 'client_credentials',
                        'client_secret': client_secret
                    })
                else:
                    raise ValueError(
                        "Incompatible arguments passed to connect to secured Evolve App Server. You must specify at least "
                        "(username, password) or (client_secret) for a secure connection with token based auth.")

    def __get_request_headers(self, content_type: str = "application/json") -> dict:
        headers = {"content-type": content_type}
        if self.__authenticator is None:
            return headers
        else:
            headers["authorization"] = self.__authenticator.fetch_token()
        return headers

    def upload_study(
            self,
            study: Study
    ):
        """
        Uploads a new study to the Evolve App Server
        :param study: An instance of a data class representing a new study
        """
        with warnings.catch_warnings():
            if self.__verify_certificate is False:
                warnings.filterwarnings("ignore", category=InsecureRequestWarning)
            requests.post(
                construct_url(
                    protocol=self.__protocol,
                    host=self.__host,
                    port=self.__port,
                    path="/api/graphql"
                ),
                headers=self.__get_request_headers(),
                json={
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
                },
                verify=self.__verify_certificate
            )
