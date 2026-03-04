#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.eas import EasClient
from zepben.eas.client.patched_generated_client import PatchedClient


class MockResponse:
    def json(self):
        return dict(json="probably")

    def get_data(self, key: str):
        return dict(data="probably_also")

    def is_success(self):
        return True


def test_patched_client_used_in_eas_client():

    client = EasClient(host="test_host", port=9876)
    assert isinstance(client._gql_client, PatchedClient)


def test_patched_client_overrides_get_data_to_return_the_whole_json_response():

    client = EasClient(host="test_host", port=9876)
    assert client._gql_client.get_data(MockResponse()) == {'json': 'probably'}
