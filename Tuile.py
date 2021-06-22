import os
from collections import OrderedDict
from datetime import date

import pandas
from osgeo import gdal, osr
from sentinelsat import SentinelAPI, geojson_to_wkt, read_geojson
from sentinelsat import SentinelAPIError, SentinelAPILTAError, InvalidChecksumError

import Image
import psql

# https://scihub.copernicus.eu/twiki/do/view/SciHubUserGuide/FullTextSearch?redirectedfrom=SciHubUserGuide.3FullTextSearch

class Tuile:
	listImages = []

	# attributs de la classe
	def __init__(self,user,password,workdir,sensingStartTime,sensingEndTime,tiles,processinglevel):
		self.user = user
		self.password = password
		self.workdir = workdir
		self.tiles = tiles
		self.sensingStartTime = sensingStartTime
		self.sensingEndTime = sensingEndTime
		self.processinglevel = processinglevel
		self.listImages = []
	
	# telechargement des tuiles	
	def download(self):

		# creation du dossier de travail
		savedir = self.workdir+'SENTINEL-2/'
		directory = savedir+self.processinglevel
		if not os.path.exists(directory):
			os.makedirs(directory)

		if self.processinglevel == 'Level-1C':
			print("Downloading Sentinel-2A data - Processing Level-1C")
			api = SentinelAPI(self.user, self.password,'https://scihub.copernicus.eu/dhus')
			# search by polygon, time, and SciHub query keywords
			footprint = geojson_to_wkt(read_geojson('map.geojson'))
			products = api.query(footprint,
						date=(self.sensingStartTime, self.sensingEndTime),
                	    platformname='Sentinel-2',
                    	processinglevel='Level-1C')

			# convert to Pandas DataFrame
			products_df = api.to_dataframe(products)
			if len(products)>0:
				# sort and limit to first 5 sorted products
				products_df_sorted = products_df.sort_values(['cloudcoverpercentage', 'ingestiondate'], ascending=[True, True])
				products_df_sorted = products_df_sorted.head(5)
				abc = products_df_sorted.to_csv(index=False)
				f = open('listfile_level-1C.csv', 'w')
				f.write(abc)
				f.close()
				# download sorted and reduced products
				api.download_all(products_df_sorted.index, directory)
			else:
				print('no data found')
	

		elif self.processinglevel == 'Level-2A':
			print("Downloading Sentinel-2A data - Processing Level-2A")
			api = SentinelAPI(self.user, self.password,'https://scihub.copernicus.eu/dhus')
			# search by polygon, time, and SciHub query keywords
			footprint = geojson_to_wkt(read_geojson('map.geojson'))
			products = api.query(footprint,

						date=(self.sensingStartTime, self.sensingEndTime),
                	    platformname='Sentinel-2',
                    	processinglevel='Level-2A',
                     	cloudcoverpercentage=(0, 100))

			# convert to Pandas DataFrame
			products_df = api.to_dataframe(products)
			if len(products)>0:
				# sort and limit to first 5 sorted products
				products_df_sorted = products_df.sort_values(['cloudcoverpercentage', 'ingestiondate'], ascending=[True, True])
				products_df_sorted = products_df_sorted.head(5)
				abc = products_df_sorted.to_csv(index=False)
				f = open('listfile_level-2A.csv', 'w')
				f.write(abc)
				f.close()
				# download sorted and reduced products
				api.download_all(products_df_sorted.index,directory)
			else:
				print('no data found')

		else:
			print("ERROR: Sentinel-2A - invalid processing level. Please verify input parameters.")


	# creation database locale
	def database(self,):
		savedir = self.workdir+'SENTINEL-2/'
		directory = savedir+self.processinglevel
		# unzip tuile
		os.system("unzip '"+ directory+'/'+'*.zip'+"'")
		os.system("echo Database creation...")
		bddir = self.workdir+'database/'+self.processinglevel
		if not os.path.exists(bddir):
			os.makedirs(bddir)
		if self.processinglevel == 'Level-1C':
			for tile in self.tiles: #Only use by 1C Level
				os.system("mv *.SAFE/GRANULE/*"+tile+"*/IMG_DATA/"+tile+"* "+bddir)
				os.system("rm -rf *.SAFE") 
				os.system("echo Database created !")
		elif self.processinglevel == 'Level-2A':
			for tile in self.tiles: #Only use by 2A Level
				os.system("mv *.SAFE/GRANULE/*"+" "+bddir)
				os.system("rm -rf *.SAFE") 
				os.system("echo Database created !")

