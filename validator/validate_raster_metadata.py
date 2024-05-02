from os.path import join as path_join
from warper.raster_projector import project_raster
from warper.resample import resample_raster
from file_manager.raster_file_manager import RasterFileManager
from validator.validate_raster import raster_validation


def validate_raster_properties(rast_path: str, schema_json: dict):
    """
    Validate properties of raster datasets based on a user-defined JSON schema.

    Parameters
    ----------
    rast_path : str
        Path to the directory containing raster files to be validated.
    schema_json : dict
        JSON schema defining the expected properties of raster datasets.

    Returns
    -------
    bool or None
        True if all raster files conform to the defined schema, None otherwise.
    """
    # extracting only tif file from the list of files in the raster directory instance class
    raster_files = RasterFileManager(rast_path).tif_ext_file()
    
    for filename in raster_files:   
        validation_error = False  
           
        try: 
             # Validate raster properties
            raster_validation(path_join(rast_path, filename), schema_json, filename)
        except ValueError as e: 
            # Set validation error flag and print error message
            validation_error = True
            print(f"Error validating raster file: {filename}: {e}")
        
        if validation_error: 
             # Project raster if validation error occurs
            project_raster(tgt_crs=schema_json['coordinate_reference_system'], 
                            src_rast_file=path_join(rast_path, filename),
                            dst_path=path_join(rast_path, filename))
            
            # Resample raster if validation error occurs
            resample_raster(src_rast_file=path_join(rast_path, filename), 
                            tgt_res=schema_json['spatial_resolution'], 
                            dst_path=path_join(rast_path, filename))
        
        try: 
            # Re-validate raster properties after projection and resampling
            raster_validation(path_join(rast_path, filename), schema_json, filename)
 
        except ValueError as e: 
            # Set validation error flag and print error message
            validation_error = True
            print(f"Error validating ratser file {filename} after reprojection/resampling: {e}")
        else: 
            validation_error = False
                
        if validation_error:
            raise ValueError(f"Raster file {filename} properties does not conform with schema")
    
    if not validation_error:
        # Raise ValueError if validation error occurs
        print("Success validating raster files. Data conforms with the defined schema: OK")
        return True


