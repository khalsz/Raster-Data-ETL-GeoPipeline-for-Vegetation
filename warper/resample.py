import rasterio as rio
from rasterio.enums import Resampling
from os.path import basename

def resample_raster(src_rast_file:str, tgt_res: tuple, dst_path:str):
    """
    Resample a raster file to a target resolution.

    Parameters
    ----------
    src_rast_file : str
        Path to the source raster file.
    tgt_res : tuple
        Target spatial resolution as a tuple (x_resolution, y_resolution).
    dst_path : str
        Path to save the resampled raster data.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If an error occurs during the resampling process.
    """
    try: 
        # Open the source raster file
        src_data = rio.open(src_rast_file)
        
        # Check if the source raster resolution matches the target resolution
        if src_data.res != tgt_res: 
            # Calculate scale factors for resampling
            scale_factor_x = src_data.res[0]/tgt_res[0]
            scale_factor_y = src_data.res[1]/tgt_res[1]
            
            # Copy profile from source data
            profile = src_data.profile.copy()
            
            # Read data with resampling
            data = src_data.read(
                out_shape=(
                    src_data.count, 
                    int(src_data.height * scale_factor_x), 
                    int(src_data.width * scale_factor_y)
                ), 
                resampling=Resampling.bilinear
            )
            
            # Update transformation parameters
            transform = src_data.transform * src_data.transform.scale(
                (1 / scale_factor_x), 
                (1 / scale_factor_y)
            )
            
            profile.update({
                'height': data.shape[-2], 
                'transform': transform, 
                'width': data.shape[-1]
            })
            
            # Close the source raster to overwrite it  
            src_data.close()
            
            # Write resampled data to destination raster file
            with rio.open(dst_path, 'w',  **profile) as resampled_data: 
                resampled_data.write(data)
            print(f"Successfully resampled {basename(src_data.name)} to target resolution: {tgt_res}")
        else: 
            print(f"Skipping resample stage. Raster file {basename(src_data.name)} in the same resolution {src_data.res} with target's {tgt_res}")

    except Exception as e: 
        raise ValueError(f"Error resampling raster: {e}")