#Goal is to crop the unwanted erroneous area of the fits image.
#the pipeline will create necessary folders. Simply give the input path name and output path name and the base directory.
# basedir is the common path that both input and output files contain.
# input path is the specific path for that specific input image. 
# output path is the specific path for that specific output image.
#code begins!
from astropy.io import fits
import decimal, glob, sys, os   
import numpy as np

from astropy import units as u
from astropy.nddata import CCDData
import ccdproc

# Putting all the images from raw_image_folder in an array, these images in the array is then cropped for futher processing.    
def filesClassifier(targetFileName, basedir):
    files = []
    ip_files = glob.glob(basedir + '\*.fts')
    for ip_file in ip_files:
        filename = os.path.basename(ip_file)
        if(targetFileName in filename):
            files.append(ip_file)
    return files

#generic function to get the cropped images
#cobbler and checksum is used to tell the python to ignore any header data are that not standard and create the output image.

def croppedimage(ip_files,opPath):
        for ip_file in ip_files:
                raw_image_data, header= fits.getdata(ip_file,header=True,ext=0, clobber=True)       # getting image info and header info of one image.
        
                fileName = os.path.basename(ip_file)
                header['OBJ_NAME'] = fileName.split('_')[0]   #Adding the name of the object in the header of each image.    

                #xmin and xmax crops the top and bottom of the image while ymin and ymax crops the left and right side of the image.
                croppednewimage = raw_image_data[1:-1,1:-1] #cropping parameter. [xmin:-xmax,ymin:-ymax] and (minus symbol - thats what the equation says!)
        #Path to save the output image
               
                print(opPath + "\\cropped" + os.path.basename(ip_file))
                if not os.path.exists(opPath):
                        os.makedirs(opPath)
                       
                fits.writeto(opPath + "\\cropped" + "_"+header["FILTER"]+"_"+fileName,croppednewimage , header, checksum=True,overwrite=True)
        return True #used simply to remove error  

       #Giving path for input and output image for Bias, Flat and Science images.

if True:    #if condition written to run the cropped image part only once, (no need to repeat this part of the program for processing different filter for same input)(give "if false" if you don't want this part of the program to run again)
        basedir = r'C:\\Users\\Ria\\VB shared files\\archiveunziped\\VIRT_DATA_EDITED_DIRECTORY\\Directory_folder\\'

        ipBiasFiles = filesClassifier('Bias', basedir+'Apr18_2019.tar')
        opPath = basedir + 'cropped_files\\Cropped_bias'

        croppedbiasimages= croppedimage(ipBiasFiles, opPath) #Calling the function for getting cropped bias images.
             
        ipFlatFiles = filesClassifier('Flat', basedir+'Apr18_2019.tar')
        opPath = basedir + 'cropped_files\\Cropped_flat'

        croppedflatimages= croppedimage(ipFlatFiles, opPath) #Calling the function for getting cropped flat images.


        ipSciFiles = filesClassifier('FocusTest', basedir+'Apr18_2019.tar')
        opPath = basedir + 'cropped_files\\Cropped_science'

        croppedscienceimages= croppedimage(ipSciFiles, opPath) #Calling the function for getting cropped science images.
 
 #Pipeline to get the median, normalized and processed images.               

def convert2medianwithop(ipPath, comment_history,opPath,opFileName, Filter, shouldNormalize = False, shouldwritefile=True):
    
    raw_image_data = []
    raw_image_files = glob.glob(ipPath + '\*.fts') #a global path is defined here. all the images in this folder will get processed. 
       
    for raw_image_file in raw_image_files:
        #cobbler and checksum is used to tell the python to ignore any header data are that not standard and create the output image. 
           image_data,tempheader= fits.getdata(raw_image_file,header=True,ext=0, clobber=True)
        
        #checking whether all the images are from same filter.        
           if ( tempheader['FILTER'] == Filter ):
                raw_image_data.append(image_data)
                header=tempheader
           else:
                   continue     
                
    #to get the normalized image of the median flat images.           
    if(shouldNormalize):   
            Flat = np.median(raw_image_data)
            reshaped_image = (raw_image_data/Flat).reshape(2046, 2046)  #normalised data; variable name is for convenience; reshaped to the original image size.  
        #to get median image for bias and flat.     
         #Vertical stack gets each array into a one by one row, fal.reshape(1,24) => puts all the 24 values in 1 row. 
        #Vstack is used coz it is easier to find the median as it combines the images and gets the median and reshapes it back to original pixel size.      
                 
    else:
            image_data = np.vstack([image_data.reshape(1,image_data.shape[0] * image_data.shape[1]) for image_data in raw_image_data])  
        
        #calculating median using numpy and reshaping back to original pixel size.
        #multiplied by reshape to get the output image in original pixel size.              
           
            reshaped_image = np.median(image_data, axis=0).reshape(2046, 2046)    #gets the median of the image and then reshapes it in the given dimensions to ge the output image.     
    header['HISTORY']='= ' + comment_history                            #adds the history comment to the header of the final image.
    if shouldwritefile:
            if not os.path.exists(opPath):
                        os.makedirs(opPath)
            fits.writeto(opPath + opFileName +"_"+header["FILTER"]+"_"+ '.fts', reshaped_image, header, checksum=True,overwrite=True) #path to store o/p file.
    return reshaped_image  #returns o/p
    
#Assigning the path to get input cropped image. 
#Specify which "filter" you want to work with.

#to get bias medain image.

basedir = r'C:\\Users\\Ria\\VB shared files\\archiveunziped\\VIRT_DATA_EDITED_DIRECTORY\\Directory_folder\\'

ipPath = basedir + 'cropped_files\\Cropped_bias'
opPath = basedir + 'Output_files\\bias\\'
biasFilter = 'R'
comment_history = ' This is a median stack of 10 bias files information'
opFileName = 'biasmedian'

medianbiasOp = convert2medianwithop(ipPath, comment_history,opPath,opFileName, biasFilter,shouldwritefile=True) #calling the function
#shouldwritefiles = false is used to not save the output bias image each time when code is run for different filters. Make it Ture to run first time.

#to get flat median image.
ipPath = basedir + 'cropped_files\\Cropped_flat'
opPath = basedir + 'Output_files\\flat\\'
flatFilter = 'R'
comment_history = 'This is a median stack of 3 flat files information'
opFileName = 'flatmedian'

medianflatOp = convert2medianwithop(ipPath, comment_history,opPath,opFileName, flatFilter ) #calling the function

#to get flat normalized image.
ipPath = basedir + 'Output_files\\flat'
opPath = basedir + 'Output_files\\Normalized_flat\\'
medianFlatFilter = 'R'
comment_history = ' It contains median stack of 3 flat files information'
opFileName = 'normalizedflat'

normalizeflat = convert2medianwithop(ipPath, comment_history,opPath,opFileName, medianFlatFilter ,shouldNormalize = True) #calling the function

# To create final science image.
sci_images = glob.glob( basedir+ 'cropped_files\\Cropped_science\\*.fts')
opPath = 'Output_files\\science\\'
if not os.path.exists(basedir +opPath):
        os.makedirs(basedir +opPath)
for sci_image in sci_images:
    image_sci_data,header = fits.getdata(sci_image, header = True, ext =0,cobbler=True) 
    if (header['FILTER'] == medianFlatFilter):       #filter check; checking whether the filter of science and flat images are same.   
        finalscience = (image_sci_data - medianbiasOp)/normalizeflat   #getting the final science image.
        header['HISTORY']='= This final science image contains information of 10 bias and 10 flat images.'
        fits.writeto(basedir + opPath+ os.path.basename(sci_image),finalscience,header,checksum=True,overwrite=True) #path to store the output image.

#To get cosmic ray removed image. 
basedir = r'C:\\Users\\Ria\\VB shared files\\archiveunziped\\VIRT_DATA_EDITED_DIRECTORY\\Directory_folder\\'
crr_images = glob.glob( basedir+ 'Output_files\\science\\*.fts')
opPath = 'Output_files\\cosmic_ray_removed_science\\'
# getting the input image file and data.
for crr_image in crr_images:  
    image_sci, header = fits.getdata(crr_image, header=True, ext=0, cobbler=True)

# Getting the deviation, gain value for the image. the input gain in line 16 is used if the units of image is different from the read out noise.
# gain and read out noise depends on the detector. So enter the appropriate value.

    data = CCDData(image_sci, unit='adu')
# cleaning the image and removing the cosmic ray using lacosmic
    if (header['FILTER'] == medianFlatFilter): #to process the images with only specific filter name.    
        cr_cleaned = ccdproc.cosmicray_lacosmic(data,sigclip=5,gain=2.6,readnoise=15,niter=4,cleantype="medmask",psfsize=5)

# saving the output fits image.
        if not os.path.exists(basedir +opPath):
                os.makedirs(basedir +opPath)
        fits.writeto(basedir + opPath +"\crr_"+ os.path.basename(crr_image), np.array(cr_cleaned), header, checksum=True,overwrite=True)

# hooray!! end of code!! :)

