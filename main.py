import sys
import os
import time
import traceback
import pandas as pd
from read_fncs import read_all_data
from rest_fncs import set_setpoint
from other_fncs import check_options, fill_nans
from glycosylation_python.glyco.mpc_data.glyco_qss_move_one_step_mpc import MPCWrapper

## user edits this
# name of folder all of the results are placed in
foldername = 'data'
# file exported from Agilent Bioconfirm software
glycanname = 'glycans'
# name of all the other files
# need to have column headers in excel files
#filenames = ['rebel.xlsx', 'nova_octet.xlsx', 'galactose_uridine.xlsx', 'ns_nsd.xlsx']
# for testing just put everything in one
filenames = ['other.xlsx']

# experimental configuration (reactor number and control loop)
# control loop selection is a string of either Med, Glut, or Gluc
fma_rn, fma_cl = 2, 'med'
fmb_rn, fmb_cl = 2, 'glut'
gal_rn, gal_cl = 2, 'glut'
urd_rn, urd_cl = 2, 'gluc'

# make sure correct control loop syntax selection
# loops = [med_cl, gal_cl, urd_cl]
# options = ['med', 'glut', 'gluc']
# check_options(loops, options)

# for testing
def set_setpoint(a, b, c):
    pass

# create mpc wrapper object
#wrapper = MPCWrapper()
wrapper = MPCWrapper(days=4, real_plant=True)

for i in range(4): #while True:
    try:
        day = f'{i}'#input('Enter the day. Must be an integer')
        # Read in data
        data = read_all_data(foldername, day, glycanname, filenames)
        data = fill_nans(data)
        data.to_excel('dataframe.xlsx')

        # Feed data to glycopy and get back new setpoints
        control_action = wrapper.move_one_step(data)
        #control_action = pd.read_pickle('example_control.pkl')
        # control action is dataframe with index of time in hours from now
        # columns are media, galactose, and uridine flowrates in L/hr
        # we need the first two rows because we want to send a pulse and then stop it

        # unpack control actions and convert to mL/hr
        fma_flow, fmb_flow, gal_flow, urd_flow = control_action.iloc[0] * 1000 # mL/hr
        fma_flow2, fmb_flow2, gal_flow2, urd_flow2 = control_action.iloc[1] * 1000 # mL/hr

        # grab time and convert to seconds
        delay = control_action.index[1]*3600 # seconds

        print('Sending control action to reactor')
        # send first control action to reactor
        set_setpoint(fma_rn, fma_cl, fma_flow)
        set_setpoint(fmb_rn, fmb_cl, fmb_flow)
        set_setpoint(gal_rn, gal_cl, gal_flow)
        set_setpoint(urd_rn, urd_cl, urd_flow)

        print('Control action occuring')

        # wait
        #time.sleep(delay)

        print('Turning control action off')

        # send second control action to reactor
        set_setpoint(fma_rn, fma_cl, fma_flow2)
        set_setpoint(fmb_rn, fmb_cl, fmb_flow2)
        set_setpoint(gal_rn, gal_cl, gal_flow2)
        set_setpoint(urd_rn, urd_cl, urd_flow2)
    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
        #raise ValueError('Stop')
    i += 1

        
# other inputs to glycopy - see glycopy user manual to know how to edit
#   length of time until next control action
#   length of time of control action
#   supplements we have
#   supplement concentration
#   units for measurements
#   objective function
#   constraints
#   measurement uncertainty