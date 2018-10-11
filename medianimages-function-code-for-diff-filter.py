#Goal is to write a python code to get median image for set of bias and flat images, to get normalized flat image of the set of median flat images and to find the final science image.
#through which one can determine the GRB brightness, study the light curve etc. 

#code begins! 
import matplotlib.pyplot as plt
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits
import numpy as np

#function to get the median image for set of bias and flat images and to get normalized flat image.

def convert2medianwithop(ipPath, noOfFiles, comment_history,opPath,opFileName, Filter, shouldNormalize = False):
    
#str is used to convert number to string since the input data is named in numbers, (i+1) because i start from 0 not 1.   
   
    raw_image_files = [get_pkg_data_filename( ipPath +str(i+1)+'.fits') for i in range(noOfFiles)] 
    raw_image_data = []
    
    for raw_image_file in raw_image_files:
#cobbler and checksum is used to tell the python to ignore any header data are that not standard and create the output image. 
           image_data,header= fits.getdata(raw_image_files[0],header=True,ext=0, clobber=True)
        #print(header['FILTER'])    #prints the image filter name
        
#checking whether all the images are from same filter.        
           if ( header['FILTER'] == Filter ):
                raw_image_data.append(image_data)
                
 #to get the normalized image of the median flat images.           
    if(shouldNormalize):   
            Flat = np.median(raw_image_data)
            reshaped_image = raw_image_data/Flat  #normalised data; variable name is for convenience

 #to get median image for bias and flat.     
 #Vertical stack gets each array into a one by one row, fal.reshape(1,24) => puts all the 24 values in 1 row. 
#Vstack is used coz it is easier to find the median as it combines the images and gets the median and reshapes it back to original pixel size.      
                 
    else:
            image_data = np.vstack([image_data.reshape(1,image_data.shape[0] * image_data.shape[1]) for image_data in raw_image_data])  
#calculating median using numpy and reshaping back to original pixel size.
#multiplied by reshape to get the output image in original pixel size.              
           
            reshaped_image = np.median(image_data, axis=0).reshape(1022, 1023)    #gets the median of the image and then reshapes it in the given dimensions to ge the output image.     
    header['HISTORY']='= ' + comment_history                            #adds the history comment to the header of the final image.
    fits.writeto(opPath + opFileName + '.fits', reshaped_image, header, checksum=True) #path to store o/p file.
    return reshaped_image  #returns o/p

#Assigning the path to get input cropped image. 
#Specify which filter you want to work with.
#to bias medain image.

biasFilter = 'I'
ipPath = 'D:/archiveunziped/ipopfiles/croppedbias/cb(10.05.18)/b'
noOfFiles = 10
comment_history = ' This is a median stack of 10 bias files information'
opPath = 'D:/archiveunziped/ipopfiles/finalop/op(10.05.19)/'
opFileName = 'biasmedian'

medianbiasOp = convert2medianwithop(ipPath, noOfFiles, comment_history,opPath,opFileName, biasFilter) #calling the function

#to get flat median image.
flatFilter = 'V'
ipPath = 'D:/archiveunziped/ipopfiles/croppedflats/cf(10.05.18)/f'
noOfFiles = 3
comment_history = 'This is a median stack of 3 flat files information'
opPath = 'D:/archiveunziped/ipopfiles/finalop/op(10.05.19)/'
opFileName = 'flatmedian1'

medianflatOp = convert2medianwithop(ipPath, noOfFiles, comment_history,opPath,opFileName, flatFilter ) #calling the function

#to get flat normalized image.
medianFlatFilter = 'V'
ipPath = 'D:/archiveunziped/ipopfiles/finalop/op(10.05.19)/flatmedian'
noOfFiles = 1
comment_history = ' It contains median stack of 3 flat files information'
opPath = 'D:/archiveunziped/ipopfiles/finalop/op(10.05.19)/'
opFileName = 'normalizedflat'

normalizeflat = convert2medianwithop(ipPath, noOfFiles, comment_history,opPath,opFileName, medianFlatFilter ,shouldNormalize = True) #calling the function

# To create final science image.
for i in range(3):
    image_sci = get_pkg_data_filename('D:/archiveunziped/ipopfiles/croppedscience/cs(10.05.18)/s'+str(i+1)+'.fits') 
    image_scidata,header = fits.getdata(image_sci, header = True, ext =0,cobbler=True) 
    if (header['FILTER'] == medianFlatFilter):       #filter check 
        finalscience = (image_scidata - medianbiasOp)/normalizeflat   #getting the final science image.
        header['HISTORY']='= This final science image contains information of 10 bias and 3 flat images.'
        fits.writeto('D:/archiveunziped/ipopfiles/finalop/op(10.05.19)/finalscience'+str(i+1)+'.fits',finalscience,header,checksum=True) #path to store the output image.
        
#hurray! end of code!!:)        