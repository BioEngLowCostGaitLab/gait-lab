#include<iostream>
#include<string>
#include<vector>
#include<chrono>
#include<stdlib.h>

#include<opencv2/core.hpp>
#include<opencv2/core/utility.hpp>
#include<opencv2/imgproc.hpp>
#include<opencv2/videoio.hpp>
#include<opencv2/calib3d.hpp>
#include<opencv2/highgui.hpp>

using namespace std;
using namespace std::chrono;		/*for timing*/
using namespace cv;

/*work out number of pairs required from number of cameras*/
int factorial(int num_cam) 
{
	int result = 1;
	int j = 1;
	for (j = 1; j < num_cam; j++) {
		result *= j;
	}
	return result;
}

int cameraconnect()
{
	int i = 0;
	VideoCapture check(0);
	while (check.isOpened())
	{
		i++;
		check.release();
		check.open(i);
	}
	check.release();
	return i;
}

vector<vector<vector<vector<Point2f>>>> mainget(vector<int> cameraID)
{
	vector<VideoCapture> input_capture;
	vector<string> captureindex;
	int k;
	string tempstring;
	for (k = 0; k < 10; k++)
	{
		tempstring = "Camera ";
		tempstring = tempstring += char(k);
		captureindex.push_back(tempstring);
	}

	Size boardsize;

	boardsize.width = 8;		/*should be obtained from settings file*/
	boardsize.height = 6;

	int i = 0;
	int j = 0;

	int num_cam = cameraID.size();
	int num_corner = boardsize.width * boardsize.height;
	int num_img_pts = 25;		/*also obtained from settings file*/

	int suc_pair = 0;
	int req_pair = factorial(num_cam);

	int time_delay = 500;		/*time delay between getting frames in milliseconds, in settings file??*/

	input_capture.resize(num_cam);

	/*open camera*/
	for (i = 0; i < num_cam; i++) {
		cout << cameraID[i] << " is opening for capture." << endl;
		input_capture[i].open(cameraID[i]);
		if (input_capture[i].isOpened()) {
			cout << cameraID[i] << " successfully opened for capture." << endl;
		}
		else {
			cout << cameraID[i] << " cannot be opened for capture." << endl;
		}
	}

	/*get images*/

	vector<vector<vector<vector <Point2f> >>>
		image_points(num_cam, vector<vector<vector<Point2f>>>	/*1st index refers to the images taken from that camera, while the 2nd index is corresponding pair*/
		(num_cam, vector<vector<Point2f>>
			(0, vector<Point2f>(0))));				/*size of 3rd and 4th index not specify since push_back is being used*/

	while (suc_pair < req_pair) {

		steady_clock::time_point t1 = steady_clock::now();		/*get current time*/

		vector<vector<Point2f>> temp_img_pts(num_cam);
		vector<bool> found(num_cam,false);
		vector<Mat> image(num_cam);

		for (i = 0; i < num_cam; i++) {
			input_capture[i] >> image[i];		/*storing one frame for each cameras, find if there is a way to do all at the same time or minimise time delay*/
		}

		/*checks if there are sufficient time_delay between consecutive obtained images 
		  as images in close succession will be very similar and hence the image_points will be very similar*/
		if (duration_cast<duration<double>>(steady_clock::now() - t1) > milliseconds(time_delay)) {
			for (i = 0; i < num_cam; i++) {
				for (j = i + 1; j < num_cam; j++) {
					/*check for found pairs*/
					if (!found[i]) {
						break;		/*since found[i] is false move to next camera*/
					}
					/*implies that found[i] == true*/
					else if (found[j]) {
						/*improve corners location accuracy*/
						vector<Mat> image_gray(2);

						cvtColor(image[i], image_gray[0], COLOR_BGR2GRAY);
						cvtColor(image[j], image_gray[1], COLOR_BGR2GRAY);
						cornerSubPix(image_gray[0], temp_img_pts[i], Size(11, 11), Size(-1, -1), TermCriteria(TermCriteria::EPS + TermCriteria::COUNT, 30, 0.1));
						cornerSubPix(image_gray[1], temp_img_pts[j], Size(11, 11), Size(-1, -1), TermCriteria(TermCriteria::EPS + TermCriteria::COUNT, 30, 0.1));

						/*storing image points*/
						image_points[i][j].push_back(temp_img_pts[i]);
						image_points[j][i].push_back(temp_img_pts[j]);

						/*check for successful pairs => when there are num_img_pts image points*/
						if ((image_points[i][j].size() == num_img_pts) && (image_points[j][i].size() == num_img_pts)) {
							suc_pair++;
							cout << cameraID[i] << " and " << cameraID[j] << " has required number of image pairs." << endl;
							cout << suc_pair << "/" << req_pair << endl;
						}
					}
				}
			}
		}
	}

	cout << "All required pairs has been successfully detected." << endl;
	return image_points;
}