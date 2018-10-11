#Goal is to crop the unwanted erroneous area of the fits image. 

#code begins!

from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits
from decimal import Decimal

#generic function to get the cropped images 
#cobbler and checksum is used to tell the python to ignore any header data are that not standard and create the output image.
def croppedimage(ipPath,noOfFiles,opPath,opFileName):
    for i in range(noOfFiles):
        raw_image_files = get_pkg_data_filename( ipPath +str(i+1)+'.fits')  # getting the images from the input file.
        raw_image_data,header= fits.getdata(raw_image_files,header=True,ext=0, clobber=True)       # getting image info and header info of one image.    
#This helps in not getting the verification error, as the input image contains 'e' for exponential but python understands only 'E' for exponentials.
#This converts the 'e' to 'E'.   
        header['CD1_1'] = "{:.6E}".format(Decimal(header['CD1_1']))
        header['CD1_2'] = "{:.6E}".format(Decimal(header['CD1_2']))
        header['CD2_1'] = "{:.6E}".format(Decimal(header['CD2_1']))
        header['CD2_2'] = "{:.6E}".format(Decimal(header['CD2_2']))
        print(header)
#xmin and xmax crops the top and bottom of the image while ymin and ymax crops the left and right side of the image.        
        croppednewimage = raw_image_data[1:-1,13:-64] #cropping parameter. [xmin:-xmax,ymin:-ymax] and (minus symbol - thats what the equation says!)  
#Path to save the output image   
        fits.writeto(opPath + opFileName + str(i+1)+'.fits',croppednewimage , header, checksum=True)  

#Giving path for input and output image for Bias, Flat and Science images.    
    
ipPath = 'D:/archiveunziped/ipopfiles/bias/Bias(I)(18.06.14)/b'
noOfFiles = 10
opPath = 'D:/archiveunziped/ipopfiles/croppedbias/cb(10.05.18)/'
opFileName = 'b'

croppedbiasimages= croppedimage(ipPath, noOfFiles,opPath,opFileName) #Calling the function for getting cropped bias images.

ipPath = 'D:/archiveunziped/ipopfiles/flats/flat(V)(18.06.14)/f'
noOfFiles = 3
opPath = 'D:/archiveunziped/ipopfiles/croppedflats/cf(10.05.18)/'
opFileName = 'f'

croppedflatimages= croppedimage(ipPath, noOfFiles,opPath,opFileName) #Calling the function for getting cropped flat images.


ipPath = 'D:/archiveunziped/ipopfiles/science/science(V)(18.06.14)/s'
noOfFiles = 3
opPath = 'D:/archiveunziped/ipopfiles/croppedscience/cs(10.05.18)/'
opFileName = 's'

croppedscienceimages= croppedimage(ipPath, noOfFiles,opPath,opFileName) #Calling the function for getting cropped science images. 

#hurray! end of code!!:)