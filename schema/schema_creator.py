
import rasterio as rio
import os
from raster_metadata.create_metadata import get_rst_meta
import json



def update_schema (raster_file) -> dict:
    """
    Update the schema with metadata from a raster file.

    This function reads the metadata from the raster file specified by `raster_file`
    and updates the schema dictionary with the Coordinate Reference System (CRS)
    and spatial resolution extracted from the raster file.

    Parameters
    ----------
    raster_file : str
        The path to the raster file from which to extract metadata.

    Returns
    -------
    dict
        A dictionary containing updated schema information with CRS and spatial resolution.

    Raises
    ------
    FileNotFoundError
        If the specified `raster_file` does not exist or cannot be found.
    """
    # Load JSON schema file
    json_schema_file = os.path.abspath(os.path.join("schema", "json_schema.json"))
    with rio.open(raster_file) as raster_data: 
        # extracting metadata (json) from the rasterio format file
        raster_metadata = get_rst_meta(raster_data)
        
    # Read raster metadata    
    with open(json_schema_file, 'r') as json_file: 
        schema = json.load(json_file)
        
    # Update schema spatial resolution
    schema['spatial_resolution'] = raster_data.res

    # Write updated schema back to JSON file
    with open(json_schema_file, "w") as json_file: 
        json.dump(schema, json_file)
    
    return schema


