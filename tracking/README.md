[![gait-lab](tracking/examples/path_1.PNG)](https://github.com/anttilankinen/gait-lab)


Step 1:

	label_videos.py: annotation to label videos, most effective at labeling incorrect images. 

Step 2: 
	
	train_model.py: train the model on the images in labels folder, stores the model to the saved_models folder

Step 3:

	analyse_videos.py: analyses the video & stores the balls in a pickle file.

Step 4: 

	plot_path.py: plays video and outputs a video with pickle file details.


Extra files info:

	balls.pkl - pickle file containing balls paths
	run_model - file to run the tensorflow cnn

To Do:
	
	1) Improve plot path - fix logic to show the previous x number of frames
	2) Normalised dot product - similarity between images
	3) Add velocity and acceleration of points. (For low velocity consider points in a sphere, for higher velocity consider points in a cone)
	4) Improve the annotation software to be better for labelling correct images. (eg click on closest -> ball/not ball)
	5) Threshold for distance between points (Check if the change in velocity is very rapid, if it is lower threshold)
