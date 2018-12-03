## SFM Install notes
This project requires:

- Ubuntu 16.04
- OpenCV3 (3.1.0 With extra contrib modules)
- PCL (1.8.1)
- Ceres solver (1.14.0)

## Clean Install
The following dependencies are required:

```
sudo apt install git
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libgtk-3-dev
sudo apt-get install libatlas-base-dev gfortran
sudo apt-get install python2.7-dev python3.5-dev
sudo apt-get install cmake
sudo apt-get install libgoogle-glog-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libeigen3-dev
sudo apt-get install libsuitesparse-dev
sudo apt-get install libboost-all-dev
sudo apt-get install freeglut3-dev
sudo apt-get install doxygen
```

## OpenCV3

Followed the instructions [here](https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/) to install version 3.1.0

## PCL
Compile PCL 1.8.1 from source. 

- Need to compile VTK from source too (Used VTK-7.1.1 due to OpenGL errors on parallels).
- Also, ccmake required to configure the PCL installation.

## PCL with python (python-pcl)
```
git clone https://github.com/strawlab/python-pcl.git
pip install --upgrade pip
pip install cython==0.25.2
pip install numpy
python setup.py build_ext -i
python setup.py install
```
If errors, either
```
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
```
or comment out dependency on pcl_2d-1.8 in PKG_CONFIG_PATH/pcl_features-1.8.pc

## Ceres
Followed instructions [here](http://ceres-solver.org/installation.html#linux)
Compile PCL 1.8.1 from source. Need to compile VTK from source too (Used VTK-7.1.1 due to OpenGL errors on parallels).
Also, ccmake required to configure the PCL installation.
