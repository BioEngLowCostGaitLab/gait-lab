#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <algorithm>
#include <iterator>
#include <cmath>
#include <fstream>

using namespace std;

int main()
{	
	ifstream myfile;
	myfile.open("Gaitsway.txt");
	string s;
	vector <string> vfile;
	vector <double> tdata;
	vector <float> xdata;
	vector <float> ydata;
	vector <float> zdata;
	while(getline(myfile, s).good()){
   		 if(s.find("\t") != string::npos){
        	string delimiter = "\t";
			size_t pos = 0;
			string token;
       	while ((pos = s.find(delimiter)) != string::npos){
            token = s.substr(0, pos);
            s.erase(0, pos + delimiter.length());
            vfile.push_back(token);
        }
        vfile.push_back(s);
    	}
    	else{
        vfile.push_back(s);
    	}
	
	}
	
	for(int i=1; i<vfile.size(); i = i+6){
		double timestamp = stod(vfile[1]);
		double temp = stod(vfile[i]);
		double time = temp - timestamp;
		tdata.push_back(time);
	}

	for(int i=2; i<vfile.size(); i = i+6){
		xdata.push_back(stof(vfile[i]));
	}

	for(int i=3; i<vfile.size(); i = i+6){
		ydata.push_back(stof(vfile[i]));
	}

	for(int i=4; i<vfile.size(); i = i+6){
		zdata.push_back(stof(vfile[i]));
	}

	for(int i=0; i<xdata.size(); i++){
		cout <<	"x: " << xdata[i] << " y: " << ydata[i] << " z: " << zdata[i] << endl;
		
	}	

	ofstream outfile ("data.txt");
	
	for(int i = 0; i<xdata.size(); i++){
		outfile << tdata[i] << endl;
		outfile << xdata[i] << endl;
		outfile << ydata[i] << endl;
		outfile << zdata[i] << endl;
	}
	outfile.close();
		
}
