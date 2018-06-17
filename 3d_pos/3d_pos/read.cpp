#include <iostream>
#include <sstream>
#include <string>
#include <ctime>
#include <cstdio>
#include <vector>
#include <iterator>

#include <opencv2/core.hpp>
#include <opencv2/core/utility.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/calib3d.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include "cameracal.h"

void get_images(vector<vector<vector<vector<Point2f>>>> &imgs, int camerano, int img_no, int pts_no)
{
	FileStorage calibpts("C:/Gait-Lab/resources/JSONfiles/calibpts.json", FileStorage::READ);
	FileNode cameranode = calibpts["calibpts"];
	FileNode cameranode_2;
	FileNode imagenode;
	FileNode pointnode;
	Point2f temp;
	imgs.resize(camerano);
	int i = 0;
	for (FileNodeIterator camerait = cameranode.begin(); camerait != cameranode.end(); i++, ++camerait)
	{
		imgs[i].resize(camerano);
		cameranode_2 = (*camerait)["cam_1"];
		int l = 0;
		for (FileNodeIterator camerait_2 = cameranode_2.begin(); camerait_2 != cameranode_2.end(); l++, ++camerait_2)
		{
			imgs[i][l].resize(img_no);
			imagenode = (*camerait_2)["cam_2"];
			int j = 0;
			for (FileNodeIterator imageit = imagenode.begin(); imageit != imagenode.end(); j++, ++imageit)
			{
				pointnode = (*imageit)["images"];
				for (FileNodeIterator pointit = pointnode.begin(); pointit != pointnode.end(); ++pointit)
				{
					(*pointit)["points"]>> temp;
					//cout << i <<" " << l <<" "<< j << endl;
					imgs[i][l][j].push_back(temp);
				}
			}
		}
	}
	calibpts.release();
}


void read(vector<vidcamera> &vidvec)
{
	FileStorage calsave("C:/Gait-Lab/resources/JSONfiles/calibration.json", FileStorage::READ);
	FileNode camnode = calsave["camera"];
	FileNodeIterator camit = camnode.begin(), camit_end = camnode.end();
	// iterate through a sequence using FileNodeIterator
	for (; camit != camit_end; ++camit)
	{
		vidcamera temp;
		(*camit)["index"] >> temp.index;
		(*camit)["cam_mat"] >> temp.cam_mat;
		(*camit)["dist_coeff"] >> temp.dist_coeff;
		(*camit)["proj_mat"] >> temp.proj_mat;
		(*camit)["rot_mat"] >> temp.rot_mat;
		(*camit)["trans_mat"] >> temp.trans_mat;
		(*camit)["rect_mat"] >> temp.rect_mat;
		vidvec.push_back(temp);
	}
	calsave.release();
}