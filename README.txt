Pratishta Yerakala
py2211
W4260 Final Project - KOI Web App

i) Introduction
We have been given a brief introduction to the Kepler discoveries and how to
use the python module kplr to get information about these objects. The kplr
API (http://dan.iel.fm/kplr/#api-interface) allow us to input a KOI number
and extract information about the system such as light curves and fits
files. But we can also use that information to manipulate the data and
produce model-fitting plots. Having access to the data in this manner allows
this app to use numerical methods and other techniques to display general
behavior of the system so that we could easily decide if we would like to
study it further (especially if there are any interesting patterns). The app
uses Flask (http://flask.pocoo.org/docs/0.10/quickstart/) 

ii) Numerical methods
The app makes use of model-fitting from problem set 7. While Chi-Squared can
be calculated, it cannot be displayed at this time in the app development
process. However, the model-fitting code can used. Taking in user input, the
app uses the model-fitting code from the problem set but allows the model to
be fit to an KOI the user chooses. 

iii) Summary
The app uses Flask to serve contents to the web. All the files and
directories need to be downloaded in that structure for the app to work on
the local host. Python code for the numerical methods are written in "koiapp.py"
and the app itself can be run by:

$ python koiapp.py

Then, on a browser (preferably Firefox, since the app hasn't been tested on
others), with "localhost:5000" in the url box, the app will show. Cache
needs to be disabled in the browser, or else new plots will not display when
new KOI numbers are entered. The .html files are stored in the "templates"
directory and the plots generated from the app are stored in the "static"
folder.

What it can do: 
It can work on the localhost, and on port 5000 by default. It asks for a KOI
number as user input. Once "Submit query" or the return key has been
pressed, it displays a light curve of the system. In the new page,
additional boxes are available so that the viewer could input another KOI
number (probably the one that they're currently looking at the light curve
for) and the start and end times for the ecplises. The user should also put
in the t_0 of where the lowest luminosity is. The submit box has a step
feature so that the user could adjust the step and have a more accurate
result. (If the user enters only a KOI number in the "Enter eclipse section:" page,
the whole lightcurve for that system will display.) Once that is submitted, the 
app displays a model (in red and '-' for linestyle). 


What it cannot do: 
There have been no error checks done, so the app assumes that the user will
input the correct parameters at all times. Else, the app doesn't exactly
crash, but will display error messages (albeit in an ungraceful manner). The
app also unfortunately, at this stage, only runs on the localhost. Ideally,
it would be on a server with its own domain name but that's looking into the
future to deploy the app. 

A good test: 
KOI: 97.01
start: 124
end: 125
tau0: 124.51

Of course, if the user has a good enough eye, they can make models with
other eclipses but the data above can produce a definite model that fits
pretty well. 

iv) Discussion
The Kepler Mission site (http://kepler.nasa.gov/Mission/discoveries/) has
information on all the systems discovered so far. Clicking on an object
allows us to see the light curves, size, mass, and a lot of other features.
The reason the KOI Web App might be useful despite the convenient use of the
original Kepler site is so that numerical methods can be used to analyze the
information provided. It might be especially useful if there were to be
a study done on certain types of planets (such as ones that have specific
behaviors in eclipses, or systems with overall increase or decrease in
luminosity). 

I would like to develop this app much further than what it can
do now (and make it look a lot better hopefully!) so that it could implement
other numerical methods as well. I'd like for it to first and foremost, do
error-checking. Then, provide a better user interface to make the app seem
more complete before adding additional features (which might end up becoming
more difficult to adjust to the design later). Then, I'd like to take
advantage of the kplr API to acquire fits files and do some sort of image
analysis. 

This is my first time doing anything like front-end development for making
an app but I think it was an excellent learning experience. I loved using
numerical methods with data in astrophysics, but I think it would be even
better to share those discoveries with an audience who only need a glimpse
to appreciate the data. I think it would also be useful - and this is
something I'd like to improve with the app - is have an educational
component so that the user could learn more about numerical methods as they
tinker with the app. 
