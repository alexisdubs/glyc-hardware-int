import sys
import os
import time
from read_fncs import read_all_data
# for testing
#from rest_fncs import set_setpoint
import pandas as pd

## user edits this
# path to glycopy code
glycopy_path = ".."
# bioreactor inoculation time
start_time = '2024-08-01 00:00'
# name of folder all of the results are placed in
foldername = 'data'
# file exported from Agilent Bioconfirm software
# add a column with the time of the sample
glycanname = 'glycans.xls'
# name of all the other files
# standard formatting is Col 1: timestamp, other columns are measurements
# need to have column headers in excel files
#filenames = ['rebel.xlsx', 'nova_octet.xlsx', 'galactose_uridine.xlsx', 'ns_nsd.xlsx']
# for testing just put everything in one
filenames = ['other.xlsx']

# experimental configuration (reactor number and control loop number)
med_rn, med_cl = 2, 1
gal_rn, gal_cl = 2, 2
urd_rn, urd_cl = 2, 3

# import glycopy mpc code
# Get the absolute path of the directory
other_directory = os.path.abspath(glycopy_path + "/glycosylation_python/glyco/mpc_data")
# Add the directory to the system path
sys.path.append(other_directory)
# Now you can import the module
from glyco_qss_move_one_step_mpc import MPCWrapper

# for testing
def set_setpoint(a, b, c):
    pass

# create mpc wrapper object
wrapper = MPCWrapper()

while True:
    cont = input('Press \'y\' to read in data and calculate new setpoints. Press \'e\' to exit.')
    if cont == 'e':
        break
    if cont == 'y':
        # Read in data
        data = read_all_data(foldername, glycanname, filenames, start_time)

        # Feed data to glycopy and get back new setpoints
        control_action = wrapper.move_one_step(data, real_plant=True)

        # control action is dataframe with index of time in hours from now
        # columns are media, galactose, and uridine flowrates in L/hr
        # we need the first two rows because we want to send a pulse and then stop it

        # unpack control actions and convert to mL/hr
        med_flow, gal_flow, urd_flow = control_action.iloc[0] * 1000 # mL/hr
        med_flow2, gal_flow2, urd_flow2 = control_action.iloc[1] * 1000 # mL/hr

        # grab time and convert to seconds
        delay = control_action.index[1]*3600 # seconds

        # send first control action to reactor
        set_setpoint(med_rn, med_cl, med_flow)
        set_setpoint(gal_rn, gal_cl, gal_flow)
        set_setpoint(urd_rn, urd_cl, urd_flow)

        # wait
        time.sleep(delay)

        # send second control action to reactor
        set_setpoint(med_rn, med_cl, med_flow2)
        set_setpoint(gal_rn, gal_cl, gal_flow2)
        set_setpoint(urd_rn, urd_cl, urd_flow2)

        
# other inputs to glycopy - see glycopy user manual to know how to edit
#   length of time until next control action
#   length of time of control action
#   supplements we have
#   supplement concentration
#   units for measurements
#   objective function
#   constraints