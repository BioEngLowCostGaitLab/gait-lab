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

void save_images(vector<vector<vector<vector<Point2f>>>> imgs)
{
	FileStorage calibpts("C:/Gait-Lab/resources/JSONfiles/calibpts.json", FileStorage::WRITE);
	calibpts << "calibpts" << "[";
	for (int i = 0; i < imgs.size(); i++)
	{
		calibpts << "{:";
		calibpts <<"cam_1"<<"[:";
		for (int j = 0; j < imgs[i].size(); j++)
		{
			calibpts << "{:";
			calibpts <<"cam_2"<<"[:";
			for (int k = 0; k < imgs[i][j].size(); k++)
			{
				calibpts << "{:";
				calibpts <<"images"<<"[:";
				for (int l = 0; l < imgs[i][j][k].size(); l++)
				{
					calibpts << "{:";
					calibpts <<"points"<< imgs[i][j][k][l];
					calibpts << "}";
				}
				calibpts << "]"<<"}";
			}
			calibpts << "]"<<"}";
		}
		calibpts << "]"<<"}";
	}
	calibpts << "]";
}

void store(vector<vidcamera> vidvec)
{
	FileStorage calsave("C:/Gait-Lab/resources/JSONfiles/calibration.json", FileStorage::WRITE);
	calsave << "camera" << "[";
	for (int i = 0; i < vidvec.size(); i++)
	{
		calsave << "{:";
		calsave << "index" << vidvec[i].index << "cam_mat" << vidvec[i].cam_mat << "dist_coeff" << vidvec[i].dist_coeff << "proj_mat" << vidvec[i].proj_mat << "rot_mat" << vidvec[i].rot_mat << "trans_mat" << vidvec[i].trans_mat << "rect_mat" <<vidvec[i].rect_mat;
		calsave << "}";
	}
	calsave << "]";
	calsave.release();
}