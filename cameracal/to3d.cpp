#include <opencv2/core.hpp>
#include <opencv2/calib3d.hpp>
#include <opencv2/imgproc.hpp>

#include<iostream>
#include <vector>

using namespace cv;
using namespace std;

int triangulate(Mat c1, Mat c2, Mat d1, Mat d2, Mat r1, Mat r2, Mat p1, Mat p2, vector<Point2f> pt1, vector<Point2f> pt2) 
{
	vector<Point2f> pto;
	vector<Point2f> ptt;
	vector<Point2f> upt1(3);
	vector<Point2f> upt2(3);

	pto.push_back(Point2f(796.f, 645.f));
	pto.push_back(Point2f(691.f, 657.f));
	pto.push_back(Point2f(715.f, 819.f));

	ptt.push_back(Point2f(1233.f, 681.f));
	ptt.push_back(Point2f(929.f, 1057.f));
	ptt.push_back(Point2f(731.f, 867.f));

	undistortPoints(pt1, upt1, c1, d1, r1, p1);
	undistortPoints(pt2, upt2, c2, d2, r2, p2);


	Mat outpoints(4, 1, CV_8UC1);
	triangulatePoints(p1, p2, upt1, upt2, outpoints);
	cout << outpoints << endl;

	return 0;
}