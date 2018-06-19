/* This is sample from the OpenCV book. The copyright notice is below */

/* *************** License:**************************
Oct. 3, 2008
Right to use this code in any way you want without warranty, support or any guarantee of it working.

BOOK: It would be nice if you cited it:
Learning OpenCV: Computer Vision with the OpenCV Library
by Gary Bradski and Adrian Kaehler
Published by O'Reilly Media, October 3, 2008

AVAILABLE AT:
http://www.amazon.com/Learning-OpenCV-Computer-Vision-Library/dp/0596516134
Or: http://oreilly.com/catalog/9780596516130/
ISBN-10: 0596516134 or: ISBN-13: 978-0596516130

OPENCV WEBSITES:
Homepage:      http://opencv.org
Online docs:   http://docs.opencv.org
Q&A forum:     http://answers.opencv.org
Issue tracker: http://code.opencv.org
GitHub:        https://github.com/opencv/opencv/
************************************************** */

#include "opencv2/calib3d.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"

#include <vector>
#include <string>
#include <algorithm>
#include <iostream>
#include <iterator>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include "cameracal.h"

using namespace cv;
using namespace std;

double computeEpipolarErrors(const vector<vector<Point3f> >& objectPoints,
	const vector<vector<vector<Point2f>>>& imagePoints, const Mat cameraMatrix[2], const Mat distCoeffs[2], const Mat F,
	vector<double>& perViewErrors);

void stereomain(vidcamera &cam_1, vidcamera &cam_2, int camindex_1, int camindex_2, int camerano, int nimages, int boardwidth,int boardheight, double squareSize, Size imageSize, bool errorcheck)
{
	vector<vector<vector<Point2f>>> imagePoints(2);
	vector<vector<Point3f>> objectPoints(1);

	int j;

	int totalpoints = boardheight*boardwidth;

	imagePoints[0].resize(nimages);
	for (j = 0; j < imagePoints[0].size(); j++)
		imagePoints[0][j] = cam_1.img_points[camindex_2][j];
	
	imagePoints[1].resize(nimages);
	for (j = 0; j < imagePoints[1].size(); j++)
		imagePoints[1][j] = cam_2.img_points[camindex_1][j];

	for (int i = 0; i < boardheight; i++)
		for (int j = 0; j < boardwidth; j++)
			objectPoints[0].push_back(Point3f(j*squareSize, i*squareSize, 0));
	
	objectPoints.resize(imagePoints[0].size(), objectPoints[0]);

	Mat cameraMatrix[2], distCoeffs[2];
	cameraMatrix[0] = cam_1.cam_mat;
	cameraMatrix[1] = cam_2.cam_mat;
	distCoeffs[0] = cam_1.dist_coeff;
	distCoeffs[1] = cam_2.dist_coeff;
	
	Mat R, T, E, F;

	stereoCalibrate(objectPoints, imagePoints[0], imagePoints[1],
		cameraMatrix[0], distCoeffs[0],
		cameraMatrix[1], distCoeffs[1],
		imageSize, R, T, E, F,
		CALIB_FIX_ASPECT_RATIO +
		CALIB_SAME_FOCAL_LENGTH +
		CALIB_RATIONAL_MODEL,
		TermCriteria(TermCriteria::COUNT + TermCriteria::EPS, 100, 1e-5));
	
	vector<double> perViewErrors;
	double avgepipolar = computeEpipolarErrors(objectPoints, imagePoints, cameraMatrix, distCoeffs, F, perViewErrors);
	cout<< "Cameras "<< camindex_1 <<" and "<< camindex_2 <<" have an epipolar error of "<< avgepipolar << endl;
	cout << endl;
	// CALIBRATION QUALITY CHECK
	// because the output fundamental matrix implicitly
	// includes all the output information,
	// we can check the quality of calibration using the
	// epipolar geometry constraint: m2^t*F*m1=0
	if (errorcheck)
	{
		if (avgepipolar > 1)
		{
			vector <double>::difference_type dist;
			vector<double>::iterator vit = perViewErrors.begin();

			do
			{
				if (*vit <= 1)
				{
					vit++;
				}
				else
				{
					dist = distance(perViewErrors.begin(), vit);
					imagePoints[0].erase(imagePoints[0].begin() + dist);
					imagePoints[1].erase(imagePoints[1].begin() + dist);
					objectPoints.erase(objectPoints.begin() + dist);
				}
			} while (vit != perViewErrors.end());

			stereoCalibrate(objectPoints, imagePoints[0], imagePoints[1],
				cameraMatrix[0], distCoeffs[0],
				cameraMatrix[1], distCoeffs[1],
				imageSize, R, T, E, F,
				CALIB_FIX_ASPECT_RATIO +
				CALIB_FIX_INTRINSIC +
				CALIB_SAME_FOCAL_LENGTH +
				CALIB_RATIONAL_MODEL,
				TermCriteria(TermCriteria::COUNT + TermCriteria::EPS, 100, 1e-5));
		}
	}

	Mat R1, R2, P1, P2, Q;
	Rect validRoi[2];

	stereoRectify(cameraMatrix[0], distCoeffs[0],
		cameraMatrix[1], distCoeffs[1],
		imageSize, R, T, R1, R2, P1, P2, Q,
		CALIB_ZERO_DISPARITY, 1, imageSize, &validRoi[0], &validRoi[1]);
	cam_1.getextrinsic(T, R, F, R1, P1, Q, camindex_2);
	cam_2.getextrinsic(T, R, F, R2, P2, Q, camindex_1);
}

double computeEpipolarErrors(const vector<vector<Point3f> >& objectPoints,
	const vector<vector<vector<Point2f>>>& imagePoints, const Mat cameraMatrix[2], const Mat distCoeffs[2], const Mat F,
	 vector<double>& perViewErrors)
{
	int i, j, k;
	double errim;
	double err = 0;
	int npoints = 0;
	vector<Vec3f> lines[2];
	int nimages = imagePoints[0].size();
	for (i = 0; i < nimages; i++)
	{
		errim = 0;
		// i is the image index, k the caamera index, and j the point index;
		int npt = (int)imagePoints[0][i].size();
		Mat imgpt[2];
		for (k = 0; k < 2; k++)
		{
			//Create points Matrix, undistorts them and computes corresponding epilines. Do for both cameras for the same images.
			imgpt[k] = Mat(imagePoints[k][i]);
			undistortPoints(imgpt[k], imgpt[k], cameraMatrix[k], distCoeffs[k], Mat(), cameraMatrix[k]);
			computeCorrespondEpilines(imgpt[k], k + 1, F, lines[k]);
		}
		for (j = 0; j < npt; j++)
		{
			//Performs the error calculation for each point;
			double errij = fabs(imagePoints[0][i][j].x*lines[1][j][0] +
				imagePoints[0][i][j].y*lines[1][j][1] + lines[1][j][2]) +
				fabs(imagePoints[1][i][j].x*lines[0][j][0] +
					imagePoints[1][i][j].y*lines[0][j][1] + lines[0][j][2]);
			err += errij;
			errim += errij;
		}
		npoints += npt;
		perViewErrors.push_back(errim / (double)npt);
	}
	return err / npoints;
}