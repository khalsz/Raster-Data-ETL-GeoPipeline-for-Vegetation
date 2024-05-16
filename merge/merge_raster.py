import rasterio as rio
import os


def get_all_tiff_paths(dirs:list[str]) -> list[str]:  
    """
    Extracts all TIFF file paths from a list of directories.

    Args:
        dirs: A list of directory paths to search for TIFF files.

    Returns:
        A list containing absolute paths to all TIFF files found within the directories.

    Raises:
        FileNotFoundError: If any directory in the provided list cannot be accessed.
        Exception: If any other error occurs during file path extraction.
    """ 
    tif_filepaths= [] 
    for dir in dirs:  
        try: 
            files = os.listdir(dir)
            if files: 
                tif_files = [f for f in files if f.endswith('.tif')]
                tif_filepaths.extend(list(map(lambda f: os.path.join(dir, f), tif_files)))
            else: 
                print(f"No TIFF files found in directory: {dir}")    
        except FileNotFoundError as e: 
            raise FileNotFoundError(f"Error accessing directory: {dir}") from e
        except Exception as e: 
            raise Exception(f"Error extracting file file path {dir}") from e
    return tif_filepaths



def stitch_tiffs_by_pattern(dirs:list[str], dest_path:str) -> None: 
    """
    Stitches TIFF files based on filename patterns and saves the result to a specified path.

    Args:
        dirs: A list of directory paths containing the TIFF files.
        dest_path: The destination path where the stitched image will be saved.
        output_format: The format of the stitched image (optional, defaults to the format of the input files).

    Raises:
        RasterioIOError: If there's an error opening a raster file.
        Exception: If any other error occurs during the stitching process.
    """

    tif_paths = get_all_tiff_paths(dirs)
    hashmap = {} # path : index
    for i, path in enumerate(tif_paths): 
        try: 
            path = path.replace("\\", "/")
            pattern = path.split("/")[-1].split(".")[0]
            dest_file = os.path.join(dest_path, pattern, '.tif')
            if pattern in hashmap: 
                first_tiff = rio.open(path, 'r')
                second_tiff = rio.open(path[hashmap[pattern]], 'r')
                rio.merge.merge([first_tiff, second_tiff], indexes = 1, dst_path= dest_file)
            hashmap[pattern] = i

        except rio.errors.RasterioIOError as RasterioIOError: 
            raise RasterioIOError(f"error opening raster file {pattern}") from RasterioIOError
        except Exception as e: 
            raise Exception(f"error stitching raster file {pattern}") from e
    return dest_path

            





