import os 
import shutil
from dataclasses import dataclass, field

    

@dataclass
class RasterFileManager: 
    """
    Class for managing raster files.

    This class provides methods for handling raster files, including listing TIFF files,
    moving files from one directory to another, and copying files from one directory to another.

    Attributes
    ----------
    raster_file_dir : str
        The path to the directory containing raster files.
    file_list : list[str]
        A list of predefined variable names for ML models.

    Methods
    -------
    tif_ext_file() -> list[str]:
        Get a list of TIFF files in the given directory.
    move_file(dest_dir: str) -> None:
        Move raster files from a source directory to a destination directory.
    copy_files(dest_dir: str) -> None:
        Copy raster files from a source directory to a destination directory.
    """
    
    raster_file_dir: str = None
    # initalizing variable list for the ML model
    file_list : list[str] = field(init=False, default_factory =lambda:
                                    ['agb', 'int', 'ele', '_p75', '_p99', 
                                     '_std', '_kur', '_ske', 'red', 'green',
                                     'blue', 'nir', '_dns'])    
    
    def tif_ext_file(self) -> list[str]:
        """
        Get a list of TIFF files in the given directory.

        Returns
        -------
        List[str]
            A list of TIFF files in the directory.
        """ 
        tif_files = [file.lower() for file in os.listdir(self.raster_file_dir) if file.endswith('.tif')]
        return tif_files
    
    def move_file (self, dest_dir: str) -> None: 
        """
        Move raster files from a source directory to a destination directory.

        Parameters
        ----------
        dest_dir : str
            The path to the destination directory where raster files will be moved.

        Returns
        -------
        None
            Prints a success message if all raster files are successfully moved.

        Raises
        ------
        Exception
            If an error occurs while moving files.
        """
        try: 
            # extracting files in the source directory
            files = self.tif_ext_file()
            
            # initalizing and moving source files to destination path
            for file in files: 
                src_path = os.path.join(self.raster_file_dir, file)
                dest_path = os.path.join(dest_dir, file)
                shutil.move(src_path, dest_path)

            print("successfully moved all raster file in the source directory")
        except Exception as e: 
            raise Exception (f"Error moving file: {e}")
    
    
    def copy_files(self, dest_dir:str) -> None: 
        """
        Copy raster files from a source directory to a destination directory.

        Parameters
        ----------
        dest_dir : str
            The path to the destination directory where raster files will be copied.

        Returns
        -------
        None
            Prints a success message if all raster files are successfully copied.

        Raises
        ------
        Exception
            If an error occurs while copying files.
        """
        try: 
            files = self.tif_ext_file()
            
            for file in files: 
                src_path = os.path.join(self.raster_file_dir, file)
                shutil.copy2(src_path, dest_dir)
            print("successfully copied all raster file in the source directory")
        except Exception as e: 
            raise Exception (f"Error copying file: {e}")
        



    

