
#include "opencv2/opencv.hpp"
#include <vector>
#include <iostream>

void MyFilledCircle(cv::Mat img, cv::Point center);

int main() {
	const int fps = 30;
	cv::Mat frame, frame_gray, frame_blur, canny, frame1, frameDiff;

	int lowThreshold = 0;
	int const maxLowThreshold = 100;

	cv::VideoCapture vid(1);

	if (!vid.isOpened()) {
		return -1;
	}

	cv::namedWindow("Canny", CV_WINDOW_AUTOSIZE);
	cv::createTrackbar("Min:", "Canny", &lowThreshold, maxLowThreshold); vid.read(frame); cv::cvtColor(frame, frame_gray, CV_BGR2GRAY); frame_gray.copyTo(frame1);

	while (vid.read(frame)) {
		cv::cvtColor(frame, frame_gray, CV_BGR2GRAY);

		cv::GaussianBlur(frame_gray, frame_blur, cv::Size(5, 5), 3, 3);
		cv::Canny(frame_blur, canny, lowThreshold, lowThreshold * 3, 3);
		cv::absdiff(frame_gray, frame1, frameDiff);
		frame_gray.copyTo(frame1);

		cv::imshow("Frame", frame);
		cv::imshow("Difference", frameDiff);
		cv::imshow("Blur", frame_blur);
		cv::imshow("Canny", canny);


		if (cv::waitKey(1000 / fps) != 255) {
			break;
		}
		
	}
		
	return 1;
}

void MyFilledCircle(cv::Mat img, cv::Point center)
{
	cv::circle(img, center, 400 / 32,
		cv::Scalar(0, 0, 255),
		cv::FILLED, cv::LINE_8);
}


