import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np
import rasterio



def transformer (src_rst: rasterio.io.DatasetReader, tgt_crs:int): 
    """
    Calculate transformation parameters for reprojection of a raster file from one CRS to another.

    Parameters
    ----------
    src_rst : rasterio DatasetReader
        Source raster data to be transformed.
    tgt_crs : int
        Target coordinate reference system.

    Returns
    -------
    Tuple
        Tuple containing metadata and transformation parameters of the transformed raster data.
    """
    try: 
        # Calculate transformation parameters for reprojection
        transform, width, height = calculate_default_transform(
            src_rst.crs, tgt_crs, src_rst.width, 
            src_rst.height, *src_rst.bounds)

        # Check if transformation parameters are valid
        if transform is None or width <= 0 or height <= 0: 
            raise ValueError("Unable to calculate transform or raster dimension")
        
        # Create a copy of raster metadata to prevent alteration of the source when new args are changed 
        profile = src_rst.meta.copy()
        
        # updating of new args
        profile.update({
            'crs': tgt_crs, 
            'transform': transform, 
            'width': width, 
            'height': height
        })
        
        return profile, transform
    
    except Exception as e: 
        raise RuntimeError(f"Error: {e}")
            
     

def reprojector (src_rst:rasterio.io.DatasetReader, kwargs: dict, tgt_transform, tgt_crs:int, dst_path:str):
    """
    Reproject and resample raster data to the target coordinate reference system and spatial resolution, then save to a new file.

    Parameters
    ----------
    src_rst : rasterio DatasetReader
        Source raster data to be reprojected.
    kwargs : dict
        Metadata for the destination raster.
    tgt_transform : Affine
        Target transformation parameters for reprojection.
    tgt_crs : int
        Target coordinate reference system for reprojection.
    dst_path : str
        Path to save the reprojected raster.

    Returns
    -------
    bool
        True if the reprojection process is completed successfully.
    """
    try: 
    # Perform reprojection
        data, _ = reproject(
            source=src_rst.read(),
            destination=np.zeros((src_rst.count, kwargs['height'], kwargs['width'])),
            src_transform=src_rst.transform, 
            src_crs=src_rst.crs,
            dst_transform=tgt_transform,
            dst_crs=tgt_crs,
            dst_nodata=src_rst.nodata,
            resampling=Resampling.bilinear
            )
        
        # Close the source raster to overwrite it
        src_rst.close()
        
        # Write the reprojected data to the destination raster
        with rio.open(dst_path, 'w', **kwargs) as proj_rst: 
            proj_rst.write(data)
            
        print(f"Raster source file reprojection and resample process completed successfully.")
        return True 
    except (FileNotFoundError, rio.errors.RasterioIOError) as e: 
        raise RuntimeError(f"Error: {e}")