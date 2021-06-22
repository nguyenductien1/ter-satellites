from osgeo import gdal, osr
import psycopg2
import subprocess
import glob


#Create connection to database
def connection():
    connection = psycopg2.connect(database="ter", user="dtn", password="pwpw")
    return connection

#Get raster from database -> create virtual path of file
def retriveData(band):
    connection = psycopg2.connect(database="ter", user="dtn", password="pwpw")
    cursor = connection.cursor()
    query= "WITH clip(geom) AS (SELECT ST_Transform(ST_SetSRID(area, 4326),4326) \
     FROM area WHERE area.area_name='nefta') SELECT ST_Clip(rast, 1, geom, true) \
     as rast INTO TEMP r_"+ band + " FROM " + band + " , clip WHERE ST_Intersects(rast, geom);"
    cursor.execute(query)
    vsipath = '/vsimem/from_postgis/'+band
    cursor.execute("SELECT ST_AsGDALRaster(ST_Union(rast), 'GTiff') FROM r_"+band+";")
    gdal.FileFromMemBuffer(vsipath, bytes(cursor.fetchone()[0]))
    return vsipath

#Version 2 faster to get raster from database -> create virtual path of file
def retriveData2(band, lonMin, latMin, lonMax, latMax, dateAcquisition):
    latMin = str(latMin)
    lonMin = str(lonMin)
    latMax = str(latMax)
    lonMax = str(lonMax)
    dateAcquisition = str("'%"+dateAcquisition+"%'")
    connection = psycopg2.connect(database="ter", user="dtn", password="pwpw")
    cursor = connection.cursor()
    query = ("SELECT ST_AsGDALRaster(rast,'GTiff')"+ 
            " FROM ("+ 
                "SELECT ST_Clip(rast,ST_Transform(ST_GeomFromText('POLYGON(("+
                    lonMin+" "+ latMin+"," +lonMax+" "+ latMin+"," + lonMax+" "+ latMax+","\
                     + lonMin+" "+ latMax+"," + lonMin+" "+ latMin+"))',4326),4326)) AS rast "+ 
                "FROM ("+ 
                    "SELECT ST_Union(rast) as rast from ("+
                        "SELECT rast FROM "+ band + " WHERE ST_Intersects("+band+".rast,"+
                            "ST_Transform(ST_GeomFromText('POLYGON(("+
                                lonMin+" "+ latMin+"," +lonMax+" "+ latMin+"," + lonMax+" "+ latMax+"," +\
                                 lonMin+" "+ latMax+"," + lonMin+" "+ latMin+
                                "))',4326),4326)) AND "+ band+".filename LIKE "+ dateAcquisition+ 
                    ") AS rast"+
                ") AS rast"+               
            ") AS rast;")
    cursor.execute(query)
    vsipath = '/vsimem/from_postgis/'+band
    gdal.FileFromMemBuffer(vsipath, bytes(cursor.fetchone()[0]))
    return vsipath


