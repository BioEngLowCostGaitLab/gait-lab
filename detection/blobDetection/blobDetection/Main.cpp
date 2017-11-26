#include "opencv2\opencv.hpp"
#include "opencv2\features2d.hpp"
#include <vector>


int main()
{
	cv::VideoCapture cap("IMG_1496.MOV"); /* Copy this video to 
										  gait-lab/detection/blobDetection/blobDetection. It will
										  not be pushed to the repo as all MOV, mp4, jpg and png files are ignored.*/
	cv::Mat frame, keypoint_frame;
	cv::SimpleBlobDetector::Params params;
 
	params.minThreshold = 10;
	params.maxThreshold = 200;
 
	params.filterByColor = true;
	params.blobColor = 255; //white blob

	params.filterByArea = true;
	params.minArea = 500;

	params.filterByCircularity = true;
	params.minCircularity = 0.1;

	cv::Ptr<cv::SimpleBlobDetector> detector= cv::SimpleBlobDetector::create(params);

	if (!cap.isOpened()) return -1;

	while (cap.isOpened())
	{
		std::vector<cv::KeyPoint> keypoints;
		cap >> frame;
		cv::Mat frame_gray, frame_bin;

		if (frame.empty()) break;

		cv::cvtColor(frame, frame_gray, cv::COLOR_RGB2GRAY);
		cv:threshold(frame_gray, frame_bin, 50, 255, cv::THRESH_BINARY);
		/*cv::adaptiveThreshold(frame_gray, frame_bin, 255, cv::ADAPTIVE_THRESH_MEAN_C, \
			cv::THRESH_BINARY, 11, 2);*/ // good to know for later use
		detector->detect(frame_bin, keypoints);
		cv::drawKeypoints(frame, keypoints, keypoint_frame, \
		cv::Scalar(0, 0, 255), cv::DrawMatchesFlags::DRAW_RICH_KEYPOINTS);

		cv::transpose(keypoint_frame, keypoint_frame);
		std::cout << keypoints.size() << std::endl;
		cv::imshow("blobs", keypoint_frame);
		char c = (char)cv::waitKey(25);
		if (c == 27)
			break;
		
	}

	cap.release();

	cv::destroyAllWindows();
	return 0;
}