from file_manager.raster_file_manager import RasterFileManager
from validator.validate_raster_metadata import validate_raster_properties
from validator.validate_file import validate_file_list
from merge.merge_raster import stitch_tiffs_by_pattern
from os.path import join
from os.path import dirname
import os
import shutil
from schema.schema_creator import update_schema
import tempfile
import rasterio as rio
from warper.raster_projector import project_raster
import json
from rasterio.crs import CRS


canopy_metrics_var_dir = ["C:/Users/khalsz/Documents/CarbonKeepers/lidar_data/drive-download-20240509T134954Z-001/ept_NY5023/ept-data/canopy_metrics", 
                          "C:/Users/khalsz/Documents/CarbonKeepers/lidar_data/drive-download-20240509T134954Z-001/ept_NY5022/ept-data/canopy_metrics", 
                          "C:/Users/khalsz/Documents/CarbonKeepers/lidar_data/drive-download-20240509T134954Z-001/ept_NY5122/ept-data/canopy_metrics", 
                          "C:/Users/khalsz/Documents/CarbonKeepers/lidar_data/drive-download-20240509T134954Z-001/ept_NY5123/ept-data/canopy_metrics"]

# canopy_metrics_var_dir = "C:/Users/khalsz/Documents/CarbonKeepers/lidar_data/canopy_metrics"
rast_files = "C:/Users/khalsz/Documents/CarbonKeepers/lidar_data/raster_file"



def AGB_raster_processor(canopy_metrics_var_dir: str, rast_files_dir: str) -> bool:
    """
    Process raster files for AGB estimation.

    This function performs several steps:
    1. Creates a schema.
    2. Moves all other variables to the same location as the forest canopy metrics raster variable.
    3. Validates to ensure the right variables are in the canopy_metrics_var_dir.
    4. Validates the metadata of the raster variables.

    Parameters
    ----------
    canopy_metrics_var_dir : str
        The path to the directory containing forest canopy metrics raster variables.
    rast_files : str
        The path to the directory containing all raster files.

    Returns
    -------
    bool
        True if all steps are successfully completed, otherwise False.

    Raises
    ------
    Exception
        If an error occurs during any of the processing steps.
    """
    
    # create temporary directory to move all raster files
    with tempfile.TemporaryDirectory() as temp_dir: 
        
        # creating temporary directory file instance
        temp_dir_inst = RasterFileManager(temp_dir)
        
        # stitching together (by file name pattern) raster files from canopy metrics extrator
        stiched_rast = stitch_tiffs_by_pattern(dirs = canopy_metrics_var_dir, dest_path=join(dirname(rast_files_dir), 'lidar_raster'))
        
        # creating file class instances
        raster_dir_inst = RasterFileManager(rast_files_dir)
        lidar_dir_inst = RasterFileManager(stiched_rast)
        lidar_raster_dir = lidar_dir_inst.tif_ext_file()
        
        # initializing json file path
        json_schema_file = os.path.abspath(os.path.join("schema", "json_schema.json"))
        
        with open(json_schema_file, 'r') as json_file: 
            schema = json.load(json_file)
            
        # assigning CRS attribute for raster files with None CRS value    
        for file_name in lidar_raster_dir: 
            file_path = join(lidar_dir_inst.raster_file_dir, file_name)
            with rio.open(file_path, 'r+') as lid_rast:
                if lid_rast.crs is None: 
                    lid_rast.crs = CRS.from_epsg(schema['crs'])
                  
        # updating existing schema with attribute of forest canopy metrics raster variable
        schema = update_schema(join(lidar_dir_inst.raster_file_dir, lidar_dir_inst.tif_ext_file()[0]))
        
        # copying all other tif file variables to the same location
        raster_dir_inst.copy_files(dest_dir=temp_dir_inst.raster_file_dir)
        lidar_dir_inst.copy_files(dest_dir=temp_dir_inst.raster_file_dir)
        
        # creating raster variable files final destination
        parent_dir = dirname(lidar_dir_inst.raster_file_dir)
        final_directory = os.path.join(parent_dir, "final_variable")
        if os.path.exists(final_directory): 
            shutil.rmtree(final_directory)
        os.mkdir(final_directory)
        
        # validating to ensure the right variables are in the 
        validate_file_list(temp_dir_inst.raster_file_dir)
        
        # validating the raster variable metadata. 
        validat_result = validate_raster_properties(temp_dir_inst.raster_file_dir, schema)
        
        if validat_result: 
            # moving all from the temporary storage
            temp_dir_inst.move_file(dest_dir=final_directory)
            print("Validation process complete. All data variable passed validation process!")
        else: 
            raise Exception(f"Error validating variables")


if __name__ == "__main__": 
    AGB_raster_processor(canopy_metrics_var_dir, rast_files)
    
     