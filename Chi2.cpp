#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

float ptnu_bin[6] = {0.0, 0.5, 1.0, 1.5, 2.0, 4.0};

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
vector<vector<float> > read_files(std::string files, bool is_model=false, int verbose = 0){
    vector<vector<float> > data;
    vector<float> a, b;
    float ai, bi;

    ifstream file(files.c_str());
    if (!file) {
        cout << "Error opening file" << endl;
        exit(EXIT_FAILURE);
    }

    while (file >> ai >> bi) {
        a.push_back(ai);
        b.push_back(bi);
    }
    
    data.push_back(a);
    data.push_back(b);

    vector<float > model;
    for (int i=0; i < (sizeof(ptnu_bin)/sizeof(float) - 1); i++){
        float variable_value = get_bin(data, ptnu_bin[i], ptnu_bin[i+1], verbose); 
        model.push_back(variable_value);
        if(verbose > 1 ) cout << "bin "<< i << ", value " << variable_value << endl; 
    }

    float a_v = get_bin(data, 0.0, 0.5, verbose);

    cout << "Number of lines: " << a.size() << endl;
    
    return data;
}

int main(){

    cout<<" hello Huma"<<endl;
    
    vector<vector<float> > data = read_files("/Users/marvinascenciososa/Downloads/chisq/5M_data/ptnu.txt", false, 2);

    cout << "read from here " << endl; 

    //for (int j = 0; j < data[0].size(); j++){
    //    cout << data[0][j] << " " << data[1][j] <<endl;
    //}

    return 0;
}
