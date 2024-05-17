# Raster Data ETL GeoPipeline for Vegetation

## Overview
The Raster Data ETL GeoPipeline for Vegetation an ETL (Extract, Transform, Load) pipeline designed for efficient processing of raster data for vegetation estimation. This pipeline provides functionalities to validate, process, and manipulate raster data to ensure they conform to predefined schemas and meet the requirements for further analysis or modeling of forest biomass estimation.


## Features
**Raster File Management**: The application includes a RasterFileManager class for managing raster files. It provides methods for listing, moving, and copying raster files.
**Data Validation**: The application offers data validation capabilities to ensure that raster files meet specific criteria defined by a JSON schema. It validates properties such as coordinate reference system (CRS), spatial resolution, and band count.
**Data Processing**: The application provides functions for processing raster files, including resampling, reprojection, and schema updates.

## Project Structure:
The project consists of several components organized into modules:

1. **Data Processing Modules**: These modules contain functions and classes for raster data processing.
    - **raster_metadata**: Extracts metadata from raster files and updates schema information.
    - **raster_projector**: Handles raster projection to a target coordinate reference system (CRS).
    - **resample**: Implements raster resampling to a specified spatial resolution.
    - **validator**: Validates raster metadata properties and ensures conformity to a defined schema.
2. **File Management Modules**: These modules manage raster files, including listing, moving, and copying operations.
    - **raster_file_manager**: Manages operations related to raster file handling.
3. **Schema Creation and Update**: These modules create and update schema information for raster files.
    - **schema_creator**: Generates and updates JSON schema for raster datasets.
4. **Main Script**: The main script orchestrates the entire processing workflow.
    - **AGB_raster_processor**: Executes the automated raster data processing workflow for AGB estimation.

## Usage:
To utilize this automated raster data processing workflow:

1. Clone the repository to your local machine.
2. Install the required dependencies listed in `requirements.txt`.
3. Define the directory paths containing raster files for forest canopy metrics and other variables.
4. Run the AGB_raster_processor.py script with the appropriate directory paths as arguments.
5. Monitor the execution of the automated workflow, which includes metadata extraction, validation, transformation, and loading steps.
6. Upon successful completion, retrieve the processed raster data consolidated in the final variable directory for further analysis.

## Requirements:
Ensure you have the following dependencies installed:

- Python 3.x
- Rasterio
Other dependencies specified in requirements.txt

## Contributions and Feedback:
Contributions to this project are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.

## License:
This project is licensed under the MIT License.
