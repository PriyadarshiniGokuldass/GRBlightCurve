from astropy import units as u
import numpy as np
from astropy.nddata import CCDData
import ccdproc
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits


image_sci = get_pkg_data_filename('D:/archiveunziped/cosmic_ray_rejection/finalscience1.fits')
image_sci, header = fits.getdata(image_sci, header=True, ext=0, cobbler=True)
print(image_sci)
data = CCDData(image_sci, unit='adu')
data_with_deviation = ccdproc.create_deviation(data, gain=1.5 * u.electron/u.adu, readnoise= 10* u.electron)

gain_corrected = ccdproc.gain_correct(data_with_deviation, 1.5*u.electron/u.adu)
# cr_cleaned = ccdproc.cosmicray_median(gain_corrected, mbox=11, rbox=11, gbox=5)
cr_cleaned = ccdproc.cosmicray_lacosmic(gain_corrected, sigclip=5)
fits.writeto('D:/archiveunziped/ipopfiles/finalop/cosrayfinalsciopla.fits', np.array(cr_cleaned), checksum=True)
fits.writeto('D:/archiveunziped/ipopfiles/finalop/cosrayfinalsciipla.fits', np.array(image_sci), checksum=True)
