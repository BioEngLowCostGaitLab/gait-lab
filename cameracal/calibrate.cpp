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

using namespace cv;
using namespace std;

double computeReprojectionErrors(const vector<vector<Point3f> >& objectPoints,
	const vector<vector<Point2f> >& imagePoints,
	const vector<Mat>& rvecs, const vector<Mat>& tvecs,
	const Mat& cameraMatrix, const Mat& distCoeffs,
	vector<float>& perViewErrors);

int calibratemain(vidcamera &vidcam, int camerano, int imgno, int boardheight,int boardwidth,int squareSize,Size imageSize, bool errorcheck, int index)
{
	vector<vector<Point2f>> imagePoints;
	Mat cameraMatrix, distCoeffs;
	vector<vector<Point3f>> objectPoints(1);
	vector<Mat> rvecs, tvecs;
	vector<float> perViewErrors;
	vector<float>::iterator vit;
	double mean_error;
	vector <float>::difference_type dist;

	for (int i = 0; i < camerano; i++)
		for (int j = 0; j <imgno; j++)
		{
			if (i != index)
			{
				imagePoints.push_back(vidcam.img_points[i][j]);
			}
		}

	for (int i = 0; i < boardheight; ++i)
		for (int j = 0; j < boardwidth; ++j)
			objectPoints[0].push_back(Point3f(j*squareSize, i*squareSize, 0));

	objectPoints.resize(imagePoints.size(), objectPoints[0]);

	calibrateCamera(objectPoints, imagePoints, imageSize, cameraMatrix, distCoeffs, rvecs,tvecs, CALIB_FIX_ASPECT_RATIO|CALIB_FIX_PRINCIPAL_POINT);
	mean_error = computeReprojectionErrors(objectPoints, imagePoints, rvecs, tvecs, cameraMatrix, distCoeffs, perViewErrors);
	for (int i = 0; i < perViewErrors.size(); i++)
		cout << perViewErrors[i] << endl;

	double maxerror = 1.7;
	int minsize = 3;

	vector<vector<Point2f>> new2D;
	vector<vector<Point3f>> new3D;
	Mat prevCameraMatrix, prevdistcoeffs;
	while (errorcheck && (mean_error>1) && (imagePoints.size()>minsize))
	{	
		prevCameraMatrix = cameraMatrix;
		prevdistcoeffs = distCoeffs;
		for (int i = 0; i < imgno; i++)
		{
			if (perViewErrors[i] < maxerror)
			{
				new2D.push_back(imagePoints[i]);
				new3D.push_back(objectPoints[i]);
			}
		}
		imagePoints = new2D;
		objectPoints = new3D;
		new2D.clear();
		new3D.clear();
		rvecs.clear();
		tvecs.clear();
		perViewErrors.clear();
		calibrateCamera(objectPoints, imagePoints, imageSize, cameraMatrix, distCoeffs, rvecs, tvecs, CALIB_FIX_ASPECT_RATIO | CALIB_FIX_PRINCIPAL_POINT);
		mean_error = computeReprojectionErrors(objectPoints, imagePoints, rvecs, tvecs, cameraMatrix, distCoeffs, perViewErrors);
		cout << "mean_Error: " << mean_error << endl;
		for (int i = 0; i < perViewErrors.size(); i++)
			cout << perViewErrors[i] << endl;
	}
	if (imagePoints.size() < 3)
	{
		cameraMatrix = prevCameraMatrix;
		distCoeffs = prevdistcoeffs;
	}
	vidcam.getintrinsic(cameraMatrix, distCoeffs);

	return 0;
}

double computeReprojectionErrors(const vector<vector<Point3f> >& objectPoints,
	const vector<vector<Point2f> >& imagePoints,
	const vector<Mat>& rvecs, const vector<Mat>& tvecs,
	const Mat& cameraMatrix, const Mat& distCoeffs,
	vector<float>& perViewErrors)
{
	vector<Point2f> imagePoints2;
	size_t totalPoints = 0;
	double totalErr = 0, err;
	perViewErrors.resize(objectPoints.size());

	for (size_t i = 0; i < objectPoints.size(); ++i)
	{
		projectPoints(objectPoints[i], rvecs[i], tvecs[i], cameraMatrix, distCoeffs, imagePoints2);
		err = norm(imagePoints[i], imagePoints2, NORM_L2);
		size_t n = objectPoints[i].size();
		perViewErrors[i] = (float)std::sqrt(err*err / n);
		totalErr += err*err;
		totalPoints += n;
	}

	return std::sqrt(totalErr / totalPoints);
}
