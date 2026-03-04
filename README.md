# Evolve App Server Python Client #

This library provides a wrapper to the Evolve App Server's API, allowing users of the evolve SDK to authenticate with
the Evolve App Server and upload studies.

# Usage #

```python
from geojson import FeatureCollection
from zepben.eas import EasClient, StudyInput, StudyResultInput, GeoJsonOverlayInput, ResultSectionInput, SectionType

eas_client = EasClient(
    host="<host>",
    port=1234,
    access_token="<access_token>",
    asynchronous=False,
)

eas_client.upload_study(
    StudyInput(
        name="<study name>",
        description="<study description>",
        tags=["<tag>", "<tag2>"],
        results=[
            StudyResultInput(
                name="<result_name>",
                geoJsonOverlay=GeoJsonOverlayInput(
                    data=FeatureCollection(...),
                    styles=["style1"]
                ),
                sections=[
                    ResultSectionInput(
                        type=SectionType.TABLE,
                        name="<table name>",
                        description="<table description>",
                        columns=[
                            {"key": "<column 1 key>", "name": "<column 1 name>"},
                            {"key": "<column 2 key>", "name": "<column 2 name>"},
                        ],
                        data=[
                            {"<column 1 key>": "<column 1 row 1 value>", "<column 2 key>": "<column 2 row 1 value>"},
                            {"<column 1 key>": "<column 1 row 2 value>", "<column 2 key>": "<column 2 row 2 value>"}
                        ]
                    )
                ]
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
The EasClient can operate in async mode if specified, like so:

```python
from aiohttp import ClientSession
from geojson import FeatureCollection
from zepben.eas import EasClient, StudyInput, StudyResultInput, GeoJsonOverlayInput, ResultSectionInput, SectionType


async def upload():
    eas_client = EasClient(
        host="<host>",
        port=1234,
        access_token="<access_token>",
        asynchronous=True,  # returns all methods as plain async methods
    )

    await eas_client.upload_study(
        StudyInput(
            name="<study name>",
            description="<study description>",
            tags=["<tag>", "<tag2>"],
            results=[
                StudyResultInput(
                    name="<result_name>",
                    geoJsonOverlay=GeoJsonOverlayInput(
                        data=FeatureCollection(...),
                        styles=["style1"]
                    ),
                    sections=[
                        ResultSectionInput(
                          type=SectionType.TABLE,
                          name="<table name>",
                          description="<table description>",
                          columns=[
                              {"key": "<column 1 key>", "name": "<column 1 name>"},
                              {"key": "<column 2 key>", "name": "<column 2 name>"},
                          ],
                          data=[
                              {"<column 1 key>": "<column 1 row 1 value>", "<column 2 key>": "<column 2 row 1 value>"},
                              {"<column 1 key>": "<column 1 row 2 value>", "<column 2 key>": "<column 2 row 2 value>"}
                          ]
                        )
                    ]
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

# Development #

To regenerate the graphql client you will need to install `zepben.eas` with `eas-codegen` optional dependencies, then run:

```shell
ariadne-codegen
```