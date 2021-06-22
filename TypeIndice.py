#!/usr/bin/python
# -*- coding: UTF-8 -*-

class TypeIndice:

	def __init__(self,nom_indice):
		self.nomIndice = nom_indice

	def displayNomIndice(self):
		print("L'indice choisi est: " + self.nomIndice)

	def calcul_ndvi(self,red,nir):
		print("Comments: NDVI is a measure of vegetation greenness that can give some indication of the health of vegetation. \n"
			"The calculation uses bands 4 (red) and 8 (near-infrared).\n")
		return ((nir - red)/(nir + red))
		
	def calcul_ndwi(self,nir, green):
		print("Comments: NDWI.\n"
			"The calculation uses bands xx (green) and 8 (near-infrared).\n")
		return ((green - nir)/(green + nir))
    		
	# The Normalized Difference Moisture Index (NDMI)
	# NDMI (Sentinel 2 MSI) : NIR=B8, SWIR=B11
	def calcul_ndmi(self,nir, swir):
		print("Comments: NDMI is the normalized difference moisture index.\n"
			"The calculation uses bands 11 (swir) and 8 (near-infrared).\n")
		return ((nir - swir)/(nir + swir))
   
	# The Normalized Burn Ratio (NBR) is an index designed to highlight burnt areas in large fire zones
	# NBR (Sentinel 2 MSI) : NIR=B8, SWIR=B11   
	def calcul_nbr(self,nir, swir):
   		return ((nir - swir)/(nir + swir))  

	#DVI
	def calcul_dvi(self,nir,red):
    		return (nir-red)
	
	#ARVI
	def calcul_arvi(self,nir,red,B2):
    		return (nir-(2*red)+B2)/(nir+(2*red)+B2)

	#GCI
	def calcul_gci(self,B9,B3):
    		return (B9/B3)-1

	#BAI: Burn Area Index
	def calcul_bai(self,red, nir):
		return 1/((0.1 - red)**2 + (0.06 - nir)**2)

	#EVI: Enhanced Vegetation Index 
	def calcul_evi(self,red, nir, blue):
		return  (2.5 * (nir - red)) / ((nir + 6.0 * red - 7.5 * blue) + 1.0)

	#GDVI
	def calcul_gdvi(self,nir, green):
		return (nir - green)

	#GNDVI
	def calcul_gndvi(self,nir,green ):
		return ((nir - green)/(nir + green))

	#RVI
	def calcul_rvi(self,red, nir):
    		return (nir/red)

	#VARI
	def calcul_vari(self,red, green, blue):
    		return ((green - red)/(green + red - blue))

	#LAI 
	def calcul_lai(self,nir, red, swir):
    		return ((nir)/(red + swir))   
