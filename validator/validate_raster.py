import rasterio as rio
from raster_metadata.create_metadata import get_rst_meta


def validate_crs(raster_metadata, schema_json, file_name): 
    """
    Validate the Coordinate Reference System (CRS) of the raster file.

    Parameters
    ----------
    raster_metadata : dict
        Metadata of the raster file.
    schema_json : dict
        JSON schema defining the expected properties of the raster dataset.
    file_name : str
        Name of the raster file.

    Raises
    ------
    ValueError
        If the CRS of the raster file does not match the expected CRS defined in the schema.
    """
    
    # checking of the CRS of the raster file matches the custom defined
    if raster_metadata['crs'].to_epsg() != schema_json['coordinate_reference_system']: 
        raise ValueError(f"ValueError: The raster file {file_name} has a a wrong CRS. "
                f"Expected CRS:{schema_json['coordinate_reference_system']}, found: {raster_metadata.crs}"
                f"Raster file {file_name} is needs to be projected")
       
def validate_spatial_resolution(raster_metadata, schema_json, file_name): 
    """
    Validate the spatial resolution of the raster file.

    Parameters
    ----------
    raster_metadata : dict
        Metadata of the raster file.
    schema_json : dict
        JSON schema defining the expected properties of the raster dataset.
    file_name : str
        Name of the raster file.

    Raises
    ------
    ValueError
        If the spatial resolution of the raster file does not match the expected resolution defined in the schema.
    """
    
    # checking of the spatial resolution of the raster file matches the custom defined
    if raster_metadata['res'] != schema_json['spatial_resolution']: 
        raise ValueError(f"The raster file {file_name} has a wrong Spatial Resolution. " 
                            f"Expected: {schema_json['spatial_resolution']}, found: {raster_metadata['res']}."
                            f"This raster file {file_name} needs Resampling")

def validate_maxband_count(raster_data, schema_json, file_name): 
    """
    Validate the maximum band count of the raster file.

    Parameters
    ----------
    raster_data : rasterio DatasetReader
        Raster data to be validated.
    schema_json : dict
        JSON schema defining the expected properties of the raster dataset.
    file_name : str
        Name of the raster file.

    Raises
    ------
    ValueError
        If the band count of the raster file exceeds the maximum limit defined in the schema.
    """
    
    # checking the validaty of the band count in the raster file. 
    if raster_data.count > schema_json['number of bands']['max']: 
        raise ValueError(f"The number of bands in the file {file_name} exceed the max limit. "
                            f"Expected max bands: {schema_json['number of bands']['max']}, but found {raster_data.count}")
 

def raster_validation(raster_file:str, schema_json:dict, filename:str):
    """
    Validate properties of the raster file based on the provided schema.

    Parameters
    ----------
    raster_file : str
        Path to the raster file to be validated.
    schema_json : dict
        JSON schema defining the expected properties of the raster dataset.
    filename : str
        Name of the raster file.

    Raises
    ------
    ValueError
        If any of the raster properties do not conform to the schema.
    """
    with rio.open(raster_file) as raster_data:      
        metadata = get_rst_meta(raster_data)
        # validating the max band count of the raster file. 
        validate_maxband_count(raster_data, schema_json, filename)
        # validating the CRS of the raster file. 
        validate_crs(metadata, schema_json, filename)
        # validating the spatial resolution of the raster file.
        validate_spatial_resolution(metadata, schema_json, filename)