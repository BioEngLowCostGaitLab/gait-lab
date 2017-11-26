#include "opencv2\opencv.hpp"
#include "opencv2\features2d.hpp"
#include <vector>



// does not work yet, exceptoin thrown at detector.detect
int main()
{
	cv::VideoCapture cap("IMG_1496.MOV");
	cv::SimpleBlobDetector detector;

	if (!cap.isOpened()) return -1;

	while (cap.isOpened())
	{
		cv::Mat frame, keypoint_frame;
		std::vector<cv::KeyPoint> keypoints;
		cap >> frame;

		if (frame.empty()) break;

		detector.detect(frame, keypoints);
		cv::drawKeypoints(frame, keypoints, keypoint_frame,\
		cv::Scalar(0, 0, 255), cv::DrawMatchesFlags::DRAW_RICH_KEYPOINTS);

		cv::transpose(keypoint_frame, keypoint_frame);
		cv::flip(keypoint_frame, keypoint_frame, 1);

		cv::imshow("blobs", keypoint_frame);
		char c = (char)cv::waitKey(25);
		if (c == 27)
			break;
		
	}

	cap.release();

	cv::destroyAllWindows();
	return 0;
}