import rasterio as rio
from os.path import basename
from raster_metadata.create_metadata import get_crs
from warper.crs_transformer import transformer, reprojector



def project_raster(tgt_crs: int, src_rast_file:str, dst_path: str): 
    """
    Convert the coordinate reference system of a raster file.

    This function converts the coordinate reference system (CRS) of a raster file
    to the specified target CRS using the transformer and reprojector functions.

    Parameters
    ----------
    tgt_crs : int
        Target CRS to which the source raster will be projected.
    src_rast_file : str
        Path to the source raster file.
    dst_path : str
        Path to save the projected raster data.

    Returns
    -------
    bool
        True if the conversion is successful.

    Raises
    ------
    ValueError
        If an error occurs during the conversion process.
    """
    try:
        # opening raster file
        with rio.open(src_rast_file) as src_rast: 
        
        # extracting source and target raster crs info
            src_crs = get_crs(src_rast)
        
            if tgt_crs != src_crs:
                kwargs, transform = transformer(src_rast, tgt_crs)
                reprojector(src_rast, kwargs, transform, tgt_crs, dst_path)
                print(f"raster file {basename(src_rast.name)} successfully" \
                        f"reporjected from {src_crs} to {tgt_crs} projection")
            else: 
                print(f"Skipping projection stage. Raster file {basename(src_rast.name)} in the same CRS {src_crs} with target's {tgt_crs}")
    except FileNotFoundError as e: 
        raise ValueError(f"File Error: {e}")
    except rio.errors.RasterioIOError as e: 
        raise ValueError(f"Rasterio I/O error: {e}")
    

