// testProject.cpp : Defines the entry point for the console application.
// Run this code to see if it works. The path to opencv/build is defined as "OPENCV3_DIR".

#include "stdafx.h"
#include "opencv2\opencv.hpp"

using namespace cv;

int main()
{	
	Mat test = imread("picture.jpg");
	imshow("It works!", test);
	waitKey(0);
    return 0;
}

