import os
import argparse
import Pipeline

if __name__ == "__main__":
	print("In main.py")

	parser = argparse.ArgumentParser(description = "Available options")
	parser.add_argument("-d", "--data_path", type = str, metavar = "", required = True, help = "Input dataset folder path")
	parser.add_argument("-s", "--show_clouds", type = bool, default = False, metavar = "", help = "Show result point clouds")
	parser.add_argument("-n", "--no_save_clouds", type = bool, default = False, metavar = "", help = "Don't save cloud outputs")
	parser.add_argument("-f", "--file_name", metavar = "", required = True, help = "Name of output filename (without .pcd)")
	
	args = parser.parse_args()

	folder_path = os.path.abspath(args.data_path)
	show_clouds = args.show_clouds
	save_clouds = not args.no_save_clouds
	file_name = args.file_name

	############
	# Pipeline #
	############ 

	# Create instance of pipeline
	pipeline = Pipeline.Pipeline(folder_path, file_name)
	print(pipeline.folder_path)
	# and run
	pipeline.run(save_clouds, show_clouds)
	



	