import os
import argparse
import Pipeline

if __name__ == "__main__":
	print("In main.py")

	parser = argparse.ArgumentParser(description = "Available options")
	parser.add_argument("-d", "--data_path", type = str, metavar = "", required = True, help = "Input dataset folder path")
	parser.add_argument("-s", "--show_clouds", type = bool, default = False, metavar = "", help = "Show result point clouds")
	parser.add_argument("-n", "--no_save_clouds", type = bool, default = False, metavar = "", help = "Don't save cloud outputs")

	args = parser.parse_args()

	folder_path = os.path.abspath(args.data_path)
	show_clouds = args.show_clouds
	save_clouds = args.no_save_clouds

	############
	# Pipeline #
	############ 

	# Create instance of pipeline
	pipeline = Pipeline.Pipeline(folder_path)
	print(pipeline.folder_path)
	# and run
	pipeline.run(save_clouds, show_clouds)
	



	