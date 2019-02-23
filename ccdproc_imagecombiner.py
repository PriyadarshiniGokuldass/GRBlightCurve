# Goal is to combine the 'n' number of images to get a summed image of same filter type to check whehter the GRBs are visible in the summed image.
#code begins!
from astropy.io import fits
import ccdproc, glob, os
import numpy as np 
from ccdproc import Combiner
from astropy.nddata import CCDData
# Initializing the path to the folder.
basedir = os.path.join( os.getcwd() + '\GRB180224A\\2018-02-25\\') 
outputFile = os.path.join(basedir + "combinedimage.fits")
targetDir =   os.path.join(basedir+'WCS\*.fits')
ip_files = glob.glob(targetDir)
#Here the images are appended into different arrays w.r.t their filter types - this makes combining the images easy since the folder might contain different filter type image.
ccdObjArray = {} #creating an empty array to store the respective filter images in different arrays. 
ccdHeaderArray={} #Making an array to store the header of each image with respect to it's filter type.
for ip_file in ip_files:
    imageData, header= fits.getdata(ip_file,header=True,ext=0, clobber=True)   # getting image info and header info of one image.
    ccdObj = CCDData(imageData, unit='adu')
    filterName = header["FILTER"]
    if( filterName in ccdObjArray ):
        ccdObjArray[filterName].append(ccdObj) #checks whether filter type matches with any of the existing array.
    else:
        ccdObjArray[filterName] = [ccdObj] #If an array for particular fitler doesn't exist, a new array gets created and then the image gets stored.
        ccdHeaderArray[filterName] = header #contains the header of the images.
#Image combining is done below. 
for filterName in ccdObjArray:
    opPath = os.path.join( basedir + '\combinedimages') #output image folder is created
    if not os.path.exists(opPath):
        os.makedirs(opPath)
    opTarget = opPath + '\summed_'+filterName+'_files.fits'

    combineimage = np.array( ccdproc.combine( ccdObjArray[filterName], method='sum')) #image is combined
    header = ccdHeaderArray[ filterName ] 
    fits.writeto(opTarget ,combineimage ,  header, overwrite=True, checksum=True)#Image is written to the folder, overwrite=True - overwrites the already existing image in the folder. 

# print(' end of code! ')
# hooray!! end of code!! :)