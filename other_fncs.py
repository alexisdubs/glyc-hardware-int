import os
import pandas as pd
import numpy as np

def check_options(variables, options):
    invalid_vars = [var for var in variables if var not in options]
    if invalid_vars:
        raise Exception(f"The following options are not valid: {', '.join(invalid_vars)}")
    
def fill_nans(data):
    path = os.path.join('glycosylation_python', 'glyco', 'mpc_data', 'name_dict.xlsx')
    name_dict = pd.read_excel(path)
    variable_names = name_dict['external'].tolist()
    for var in variable_names:
        if var not in data.columns:
            data[var] = np.nan  # Add missing variable with NaN values
    return data
