# Problem 1 

import kplr
import numpy as np 
from pyfits import * 
import matplotlib
import matplotlib.pyplot as plt
from math import * 
#%matplotlib inline

client = kplr.API()
koi = client.koi(97.01) # Find the target KOI.
lcs = koi.get_light_curves(short_cadence=False) # Get list of datasets.
f = lcs[0].open() # open the first light-curve dataset
hdu_data = f[1].data

time = hdu_data["time"] # get the time of each observation
flux = hdu_data["sap_flux"] # get the flux
flux_err = hdu_data["sap_flux_err"] # get the error in the flux
f.close()

plt.figure(figsize=(12, 8), facecolor='white')

plt.plot(time, flux, linestyle='None', marker='.', color= 'black', markersize=5.0)
plt.xlabel('Time (UTC)', fontsize=12)
plt.ylabel('Flux (counts/s)', fontsize=12)
plt.title('KOI 97 Light Curve', fontsize=20)

plt.show()
