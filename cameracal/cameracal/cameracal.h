#include <iostream>
#include <vector>
#include <iostream>
#include <sstream>
#include <string>
#include <ctime>
#include <cstdio>

#include <opencv2/core.hpp>
#include <opencv2/core/utility.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/calib3d.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/core.hpp>

using namespace std;
using namespace cv;

class vidcamera
{
private:
	int cam_id;

public:
	int index;
	Mat cam_mat;
	Mat dist_coeff;
	vector<Mat> proj_mat;
	vector<Mat> rect_mat;
	vector<Mat> fund_mat;
	vector<Mat> disparity_map;
	Mat rot_mat;
	Mat trans_mat;
	vector<vector<vector<Point2f>>> img_points;
	vidcamera(int c_id, int camerano);
	vidcamera(const vidcamera &copy_cam);
	void resizevectors(int cam_no, int imgno, int imgpts);
	void getintrinsic(Mat cam_matrix, Mat distort_mat);
	void getextrinsic(Mat T, Mat R, Mat F, Mat rect, Mat Proj, Mat Q, int camind);
	~vidcamera();
};

int cameraconnect();

int calibratemain(vidcamera &vidcam, int camerano, int imgno, int boardheight, int boardwidth, int squareSize, Size imageSize, bool errorcheck, int index);

void stereomain(vidcamera &cam_1, vidcamera &cam_2, int camindex_1, int camindex_2, int camerano, int nimages, int boardwidth, int boardheight, int squareSize, Size imageSize, bool errorcheck);

vector<vector<vector<vector<Point2f>>>> mainget(vector<int> cameraID);

void getpoints(vector<vidcamera> &vidvec, vector<vector<vector<vector<Point2f>>>> img_points, int camerano, int image_no, int totalpts);

void showpoints(vector<vidcamera> &vidvec, int camerano, int image_no, int totalpts);
#pragma once
