import pandas as pd
import os

def read_data(file_path):
    """
    Reads one Excel file and returns the Pred Mods and %Quant (Area) columns
    """
    df = pd.read_excel(file_path, header=1)
    columns_to_keep = ['Pred Mods', '%Quant (Area)']
    df = df[columns_to_keep]
    return df


def simplify_data(data):
    '''
    Input: data (pandas dataframe) with column of Pred Mods and %Quant (Area)
    Combines similar glycoforms
    '''
    keys = ['1*G0 ', '1*G0F', '1*G1(', '1*G1F', '1*G2 ', '1*G2F',
        '2*G0 ', '2*G0F', '2*G1(', '2*G1F', '2*G2 ', '2*G2F']
   
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
        data_comb[keys_comb[i]] = (data_simp[keys[i]]/2 + data_simp[keys[i+6]])
   
    data_comb = list(data_comb.items())
    return data_comb

def read_simp_glycan(filepath):
    # returns dataframe
    # read in data
    data = read_data(filepath)
    # simplify the data
    glycan_data = simplify_data(data)
    # convert list to dataframe
    glycan_df = pd.DataFrame(glycan_data)
    # flip orientation
    glycan_df = glycan_df.transpose()
    # make name of glycans column names
    glycan_df.columns = glycan_df.iloc[0]
    glycan_df = glycan_df[1:]
    return glycan_df

def get_glycan_data(foldername, glycanname):
    # returns df with all the glycan data
    path = os.path.join(foldername, glycanname)
    if os.path.isfile(path):
        # If it's a file, read it directly
        data = read_simp_glycan(path)
    elif os.path.isdir(path):
        df_list = []
        # If it's a directory, read all files in the directory
        files = os.listdir(path)
        for file in files:
            file_path = os.path.join(path, file)
            df = read_simp_glycan(file_path)
            df_list.append(df)
        # combine all the glycan data
        data = pd.concat(df_list)
        data = data.mean().to_frame().transpose()
    return data

def read_all_data(foldername, time, glycanname, filenames):
    # all inputs are strings
    
    # time is when the data was collected
    # data for each time point is in folder with that name
    path = os.path.join(foldername, time)

    # glycans
    glycan_df = get_glycan_data(path, glycanname)

    # Read in all the rest
    df_list = []
    # read in each file into a dataframe
    for filename in filenames:
        file_path = os.path.join(path, filename)
        df = pd.read_excel(file_path)
        df_list.append(df)

    # add glycans to list of dataframes with all the data
    df_list.append(glycan_df)

    # combine all the dataframes
    data_all = pd.concat(df_list, axis=1)

    # set index as time in hours
    data_all.index = pd.Index([24*int(time)]*len(data_all))
    
    return data_all

glycans = get_glycan_data('data', 'glycans')
glycans.to_excel('glycans.xlsx')
