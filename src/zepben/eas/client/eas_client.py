#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import warnings

import requests
from urllib3.exceptions import InsecureRequestWarning
from zepben.auth.eas.authenticator import EasAuthenticator
from zepben.eas.client.study import Study

__all__ = ["EasClient"]


class EasClient:
    """
    A class used to represent a client to the Evolve App Server, with methods that represent requests to its API.
    """

    __host: str
    __port: int
    __verify_certificate: bool = True
    __access_token: str = None
    __authenticator = None

    def __init__(
            self,
            host: str,
            port: int,
            authenticator: EasAuthenticator = None,
            verify_certificate: bool = True
    ):
        """
        :param host: The host string of the Evolve App Server, including the protocol, e.g."https://evolve.local"
        :param port: The port on which to make requests to the Evolve App Server, e.g. 7624
        :param verify_certificate: Set this to False to disable SSH certificate verification
        """
        self.__host = host
        self.__port = port
        self.__authenticator = authenticator
        self.__verify_certificate = verify_certificate

    def __get_request_headers(self, content_type: str = "application/json") -> dict:
        headers = {"content-type": content_type}
        if self.__authenticator is None:
            return headers
        if self.__authenticator.get_server_config().auth_method is not self.__authenticator.ServerConfig.AuthMethod.NONE:
            headers["authorization"] = "Bearer {token}".format(token=self.__authenticator.get_token())
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
                "{host}:{port}/api/graphql".format(host=self.__host, port=self.__port),
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
