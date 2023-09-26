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
            if not row.index.isin(["x", "y"]).sum() == 2:
                raise ValueError("Point coordinates 'x' and/or 'y' are missing in df")
            feature["geometry"]["type"] = "Point"
            feature["geometry"]["coordinates"] = [row["x"], row["y"]]

        elif geometry_type == "LineString":
            geometry = dict(ast.literal_eval(row["geometry"]))
            if geometry["type"] != "LineString":
                raise ValueError("Geometry type in df is not 'LineString', but {}.".format(geometry["type"]))
            feature["geometry"]["type"] = geometry["type"]
            feature["geometry"]["coordinates"] = geometry["coordinates"]

        elif geometry_type == "MultiPolygon":
            geometry = dict(ast.literal_eval(row["geometry"]))
            if geometry["type"] != "MultiPolygon":
                raise ValueError("Geometry type in df is not 'MultiPolygon', but {}.".format(geometry["type"]))
            feature["geometry"]["type"] = geometry["type"]
            feature["geometry"]["coordinates"] = geometry["coordinates"]

        else:
            raise ValueError("Geometry type can only be 'Point' or 'LineString'.")

        for prop in properties:
            feature["properties"][prop] = row[prop]

        geojson["features"].append(feature)

    return geojson
