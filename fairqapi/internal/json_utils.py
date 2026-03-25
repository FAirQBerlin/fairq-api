"""Internal json helper functions."""

import ast


def df_to_geojson(df, properties, geometry_type="Point"):
    """
    Transform pandas df into geojson format.

    :param pd.DataFrame df: pandas df containing either Point or LineString geometries
    :param list properties: list of column names to be put into properties
    :param string geometry_type: "Point" or "LineString"
    """
    geojson = {"type": "FeatureCollection", "features": []}

    for _, row in df.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {"type": [], "coordinates": [], "crs": "EPSG:25833"},
            "properties": {},
        }

        if geometry_type == "Point":
            if row.index.isin(["x", "y"]).sum() != 2:
                msg = "Point coordinates 'x' and/or 'y' are missing in df"
                raise ValueError(msg)
            feature["geometry"]["type"] = "Point"
            feature["geometry"]["coordinates"] = [row["x"], row["y"]]

        elif geometry_type == "LineString":
            geometry = dict(ast.literal_eval(row["geometry"]))
            if geometry["type"] != "LineString":
                msg = f"Geometry type in df is not 'LineString', but {geometry['type']}."
                raise ValueError(msg)
            feature["geometry"]["type"] = geometry["type"]
            feature["geometry"]["coordinates"] = geometry["coordinates"]

        elif geometry_type == "MultiPolygon":
            geometry = dict(ast.literal_eval(row["geometry"]))
            if geometry["type"] != "MultiPolygon":
                msg = f"Geometry type in df is not 'MultiPolygon', but {geometry['type']}."
                raise ValueError(msg)
            feature["geometry"]["type"] = geometry["type"]
            feature["geometry"]["coordinates"] = geometry["coordinates"]

        else:
            msg = "Geometry type can only be 'Point' or 'LineString'."
            raise ValueError(msg)

        for prop in properties:
            feature["properties"][prop] = row[prop]

        geojson["features"].append(feature)

    return geojson
