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

#include "cameracal.h"

using namespace cv;
using namespace std;

void triangulateFound(Mat proj_1, Mat proj_2, vector<Point2f> pts_1, vector<Point2f> pts_2, Mat &out);

Point3f pttransformer(Mat rot_mat, Mat trans_mat, Point3f pt)
{
	Point3f newpoint;
	pt = pt+Point3f(trans_mat.at<float>(0, 0), trans_mat.at<float>(1, 0), trans_mat.at<float>(2, 0));
	newpoint.x = rot_mat.at<float>(0, 0)*pt.x + rot_mat.at<float>(0, 1)*pt.y + rot_mat.at<float>(0, 2)*pt.z;
	newpoint.y = rot_mat.at<float>(1, 0)*pt.x + rot_mat.at<float>(1, 1)*pt.y + rot_mat.at<float>(1, 2)*pt.z;
	newpoint.z = rot_mat.at<float>(2, 0)*pt.x + rot_mat.at<float>(2, 1)*pt.y + rot_mat.at<float>(2, 2)*pt.z;
	return newpoint;
}


void get_3d(const vidcamera &cam_1, const vidcamera &cam_2, vector<vector<vector<vector<Point3f>>>> &object_points, int camerano, int frameno, int markerno)
{
	int ind_1 = cam_1.index; 
	int ind_2 = cam_2.index;
	Mat homogeneous;
	Mat threed;
	Mat trans;
	for (int k = 0; k < frameno; k++)
	{	
		triangulateFound(cam_1.proj_mat[ind_2], cam_2.proj_mat[ind_1], cam_1.markerpts[k], cam_2.markerpts[k], homogeneous);
		transpose(homogeneous, trans);
		convertPointsFromHomogeneous(trans, threed);
		for (int p = 0; p < markerno; p++)
		{
			object_points[ind_1][ind_2][k][p] = Point3f(threed.at<float>(p, 0), threed.at<float>(p, 1), threed.at<float>(p, 2));
		}
		/*if (ind_1 > 0)
		{
			for (int p = 0; p < markerno; p++)
			{
				object_points[ind_1][ind_2][k][p] = pttransformer(cam_1.rot_mat, cam_1.trans_mat, object_points[ind_1][ind_2][k][p]);
			}
		}*/
	}
}

void triangulateFound(Mat proj_1, Mat proj_2, vector<Point2f> pts_1, vector<Point2f> pts_2, Mat &out)
{
	vector<int> index;
	vector<vector<Point2f>> found(2);
	Mat temp;

	out = Mat::zeros(Size((int)pts_1.size(),4), CV_32FC1);

	for (int i = 0; i < pts_1.size(); i++)
	{
		if (pts_1[i] != Point2f(-1, -1) && pts_2[i] != Point2f(-1, -1))
		{
			found[0].push_back(pts_1[i]);
			found[1].push_back(pts_2[i]);
			index.push_back(i);
		}
	}
	if (found[0].size() != 0)
	{
		triangulatePoints(proj_1, proj_2, found[0], found[1], temp);
		for (int j = 0; j < index.size(); j++)
		{
			for (int k = 0; k < 4; k++)
			{
				out.at<float>(k,index[j]) = temp.at<float>(k,j);
			}
		}
	}
}


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

	return 0;
}