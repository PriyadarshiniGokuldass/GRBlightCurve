from astropy.io import fits
import ccdproc, glob, os
import numpy as np 
import matplotlib.pyplot as plt
import xlrd 
from openpyxl import Workbook, load_workbook

file_loc = (r"C:\Users\Ria\VB shared files\archiveunziped\word_files\GCN_data_edited.xlsx") 

def getRow(minRow, maxRow, data):
    tempRow = []
    for x in range(len(data)):
        if( x > minRow and x < maxRow):
            tempRow.append(data[x].value)    
    return tempRow

wb = load_workbook(file_loc)
source = wb["GRB171010A"]
tT0 = getRow(5, 19, source['A'])
flux = getRow(5, 19, source['J'])
fluxError = getRow(5, 19, source['M'])

upperLimit=[flux + fluxError for flux, fluxError in zip(flux, fluxError) ]
lowerLimit=[flux - fluxError for flux, fluxError in zip(flux, fluxError) ]
print(upperLimit)
print(lowerLimit)
plt.figure()
plt.errorbar(tT0,flux,xerr=upperLimit,yerr=lowerLimit,fmt='o')
plt.xlabel('t-T0(days)')
plt.ylabel('Flux(Jy)')
plt.show()

# tT0=[0.3,0.6208333,0.6208333,1.2391667,0.76208333,0.76208333,1.504167,0.869959491,2.6216667,2.6216667,2.6216667,2.6216667,2.6216667,2.6216667,0.5625]

# flux=[8.81E-04,2.13E-04,3.54E-05,1.09E-04,3.10E-04,5.39E-04,7.92E-05,2.00E-04,5.71E-05,6.87E-05,8.79E-05,2.28E-04,4.89E-05,3.21E-05,3.22E-04]

# fluxError=[1.60E-05,4.00E-06,1.60E-06,6.00E-06,4.30E-05,5.70E-05,0.00E+00,3.00E-06,1.10E-06,1.20E-06,1.60E-06,4.00E-06,1.30E-06,9.00E-07,0.00E+00]

# upperLimit=[flux + fluxError for flux, fluxError in zip(flux, fluxError) ]
# lowerLimit=[flux - fluxError for flux, fluxError in zip(flux, fluxError) ]

# # print(upperLimit)
# # print(len(upperLimit))
# # print(lowerLimit)
# # print(len(lowerLimit))

# plt.figure()
# plt.errorbar(tT0,flux,xerr=upperLimit,yerr=lowerLimit,fmt='o')
# plt.xlabel('t-T0(days)')
# plt.ylabel('Flux(Jy)')
# plt.show()
