# Evolve App Server Python Client #

This library provides a wrapper to the Evolve App Server's API, allowing users of the evolve SDK to authenticate with
the Evolve App Server and upload studies.

# Usage #

```python
from zepben.eas import EasClient, Study

eas_client = EasClient(
    host="<host>",
    port=1234,
    client_id="<client_id>",
    username="<username>",
    password="<password>",
    client_secret="<client_secret>"
)

eas_client.upload_study(
    Study(
        name="<study name>",
        description="<study description>",
        tags=["<tag>", "<tag2>"],
        results=[
            Study.Result(
                name="<result_name>",
                geo_json_overlay=Study.Result.GeoJsonOverlay(
                    data=FeatureCollection( ... ),
                    styles=["style1"]
                ),
                sections=Study.Result.Section(
                    type="TABLE",
                    name="<table name>",
                    description = "<table description>",
                    columns=[
                        { "key": "<column 1 key>", "name": "<column 1 name>" },
                        { "key": "<column 2 key>", "name": "<column 2 name>" },
                    ],
                    data=[
                        { "<column 1 key>": "<column 1 row 1 value>", "<column 2 key>": "<column 2 row 1 value>" },
                        { "<column 1 key>": "<column 1 row 2 value>", "<column 2 key>": "<column 2 row 2 value>" }
                    ]
                )
            )
        ],
        styles=[
            {
                "id": "style1",
                # other Mapbox GL JS style properties
            }
        ]
    )
)

```