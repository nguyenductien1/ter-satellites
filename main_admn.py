import os
import Tuile
from osgeo import gdal, osr
import rasterio
import user_database
import Image
import TicToc
# l'administrateur peut telecharger des nouvelles images pour ajouter dans la base de donnee
# identifiants open access
user = 'nguyenductien1'
password = 'Conchocon199@'

sensingStartTime = '20210208'
sensingEndTime = '20210212' # intervalle useful for downloading temporal series
tile = 'T31TEJ' # enter le nom de la tuile ou des tuiles à télécharger
tuiles = [tile]
workdir = '/home/dtn/Documents/ter-python/'


#instance objet tuile
tuile = Tuile.Tuile(user,password,workdir,sensingStartTime,sensingEndTime,tuiles,'Level-1C')

""" 1. telechargment des images pour objet tuile (une tuile est une collection d'images)"""
#tuile.download() #ex nom tuile = S2A_MSIL1C_20210327T102021_N0209_R065_T32SLC_20210327T122440

""" 2. creation de la base de donnee locale si voulu """
#tuile.database()
""" 3. Create instant of image """
image = Image.Image('T31TEJ', '20210211', '104151', 'Level-1C')

"""4. Convertire jp2 ver tif"""

def convert_main():
		if __name__ == '__main__':
			image.preprocess()
#convert_main() 

"""5. pour pusher vers postgis"""

def push_main():
    TicToc.tic()
    if __name__ == '__main__':
        image.push()
    TicToc.toc()
#push_main()
 
""" Get infomations of a tuile """
def getTuileInfo(fileName):
    name = 'T31TEJ'
    ds_raster = rasterio.open(fileName)
    bounds = ds_raster.bounds
    lonMin= bounds.left
    latMin = bounds.bottom
    lonMax = bounds.right
    latMax = bounds.top
    coor = [name, lonMin,latMin,lonMax,latMax]
    return coor
"""6. Get tuile Infos """
#tuilInfos = getTuileInfo('/home/dtn/Documents/ter-python/database/Level-1C/T31TEJ_20210211T104151_B01.tif')
"""7. Push tuile Infos to database"""
#user_database.insertTuileInfo(tuilInfos[1],tuilInfos[3], tuilInfos[2], tuilInfos[4], tuilInfos[0])
"""8. Up date info of sensing date of each tuile"""
#Update sensing_date table
#user_database.insertTuileSensingDate('2021-02-16', 3)