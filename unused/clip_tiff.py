from osgeo import gdal

gdal.UseExceptions()

file_in = "/Users/dtn/SENTINEL-2/L2A_T32SLC_A029477_20210212T101919_2021-02-12/B01_wgs84.tif"
shp = "./shape_files/map.shp"
file_out = "/Users/dtn/SENTINEL-2/L2A_T32SLC_A029477_20210212T101919_2021-02-12/B01_cutted.tif"

result = gdal.Warp(file_out, file_in, cutlineDSName=shp)