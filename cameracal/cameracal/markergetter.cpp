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

using namespace std;
using namespace cv;

void swap_markers(Point2f &mark_1, Point2f &mark_2);
void sort_markers(vector<Point2f> &marklist);
void undistort_found(vector<Point2f> in, vector<Point2f> &out, Mat cam_mat, Mat dist_coeff, Mat rect_mat, Mat proj_mat);

void fillmarker()
{
	vector<Point2f> temp(5);
	temp[0] = Point2f(255, 350);
	temp[1] = Point2f(360, 780);
	temp[2] = Point2f(20, 150);
	temp[3] = Point2f(60, 580);
	temp[4] = Point2f(180, 90);

	vector<Point2f> temp_2(5);
	temp_2[0] = Point2f(200, 150);
	temp_2[1] = Point2f(380, 650);
	temp_2[2] = Point2f(10, 120);
	temp_2[3] = Point2f(30, 420);
	temp_2[4] = Point2f(90, 380);

	vector<vector<Point2f>> markerpts(5,temp);
	vector<vector<Point2f>> markerpts_2(5, temp_2);
	vector<vector<vector<Point2f>>> markervec(2, markerpts);
	markervec[1] = markerpts_2;

	FileStorage markersave("C:/Gait-Lab/resources/JSONfiles/markers.json", FileStorage::WRITE);
	markersave << "markerpts" << "[";
	for (int i = 0; i < markervec.size(); i++)
	{
		markersave << "{:";
		markersave << "camera" << i;
		markersave << "imglist" << "[:";
		for (int j = 0; j < markervec[i].size(); j++)
		{
			markersave << "{:";
			markersave << "image" << j;
			markersave << "ptslist" <<"[:";
			for (int k = 0; k < markervec[i][j].size(); k++)
			{
				markersave << "{:";
				markersave << "colour" << "blue";
				markersave << "point" <<markervec[i][j][k];
				markersave << "}";
			}
			markersave << "]"<<"}";
		}
		markersave<< "]"<<"}";
	}
	markersave << "]";
	markersave.release();
}

void storemarker(const vector<vidcamera> &vidvec)
{
	FileStorage markersave("C:/Gait-Lab/resources/JSONfiles/markers.json", FileStorage::WRITE);
	markersave << "markerpts" << "[";
	for (int i = 0; i < vidvec.size(); i++)
	{
		markersave << "{:";
		markersave << "camera" << i;
		markersave << "imglist" << "[:";
		for (int j = 0; j < vidvec[i].markerpts.size(); j++)
		{
			markersave << "{:";
			markersave << "image" << j;
			markersave << "ptslist" << "[:";
			for (int k = 0; k < vidvec[i].markerpts[j].size(); k++)
			{
				markersave << "{:";
				markersave << "colour" << "blue";
				markersave << "point" << vidvec[i].markerpts[j][k];
				markersave << "}";
			}
			markersave << "]" << "}";
		}
		markersave << "]" << "}";
	}
	markersave << "]";
	markersave.release();
}

void markergetter(vector<vidcamera> &vidvec, int img_no)
{
	FileStorage markersave("C:/Gait-Lab/resources/JSONfiles/markers.json", FileStorage::READ);
	FileNode cameranode = markersave["markerpts"];
	FileNode imagenode;
	FileNode pointnode;
	Point2f temp;
	int n;
	int i = 0;
	for (FileNodeIterator camerait = cameranode.begin(); camerait != cameranode.end(); i++, ++camerait)
	{
		vidvec[i].markerpts.resize(img_no);
		imagenode = (*camerait)["imglist"];
		int j = 0;
		for (FileNodeIterator imageit = imagenode.begin(); imageit != imagenode.end(); j++, ++imageit)
		{
			pointnode = (*imageit)["ptslist"];
			for (FileNodeIterator pointit = pointnode.begin(); pointit != pointnode.end(); ++pointit)
			{
				(*pointit)["coords"] >> temp;
				//cout << temp<<endl;
				vidvec[i].markerpts[j].push_back(temp);
			}
			sort_markers(vidvec[i].markerpts[j]);

			if (i == 1)
				n = 0;
			else
				n = 1;

			//undistort_found(vidvec[i].markerpts[j], vidvec[i].markerpts[j], vidvec[i].cam_mat, vidvec[i].dist_coeff,vidvec[i].rect_mat[n],vidvec[i].proj_mat[n]);
		}
	}

	markersave.release();
}

void undistort_found(vector<Point2f> in, vector<Point2f> &out, Mat cam_mat, Mat dist_coeff, Mat rect_mat, Mat proj_mat)
{
	vector<int> index;
	vector<Point2f> found;
	for (int i = 0; i<in.size() ;i++)
	{
		if (in[i] != Point2f(-1,-1))
		{
			found.push_back(in[i]);
			index.push_back(i);
		}
	}
	
	if (found.size() != 0)
	{
		undistortPoints(found, found, cam_mat, dist_coeff, rect_mat, proj_mat);
		for (int j = 0; j < index.size(); j++)
		{
			in[index[j]] = found[j];
		}
	}
	out = in;
}

void sort_markers(vector<Point2f> &marklist)
{
	for (int i = 1; i < marklist.size(); i++)
	{
		for (int j = i; j > 0; j--)
		{
			if (marklist[j].y < marklist[j - 1].y)
			{
				swap_markers(marklist[j], marklist[j - 1]);
			}
			else
			{
				break;
			}
		}
	}
}

void swap_markers(Point2f &mark_1, Point2f &mark_2)
{
	Point2f temp;
	temp = mark_1;
	mark_1 = mark_2;
	mark_2 = temp;
}