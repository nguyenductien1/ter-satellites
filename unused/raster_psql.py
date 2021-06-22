from osgeo import gdal, osr
import psycopg2
import subprocess
fileName='/Users/dtn/SENTINEL-2/L2A_T32SLC_A029477_20210212T101919_2021-02-12/B03_crop_rs.tif' #tiff_file_name and location
tableName = 'nefta'
raster = gdal.Open(fileName)
proj = osr.SpatialReference(wkt=raster.GetProjection())
print(proj)
projection=str(proj.GetAttrValue('AUTHORITY',1))
print(projection)
gt =raster.GetGeoTransform()
print(gt)
pixelSizeX =str(round(gt[1]))
print(gt[1])
print(pixelSizeX)
pixelSizeY =str(round(-gt[5]))
print(pixelSizeY)
#cmds = 'raster2pgsql -s '+projection+' -I -C -M "'+fileName+'" -F -t '+pixelSizeX+'x'+pixelSizeY+' public.'+tableName+' | psql -d ter -U dtn -p 5432'
#subprocess.call(cmds, shell=True)