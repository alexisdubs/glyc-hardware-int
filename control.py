# %%
from read_fncs import read_all_data
from rest_fncs import set_setpoint
import pandas as pd

# %%
def dummy_control(data):
    med_flow = 1
    gal_conc = 0.1
    urd_conc = 0.1
    return med_flow, gal_conc, urd_conc


## user edits this
# name of folder all of the results are placed in
foldername = 'data'
start_time = '2024-08-01 00:00'
# file exported from Agilent Bioconfirm software
glycanname = 'glycans.xls'
glycan_time = ['2024-08-01 12:00']
# name of all the other files
# standard formatting is Col 1: timestamp, other columns are measurements
# need to have column headers in excel files
filenames = ['rebel.xlsx', 'nova_octet.xlsx', 'galactose_uridine.xlsx', 'ns_nsd.xlsx']
# for testing
filenames = ['other.xlsx']
# experimental configuration (reactor number and control loop number)
med_rn, med_cl = 2, 1
gal_rn, gal_cl = 2, 2
urd_rn, urd_cl = 2, 3

# %%

# Read in data
data = read_all_data(foldername, glycanname, filenames, start_time, glycan_time)

## Feed data to glycopy and get back new setpoints
[med_flow, gal_flow, urd_flow] = dummy_control(data)

# send to reactor
# set_setpoint(med_rn, med_cl, med_flow)
# set_setpoint(gal_rn, gal_cl, gal_flow)
# set_setpoint(urd_rn, urd_cl, urd_flow)


# other inputs to yingjie's code
#   length of time until next control action
#   length of time of control action
#   supplements we have
#   units for measurements
#   objective function
#   constraints
