## IMPORT THINGS
# surely there is a better way to do this, but copying from Yingjie's code rn
import os
import sys
import pandas as pd
import time

from glycosylation_python.glyco.mpc_data_individual.estimate_cell_culture import estimate_cell_culture
from glycosylation_python.glyco.mpc_data_individual.estimate_nsd import estimate_nsd
from glycosylation_python.glyco.mpc_data_individual.estimate_golgi import estimate_golgi
from glycosylation_python.glyco.mpc_data_individual.simulate import simulate_trajectory
from glycosylation_python.glyco.mpc_data_individual.dynamic_optimization import optimize
from glycosylation_python.glyco.mpc_data_individual.operation_generation import generate_operation_disturbed

# EXPERIMENTAL CONFIGURATION (reactor number and control loop)
# control loop selection is a string of either Med, Glut, or Gluc
# list of reactor numbers for control loops
# FMA, FMB, Glutamine, Glucose, Uridine, Galactose
# rn = [2, 2, 2, 1, 1, 1]
# cl = ['med', 'glut', 'gluc', 'med', 'glut', 'gluc']
rn = [2]
cl = ['med']

# for testing
def set_setpoint(a, b, c):
    pass

## DATA ACQUIRING
# all of the data processing is taken care of manually - just put it in the appropriate excel file
# in glyco/mpc_data_individual/experimental_data
# want to put data in cell_culturue_i, golgi_i, and nsd_i

## RUN GLYCOPY
# set up number of control intervals
n_interval = 12

for interval in range(1, n_interval+1):

    # tell the user what's up
    print(f'Iteration {interval}')
    input('Press Enter to execute')

    # Run Glycopy
    control_file_path = f'glycosylation_python/glyco/mpc_data_individual/control/control_setting_{interval}.xlsx'
    t_control = pd.read_excel(control_file_path, index_col=0, sheet_name='time').control.iloc[0]

    # don't estimate parameters on the first interval because we don't have any data
    if interval > 0:
        estimate_cell_culture(interval=interval, ls_max=50, opt_tol=1e-4)
        estimate_nsd(interval=interval, ls_max=20, opt_tol=1e-4)
        estimate_golgi(interval=interval, ls_max=20, opt_tol=1e-4)
        # Estimated full trajectory and estimated state at the beginning of the current interval
        simulate_trajectory(interval=interval, t_state=t_control, use_qss=True, true_parameters=False)

    optimize(interval=interval, cleo_network=False)
    generate_operation_disturbed(interval, rel_disturbance_level=0.)

    # get control actions
    # rn not checking to be sure file is done being written to - might need to do this later
    # filepath to file with control actions in them
    doe_file_path = f'glycosylation_python/glyco/mpc_data_individual/experimental_data/DOEs_full_{interval}.xlsx'
    # read in dataframe with all control actions
    df = pd.read_excel(doe_file_path, header=1)
    # just look at the two rows with the current control action
    # not sure if this is correct
    control_action = df.iloc[2*interval : 2*interval+2]
    print(control_action)

    # unpack control actions and convert to mL/hr
    flow1 = control_action.iloc[0, 1] * 1000 # mL/hr
    flow2 = control_action.iloc[1, 1] * 1000 # mL/hr

    # grab time and convert to seconds
    delay = (control_action.iloc[1,0] - control_action.iloc[1,1])*3600 # seconds

    print('Sending control action to reactor')
    # send first control action to reactor
    for i in range(len(cl)):
        set_setpoint(rn[i], cl[i], flow1[i])

    print('Control action occuring')

    # wait
    time.sleep(delay)

    print('Turning control action off')

    # send second control action to reactor
    for i in range(len(cl)):
        set_setpoint(rn[i], cl[i], flow2[i])