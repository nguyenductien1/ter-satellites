import Image
import threading
from multiprocessing import Process
from osgeo import gdal, osr
import subprocess
import TicToc
import psycopg2

"""
nomTuile = 'T32SLC'
dateAcquisition = '20210212' 
heureAcquisition= '101131'
processingLevel = 'Level-1C'
"""

#image = Image.Image(nomTuile, dateAcquisition, heureAcquisition,'Level-1C')
def createImage(nomTuile, dateAcquisition, heureAcquisition, processingLevel):
    return Image.Image(nomTuile, dateAcquisition, heureAcquisition,processingLevel)
   
def convert(band, nomTuile, dateAcquisition, heureAcquisition, processingLevel):
    image = createImage(nomTuile, dateAcquisition, heureAcquisition, processingLevel)
    image.convert2Tiff(band)

def getTableName(nomTuile):
    nomTuile = str("'%"+nomTuile+"%'").lower()
    query = ("select count(table_name) "+
            "from information_schema.tables " +
            "where table_schema = 'public' and table_name like "+ nomTuile )
    connection = psycopg2.connect(database="ter", user="dtn", password="1122")
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0]

def uploadToPSQL(band, nomTuile, dateAcquisition, heureAcquisition, processingLevel):
    fileName = './database/' + processingLevel + '/' + nomTuile + '_' + dateAcquisition + 'T' + heureAcquisition + '_' + band + '.tif'
    raster = gdal.Open(fileName)
    proj = osr.SpatialReference(wkt=raster.GetProjection())
    projection=str(proj.GetAttrValue('AUTHORITY',1))
    tableName = nomTuile + "_" + band + '_' + projection
    #gt =raster.GetGeoTransform()
    #pixelSizeX =str(round(gt[1]))
    pixelSizeX = '100'
    #pixelSizeY =str(round(-gt[5]))
    pixelSizeY = '100'
    if getTableName(nomTuile) == 0:
        cmds = 'raster2pgsql -s '+projection+' -I -C -M "'+fileName+'" -F -t '+pixelSizeX+'x'+pixelSizeY+' public.'+tableName+' | PGPASSWORD=1122 psql -d ter -U dtn -p 5432'
    elif getTableName(nomTuile) > 0:
        cmds = 'raster2pgsql -s '+projection+' -a -I -C -M "'+fileName+'" -F -t '+pixelSizeX+'x'+pixelSizeY+' public.'+tableName+' | PGPASSWORD=1122 psql -d ter -U dtn -p 5432'
    
    subprocess.call(cmds, shell=True)

def preprocess():
    listOfBand = ['B01','B02','B03','B04','B05','B06','B07','B08','B8A','B09','B10','B11','B12']
    listOfProcess = []
    Parts = []
    # n processeur(s) que on veut utiliser pour calculer
    Processors = 4
    #Diviser la liste de fichier à 'n de processeurs' Parts
    for i in range(0, len(listOfBand), Processors):
        Parts.append(listOfBand[i:i + Processors]) 
    for part in Parts:
        #print(part)
        for band in part:
            p = Process(target=convert, args=(band,))
            p.start()
            listOfProcess.append(p)
            print(band + " is running" + str(p.is_alive))
        for p in listOfProcess:
            p.join()
    print("Converted!!!")

def push():
    listOfBand = ['B01','B02','B03','B04','B05','B06','B07','B08','B8A','B09','B10','B11','B12']
    listOfProcess = []
    Parts = []
    # n processeur(s) que on veut utiliser pour calculer
    Processors = 4
    #Diviser la liste de fichier à 'n de processeurs' Parts
    for i in range(0, len(listOfBand), Processors):
        Parts.append(listOfBand[i:i + Processors]) 
    for part in Parts:
        #print(part)
        for band in part:
            p = Process(target=uploadToPSQL, args=(band,))
            p.start()
            listOfProcess.append(p)
            print(band + " is running" + str(p.is_alive))
        for p in listOfProcess:
            p.join()
    print("All date are stored in database!!!")

def convert_main():
    if __name__ == '__main__':
        preprocess()

def push_main():
    TicToc.tic()
    if __name__ == '__main__':
        push()
    TicToc.toc()

#convert_main()
#push_main()
abc = getTableName('t32SLc')
print(abc)

