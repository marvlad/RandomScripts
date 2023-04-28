import pandas as pd

model_path = '/5M_data/' 
data_path = '/E866data/'

mnu_bin  = [4.5, 5.5, 6.5, 7.5, 8.5, 9.0, 10.7, 15.0]
ptnu_bin = [0.0, 0.5, 1.0, 1.5, 2.0, 4.0]
x1nu_bin = [0.15, 0.35, 0.45, 0.55, 0.65, 0.85]
x2nu_bin = [0.02, 0.04, 0.06, 0.08, 0.10, 0.14, 0.24]
xfnu_bin = [0.0, 0.25, 0.35, 0.45, 0.55, 0.8]

data_bin = {'mnu':mnu_bin, 'x1nu':x1nu_bin, 'x2nu':x2nu_bin,'xfnu':xfnu_bin,'ptnu':ptnu_bin }
#variablie_names = ['x1nu','x2nu','xfnu','mnu','ptnu']
#variablie_names = ['ptnu']

def get_bin(variable,lim_0, lim_1, vrb):
    bin = 0
    bin_c = 0
    # iterate over rows using iterrows
    for index, row in variable.iterrows():
        if row['xaxis'] >= lim_0 and row['xaxis'] < lim_1:
            bin += row['yaxis']
            bin_c += 1
    if vrb > 1:
        print('Creating the binning: ', lim_0, lim_1, bin, bin_c) 
    return bin/bin_c

def read_file(path,is_mc, d_bins, vrb):
    variable_values = []
    r_values = []

    with open(path, 'r') as file:
        for line in file:
            p = line.split()
            if is_mc == True:
                variable_values.append([float(p[0]),float(p[1])])
            else:
                variable_values.append([float(p[1]),float(p[2])])

    variable = pd.DataFrame(variable_values, columns=['xaxis','yaxis'])
    if vrb > 1:
        print('This is the dataFrame from the file:')
        print(variable)
    if is_mc == True:
        for i in range(0,(len(d_bins)-1)):
            r_values.append(get_bin(variable, d_bins[i], d_bins[i+1], vrb))
        return pd.DataFrame(r_values,columns=['yaxis_m'])
    else:
        variable.rename(columns = {'xaxis':'yaxis_d', 'yaxis':'yaxis_d_e'}, inplace = True)
        return variable

def get_chi2(d_pd,m_pd, variable, vrb):
    chi2 = 0
    if variable == 'mnu':
        m_pd = m_pd.drop(5).reset_index(drop=True)

    full_data = pd.concat([d_pd, m_pd], axis=1)
    if vrb > 1:
        print('Inputs for the Chi2 of ', variable, 'in dataFram')
        print(full_data)

    # iterate over rows using iterrows
    for index, row in full_data.iterrows():
        s_chi2_n = (row['yaxis_d'] - row['yaxis_m'])
        s_chi2_d = row['yaxis_d_e'] 
        s_chi2   = s_chi2_n/s_chi2_d
        if vrb > 1:
            print('Chi2 INFO: ', row['yaxis_d'], row['yaxis_d_e'], row['yaxis_m'],s_chi2_n, s_chi2_d, s_chi2*s_chi2)
        chi2 += s_chi2 * s_chi2 

    return chi2 

def get_chi2_variable(variable, is_pp, vrb):
    if is_pp == True:
        end_txt = 'pp.txt'
    else:
        end_txt = '.txt'
    
    path_file_model = model_path + variable + end_txt 
    path_file_data = data_path + variable + 'data' + end_txt

    #print('Reading the data and model files from:')
    #print(path_file_data)
    #print(path_file_model)

    model = read_file(path_file_model, True, data_bin[variable], vrb)
    data = read_file(path_file_data, False, data_bin[variable], vrb)

    return get_chi2(data,model, variable, vrb)

def get_all_chi2(variable_names, is_pp, vrb):
    for i in range(len(variable_names)):
        if is_pp == True:
            tag = 'pp'
        else:
            tag = ''
        print(variable_names[i], tag, get_chi2_variable(variable_names[i], is_pp, vrb))

def main():
    variable_names = ['x1nu','x2nu','xfnu','mnu','ptnu']
    variable_names = ['ptnu']
    get_all_chi2(variable_names, True, 0)
    #get_all_chi2(variable_names, False)

if __name__ == "__main__":
    main()
