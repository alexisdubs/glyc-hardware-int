# Questions for Naresh
1. What is initial volume in bioreactor?
2. Do we have SOP written out for bioreactor run?

# Questions for Jing/Yingjie
1. Have you done any analysis on thee old data from the last fed batch run? Are we planning to do any?
2. Were you able to find any conditions/objectives that led to the control action not just being dump everything in on day 1?
3. Should we allow for this behavior or not?
4. What supplements do we want?
no answers to any of these

# Setup
## model_setting_0_estimate
1. What is initial volume? - 1.5 L
2. How to estimate some initial concentrations?  
    pull from old runs to figure out estimates?
    put estimates in this file and then also in estimated parameters file
3. Need to set concentration feeds - decide on feeds and conc

## control_setting_0
1. Do i need to change multipliers and u0?
    u0 should be tvx0 flattened
2. What is multipliers?? - just leave alone
3. Need to set tvx0, lb, and ub
4. Need to set sampling time and control time in control_setting_0  

## estimated_parameters_0
1. I leave all the parameters the same?
2. Put unknown concentrations in control tab of estimated_parameters_cell_culture
3. How do i have estimate the unknown concentrations??
4. same questions for all the other parameter files

# To Do
1. Go through setup questions with Yingjie
2. Other setup
    - all feed concentration
    - limits
    - initial estimates for some things
2. Test out code operation with sample data from last run
3. test out operation with hardware

# Other notes
glucose constraint  
can we model osmotic pressure? - constraint on osmotic pressure?

# Operation
1. Get data from Naresh - put into format given by Yingjie
2. Run code
3. Get control output from DOEs_full_i.xlsx - where is this file?? - mpc_data_individual/experimental data
4. Send control output to bioreactor - use old script 
5. don't need to keep code running - just need to feed it right index and it will read from excel files