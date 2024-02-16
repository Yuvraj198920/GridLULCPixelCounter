# hook-gdal.py
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files

binaries = collect_dynamic_libs("osgeo")
datas = collect_data_files("osgeo", subdir="gdal-data")
