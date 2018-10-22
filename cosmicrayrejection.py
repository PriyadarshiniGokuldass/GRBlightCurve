# Goal of the pipeline is to remove the unwanted cosmic ray from the final science image.
from astropy import units as u
import numpy as np
from astropy.nddata import CCDData
import ccdproc
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits

# getting the input image file and data.
image_sci = get_pkg_data_filename('D:/archiveunziped/cosmic_ray_rejection/finalscience1.fits')
image_sci, header = fits.getdata(image_sci, header=True, ext=0, cobbler=True)
# print(image_sci)

# Getting the deviation, gain value for the image. the input gain in line 16 is used if the units of image is different from the read out noise.
# gain and read out noise depends on the detector. So enter the appropriate value.

data = CCDData(image_sci, unit='adu')
data_with_deviation = ccdproc.create_deviation(data, gain=1.5 * u.electron/u.adu, readnoise= 10* u.electron)

gain_corrected = ccdproc.gain_correct(data_with_deviation, 1.5*u.electron/u.adu)

# cleaning the image and removing the cosmic ray by two methods.
# method one : by finding median.
cr_cleaned = ccdproc.cosmicray_median(gain_corrected, mbox=11, rbox=11, gbox=5)

# method 2 by using lacosmic
# cr_cleaned = ccdproc.cosmicray_lacosmic(gain_corrected, sigclip=5)

# saving the output fits image.
fits.writeto('D:/archiveunziped/ipopfiles/finalop/cosrayfinalsciop.fits', np.array(cr_cleaned), checksum=True)

# hooray!! end of code!! :)

