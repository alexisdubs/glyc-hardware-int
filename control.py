from read_fncs import read_all_data
# from rest_fncs import set_setpoint
import pandas as pd

def dummy_control(data):
    med_flow = 1
    gal_conc = 0.1
    urd_conc = 0.1
    return med_flow, gal_conc, urd_conc


## user edits this
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
# concentration of supplement solutions
gal_stock_conc = 50
urd_stock_conc = 50
# experimental configuration (reactor number and control loop number)
med_rn, med_cl = 2, 1
gal_rn, gal_cl = 2, 2
urd_rn, urd_cl = 2, 3

# Read in data
data = read_all_data(foldername, glycanname, filenames)
print(data)

## Feed data to glycopy and get back new setpoints
# output is overall media flowrate and concentration of galactose and uridine
[med_flow, gal_conc, urd_conc] = dummy_control(data)

# calculate supplemental solution flowrates
gal_flow = med_flow*gal_conc/gal_stock_conc
urd_flow = med_flow*urd_conc/urd_stock_conc

# send to reactor
# set_setpoint(med_rn, med_cl, med_flow)
# set_setpoint(gal_rn, gal_cl, gal_flow)
# set_setpoint(urd_rn, urd_cl, urd_flow)


# other inputs to yingjie's code
#   length of time until next control action
#   length of time of control action
#   supplements we have
#   units for measurements
