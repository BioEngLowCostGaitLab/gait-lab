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
	vector<Mat> rot_mat;
	vector<Mat> trans_mat;
	vector<vector<vector<Point2f>>> img_points;
	vector<vector<Point2f>> markerpts;

	vidcamera();
	vidcamera(int c_id, int camerano);
	vidcamera(const vidcamera &copy_cam);
	void resizevectors(int cam_no, int imgno, int imgpts);
	void getintrinsic(Mat cam_matrix, Mat distort_mat);
	void getextrinsic(Mat T, Mat R, Mat F, Mat rect, Mat Proj, Mat Q, int camind);
	void clrimg();
	void getmarker(FileNodeIterator &markerit);

	~vidcamera();
};

int cameraconnect();

vector<vector<vector<vector<Point2f>>>> mainget(vector<vector<int>> calibrate_pairs,vector<int> cameraID, Size boardsize, int num_img_points, int time_delay, Size imagesize);

void getpoints(vector<vidcamera> &vidvec, vector<vector<vector<vector<Point2f>>>> img_points, int camerano, int image_no, int totalpts);

void showpoints(vector<vidcamera> &vidvec, int camerano, int image_no, int totalpts);

void store(vector<vidcamera> vidvec);

void read(vector<vidcamera> &vidvec);

void fillmarker();

void markergetter(vector<vidcamera> &vidvec, int img_no);

void storemarker(const vector<vidcamera> &vidvec);

void get_3d(const vidcamera &cam_1, const vidcamera &cam_2, vector<vector<vector<vector<Point3f>>>> &object_points, int camerano, int frameno, int markerno);

Point3f pttransformer(Mat rot_mat, Mat trans__mat, Point3f pt);

void save_images(vector<vector<vector<vector<Point2f>>>> imgs);

void get_images(vector<vector<vector<vector<Point2f>>>> &imgs, int camerano, int img_no, int pts_no);

void find_cameras(vector<int> camid);

vector<vector<vector<vector<Point2f>>>> get_all(vector<int> cameraID, Size boardsize, int num_img_pts, int time_delay, Size imagesize);

#pragma once
