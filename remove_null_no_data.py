import geopandas as gpd

grid = gpd.read_file("data/grid_output/common_grid_90m_with_lulc.shp")
filtered_grid = grid[grid["grid_id"].notnull()]
filtered_grid.to_file("data/grid_output/filtered_grid_90m_with_lulc.shp")
