#  Goal of the pipeline is to remove the unwanted cosmic ray from the final science image.
from astropy import units as u
import numpy as np
from astropy.nddata import CCDData
import ccdproc
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits
import decimal, glob, sys, os
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
        