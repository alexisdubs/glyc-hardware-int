from read_fncs import read_all_data
from rest_fncs import set_setpoint
import pandas as pd

# user edits this
# name of folder all of the results are placed in
foldername = 'data'
# file exported from Agilent Bioconfirm software
glycanname = 'glycans.xls'
# name of all the other files
# standard formatting is Col 1: variable name, Col 2: units, Col3+: measurements
# need to have column headers in excel files
filenames = ['rebel.xlsx', 'nova_octet.xlsx', 'galactose_uridine.xlsx', 'ns_nsd.xlsx']
# for testing
filenames = ['other.xlsx']

data = read_all_data(foldername, glycanname, filenames)

## Feed data to glycopy and get back new setpoints
# output is overall media flowrate and concentration of galactose and uridine

## Translate setpoints to reactor and control loop numbers
# need to translate concentration of galactose and uridine to flow rates for concentrated supplements

#for testing
reactorNumber = '2'
controlLoopNumber = 1
flowRateSpt = 123

# sent setpoints to reactor
set_setpoint(reactorNumber, controlLoopNumber, flowRateSpt)


