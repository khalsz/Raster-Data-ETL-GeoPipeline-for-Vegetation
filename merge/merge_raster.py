import rasterio as rio
from rasterio import open
from rasterio.merge import merge
from rasterio.errors import RasterioIOError
import os
from collections import defaultdict
from os.path import join
import shutil



def stitch_tiffs_by_pattern(dirs:list[str], dest_path:str) -> str: 
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
    try:   
        tif_file_paths = get_all_tiff_paths(dirs) 
        os.makedirs(dest_path, exist_ok = True)
        filename_groups = defaultdict(list) # filename : paths[list]
        for path in tif_file_paths: 
            path = path.replace("\\", "/") # Consistent path separator
            filename = path.split("/")[-1].split(".")[0] # Extract filename without extension
            filename_groups[filename].append(path)
        for img_name, img_paths in filename_groups.items():
            dest_file = join(dest_path, img_name + '.tif')
            if len(img_paths) > 1: 
                merge_img_by_name(img_paths, dest_file, img_name)
            else: 
                shutil.copyfile(img_paths[0], dest_file)
        # return destination path string 
        print("Raster files stitching completed")
        return dest_path
    except Exception as e: 
        raise Exception(f"Error stitching raster file") from e
        

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
            
def merge_img_by_name(img_paths:list[str], file_dest: str, img_name: str) -> None: 
    """
        Stitches a list of TIFF files based on filename and saves the result.

        Args:
        img_paths: A list of paths to the TIFF images to be stitched.
        file_dest: The destination path for the stitched image.
        img_name: The name of the images (used for informative messages).

        Raises:
        RasterioIOError: If there's an error opening a raster file.
        Exception: If any other error occurs during the stitching process.
    """
    rast_imgs = []
    try:
        for img_path in img_paths:     
            img = open(img_path)  
            #append rasterio.io.DatasetReader type to the list
            rast_imgs.append(img) 
        # merging the respective similar image name before closing
        merge(rast_imgs,  dst_path= file_dest)
        
        # Close all opened images if no exception is raised. 
        for ds in rast_imgs:
            ds.close()
    except RasterioIOError as e: 
        # Close all opened images before raising RasterioIOError
        for ds in rast_imgs:
            ds.close()
        raise RasterioIOError(f"Error opening raster image {img_path}") from e
    except Exception as e: 
        # Close all opened images before raising Exception
        for ds in rast_imgs:
            ds.close()
        raise Exception(f"Error merging raster files {img_name}") from e


    
    

        # # extract metadata for merged image from old one
        # out_meta = rast_imgs[0].meta.copy()
        # out_meta.update(
        #     {"driver": "GTiff", "height": merged.shape[1], "width": merged.shape[2], 
        #     "transform": transform})
        # # write new merged image to path using updated metadata
        # with open(file_dest, 'w', **out_meta) as mg_rast:
        #     mg_rast.write(merged)   