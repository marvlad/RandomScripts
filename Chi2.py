import pandas as pd

def get_bin(variable,lim_0, lim_1):
    bin = 0
    bin_c = 0
    # iterate over rows using iterrows
    for index, row in variable.iterrows():
        if row['xaxis'] >= lim_0 and row['xaxis'] < lim_1:
            bin += row['yaxis']
            bin_c += 1 
    return bin/bin_c

def read_file(path,is_mc):
    variable_values = []
    r_values = []
    d_bins = [0.0, 0.5, 1.0, 1.5, 2.0, 4.0]

    with open(path, 'r') as file:
        for line in file:
            p = line.split()
            if is_mc == True:
                variable_values.append([float(p[0]),float(p[1])])
            else:
                variable_values.append([float(p[1]),float(p[2])])

    variable = pd.DataFrame(variable_values, columns=['xaxis','yaxis'])

    if is_mc == True:
        for i in range(0,(len(d_bins)-1)):
            r_values.append(get_bin(variable,d_bins[i],d_bins[i+1]))
        return pd.DataFrame(r_values,columns=['yaxis_m'])
    else:
        variable.rename(columns = {'xaxis':'yaxis_d', 'yaxis':'yaxis_d_e'}, inplace = True)
        return variable

def get_chi2(d_pd,m_pd, pv):
    chi2 = 0
    full_data = pd.concat([d_pd, m_pd], axis=1)

    # iterate over rows using iterrows
    for index, row in full_data.iterrows():
        s_chi2 = (row['yaxis_d'] - row['yaxis_m'])
        if pv > 1:
            print(row['yaxis_d'], row['yaxis_d_e'],row['yaxis_m'],s_chi2, (s_chi2*s_chi2), (s_chi2*s_chi2)/row['yaxis_d_e'])
        chi2 += (s_chi2*s_chi2)/row['yaxis_d_e'] 
    
    return chi2 

def main():
    filepath_m='ptnu.txt'
    filepath_d='ptnudata.txt'

    model = read_file(filepath_m, True)
    data = read_file(filepath_d, False)

    print(get_chi2(data,model,0))

if __name__ == "__main__":
    main()
