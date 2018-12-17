#Goal is to crop the unwanted erroneous area of the fits image.

#code begins!

# from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits
import decimal, glob, sys, os   
import numpy as np

from astropy import units as u
from astropy.nddata import CCDData
import ccdproc

#generic function to get the cropped images
#cobbler and checksum is used to tell the python to ignore any header data are that not standard and create the output image.

def croppedimage(ipPath,opPath):
        ip_files = glob.glob(ipPath + '\*.fits') #a global path is defined here. all the images in this folder will get processed. 
        for ip_file in ip_files:
        #raw_image_files = get_pkg_data_filename( ipPath +str(i+3)+'.fits')  # getting the images from the input ip_file.
                raw_image_data, header= fits.getdata(ip_file,header=True,ext=0, clobber=True)       # getting image info and header info of one image.
        #This helps in not getting the verification error, as the input image contains 'e' for exponential but python understands only 'E' for exponentials.
        #This converts the 'e' to 'E'.
                print(header)

                header['CD1_1'] = "{:.6E}".format(decimal.Decimal(header['CD1_1']))
                header['CD1_2'] = "{:.6E}".format(decimal.Decimal(header['CD1_2']))
                header['CD2_1'] = "{:.6E}".format(decimal.Decimal(header['CD2_1']))
                header['CD2_2'] = "{:.6E}".format(decimal.Decimal(header['CD2_2']))

                #xmin and xmax crops the top and bottom of the image while ymin and ymax crops the left and right side of the image.
                croppednewimage = raw_image_data[1:-1,13:-64] #cropping parameter. [xmin:-xmax,ymin:-ymax] and (minus symbol - thats what the equation says!)
        #Path to save the output image
                #fits.writeto(opPath + opFileName + str(i+1)+'.fits',croppednewimage , header, checksum=True)

                print(opPath + "\cropped" + os.path.basename(ip_file))
                #os.path.basename(ip_file) - assigns original name of the ip_file and returns true at the end of the  function.
                fits.writeto(opPath + "\cropped" + "_"+header["FILTER"]+"_"+os.path.basename(ip_file),croppednewimage , header, checksum=True)
        return True #used simply to remove error  

        #Giving path for input and output image for Bias, Flat and Science images.

if True:    #if condition written to run the cropped image part only once, (no need to repeat this part of the program for processing different filter for same input)(give if false if you don't want this part of the program to run again)
        basedir = r'C:\\Users\\Ria\\VB shared files\\archiveunziped\\raw_processed_data_folder\\GRB180614A'

        ipPath = basedir + '\Bias_archivezip'
        opPath = basedir + '\\2018-08-27\cropped_files\Cropped_bias'

        croppedbiasimages= croppedimage(ipPath, opPath) #Calling the function for getting cropped bias images.

        ipPath = basedir + '\\flat_archivezip'
        opPath = basedir + '\\2018-08-27\cropped_files\Cropped_flat'

        croppedflatimages= croppedimage(ipPath, opPath) #Calling the function for getting cropped flat images.


        ipPath = basedir + '\\2018-08-27\science_archivezip'
        opPath = basedir + '\\2018-08-27\cropped_files\Cropped_science'

        croppedscienceimages= croppedimage(ipPath, opPath) #Calling the function for getting cropped science images.


def convert2medianwithop(ipPath, comment_history,opPath,opFileName, Filter, shouldNormalize = False):
    
#str is used to convert number to string since the input data is named in numbers, (i+1) because i start from 0 not 1.   
   
    raw_image_data = []
    raw_image_files = glob.glob(ipPath + '\*.fits') #a global path is defined here. all the images in this folder will get processed. 
    for raw_image_file in raw_image_files:
#cobbler and checksum is used to tell the python to ignore any header data are that not standard and create the output image. 
           image_data,tempheader= fits.getdata(raw_image_file,header=True,ext=0, clobber=True)
        #print(header['FILTER'])    #prints the image filter name
        
#checking whether all the images are from same filter.        
           if ( tempheader['FILTER'] == Filter ):
                raw_image_data.append(image_data)
                header=tempheader
           else:
                   continue     
                
 #to get the normalized image of the median flat images.           
    if(shouldNormalize):   
            Flat = np.median(raw_image_data)
            reshaped_image = (raw_image_data/Flat).reshape(1022, 1023)  #normalised data; variable name is for convenience

 #to get median image for bias and flat.     
 #Vertical stack gets each array into a one by one row, fal.reshape(1,24) => puts all the 24 values in 1 row. 
#Vstack is used coz it is easier to find the median as it combines the images and gets the median and reshapes it back to original pixel size.      
                 
    else:
            image_data = np.vstack([image_data.reshape(1,image_data.shape[0] * image_data.shape[1]) for image_data in raw_image_data])  
#calculating median using numpy and reshaping back to original pixel size.
#multiplied by reshape to get the output image in original pixel size.              
           
            reshaped_image = np.median(image_data, axis=0).reshape(1022, 1023)    #gets the median of the image and then reshapes it in the given dimensions to ge the output image.     
    header['HISTORY']='= ' + comment_history                            #adds the history comment to the header of the final image.
    fits.writeto(opPath + opFileName +"_"+header["FILTER"]+"_"+ '.fits', reshaped_image, header, checksum=True) #path to store o/p file.
    return reshaped_image  #returns o/p
    
#Assigning the path to get input cropped image. 
#Specify which filter you want to work with.
#to bias medain image.

basedir = r'C:\\Users\\Ria\\VB shared files\\archiveunziped\\raw_processed_data_folder\\GRB180614A\\2018-08-27\\'

ipPath = basedir + 'cropped_files\Cropped_bias'
opPath = basedir + 'Output_files\\bias\\'
biasFilter = 'I'
comment_history = ' This is a median stack of 10 bias files information'
opFileName = 'biasmedian'

medianbiasOp = convert2medianwithop(ipPath, comment_history,opPath,opFileName, biasFilter) #calling the function

#to get flat median image.
ipPath = basedir + 'cropped_files\Cropped_flat'
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
sci_images = glob.glob( basedir+ 'cropped_files\\Cropped_science\\*.fits')

for sci_image in sci_images:
    image_sci_data,header = fits.getdata(sci_image, header = True, ext =0,cobbler=True) 
    if (header['FILTER'] == medianFlatFilter):       #filter check 
        finalscience = (image_sci_data - medianbiasOp)/normalizeflat   #getting the final science image.
        header['HISTORY']='= This final science image contains information of 10 bias and 3 flat images.'
        fits.writeto(basedir + 'Output_files\\science\\'+ os.path.basename(sci_image),finalscience,header,checksum=True) #path to store the output image.

#To get cosmic ray removed image. 
basedir = r'C:\\Users\\Ria\\VB shared files\\archiveunziped\\raw_processed_data_folder\\GRB180614A\\2018-08-27\\'
crr_images = glob.glob( basedir+ 'Output_files\\science\\*.fits')
# getting the input image file and data.
for crr_image in crr_images:  
#image_sci = get_pkg_data_filename('/media/sf_VB_shared_files/archiveunziped/cosmic_ray_rejection/finalscience3.fits')
    image_sci, header = fits.getdata(crr_image, header=True, ext=0, cobbler=True)
# print(image_sci)

# Getting the deviation, gain value for the image. the input gain in line 16 is used if the units of image is different from the read out noise.
# gain and read out noise depends on the detector. So enter the appropriate value.

    data = CCDData(image_sci, unit='adu')
# data_with_deviation = ccdproc.create_deviation(data, gain=2.6 * u.electron/u.adu, readnoise= 15* u.electron) #not needed for this work.

# gain_corrected = ccdproc.gain_correct(data_with_deviation, 2.6*u.electron/u.adu) #not needed for this work.

# cleaning the image and removing the cosmic ray using lacosmic

    cr_cleaned = ccdproc.cosmicray_lacosmic(data,sigclip=5,gain=2.6,readnoise=15,niter=4,cleantype="medmask",psfsize=5)

# saving the output fits image.
    fits.writeto(basedir + 'Output_files\\cosmic_ray_removed_science\\'+"\crr_"+ os.path.basename(crr_image), np.array(cr_cleaned), header, checksum=True)

# hooray!! end of code!! :)

fits.writeto(opPath + "\cropped" + "_"+header["FILTER"]+"_"+os.path.basename(ip_file),croppednewimage , header, checksum=True)
                
#hurray! end of code!!:)