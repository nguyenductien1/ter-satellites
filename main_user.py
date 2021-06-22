import Indice
import TypeIndice
import Image
import user_database
"""
# l'utilisateur choisit la zone et l'indice ou les indices a calculer

# choix image pour calcul (une image est une collection de bandes spectrales pour des resolutions donnees)
#--- l'utilisateur entre le nom de la tuile, la date d'acquisition et l'heure d'acquisition
nomTuile = 'T31TEJ'
dateAcquisition = '20210216' 
heureAcquisition= '101029'  

image = Image.Image(nomTuile, dateAcquisition, heureAcquisition,'Level-1C')

# choix de l'indice a calculer
nom_indice = 'NDMI' # entrer nom indice

# calcul indice
# definition de la zone de calcul
lonMin = 3.829078674316406
lonMax = 3.9121627807617188
latMin = 43.600035399518525
latMax = 43.628123412124616
interp = 'Cubic'

indice = Indice.Indice(nomTuile, dateAcquisition, nom_indice, lonMin, lonMax, latMin, latMax, interp)

index = indice.calculIndice_psql(image,nom_indice, '1')

"""
#Function for API return
def calcul_api(nomTuile, dateAcquisition, nomIndice, lonMin,lonMax,latMin,latMax,interp,imgFormat,lmin,lmax, width, height, username):
    image = Image.Image(nomTuile, dateAcquisition, '100101','Level-1C')
    indice = Indice.Indice(nomTuile, dateAcquisition, nomIndice, lonMin,lonMax,latMin,latMax,interp)
    userID = user_database.getIDbyUserName(username)
    print(nomIndice)
    index = indice.calculIndice_psql(image, nomIndice, userID)
    lmin=lmin ; lmax=lmax
    img_base64 = indice.getImageEncode(index,lmin,lmax,imgFormat,width,height, nomIndice)
    return img_base64

