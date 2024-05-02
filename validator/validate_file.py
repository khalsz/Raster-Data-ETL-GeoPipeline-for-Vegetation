import os
from file_manager.raster_file_manager import RasterFileManager

def validate_file_list(file_dir: str) -> None: 
        
    """
    Validate the variable sets in a directory containing raster files.

    Parameters
    ----------
    file_dir : str
        The path to the directory containing different file format.
    var_list : list
        A list of predefined variable names.

    Returns
    -------
    None
        Prints a success message if the variable sets are valid.

    Raises
    ------
    ValueError
        If the number of raster files in the directory doesn't match the number of predefined variables,
        or if the names of raster files don't match the predefined variable names.
    KeyError
        If there is a mismatch between the raster file names and the predefined variable names.
    """
        
    # initializing lenght of files in the raster variable directory
    raster_file_len = len([file for file in os.listdir(file_dir) if file.endswith('.tif')])
    
    # raster file manager instance
    raster_file = RasterFileManager()
    
    # initializing length of the listed predefined variables 
    raster_file_list = raster_file.file_list
    var_len = len(raster_file_list)
    
    # extracting file names from the raster variable directory
    raster_files_names = [os.path.splitext(file)[0].lower() for file in os.listdir(file_dir) if file.endswith('.tif')] 
    
    # validating the lenght of the variables in raster variable directory
    if raster_file_len != var_len: 
        error_message1 = f"The root file contains: {raster_file_len} while the variable list contains: {var_len}"
        error_message2 = f"There are {raster_files_names} variables in the root path," \
                            f"while the variable list contains {raster_file_list}"
        raise ValueError(f"{error_message1} \n {error_message2}")
    
    # validating the files in the raster variable
    if sorted(raster_files_names) != sorted(raster_file_list): 
        error_message3 = f"There is a mismatch. The file directory contains: {set(raster_file_list) - set(raster_files_names)}"\
                        f"more than the defualt file list or default file list contains: {set(raster_files_names) - set(raster_file_list)} " \
                        f"more than in the file directory"
        raise KeyError(f"{error_message3}")
    else: 
        print(f"The file contains the right variable sets.")
        

