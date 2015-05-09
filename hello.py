import flask
from flask import request
#from flask import Response
from werkzeug.wrappers import Response
import os
import kplr
import numpy as np 
from pyfits import * 
from scipy import integrate
from scipy.special import gammaincc
from copy import *
import matplotlib
import matplotlib.pyplot as plt, mpld3
from math import * 

app = flask.Flask (__name__)


def getLC(koinum, koistr):
	client = kplr.API()
	koi = client.koi(koinum) # Find the target KOI.
	lcs = koi.get_light_curves(short_cadence=False) # Get list of datasets.
	f = lcs[0].open() # open the first light-curve dataset
	hdu_data = f[1].data

	time = hdu_data["time"] # get the time of each observation
	flux = hdu_data["sap_flux"] # get the flux
	flux_err = hdu_data["sap_flux_err"] # get the error in the flux
	f.close()

	plt.figure(figsize=(10, 6), facecolor='white')
	plt.plot(time, flux, linestyle='None', marker='.', color= 'black', markersize=5.0)
	plt.xlabel('Time (UTC)', fontsize=12)
	plt.ylabel('Flux (counts/s)', fontsize=12)
        plotName = "KOI %s Light Curve" %koistr
	plt.title(plotName, fontsize=20)
        imgname = "koiplot.png" 
	path = "/home/prattography/Documents/moduni/final/static"
	fullpath = os.path.join(path, imgname)
	plt.savefig(fullpath)

def getModel(koinum, koistr, start, end, int0):
        client = kplr.API()
        koi = client.koi(koinum) # Find the target KOI.
        lcs = koi.get_light_curves(short_cadence=False) # Get list of datasets.
        f = lcs[0].open() # open the first light-curve dataset
        hdu_data = f[1].data
        
        time = hdu_data["time"] # get the time of each observation
        flux = hdu_data["sap_flux"] # get the flux
        flux_err = hdu_data["sap_flux_err"] # get the error in the flux
        f.close()
        
        newtime = []
        newflux = []
        newfluxerr = []
        for i in range (0, len(time)):
            if ((time[i] > start) and (time[i] < end)): 
                newtime.append(time[i])
                newflux.append(flux[i]) 
                newfluxerr.append(flux_err[i])
                
        fluxavglist1 = deepcopy(newflux)
        
        for k in range (0, 5):
            fluxavglist2 = []
            newfluxavg = np.mean(fluxavglist1)
            newfluxstd = np.std(fluxavglist1)
            for j in range (0, len(newflux)):
                if ((np.abs(newflux[j] - newfluxavg)/ newfluxstd) <= 2):
                    fluxavglist2.append(newflux[j])
            fluxavglist1 = deepcopy(fluxavglist2)
        
        # print (newfluxavg, newfluxstd); just to test what those values are 
        
        normalizedflux = newflux / newfluxavg
        normalizedfluxerr = newfluxerr / newfluxavg
        
        def modelFunc(ti, p, tau, t0):
            p = 0.078
            z = abs(ti - t0) / tau
            def delta(p, r, z):
                if ((r >= (z + p)) or (r <= (z - p))):
                   # print "boO"
                    return 0
                elif ((r + z) <= p):
                    #print "boo dos"
                    return 1
                else: 
                    #print "ay"
                    return ((1/pi) * acos((z**2 - p**2 + r**2)/(2*z*r)))
                
            def I(r):
                mu = (1 - r**2)**0.5
                return 1 - (1 - (mu**0.5))
                
            def function1(r):
                deltaresult = delta(p, r, z) # stored delta value in deltaresult 
                return I(r) * (1 - deltaresult) * (2*r)
            
            def function2(r):
                return I(r) * 2*r    
            
            func1 = integrate.quad(function1, 0, 1)
            func2 = integrate.quad(function2, 0, 1)
            flux = func1[0] / func2[0]
            return flux
        
        p = 0.078
        tau = 0.1
        t0 = int0
        modelFlux = []
        for i in range (0, len(newtime)):
            f = modelFunc(newtime[i], p, tau, t0)
            modelFlux.append(f)
    
        # computing the Chi Squared
        chiSquared = 0
        for i in range(0, len(newtime)):
            chiSquared += ((normalizedflux[i] - modelFlux[i]) / normalizedfluxerr[i])**2
            #print chiSquared
        
        #return chiSquared
        plt.figure(figsize=(10, 6), facecolor='white')

        plt.plot(newtime, normalizedflux, linestyle='None', marker='.', color= 'black', markersize=7.0)
        plt.plot(newtime, modelFlux, linestyle='-', marker='.', color= 'red', markersize=7.0)
        plt.xlabel('Time (UTC)', fontsize=12)
        plt.ylabel('Flux Ratio', fontsize=12)
        plotName = "KOI %s Light Curve" %koistr
	plt.title(plotName, fontsize=20)
        imgname = "koiplotmodel.png" 
	path = "/home/prattography/Documents/moduni/final/static"
	fullpath = os.path.join(path, imgname)
	plt.savefig(fullpath)
         
@app.route('/') 
def hello():
	return flask.render_template('index.html')


@app.route('/koi-lookup', methods=['POST', 'GET'])
def show_kplr_plot():
	searchwordFlt = request.args.get('key', '', type=float)
	searchwordStr = request.args.get('key', '')
        getLC(searchwordFlt, searchwordStr)
       # getModel(searchwordFlt, searchwordStr)
        #resp = Response()
        resp = flask.render_template('display.html')
  
        return resp #  flask.render_template('display.html')

@app.route('/koi-model', methods=['POST', 'GET'])
def show_model_section():
	searchwordFlt = request.args.get('key', '', type=float)
	searchwordStr = request.args.get('key', '')
        startStr = request.args.get('start', '')
        endStr = request.args.get('end', '')
        startFlt = request.args.get('start', '', type=float)
        endFlt = request.args.get('end', '', type=float)
        tauFlt =  request.args.get('taunot', '', type=float)
        if (endStr == '' or startStr == ''):
                return show_kplr_plot()
        else:
                getModel(searchwordFlt, searchwordStr, startFlt, endFlt, tauFlt)
                return flask.render_template('displaymodel.html')
        
if __name__ == "__main__":
	app.run(debug=True)
