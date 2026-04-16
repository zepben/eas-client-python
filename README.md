# Evolve App Server Python Client #

This library provides a wrapper to the Evolve App Server's API, allowing users of the Evolve SDK to authenticate with
the Evolve App Server and upload studies.

# Usage #

```python
from geojson import FeatureCollection
from zepben.eas import EasClient, StudyInput, StudyResultInput, GeoJsonOverlayInput, ResultSectionInput, SectionType, Mutation

eas_client = EasClient(
    host="<host>",
    port=1234,
    access_token="<access_token>",
    asynchronous=False,
)

eas_client.mutation(
    Mutation.add_studies(
        [
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
from zepben.eas import EasClient, StudyInput, StudyResultInput, GeoJsonOverlayInput, ResultSectionInput, SectionType, Mutation


async def upload():
    eas_client = EasClient(
        host="<host>",
        port=1234,
        access_token="<access_token>",
        asynchronous=True,  # returns all methods as plain async methods
    )

    await eas_client.mutation(
        Mutation.add_studies(
            [
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
            ]
        )
    )

    await eas_client.close()
```

# I'm used to the old client, what do i do? #

## Migrating existing code ##

Most of the objects passed into requests are similar.
The new EasClient is fully type hinted and self documenting.

For example.

```python
from zepben.eas import EasClient, WorkPackageInput, HcExecutorConfigInput, FeederConfigsInput, FeederConfigInput

client = EasClient(host='host', port=1234)
client.get_work_package_cost_estimation(
    WorkPackageInput(
        feederConfigs=FeederConfigsInput(
            configs=[
                FeederConfigInput(
                    feeder='myFeeder',
                    years=[2024, 2025],
                    scenarios=['scenario1']
                )
            ]
        )
    )
)
```

Hovering over any kwarg or looking at any class definition will show all possible parameters, and their expected types.

## Enabling legacy convenience methods ##

Legacy convenience methods can be enabled by passing `enable_legacy_methods` to `__init__` of `EasClient`. eg:

```python
from zepben.eas import EasClient

client = EasClient(enable_legacy_methods=True)
```

This will enable all `deprecated` and `opt_in` methods on the class, they are disabled by default.

# Development #

To regenerate the graphql client you will need to install `zepben.eas` with `eas-codegen` optional dependencies:

```shell
pip install -e ".[eas-codegen]"
```

With these installed and EAS running locally on port 7654, you can then generate the client:

```shell
python ariadne-codegen.py
```
