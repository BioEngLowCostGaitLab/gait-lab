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

vidcamera::vidcamera(int c_id, int camerano)
{
	cam_id = c_id;
	proj_mat.resize(camerano);
	rect_mat.resize(camerano);
	fund_mat.resize(camerano);
	disparity_map.resize(camerano);
}

vidcamera::vidcamera(const vidcamera &copy_cam)
{
	this->index = copy_cam.index;
	this->cam_id = copy_cam.cam_id;
	this->cam_mat = copy_cam.cam_mat;
	this->dist_coeff = copy_cam.dist_coeff;
	this->img_points = copy_cam.img_points;
	this->proj_mat = copy_cam.proj_mat;
	this->rect_mat = copy_cam.rect_mat;
	this->rot_mat = copy_cam.rot_mat;
	this->trans_mat = copy_cam.trans_mat;
	this->fund_mat = copy_cam.fund_mat;
	this->disparity_map = copy_cam.disparity_map;
}

vidcamera::~vidcamera()
{
}

void vidcamera::resizevectors(int cam_no, int imgno, int imgpts)
{
	int i, j;
	img_points.resize(cam_no);
	for (i = 0; i < cam_no; i++)
	{
		img_points[i].resize(imgno);
		for (j = 0; j < imgno; j++)
		{
			img_points[i][j].resize(imgpts);
		}
	}
}

void vidcamera::getintrinsic(Mat cam_matrix, Mat distort_mat)
{
	cam_mat = cam_matrix;
	dist_coeff = distort_mat;
}

void vidcamera::getextrinsic(Mat T, Mat R, Mat F, Mat rect, Mat Proj, Mat Q, int camind)
{
	if (camind == 0)
	{
		rot_mat = R;
		trans_mat = T;
	}

	fund_mat[camind] = F;
	rect_mat[camind] = rect;
	proj_mat[camind] = Proj;
	disparity_map[camind] = Q;
}