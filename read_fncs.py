import pandas as pd
import os

def read_data(file_path):
    """
    Reads one Excel file and returns the Pred Mods and %Quant (Area) columns
    """
    df = pd.read_excel(file_path, header=1)
    glycan_time = df['Time'].iloc[0]
    columns_to_keep = ['Pred Mods', '%Quant (Area)']
    df = df[columns_to_keep]
    return df, glycan_time

def simplify_data(data):
    '''
    Input: data (pandas dataframe) with column of Pred Mods and %Quant (Area)
    Combines similar glycoforms
    '''
    keys = ['1*G0', '1*G0F', '1*G1', '1*G1F', '1*G2', '1*G2F',
        '2*G0', '2*G0F', '2*G1', '2*G1F', '2*G2', '2*G2F']
   
    # initialize data
    default_value = 0
    data_simp = dict.fromkeys(keys, default_value)

    # combine all similar predicted mods
    # iterate through each row of the data
    for row in data.itertuples(index=False):
        pred_mod = str(row[0])
        quant_area = row[1]
        for key in keys:
            # test if glycan is in this row
            if key in pred_mod:
                # if it is add percent quant area
                data_simp[key] = data_simp[key] + quant_area
   
   
    # data_comb_area = pd.DataFrame(columns = ['Pred Mods', '%Quant (Area)'])
    # data_comb_area['Pred Mods'] = ['G0', 'G0F', 'G1', 'G1F', 'G2', 'G2F']
    keys_comb = ['G0', 'G0F', 'G1', 'G1F', 'G2', 'G2F']
    data_comb = dict.fromkeys(keys_comb, default_value)
    for i in range(6):
        data_comb[keys_comb[i]] = (data_simp[keys[i]] + 2*data_simp[keys[i+6]])
   
    data_comb = list(data_comb.items())
    return data_comb

def read_all_data(foldername, glycanname, filenames, start_time):
    # all inputs are strings
    # start_time is when the run started
    # glycan_time is when the glycan data was collected

    # glycans
    # read in glycan data
    file_path = os.path.join(foldername, glycanname)
    [data, glycan_time] = read_data(file_path)
    glycan_data = simplify_data(data)
    # convert list to dataframe
    glycan_df = pd.DataFrame(glycan_data)
    # flip orientation
    glycan_df = glycan_df.transpose()
    # make name of glycans column names
    glycan_df.columns = glycan_df.iloc[0]
    glycan_df = glycan_df[1:]

    # adjust times to be datetime type
    start_time = pd.to_datetime(start_time)
    glycan_time = pd.to_datetime(glycan_time)

    # set glycan time as index
    glycan_df.index = [glycan_time]
    glycan_df.index.name = 'datetime'

    # Read in all the rest
    df_list = []
    # read in each file into a dataframe
    for filename in filenames:
        file_path = os.path.join(foldername, filename)
        df = pd.read_excel(file_path, index_col=0)
        df_list.append(df)

    # add glycans to list of dataframes with all the data
    df_list.append(glycan_df)

    # combine all the dataframes
    data_all = pd.concat(df_list)
    # sort so in order of date time
    data_all = data_all.sort_index()

    # convert dateteime to time since start
    difference = data_all.index - start_time
    difference = difference.total_seconds()/3600
    data_all.set_index(difference, inplace=True)

    return data_all
