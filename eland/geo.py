#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

from typing import Any, Dict, List, Tuple, Union, TYPE_CHECKING

try:
    import geopandas
    from shapely.geometry import (
        GeometryCollection,
        LineString,
        MultiLineString,
        MultiPoint,
        MultiPolygon,
        Point,
        Polygon,
    )

    GEOPANDAS_INSTALLED = True
    GEO_TYPE_TO_ES_TYPE = {
        Point: "point",
        LineString: "linestring",
        Polygon: "polygon",
        MultiPoint: "multipoint",
        MultiLineString: "multilinestring",
        MultiPolygon: "multipolygon",
        GeometryCollection: "geometrycollection",
    }
except ImportError:
    GEOPANDAS_INSTALLED = False
    GEO_TYPE_TO_ES_TYPE = {}

if TYPE_CHECKING:
    from pandas import DataFrame, Series
    from geopandas import GeoDataFrame, GeoSeries


def is_geo_dataframe(dataframe: Union["DataFrame", "GeoDataFrame"]) -> bool:
    """Detects if a given dataframe is a :class:`geopandas.GeoDataFrame`"""
    if not GEOPANDAS_INSTALLED or not isinstance(dataframe, geopandas.GeoDataFrame):
        return False
    assert isinstance(dataframe, geopandas.GeoDataFrame)
    return True


def is_geo_series(series: Union["Series", "GeoSeries"]) -> bool:
    """Detects if a given series is a :class:`geopandas.GeoSeries`"""
    if not GEOPANDAS_INSTALLED or not isinstance(series, geopandas.GeoSeries):
        return False
    assert isinstance(series, geopandas.GeoSeries)
    return True


def shape_to_es(
    shape: Union[
        Point,
        LineString,
        Polygon,
        MultiPoint,
        MultiLineString,
        MultiPolygon,
        GeometryCollection,
    ]
) -> Dict[str, Any]:
    es_type = GEO_TYPE_TO_ES_TYPE.get(type(shape), None)
    if es_type is None:
        for geo_type, es_type in GEO_TYPE_TO_ES_TYPE.items():
            if isinstance(shape, geo_type):
                break
        else:
            raise ValueError(f"Unknown geometry type '{type(shape)}")

    if isinstance(shape, GeometryCollection):
        return {
            "type": es_type,
            "geometries": [shape_to_es(geom) for geom in shape.geoms],
        }
    return {"type": es_type, "coordinates": _shape_to_coords(shape)}


def _shape_to_coords(
    shape: Union[
        int,
        float,
        Tuple[float, ...],
        List[float],
        Point,
        LineString,
        Polygon,
        MultiPoint,
        MultiLineString,
        MultiPolygon,
        GeometryCollection,
    ]
) -> Union[float, List[Union[float, List[Union[float, List[float]]]]]]:
    if isinstance(shape, (int, float)):
        return shape
    # Coords are passed to this function as well so
    # we need to ensure that everything is a list.
    elif isinstance(shape, (tuple, list)):
        return list(shape)
    # All multi-polygon shapes are serialized in a list
    elif isinstance(
        shape, (MultiPoint, MultiLineString, MultiPolygon, GeometryCollection)
    ):
        return [_shape_to_coords(geom) for geom in shape.geoms]
    # Polygons needs to add exterior first then all potential holes
    elif isinstance(shape, Polygon):
        coords = [[_shape_to_coords(coord) for coord in shape.exterior.coords]]
        for interior in shape.interiors:
            coords.append([_shape_to_coords(coord) for coord in interior.coords])
        return coords
    # Lines and Points are serialized here.
    return [_shape_to_coords(coord) for coord in shape.coords]
