#!/home/user/anaconda2/bin/python

## Modified from Daniel Buscombe's starter script at https://github.com/dbuscombe-usgs/pyhum
## Supply .DAT file using -i and SON folder using -s
## OR cd into a directory with both .DAT/SON and process all using 'humall' (~/bin/humall)

import sys, getopt

from Tkinter import Tk
from tkFileDialog import askopenfilename, askdirectory

import PyHum
import os

if __name__ == '__main__': 

    argv = sys.argv[1:]
    humfile = ''; sonpath = ''

    temp = 20 # default to 20 degrees Celsius water temperature
    cs = 26983 # default to Maine East State Plane meters if no argument given

    # parse inputs to variables
    try:
       opts, args = getopt.getopt(argv,"hi:s:e:t:")
    except getopt.GetoptError:
         print 'error'
         sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
         print 'help'
         sys.exit()
       elif opt in ("-i"):
          humfile = arg
       elif opt in ("-s"):
          sonpath = arg
       elif opt in ("-e"):
          cs = arg
       elif opt in ("-t"):
          temp = arg


    # prompt user to supply file if no input file given
    if not humfile:
       print 'An input file is required!!!!!!'
       Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
       humfile = askopenfilename(filetypes=[("DAT files","*.DAT")]) 

    # prompt user to supply directory if no input sonpath is given
    if not sonpath:
       print 'A *.SON directory is required!!!!!!'
       Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
       sonpath = askdirectory()


    # print given arguments to screen and convert data type where necessary
    if humfile:
       print 'Input file is %s' % (humfile)

    if sonpath:
       print 'Son files are in %s' % (sonpath)

    doplot = 1 #yes

    # reading specific settings
    
    cs2cs_args = "epsg:"+str(cs)

    # correction specific settings
    ph = 6.7 # acidity on the pH scale
    salinity = 0.0

    # for downward-looking echosounder echogram (e1-e2) analysis
    beam = 20.0
    transfreq = 200.0 # frequency (kHz) of downward looking echosounder
    integ = 5
    numclusters = 3 # number of acoustic classes to group observations

    ## calculate and map the e1 and e2 acoustic coefficients from the downward-looking sonar
    PyHum.e1e2(humfile, sonpath, cs2cs_args, ph, temp, salinity, beam, transfreq, integ, numclusters, doplot)
