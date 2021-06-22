#!/usr/bin/python
# -*- coding: UTF-8 -*-

from osgeo import gdal, osr, ogr
import TypeIndice
import Image
from matplotlib import pyplot as plt
import psql
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import io
import base64
#import BandeSpectrale
import subprocess
import os
import string
import random
import pandas as pd
import user_database
import datetime
class Indice(object):

	# attributs de la classe
	def __init__(self, nomTuile, dateAcquisition, nom_indice,lonMin,lonMax,latMin,latMax,interp):
		self.nomIndice = nom_indice
		self.longitudeMin = lonMin
		self.latitudeMin = latMin
		self.longitudeMax = lonMax
		self.latitudeMax = latMax
		self.interp = interp
		self.nomTuile = nomTuile
		self.dateAcquisition = dateAcquisition
	
	def getBandeImage(self,image,band1):

		[b1,b1_fileNameTif] = image.getImage(band1,self.longitudeMin,self.latitudeMin,self.longitudeMax,self.latitudeMax)
		img1 = image.getBande(b1)

		return [img1,b1_fileNameTif]
	# methode pour recuperer la donnee reference pour extraire les coordonnees latlon 
	# a associer a l'indice on va attribuer les valeurs d'indices
	def getReferenceData(self,fileTiff1,fileTiff2):
		g1 = fileTiff1
		g2 = fileTiff2
		img1 = g1.ReadAsArray()
		img2 = g2.ReadAsArray()
		
		if img1.shape[0]>img2.shape[0]:
			g = g2
			img = img2
		elif img1.shape[0]<img2.shape[0]:
			g = g1
			img = img1
		else:
			g = g1
			img = img1
		return [g,img]	
	#Create random string of name file
	#def random_string(length):
	#	return ''.join(random.choice(string.ascii_letters) for m in xrange(length))
	
	def calculIndice(self,image,nomIndice):
	
		choix_indice = TypeIndice.TypeIndice(self.nomIndice)
		choix_indice.displayNomIndice() ## afficher l'indice choisi	
	
		bande = BandeSpectrale.BandeSpectrale(self.longitudeMin,self.latitudeMin,self.longitudeMax,self.latitudeMax)
		
		if self.nomIndice == 'NDVI' or self.nomIndice == 'ndvi':
			[img1,b1_fileNameTif] = self.getBandeImage(image,"B04") 
			[img2,b2_fileNameTif] = self.getBandeImage(image,"B08")

			[im1,im2] = image.checkResolution(image,img1,img2,b1_fileNameTif,b2_fileNameTif,self.interpolation)
							
			# on calcule l'indice
			ndvi = choix_indice.calcul_ndvi(im1,im2)   
			print("Calcul indice terminé.")	
			return ndvi
			
		elif self.nomIndice == 'NDMI' or self.nomIndice == 'ndmi':
			[img1,b1_fileNameTif] = self.getBandeImage(image,"B08") 
			[img2,b2_fileNameTif] = self.getBandeImage(image,"B11")

			[im1,im2] = image.checkResolution(image,img1,img2,b1_fileNameTif,b2_fileNameTif,self.interp)
							
			# on calcule l'indice
			ndmi = choix_indice.calcul_ndmi(im1,im2)   
			print("Calcul indice terminé.")	
			return ndmi
		
		elif self.nomIndice == 'NDWI' or self.nomIndice == 'ndwi':
			[img1,b1_fileNameTif] = self.getBandeImage(image,"B08") 
			[img2,b2_fileNameTif] = self.getBandeImage(image,"B03")

			[im1,im2] = image.checkResolution(image,img1,img2,b1_fileNameTif,b2_fileNameTif,self.interpolation)
							
			# on calcule l'indice
			ndwi = choix_indice.calcul_ndwi(im1,im2)   
			print("Calcul indice terminé.")	
			return ndwi
			
		else:
			print("--------------------------------------------------------------")
			print("			 ERREUR: Indice non repertorié.	     	     ")
			print("--------------------------------------------------------------\n")

	#This function 
	
	def calculIndice_psql(self,image,nomIndice, UserID):
		choix_indice = TypeIndice.TypeIndice(self.nomIndice)
		choix_indice.displayNomIndice() ## afficher l'indice choisi	
	
		#bande = BandeSpectrale.BandeSpectrale(self.longitudeMin,self.latitudeMin,self.longitudeMax,self.latitudeMax)
		
		if self.nomIndice == 'NDVI' or self.nomIndice == 'ndvi':
			B08_file = gdal.Open(psql.retriveData2(self.nomTuile + "_b08_4326", self.longitudeMin,self.latitudeMin,self.longitudeMax,self.latitudeMax, self.dateAcquisition))
			B04_file = gdal.Open(psql.retriveData2(self.nomTuile + "_b04_4326", self.longitudeMin,self.latitudeMin,self.longitudeMax,self.latitudeMax, self.dateAcquisition))
			
			img_B08 = image.getBande(B08_file)
			img_B08 = img_B08[1:-1,1:-1]
			img_B04 = image.getBande(B04_file)
			img_B04 = img_B04[1:-1,1:-1]

			[im1,im2] = image.checkResolution(image,img_B04,img_B08,B04_file,B08_file,self.interp)
							
			# on calcule l'indice
			ndvi = choix_indice.calcul_ndvi(im1,im2)   
			print("Calcul indice terminé.")	
			self.getIndexTiff(B04_file,B08_file,ndvi,nomIndice,UserID)
			return ndvi
			
		elif self.nomIndice == 'NDMI' or self.nomIndice == 'ndmi':

			B08_file = gdal.Open(psql.retriveData2(self.nomTuile + "_b08_4326", self.longitudeMin,self.latitudeMin,self.longitudeMax,self.latitudeMax, self.dateAcquisition))
			B11_file = gdal.Open(psql.retriveData2(self.nomTuile + "_b11_4326", self.longitudeMin,self.latitudeMin,self.longitudeMax,self.latitudeMax, self.dateAcquisition))
			
			img_B08 = image.getBande(B08_file)
			img_B08 = img_B08[1:-1,1:-1]
			img_B11 = image.getBande(B11_file)
			img_B11 = img_B11[1:-1,1:-1]

			[im1,im2] = image.checkResolution(image,img_B08,img_B11,B08_file,B11_file,self.interp)
							
			# on calcule l'indice
			ndmi = choix_indice.calcul_ndmi(im1,im2)
			self.getIndexTiff(B08_file,B11_file,ndmi,nomIndice, UserID)   
			print("Calcul indice terminé.")	
			return ndmi
		
		elif self.nomIndice == 'NDWI' or self.nomIndice == 'ndwi':

			B08_file = gdal.Open(psql.retriveData2(self.nomTuile + "_b08_4326", self.longitudeMin,self.latitudeMin,self.longitudeMax,self.latitudeMax, self.dateAcquisition))
			B03_file = gdal.Open(psql.retriveData2(self.nomTuile + "_b03_4326", self.longitudeMin,self.latitudeMin,self.longitudeMax,self.latitudeMax, self.dateAcquisition))
			
			img_B08 = image.getBande(B08_file)
			img_B08 = img_B08[1:-1,1:-1]
			img_B03 = image.getBande(B03_file)
			img_B03 = img_B03[1:-1,1:-1]

			[im1,im2] = image.checkResolution(image,img_B08,img_B03,B08_file,B03_file,self.interp)
							
			# on calcule l'indice
			ndwi = choix_indice.calcul_ndwi(im1,im2) 
			self.getIndexTiff(B08_file,B03_file,ndwi,nomIndice, UserID)    
			print("Calcul indice terminé.")	
			return ndwi
			
		else:
			print("--------------------------------------------------------------")
			print("			 ERREUR: Indice non repertorié.	     	     ")
			print("--------------------------------------------------------------\n")

	


	def displayIndice(self,indice,lmin,lmax):
  		fig = plt.figure(figsize=(10, 10))
  		fig.set_facecolor('white')
  		plt.imshow(indice, cmap='gray')
  		plt.colorbar()
  		plt.clim(lmin, lmax)
  		plt.title(self.nomIndice)

	def saveRasterLocal(self,indice,lmin,lmax,filename,imgFormat, UserID):
  		# creation du dossier de sauvegarde image si non existant
		savedir = '/images/'
		rootdir = '/home/dtn/Documents/HTTP-Server/sites/user_files/'
		if not os.path.exists(savedir):
			os.makedirs(savedir)
			
		fig = plt.figure(figsize=(10, 10))
		fig.set_facecolor('white')
		plt.imshow(indice, cmap='gray')
		plt.colorbar()
		plt.clim(lmin, lmax)
		plt.title(self.nomIndice)
		#filename = UserID + '_' + ''.join(random.choice(string.ascii_letters) for m in xrange(10))
		listFormat = ('eps', 'pdf', 'pgf', 'png', 'ps', 'raw', 'rgba', 'svg', 'svgz')
		if imgFormat == '':
			plt.savefig(savedir+'/'+filename+'.png')
			print("sauvegarde image indice "+self.nomIndice+" réussie !")
			
		elif imgFormat in listFormat:
  			plt.savefig(savedir+'/'+filename+'.'+imgFormat)
  			print("sauvegarde image indice "+self.nomIndice+" réussie !")
		else:
			print('ERREUR: format de sauvegarde inconnu.')
		

	def saveVectorLocal(self, in_file):
	
  		# creation du dossier de sauvegarde image si non existant
		savedir = '/images/'
		rootdir = '/home/dtn/Documents/HTTP-Server/sites/user_files'
		if not os.path.exists(rootdir+savedir):
			os.makedirs(rootdir+savedir)
		# changement extension du fichier raster	
		out_file = rootdir + savedir + '/' + in_file[:-4] + ".json"
		cmdline = ['gdal_polygonize.py', in_file, "-f", "GeoJSON", out_file]
		subprocess.call(cmdline)

	#This function return image with binary type base 64, this will be use to display in website
	def getImageEncode(self, indice, lmin, lmax, imgFormat, width, height, nomIndice):
		fig = plt.figure(figsize=(width, height))
		fig.set_facecolor('white')
		cmapVal = 'gray'
		if nomIndice == 'NDVI':
			cmapVal = 'RdYlGn'
		if nomIndice == 'NDWI' or nomIndice == 'NDMI':
			color_map = plt.cm.get_cmap('jet')
			cmapVal = color_map.reversed()
		plt.imshow(indice, cmap=cmapVal)
		plt.colorbar()
		plt.clim(lmin, lmax)
		plt.title(self.nomIndice)
		image_bytes = io.BytesIO()
		listFormat = ('eps', 'pdf', 'pgf', 'png', 'jpg', 'raw', 'rgba', 'svg', 'svgz')
		if imgFormat == '':
			plt.savefig(image_bytes, format = 'png')
			image_bytes.seek(0)
		elif imgFormat in listFormat:
			plt.savefig(image_bytes, format = imgFormat)
			image_bytes.seek(0)
		else:
			print('ERREUR: format de sauvegarde inconnu.')

		image_base64 = base64.b64encode(image_bytes.read())
		return image_base64

	#For saving file to database
	# methode pour sauvegarder les images raster tiff en images vectorielles
	def saveImageVectorLocal(self,filename,outfile):
	  	# creation du dossier de sauvegarde image si non existant
		savedir = '/images_vectorielles/'
		rootdir = '/home/dtn/Documents/HTTP-Server/sites/user_files'
		if not os.path.exists(rootdir+savedir):
			os.makedirs(rootdir+savedir)
			
		in_file = filename
		out_file = savedir+outfile+'.json'
		out_file_disk = rootdir + out_file
		cmdline = ['gdal_polygonize.py',"-nomask", in_file, "-f", "GeoJSON", out_file_disk , filename]
		subprocess.call(cmdline)
		
		print('Image vectorielle sauvegardée dans le dossier '+savedir)
		return out_file
		
	# methode pour sauvegarder l'image raster sous forme de tableau csv
	def saveDataRaster(self,rasterData,outfile):
  		# creation du dossier de sauvegarde image si non existant
		savedir = '/data_raster/'
		rootdir = '/home/dtn/Documents/HTTP-Server/sites/user_files'
		if not os.path.exists(rootdir+savedir):
			os.makedirs(rootdir+savedir)
		out_file = savedir+outfile+'.csv'
		out_file_disk = rootdir + out_file
		pd.DataFrame(rasterData).to_csv(out_file_disk)
		print('Sauvegarde données raster sous format csv terminée dans le dossier '+savedir)
		return out_file

	# methode pour obtenir l'indice en format tiff ayant les coordonnees geographiques
	def getIndexTiff(self, fileTiff1, fileTiff2, indice, nom_indice, userID):
  		# creation du dossier de sauvegarde si non existant
		savedir = '/indices_tiff'
		rootdir = '/home/dtn/Documents/HTTP-Server/sites/user_files'
		if not os.path.exists(rootdir+savedir):
			os.makedirs(rootdir+savedir)
		
		[g,img] = self.getReferenceData(fileTiff1,fileTiff2)
		
		geo  = g.GetGeoTransform()
		proj = g.GetProjection()
		shape = img.shape
		driver = gdal.GetDriverByName("GTiff")
		randomName = ''.join(random.choice(string.ascii_letters) for m in range(10))
		ds = driver.Create(rootdir+savedir+'/'+nom_indice+'_'+randomName+'.tif', shape[1], shape[0], 1, gdal.GDT_Float32)
		ds.SetGeoTransform(geo)
		ds.SetProjection(proj)
		ds.GetRasterBand(1).WriteArray(indice)
		linkToTif = savedir+'/'+nom_indice+'_'+randomName+'.tif'
		linkToTifDb = rootdir+savedir+'/'+nom_indice+'_'+randomName+'.tif'
		linkToJson = self.saveImageVectorLocal(linkToTifDb, nom_indice+'_'+randomName)
		linkToCSV  = self.saveDataRaster(indice, nom_indice+'_'+randomName)

		date = datetime.date.today().strftime("%Y-%m-%d")

		user_database.putInfosFiles(date, linkToTif, linkToCSV, linkToJson, userID)

		ds = None #sauvegarde et fermer dataset
		
		print('Fichier TIFF enregistré dans le dossier '+savedir)
	




			


