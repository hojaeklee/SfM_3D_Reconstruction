# Structure from Motion 

Project for EECS 504 (Computer Vision) in Fall 2018.

Team Members: Alex Groh, Hojae Lee, Steven Liu

## Note to grader
In our experience it took multiple hours for all of our code dependencies to compile (OpenCV, PCL, Python bindings to PCL). To save you some time, and in case the install process doesn't work for you, we included a video that shows the code running (sfm.mov).

## Installation Directions

We have tested this installation in Ubuntu 16.0.4 (LTS).

1. Clone this directory: `git clone https://github.com/hojaeklee/SfM_3D_Reconstruction.git`
2. Install python dependencies: `pip install pyyaml cython==0.25.2` 
3. Install c++ dependencies by following the links:
	* [OpenCV 3.0.0 or OpenCV 3.1.1](https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/)
	* [Point Cloud Library (PCL)](http://pointclouds.org/downloads/linux.html)
	* [Python Bindings for PCL](https://github.com/strawlab/python-pcl)
	* [Depth Motion Net (DeMoN)](https://github.com/lmb-freiburg/demon)


## Running the Pipeline
1. Go to the src directory by `cd src`.
2. Run `python main.py -d ../data -f 3dreconstruct` . This will run our pipeline on the RGBD images stored in the `data` folder, and create the `3dreconstruct.pcd` file. Note `-d` specifies the path to images folder, and `-f` specifies the filename to save the Point Cloud Data (`.pcd`) file. The filename can be freely specified. 
3. To visualize the 3D reconstruction (`.pcd` file), run `pcl_viewer 3dreconstruct.pcd`.
