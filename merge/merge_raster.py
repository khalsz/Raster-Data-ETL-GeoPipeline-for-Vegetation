import rasterio as rio
import os

dirs = []
filepaths = []

def col_tiffile_path(dirs:list[str]) -> list[str]:    
    tif_filepaths= [] 
    for dir in dirs:  
        files = os.listdir(dir)
        tif_files = list(filter(lambda f: f.endwith('.tif'), files))
        tif_filepaths.extend(map(os.path.join, (dir, tif_files))) 
    return tif_filepaths



def stitch_raster(dirs:list[str]): 
    tif_paths = col_tiffile_path(dir)
    for path in tif_paths: 
        
#     try: 
#         for dirpath, _, filenames in os.walk(self.raw_lidar_dir): 
#             for filename in filenames: 
#                 if filename.endswith(".laz") and not os.path.isfile(join(self.dir_var_dic['new_lidar_dir'], filename)): 
#                     shutil.copy2(join(dirpath, filename), self.dir_var_dic['new_lidar_dir'])

