from osgeo import gdal, ogr, osr
import numpy as np

raster_path = "data/input/LULC_2006.tif"

ds = gdal.Open(raster_path)
gt = ds.GetGeoTransform()

meters_per_degree = 111320
cell_size_degrees = 270/meters_per_degree

# Calculate the number of grid cells in x and y directions
x_cells = int((ds.RasterXSize * gt[1]) / cell_size_degrees)
y_cells = int((ds.RasterYSize * gt[5]) / -cell_size_degrees)  # Negative due to north-up convention

# Generate the grid coordinates
x_coords = np.linspace(gt[0], gt[0] + ds.RasterXSize * gt[1], x_cells)
y_coords = np.linspace(gt[3], gt[3] + ds.RasterYSize * gt[5], y_cells)

# Create a new shapefile
driver = ogr.GetDriverByName('ESRI Shapefile')
shp_path = 'data/output/2006_grid.shp'
dataSource = driver.CreateDataSource(shp_path)
layer = dataSource.CreateLayer('grid', geom_type=ogr.wkbPolygon)

# Add polygons to the shapefile
for i in range(len(y_coords)-1):
    for j in range(len(x_coords)-1):
        ring = ogr.Geometry(ogr.wkbLinearRing)
        ring.AddPoint(x_coords[j], y_coords[i])
        ring.AddPoint(x_coords[j+1], y_coords[i])
        ring.AddPoint(x_coords[j+1], y_coords[i+1])
        ring.AddPoint(x_coords[j], y_coords[i+1])
        ring.AddPoint(x_coords[j], y_coords[i])

        # Create polygon
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)

        # Create feature
        featureDefn = layer.GetLayerDefn()
        feature = ogr.Feature(featureDefn)
        feature.SetGeometry(poly)
        layer.CreateFeature(feature)
        # Cleanup
        feature = None
# Save and close DataSource
dataSource = None
