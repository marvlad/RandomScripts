#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

// Get bin range values
float get_bin(vector<vector<float> > variable , double lim_0, double lim_1, int verbose){
    float value = 0.0;
    int value_counter = 0;
    for (int j = 0; j < variable[0].size(); j++){
        float itr = variable[0][j];
        if(itr >= lim_0 && itr < lim_1){
            value += variable[1][j]; 
            value_counter++;
        } 
    }

    if(verbose > 2) cout << "Creating values based on binning: "<< lim_0 << " " << lim_1 << " " << value << " " << value_counter << endl;

    return value/value_counter;
}

// Reading the files
vector<vector<float> > read_files(string files, bool is_model=false, int verbose = 0, vector <float> variable = {}){

    // Getting the file
    ifstream file(files.c_str());

    // Make sure that the files can be open
    if (!file) {
        cout << "Error opening file" << endl;
        exit(EXIT_FAILURE);
    }

    vector<vector<float> > data;
    vector<vector<float> > model;
    vector<float> a, b;
    float ai, bi;
    string bin_a;

    vector<float > to_return; 

    if(is_model == true){
        // Getting the values from the path
        while (file >> ai >> bi) {
            a.push_back(ai);
            b.push_back(bi);
            if(verbose > 3 ) cout << ai << " " << bi << endl;
            
        }

        // Addting to the vector of vector
        data.push_back(a);
        data.push_back(b);

        // If the file is a model file, we have to do the average 
        for (int i=0; i < (variable.size() - 1); i++){
            float variable_value = get_bin(data, variable[i], variable[i+1], verbose); 
            to_return.push_back(variable_value);
            if(verbose > 1 ) cout << "bin "<< i << ", value " << variable_value << endl; 
        }

        model.push_back(to_return);
        model.push_back(to_return);

        return model;
    } else {
        while (file >> bin_a >> ai >> bi) {
            a.push_back(ai);
            b.push_back(bi);
            if(verbose > 3 ) cout << bin_a << " " << ai << " " << bi << endl;
        }
        // 'b' is the uncertainty of the measurement 
        data.push_back(a);
        data.push_back(b);

        return data;
    }
}

float get_chi2(vector<vector<float> > data, vector<vector<float> > model, int verbose){
    float chi2 = 0;
    for (int j = 0; j < data[0].size(); j++){
        float data_value = data[0][j];
        float model_value = model[0][j];
        float chi2_n = (data_value - model_value);
        float chi2_d = data[1][j];
        float s_chi2 = chi2_n / chi2_d;
        if(verbose > 1 ) cout << data_value << " " << model_value << " " << chi2_d << " , s_chi2 " << s_chi2 << endl;  
        chi2 += s_chi2*s_chi2; 
    } 

    return chi2;
}

int main(){

    int verbose = 2;
    string model_path = "/Users/marvinascenciososa/Downloads/chisq/5M_data/ptnu.txt";
    string data_path = "/Users/marvinascenciososa/Downloads/chisq/E866data/ptnudata.txt";
    vector <float> ptnu_bin{0.0, 0.5, 1.0, 1.5, 2.0, 4.0};

    vector<vector<float> > data =  read_files(data_path, false, verbose, ptnu_bin);
    vector<vector<float> > model = read_files(model_path, true, verbose, ptnu_bin); 

    cout << get_chi2(data, model, verbose) << endl; 

    return 0;
}
