import rasterio as rio
from os.path import basename


def get_rst_meta(rast_file): 
    """
    Extract metadata from a raster file.

    Parameters
    ----------
    rast_file : rio.DatasetReader
        Raster file object.

    Returns
    -------
    dict
        Dictionary containing raster metadata.
    """
    raster_metadata = {
        "width": rast_file.width, 
        "height": rast_file.height,
        "transform": rast_file.transform, 
        "crs": rast_file.crs, 
        "res": rast_file.res, 
        "count": rast_file.count
    }
    return raster_metadata
    

def get_crs(rast_file): 
    """
    Get the EPSG code of the given raster file.

    Parameters
    ----------
    rast_file : rio.DatasetReader
        Raster file object.

    Returns
    -------
    int or None
        EPSG code of the raster file's coordinate reference system (CRS).
        None if CRS is not available.
        
    Raises
    ------
    ValueError
        If an error occurs while getting the CRS.
    """
    try: 
        epsg = rast_file.crs.to_epsg() # extract raster EPSG to string
        if epsg is not None: 
            return epsg
        else: 
            raise ValueError(f"Error: Raster file {basename(rast_file.name)} CRS is None")
    except FileNotFoundError as e: 
        raise ValueError(f"File error: {e}")
    except rio.errors.RasterioIOError as e: 
        raise ValueError(f"Rasterio I/O error: {e}")
        

