import unittest
import os
from raster_process_main import AGB_raster_processor


class TestValidateRasterMetadata(unittest.TestCase): 
    """
    A test case class for validating raster metadata.

    This test case class is designed to test the functionality of functions that validate raster metadata,
    including coordinate reference system (CRS), spatial resolution, validate_raster_properties, and band count.

    Attributes:
        valid_raster_dir (str): The directory path containing valid raster files.
        invalid_raster_dir (str): The directory path containing invalid raster files.
        canopy_metrics_var_dir (str): The directory path containing canopy metrics files.
    """
    
    def setUp(self) -> None:
        """
        Set up the necessary attributes and validate the input data.

        Raises:
            FileNotFoundError: If one or both of the raster directories or the canopy metrics directory do not exist.
            ValueError: If one or both of the raster directories or the canopy metrics directory contain no files.
        """
        
        self.valid_raster_dir = "C:/Users/khalsz/Documents/Biomass_data_processor/biomass-data-processor/tests/data/valid_raster"
        self.invalid_raster_dir = "C:/Users/khalsz/Documents/Biomass_data_processor/biomass-data-processor/tests/data/invalid_raster"
        self.canopy_metrics_var_dir = "C:/Users/khalsz/Documents/Biomass_data_processor/biomass-data-processor/tests/data/canopy_metrics"
        
        
        # Check if directories exist
        if not os.path.isdir(self.valid_raster_dir) or not os.path.isdir(self.invalid_raster_dir): 
            raise FileNotFoundError("one or both of the raster directories does not exist")
        # Check if directories is empty
        if not os.listdir(self.valid_raster_dir) or not os.listdir(self.invalid_raster_dir): 
            raise ValueError("one of both of the raster directories contains no file")
        if not os.listdir(self.canopy_metrics_var_dir): 
            raise ValueError("the directory contains no file")
        

            
    def test_valid_AGB_raster_processor(self): 
        """
        Test the AGB_raster_processor function with valid inputs.

        This test checks if the AGB_raster_processor function behaves as expected
        when provided with valid input directories containing raster files.
        """
        self.assertIsNone(AGB_raster_processor(self.canopy_metrics_var_dir, self.valid_raster_dir))
    
    def test_invalid_canopy_metrics_var_dir(self): 
        """
        Test the AGB_raster_processor function with an invalid canopy metrics directory.

        This test verifies that the AGB_raster_processor function raises an exception
        when provided with an invalid canopy metrics directory.
        """
        with self.assertRaises(Exception): 
            AGB_raster_processor(self.canopy_metrics_var_dir, self.invalid_raster_dir)


if __name__ == "__main__": 
    unittest.main()

