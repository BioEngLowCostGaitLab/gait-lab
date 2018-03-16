Step 1:

	label_videos.py: annotation to label videos, most effective at labeling incorrect images. 

	ToDo: Improve the annotation software to be better for labelling correct images. (eg click on closest -> ball/not ball)

Step 2: 
	
	train_model.py: train the model on the images in labels folder, stores the model to the saved_models folder

Step 3:

	analyse_videos.py: analyses the video & stores the balls in a pickle file.

Step 4: 

	plot_path.py: plays video and outputs a video with pickle file details.



Extra files info:

	balls.pkl - pickle file containing balls paths
	run_model - file to run the tensorflow cnn
