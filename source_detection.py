#The goal of the project is to get the Xcentroid, Ycentroid and Sky background magnitude

#code begins!
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits
from decimal import Decimal
import numpy as np
from numpy import nanmean
from astropy.stats import sigma_clipped_stats
from photutils import datasets
from photutils import DAOStarFinder
import sys

#Getting input image
ipPath = r'C:\\Users\\Ria\\VB shared files\\archiveunziped\\raw_processed_data_folder\\GRB180224A\\2018-02-25\\combinedimages\summed_R_files.fits'
raw_image_files = get_pkg_data_filename( ipPath)  # getting the images from the input file.
raw_imagedata,header= fits.getdata(raw_image_files,header=True,ext=0, clobber=True)       # getting image info and header info of one image.    
# print(raw_image_data.shape)
# print(header) 
data = raw_imagedata[0:1022,0:1023]    #Getting the data in an array.
mean, median, std = sigma_clipped_stats(data, sigma=3.0) #Getting the mean, median and std of the input image.   
print((mean, median, std)) 
daofind = DAOStarFinder(fwhm=3.0, threshold=3.*std)    # threshold = 3 => 3 sigma values as upper limit.
sources = daofind(data - median)  #Gives the required data.  
for col in sources.colnames:    
    sources[col].info.format = '%.8g'  # for consistent table output, gives data upto 8 decimal places.
print(sources)    

# #hurray! end of code!!:) 

# import numpy as np
# from numpy import nanmean
# from astropy.stats import sigma_clipped_stats
# from photutils import datasets
# hdu = datasets.load_star_image()    
# # print(hdu.data.shape) 
# # sys.exit()
# data = hdu.data[0:1022, 0:1023]    
# # print(data)
# mean, median, std = sigma_clipped_stats(data, sigma=3.0)  
# print((mean, median, std)) 

