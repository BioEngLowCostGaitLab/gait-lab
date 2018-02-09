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

int main()
{
	FileStorage fs("imagepoints.xml", FileStorage::READ); // Read the settings
	if (!fs.isOpened())
	{
		cout << "Could not open the configuration file: \"" << "imagepoints.xml" << "\"" << endl;
		return -1;
	}
	else
	{
		cout << "Yeah bitches!" << endl;
	}

	Mat newmat;
	vector<int> camid;
	vector<vidcamera> vidvec;
	double squaresize = 1;
	int camerano = 2;
	int image_no = 5;
	int totalpts = 35;
	vector<vector<vector<vector<Point2f>>>> imgs(camerano, vector<vector<vector<Point2f>>>(camerano, vector<vector<Point2f>>(image_no, vector<Point2f>(totalpts))));
	vector<Point2d> vec;
	fs["img_mat"] >> newmat;
	int indexc = 0;
	for (int i = 0; i < camerano; i++)
	{
		for (int j = 0; j < camerano; j++)
		{
			for (int k = 0; k < image_no; k++)
			{
				for (int l = 0; l < totalpts; l++)
				{
					if (i == j);
					else
					{
						Point2f temppoint((newmat.at<double>(indexc, 0)), (newmat.at<double>(indexc, 1)));
						imgs[i][j][k][l] = temppoint;
						indexc++;
					}
				}
			}
		}
	}

	for (int i = 0; i < camerano; i++)
	{
		vidcamera tempcam(i, camerano);
		tempcam.index = i;
		vidvec.push_back(tempcam);
	}

	
	int boardheight = 5;
	int boardwidth = 7;
	getpoints(vidvec, imgs, camerano, image_no, totalpts);
	Size imagesize;
	imagesize.height = 720;
	imagesize.width = 1280;
	for (int i = 0; i<camerano; i++)
		calibratemain(vidvec[i], camerano, image_no, boardheight, boardwidth, 1, imagesize, 0, i);

	stereomain(vidvec[0], vidvec[1], vidvec[0].index, vidvec[1].index, camerano, image_no, boardwidth, boardheight, squaresize, imagesize, 0);

	cout << vidvec[0].cam_mat << endl;
	return 0;

}

void getpoints(vector<vidcamera> &vidvec, vector<vector<vector<vector<Point2f>>>> imgs, int camerano,int image_no, int totalpts)
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