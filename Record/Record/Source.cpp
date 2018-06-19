#include<iostream>
#include<string>
#include<chrono>
#include<vector>

#include<opencv2/core.hpp>
#include<opencv2/calib3d.hpp>
#include<opencv2/highgui.hpp>
#include<opencv2/videoio.hpp>
#include<opencv2/imgproc.hpp>
#include<opencv2/plot.hpp>

using namespace std;
using namespace cv;
using namespace std::chrono;

int main()
{
	bool close = false;
	int num_cam = 2;
	vector<VideoCapture> input_capture;

	input_capture.resize(num_cam);

	/*open camera*/
	for (int i = 0; i < num_cam; i++) {
		input_capture[i].open(i);
		if (input_capture[i].isOpened()) {
			cout << i << " successfully opened for capture." << endl;
		}
		else {
			cout << i << " cannot be opened for capture." << endl;
		}
	}
	
	for (int i = 0; i < num_cam; i++)
	{
		input_capture[i].set(CV_CAP_PROP_FRAME_HEIGHT, 720);
		input_capture[i].set(CV_CAP_PROP_FRAME_WIDTH, 1280);
		//input_capture[i].set(CV_CAP_PROP_FPS, 60);
		input_capture[i].set(CAP_PROP_AUTOFOCUS, 0);
	}
	vector<vector<Mat>> image(num_cam, vector<Mat>(150));
	Mat img;

	std::chrono::steady_clock::time_point last = std::chrono::steady_clock::now();
	std::chrono::steady_clock::time_point now; 
	for (int j = 0; j < 150; j++) {
		for (int i = 0; i < num_cam; i++)
		{
			input_capture[i].grab();
		}
		for (int i = 0; i < num_cam; i++)
		{
			input_capture[i].retrieve(image[i][j]);
		}
		now = std::chrono::steady_clock::now();
		long long duration_in_millisec = std::chrono::duration_cast<std::chrono::milliseconds>(now - last).count();
		last = now;
		cout << duration_in_millisec << endl;
	}

	/*for (int i = 0; i < 10; i++)
	{
		imshow("cam_1",image[i]);
		waitKey();
	}

	for (int i = 0; i < 10; i++)
	{
		imshow("cam_2",img2[i]);
		waitKey();
	}

	Size sz;
	sz.height = 720;
	sz.width = 1280;
	VideoWriter vidwrite("vid.avi",'FFV1',60,sz);
	string str;
	*/
	string str;
	for(int i =0; i<2; i++)
		for (int j = 0; j < 150; j++) 
		{
			str = "C:/Gait-Lab/resources/videos/video_";
			str += to_string(i);
			str += "_";
			str += to_string(j);
			str += ".bmp";
			cout << str<<endl;
			imwrite(str,image[i][j]);
		}
	
	//Size framesize;
	//framesize.width = 1280;
	//framesize.height = 720;

	//VideoWriter input_writer;


	//steady_clock::time_point t1 = steady_clock::now();


	return 0;

}
