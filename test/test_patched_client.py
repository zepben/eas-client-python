#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.eas import (
    FeederLoadAnalysisReportFields,
    EasClient,
    FeederLoadAnalysisSpecFields,
)


class MockResponse:
    def json(self):
        return dict(json="probably")

    def get_data(self, key: str):
        return dict(data="probably_also")

    def is_success(self):
        return True


def test_patched_client_used_in_eas_client():
    client = EasClient(host="test_host", port=9876)
    assert isinstance(client, EasClient)
    client.close()


def test_patched_client_overrides_get_data_to_return_the_whole_json_response():
    client = EasClient(host="test_host", port=9876)
    assert client.get_data(MockResponse()) == {"json": "probably"}
    client.close()


def test_all_fields():
    all_fields = list(FeederLoadAnalysisReportFields.all_fields())

    assert "completedAt" in [field._field_name for field in all_fields]
    assert any(isinstance(field, FeederLoadAnalysisSpecFields) for field in all_fields)
