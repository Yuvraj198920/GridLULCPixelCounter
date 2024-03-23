# GridLULCPixelCounter

### Overview
`GridLULCPixelCounter` is a Python script designed for environmental scientists, geographers, and GIS professionals to analyze land use and land cover (LULC) data. It counts the number of pixels for each LULC class within predefined grid cells and calculates the centroid for each cell. The output is a comprehensive CSV file that includes the centroid coordinates along with the pixel counts for each LULC class within each grid cell. This tool is invaluable for spatial analysis, environmental monitoring, and urban planning.

In addition to pixel counting, this toolset includes a grid creation script, `create_grid`, which generates a grid layer over any raster dataset, regardless of its coordinate reference system (CRS). A user-friendly Tkinter interface is provided for easy grid creation.

### Features
- **Pixel Counting:** Accurately counts pixels of specified LULC classes within each grid cell of a given vector layer.
- **Centroid Calculation:** Determines the geographic center (centroid) for each grid cell.
- **CSV Export:** Outputs a CSV file containing the grid cell ID, centroid coordinates (latitude and longitude), and the count of pixels for each LULC class within the cell.
- **Grid Creation:** Generates a grid layer over any raster dataset, with customizable grid size.
- **Flexibility:** Works with any raster and vector data, provided they share the same coordinate reference system (CRS).

### Prerequisites
- **Python 3.x**
- **GDAL**
- **Rasterio**
- **Geopandas**
- **Numpy**

Make sure all dependencies are installed using pip:

`pip install gdal rasterio geopandas numpy`
