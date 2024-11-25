# Evolve App Server Python Client #

This library provides a wrapper to the Evolve App Server's API, allowing users of the evolve SDK to authenticate with
the Evolve App Server and upload studies.

# Usage #

```python
from geojson import FeatureCollection
from zepben.eas import EasClient, Study, Result, Section, GeoJsonOverlay

eas_client = EasClient(
    host="<host>",
    port=1234,
    access_token="<access_token>",
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
            Result(
                name="<result_name>",
                geo_json_overlay=GeoJsonOverlay(
                    data=FeatureCollection( ... ),
                    styles=["style1"]
                ),
                sections=Section(
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

eas_client.close()
```

## AsyncIO ##
Asyncio is also supported using aiohttp. A session will be created for you when you create an EasClient if not provided via the `session` parameter to EasClient.

To use the asyncio API use `async_upload_study` like so:

```python
from aiohttp import ClientSession
from geojson import FeatureCollection
from zepben.eas import EasClient, Study, Result, Section, GeoJsonOverlay

async def upload():
    eas_client = EasClient(
        host="<host>",
        port=1234,
        access_token="<access_token>",
        client_id="<client_id>",
        username="<username>",
        password="<password>",
        client_secret="<client_secret>",
        session=ClientSession(...)
    )

    await eas_client.async_upload_study(
        Study(
            name="<study name>",
            description="<study description>",
            tags=["<tag>", "<tag2>"],
            results=[
                Result(
                    name="<result_name>",
                    geo_json_overlay=GeoJsonOverlay(
                        data=FeatureCollection( ... ),
                        styles=["style1"]
                    ),
                    sections=Section(
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

    await eas_client.aclose()
```