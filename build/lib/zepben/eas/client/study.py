from dataclasses import dataclass, field
from typing import List, Any

from geojson import GeoJSON


@dataclass
class Study:
    """ A data class representing an Evolve App Server study """

    @dataclass
    class Result:
        """ A data class representing an Evolve App Server study result """

        @dataclass
        class GeoJsonOverlay:
            """ A data class representing an Evolve App Server study result GeoJSON overlay """
            data: GeoJSON
            styles: List[str]
            source_properties: Any = None

        @dataclass
        class StateOverlay:
            """ A data class representing an Evolve App Server study result state overlay """
            data: None
            styles: List[str]

        @dataclass
        class Section:
            """ A data class representing an Evolve App Server study result data section """
            type: str
            name: str
            description: str
            columns: Any
            data: Any

        name: str
        geo_json_overlay: GeoJsonOverlay = None
        state_overlay: StateOverlay = None
        sections: List[Section] = field(default_factory=lambda: [])

    name: str
    created_by: str
    description: str
    tags: List[str]
    results: List[Result]
    styles: List[Any]
