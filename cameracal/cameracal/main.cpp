#include <iostream>
#include <vector>
#include <iostream>
#include <sstream>
#include <string>
#include <ctime>
#include <cstdio>

#include <opencv2/plot.hpp>
#include <opencv2/core.hpp>
#include <opencv2/core/utility.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/calib3d.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/core.hpp>

#include "cameracal.h"

using namespace std;
using namespace cv;
//vector<vidcamera> fullcalibrate();
void take_images(int camerano, Size imagesize, int sample_no);
float angle(Point3f a, Point3f b);
void savpoints(vector<vector<int>> calibrate_pairs, int camerano, int image_no, Size boardsize, int totalpts, Size imagesize, double squaresize, float time_delay);
vector<vidcamera> calibfrompts(vector<vector<int>> calibrate_pairs, int camerano, int image_no, Size boardsize, int totalpts, Size imagesize, double squaresize);
vector<vidcamera> fullcalibrate(int camerano, int image_no, Size boardsize, int totalpts, Size imagesize, double squaresize, float time_delay);

int main()
{	
	/*int camerano;
	camerano = cameraconnect();
	cout << "Number of cameras: " << camerano;
	cout << endl;
	cout << endl;*/
	int camerano = 2;
	int image_no = 25;
	Size boardsize;
		boardsize.height = 6;
		boardsize.width = 8;
	int totalpts = (boardsize.height) * (boardsize.width);
	Size imagesize;
	imagesize.height = 720;
	imagesize.width = 1280;
	double squaresize = 2.8;
	float time_delay = 500;

	vector<vector<int>> calibrate_pairs;
	vector<int> tempindexvec;
	for (int i = 0; i < (camerano - 1); i++)
	{
		tempindexvec.resize(2);
		tempindexvec[0] = i;
		tempindexvec[1] = i + 1;
		calibrate_pairs.push_back(tempindexvec);
		tempindexvec.clear();
	}
	
	/*vector <vidcamera> vidvec = fullcalibrate(camerano, image_no, boardsize, totalpts, imagesize, squaresize, time_delay);
	
	cout << "waiting for g" << endl;
	imshow("waiting", vidvec[1].rot_mat);
	char c = waitKey(0);
	if (c == 'g');
	
	take_images(camerano, imagesize, sample_no);*/

	savpoints(calibrate_pairs,camerano, image_no, boardsize, totalpts, imagesize, squaresize, time_delay);
	vector<vidcamera> vidvec = calibfrompts(calibrate_pairs,camerano, image_no, boardsize, totalpts, imagesize, squaresize);

	//vector<vector<vector<vector<Point2f>>>> imgs;

	//get_images(imgs, 4, 15, 48);


	/*for (int i = 0; i < 2; i++)
	{
		for (int j = 0; j < 3; j++)
		{
			cout << j << ": " << endl;
			cout << (int)imgs[1][i][j].size() << endl;
			for (int k = 0; k < imgs[1][i][j].size(); k++)
				cout << imgs[1][i][j][k] << endl;
		}
	}
	*/
	//Partition between modes

	
	//int sample_no = 150;
	//int markerno = 3;
	
	/*vector<vidcamera> vidvec;
	read(vidvec);
	markergetter(vidvec, sample_no);
	for (int i = 0; i < camerano; i++)
	{
		cout << "cam_no: " << i << endl;
		for (int j = 0; j < sample_no; j++)
			cout <<"img_no: "<< j <<" "<<vidvec[i].markerpts[j] << endl;
	}*/
	//Get markers
	/*vector<vidcamera> vidvec;
	read(vidvec);
	markergetter(vidvec,sample_no);
	vector<vector<vector<vector<Point3f>>>> obj_pts(camerano, vector<vector<vector<Point3f>>>(camerano, vector<vector<Point3f>>(sample_no, vector<Point3f>(markerno))));
	get_3d(vidvec[0], vidvec[1], obj_pts, camerano, sample_no, markerno);
	for (int i = 0; i<camerano; i++)
		for (int j = 0; j < camerano; j++)
		{
			cout << i << " " << j << endl;
			for (int k = 0; k < sample_no; k++)
			{
				cout << k << ": " << endl;
				for (int p = 0; p < markerno; p++)
					cout << obj_pts[i][j][k][p] << endl;
			}
		}
	vector<float> joint_angle;
	vector<float> time;
	for (int i = 0; i < sample_no; i++)
	{
		if ((obj_pts[0][1][i][0] != Point3f(0, 0, 0)) && (obj_pts[0][1][i][1] != Point3f(0, 0, 0)) && (obj_pts[0][1][i][2] != Point3f(0, 0, 0)))
		{
			joint_angle.push_back(angle(obj_pts[0][1][i][0] - obj_pts[0][1][i][1], obj_pts[0][1][i][2] - obj_pts[0][1][i][1]));
		}
		else
		{
			joint_angle.push_back(0);
		}

		time.push_back(0.0333333333*i);
	}

	for (int i = 0; i < joint_angle.size(); i++)
	{
		cout << obj_pts[0][1][i] << endl;
		cout << joint_angle[i] << endl;
	}

	Mat data_x(1, (int)time.size(), CV_64F);
	Mat data_y(1, (int)joint_angle.size(), CV_64F);

	for (int i = 0; i < data_x.cols; i++)
	{
		data_x.at<double>(0, i) = (double)time[i];
		data_y.at<double>(0, i) = (double)joint_angle[i];
	}

	std::cout << "data_x : " << data_x << std::endl;
	std::cout << "data_y : " << data_y << std::endl;

	Mat plot_result;
	Ptr<plot::Plot2d> plot = plot::Plot2d::create(data_x, data_y);
	
	plot->setShowGrid(true);
	plot->setPlotBackgroundColor(Scalar(255, 255, 255));
	plot->setPlotLineColor(Scalar(0, 0, 0));
	plot->setPlotGridColor(Scalar(0, 0, 0));
	plot->setPlotAxisColor(Scalar(0, 0, 0));
	plot->setInvertOrientation(1);
	plot->render(plot_result);

	imshow("Plot of joint angle against time", plot_result);
	imwrite("plot.jpg", plot_result);
	waitKey();

	FileStorage anglesave("angles.json", FileStorage::WRITE);
	anglesave << "anglesave" << joint_angle;
	anglesave.release();

	vector<float> angletest;
	FileStorage angletake("angles.json", FileStorage::READ);
	angletake["anglesave"] >> angletest;
	anglesave.release();

	for (int i = 0; i<angletest.size(); i++)
	{
		cout << "out: " << angletest[i] << endl;
	}*/
	return 0;
}



float angle(Point3f a, Point3f b)
{
	float c;
	c = a.x*b.x + a.y*b.y + a.z*b.z;
	float angle;
	//cout << sqrt(pow(a.x, 2) + pow(a.y, 2) + pow(a.z, 2)) << endl;
	//cout << sqrt(pow(b.x, 2) + pow(b.y, 2) + pow(b.z, 2)) << endl;
	angle = acos(c / (sqrt(pow(a.x, 2) + pow(a.y, 2) + pow(a.z, 2))*sqrt(pow(b.x, 2) + pow(b.y, 2) + pow(b.z, 2))));
	return angle * 180.0 / 3.1418;
}

void take_images(int camerano, Size imagesize,int sample_no)
{
	vector<int> camid;

	for (int i = 0; i < camerano; i++)
	{
		camid.push_back(i);
	}
	
	vector<VideoCapture> input_capture(camerano);

	for (int i = 0; i < camerano; i++) {
		cout << camid[i] << " is opening for capture." << endl;
		input_capture[i].open(camid[i]);
		if (input_capture[i].isOpened()) {
			cout << camid[i] << " successfully opened for capture." << endl;
		}
		else {
			cout << camid[i] << " cannot be opened for capture." << endl;
		}
	}

	for (int i = 0; i < camerano; i++)
	{
		input_capture[i].set(CV_CAP_PROP_FRAME_HEIGHT, 720);
		input_capture[i].set(CV_CAP_PROP_FRAME_WIDTH, 1280);
	}

	Mat tempimg;
	string fnm;
	for (int n = 0; n < sample_no; n++)
		for (int i = 0; i < camerano; i++)
		{
			input_capture[i] >> tempimg;
			fnm = "image_";
			fnm += to_string(n);
			fnm += "_";
			fnm += to_string(i);
			fnm += ".bmp";
			imwrite(fnm, tempimg);
		}
}

void savpoints(vector<vector<int>> calibrate_pairs,int camerano, int image_no, Size boardsize, int totalpts, Size imagesize, double squaresize, float time_delay)
{
	vector<vector<vector<vector<Point2f>>>> imgs;
	vector<int> camid;
	vector<vidcamera> vidvec;
	
	int boardheight = boardsize.height;
	int boardwidth = boardsize.width;

	for (int i = 0; i < camerano; i++)
	{
		camid.push_back(i);
	}

	find_cameras(camid);

	for (int i = 0; i < camerano; i++)
	{
		vidcamera tempcam(i, camerano);
		vidvec.push_back(tempcam);
		vidvec[i].index = i;
	}

	imgs = mainget(calibrate_pairs, camid, boardsize, image_no, time_delay, imagesize);

	save_images(imgs); 
}

vector<vidcamera> calibfrompts(vector<vector<int>> calibrate_pairs, int camerano, int image_no, Size boardsize, int totalpts, Size imagesize, double squaresize)
{
	vector<vector<vector<vector<Point2f>>>> imgs;
	vector<vidcamera> vidvec;

	int boardwidth = boardsize.width;
	int boardheight = boardsize.height;

	for (int i = 0; i < camerano; i++)
	{
		vidcamera tempcam(i, camerano);
		vidvec.push_back(tempcam);
		vidvec[i].index = i;
	}

	get_images(imgs, camerano, image_no, totalpts);

	getpoints(vidvec, imgs, camerano, image_no, totalpts);

	for (int i = 0; i < camerano; i++)
	{
		cout << "Now calibrating camera " << i << endl;
		calibratemain(vidvec[i], camerano, image_no, boardheight, boardwidth, squaresize, imagesize, 0, i);
	}

	cout << "Single camera calibration complete." << endl;
	cout << endl;

	for (int i = 0; i<calibrate_pairs.size(); i++)
		{
			int cam_1 = calibrate_pairs[i][0];
			int cam_2 = calibrate_pairs[i][1];
			cout << "Performing stereo calibration between cameras " << cam_1 << " and " << cam_2 << endl;
			stereomain(vidvec[cam_1], vidvec[cam_2], vidvec[cam_1].index, vidvec[cam_2].index, camerano, image_no, boardwidth, boardheight, squaresize, imagesize, 0);
		}
	
	store(vidvec);
	return vidvec;
}

void getpoints(vector<vidcamera> &vidvec, vector<vector<vector<vector<Point2f>>>> imgs, int camerano, int image_no, int totalpts)
{
	int i, j, k, l;
	Point2f zerpoint = (0, 0);
	for (i = 0; i < camerano; i++)
	{
		vidvec[i].resizevectors(camerano, image_no, totalpts);
	}

	for (i = 0; i < camerano; i++)
	{
		for (j = 0; j < camerano; j++)
		{
			for (k = 0; k < image_no; k++)
			{
				for (l = 0; l < totalpts; l++)
				{
					if (i != j)
					{
						vidvec[i].img_points[j][k][l] = imgs[i][j][k][l];
					}
					else
					{
						vidvec[i].img_points[j][k][l] = zerpoint;
					}
				}
			}
		}
	}
}

vector<vidcamera> fullcalibrate(int camerano, int image_no, Size boardsize, int totalpts, Size imagesize, double squaresize, float time_delay)
{
	vector<vector<vector<vector<Point2f>>>> imgs;
	vector<int> camid;
	vector<vidcamera> vidvec;

	int boardwidth = boardsize.width;
	int boardheight = boardsize.height;

	for (int i = 0; i < camerano; i++)
	{
		camid.push_back(i);
	}

	for (int i = 0; i < camerano; i++)
	{
		vidcamera tempcam(i, camerano);
		vidvec.push_back(tempcam);
		vidvec[i].index = i;
	}

	imgs = get_all(camid, boardsize, image_no, time_delay, imagesize);

	getpoints(vidvec, imgs, camerano, image_no, totalpts);

	for (int i = 0; i<camerano; i++)
		calibratemain(vidvec[i], camerano, image_no, boardheight, boardwidth, squaresize, imagesize, 0, i);

	for (int i = 0; i<camerano; i++)
		for (int j = i + 1; j<camerano; j++)
			stereomain(vidvec[0], vidvec[1], vidvec[0].index, vidvec[1].index, camerano, image_no, boardwidth, boardheight, squaresize, imagesize, 0);
	cout << vidvec[0].index << endl;
	cout << vidvec[1].index << endl;
	store(vidvec);
	return vidvec;
}

void showpoints(vector<vidcamera> &vidvec, int camerano, int image_no, int totalpts)
{
	int i, j, k, l;
	for (i = 0; i < camerano; i++)
	{
		for (j = 0; j < camerano; j++)
		{
			cout << "Camera " << i << " with " << j << endl;
			for (k = 0; k < image_no; k++)
			{
				for (l = 0; l < totalpts; l++)
				{
					cout << vidvec[i].img_points[j][k][l] << " ";
				}
				cout << endl;
			}
			cout << endl;
		}
	}
}