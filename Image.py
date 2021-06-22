#!/usr/bin/python
# -*- coding: UTF-8 -*-
from osgeo import gdal, osr
import sys
#import osr
from matplotlib import pyplot as plt
import subprocess
import TicToc
import psycopg2
import threading
from multiprocessing import Process

class Image():

	# attributs
	def __init__(self,nomTuile,dateAcquisition,heureAcquisition,processingLevel):
		self.nomTuile = nomTuile
		self.dateAcquisition = dateAcquisition
		self.heureAcquisition = heureAcquisition
		self.processingLevel = processingLevel	
		
	# methodes
	def getImage(self,BandeSpectrale,longitudeMin,latitudeMin,longitudeMax,latitudeMax):
		fileName = './database/'+self.processingLevel+'/'+self.nomTuile+'_'+self.dateAcquisition+'T'+self.heureAcquisition+'_'+BandeSpectrale
		fileNameJp2 = fileName +'.jp2'
		fileNameTif = fileName +".tif"
		fileNameWGS84 = fileName +"_wgs84.tif"
		gdal.Translate(fileNameTif, fileNameJp2)
		gdal.Warp(fileNameWGS84, fileNameTif, dstSRS='EPSG:4326')
		
		# rajouter test here !!!
		# si on ne crop pas on retourne ds
		ds = gdal.Open(fileNameWGS84)
		if ds is None:
			print("The dataset could not be opened")
			sys.exit(-1)
			
		# si on crop, on retourne ds_crop
		ds_crop = gdal.Translate(fileNameTif, ds, projWin =[longitudeMin,latitudeMax,longitudeMax,latitudeMin]) 
		
		return [ds_crop,fileNameTif]

	def convert2Tiff(self,BandeSpectrale):
		fileName = './database/'+self.processingLevel+'/'+self.nomTuile+'_'+self.dateAcquisition+'T'+self.heureAcquisition+'_'+BandeSpectrale
		fileNameJp2 = fileName +'.jp2'
		fileNameTif = fileName +".tif"
		fileNameWGS84 = fileName+".tif"
		gdal.Translate(fileNameTif, fileNameJp2)
		gdal.Warp(fileNameWGS84, fileNameTif, dstSRS='EPSG:4326')
	

	def interpolation(self,image,img1,img2,img1_fileNameTif,img2_fileNameTif,interp):
		
		# interpolation par defaut
		if interp=='':
			print('Mode interpolation par défaut.')
			ds = gdal.Warp('', img1_fileNameTif, format = 'MEM', width = img2.shape[1], height = img2.shape[0])
	
		elif interp=='NearestNeighbour':
			print('Mode interpolation: '+interp)
			ds = gdal.Warp('', img1_fileNameTif, format = 'MEM', width = img2.shape[1], height = img2.shape[0], resampleAlg = gdal.GRIORA_NearestNeighbour )

		elif interp=='Bilinear':
			print('Mode interpolation: '+interp)
			ds = gdal.Warp('', img1_fileNameTif, format = 'MEM', width = img2.shape[1], height = img2.shape[0], resampleAlg = gdal.GRIORA_Bilinear )

		elif interp=='Cubic':
			print('Mode interpolation: '+interp)
			ds = gdal.Warp('', img1_fileNameTif, format = 'MEM', width = img2.shape[1], height = img2.shape[0], resampleAlg = gdal.GRIORA_Cubic )

		elif interp=='CubicSpline':
			print('Mode interpolation: '+interp)
			ds = gdal.Warp('', img1_fileNameTif, format = 'MEM', width = img2.shape[1], height = img2.shape[0], resampleAlg = gdal.GRIORA_CubicSpline )

		elif interp=='Lanczos':
			print('Mode interpolation: '+interp)
			ds = gdal.Warp('', img1_fileNameTif, format = 'MEM', width = img2.shape[1], height = img2.shape[0], resampleAlg = gdal.GRIORA_Lanczos )
			
		else:
			print("--------------------------------------------------------------")
			print("		 ERREUR: methode interpolation inconnue.	     ")
			print("--------------------------------------------------------------\n")

		return 	self.getBande(ds)	
			
	def checkResolution(self,image,img1,img2,img1_fileNameTif,img2_fileNameTif,interp):	
			
		# on verifie que les images sont de meme taille
		if img1.shape[0] != img2.shape[0] or img1.shape[1] != img2.shape[1]:
		
			print('Les images ne sont pas de même taille.\nUne interpolation est nécessaire pour effectuer le calcul.\n')
			
			if img1.shape[0]>img2.shape[0]:	# on interpole vers la taille la plus petite
			
				print('L'' image de taile (',img1.shape[0],'x',img1.shape[1],') sera interpollée à la taille (',img2.shape[0],'x',img2.shape[1],')')
				img1 = image.interpolation(image,img1,img2,img1_fileNameTif,img2_fileNameTif,interp)
				
			else:
				print('L'' image de taile (',img2.shape[0],'x',img2.shape[1],') sera interpollée à la taille (',img1.shape[0],'x',img1.shape[1],')')
				img2 = image.interpolation(image,img2,img1,img2_fileNameTif,img1_fileNameTif,interp)
				
		return [img1, img2]
		
	def pixelSize(self,rasterImage):
		rasterImage = gdal.Open(rasterImage)
		gt = rasterImage.GetGeoTransform()
		pixelSizeX = gt[1]
		pixelSizeY =-gt[5]
		return [pixelSizeX,pixelSizeY]
	
	def originXY(self,rasterImage):
		rasterImage = gdal.Open(rasterImage)
		gt =rasterImage.GetGeoTransform()
		originX = gt[0]
		originY =-gt[3]
		return [originX,originY]
			
	def loadDataFrame(self, RasterFile):
        	band = gdal.Open(RasterFile)
        	df_band   = band.GetRasterBand(1)
        	df = df_band.ReadAsArray()
        	return df
        	
	def getBande(self,band):
		d = band.GetRasterBand(1)
		img = d.ReadAsArray()
		return img

	def getTableName(self,nomTuile,band):
		nomTuile = str("'%"+nomTuile+"_"+band+"%'").lower()
		query = ("select count(table_name) "+
				"from information_schema.tables " +
				"where table_schema = 'public' and table_name like "+ nomTuile )
		connection = psycopg2.connect(database="ter", user="dtn", password="1122")
		cursor = connection.cursor()
		cursor.execute(query)
		result = cursor.fetchone()
		return result[0]

	def uploadToPSQL(self, band):
		fileName = './database/' + self.processingLevel + '/' + self.nomTuile + '_' + self.dateAcquisition + 'T' + self.heureAcquisition + '_' + band + '.tif'
		raster = gdal.Open(fileName)
		proj = osr.SpatialReference(wkt=raster.GetProjection())
		projection=str(proj.GetAttrValue('AUTHORITY',1))
		tableName = self.nomTuile + "_" + band + '_' + projection
		pixelSizeX = '100'
		pixelSizeY = '100'
		if self.getTableName(self.nomTuile, band) == 0:
			cmds = 'raster2pgsql -s '+projection+' -I -C -M "'+fileName+'" -F -t '+pixelSizeX+'x'+pixelSizeY+' public.'+tableName+' | PGPASSWORD=1122 psql -d ter -U dtn -p 5432'
		elif self.getTableName(self.nomTuile, band) > 0:
			cmds = 'raster2pgsql -s '+projection+' -a -I -C -M "'+fileName+'" -F -t '+pixelSizeX+'x'+pixelSizeY+' public.'+tableName+' | PGPASSWORD=1122 psql -d ter -U dtn -p 5432'

		subprocess.call(cmds, shell=True)

	def preprocess(self):
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
				p = Process(target=self.convert2Tiff, args=(band,))
				p.start()
				listOfProcess.append(p)
				print(band + " is running" + str(p.is_alive))
			for p in listOfProcess:
				p.join()
		print("Converted!!!")

	def push(self): #Push raster data to data base
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
				p = Process(target=self.uploadToPSQL, args=(band,))
				p.start()
				listOfProcess.append(p)
				print(band + " is running" + str(p.is_alive))
			for p in listOfProcess:
				p.join()
		print("All data are in database!!!")

	def convert_main(self):
		if __name__ == '__main__':
			self.preprocess()

	def push_main(self):
		TicToc.tic()
		if __name__ == '__main__':
			self.push()
		TicToc.toc()
	
#	def displayImage(self,lmin,lmax):

#	def saveImage(self):

		

