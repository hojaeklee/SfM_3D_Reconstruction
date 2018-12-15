# Structure from Motion using learned depth and motion
RGB-D structure from motion with DeMoN predicted depth, rotation, and translation information. 

# Overview and abstract
DeMoN - "Depth and Motion Network for Learning Monocular Stereo" is an end-to-end convolutional network which estimates depth, camera motion, optical flow from successive image pairs. In contrast to networks which estimate depth from single image, DeMoN has learned to exploit matching between image pairs and motion parallax which provides better generality to structures not seen during training. DeMoN outperforms classic structure from motion pipelines, by a factor of 1.5 to 2 in the Sun3D, NYUv2, Scenes11, RGB-D SLAM, and MVS datasets. 

Classic Pipleline 
SIFT-> FlowFields Optical Flow -> Essential Matrix via 8pt algorithm + RANSAC -> 
-> Plane sweep stereo ->

## DeMoN Architecture
- Chain of three networks with internal encoder-decoder subnetworks
    - Bootstrap Network 
        - a series of two encoder-decoder networks which inputs image pair and outputs initial depth and motion estimate
        - Encoder 1
            - convolutional layers with 1D filters in y,x directions
            - gradually reduce spatial resolution with stride of 2 while increasing channels
        - Decoder 1
            - outputs the optical flow estimate using encoder output/representation
            - a series of up-convolutional layers with stride 2 followed by two convolutional layers
        - Encoder 2 / Decoder 2
            - same architecture as encoder/decoder 1 with 3 fully connected layers which compute camera motion and scaling factor for depth prediction. There is an inherent connection between depth and motion predicitons due to scale ambiguity. 
            - inputs optical flow + confidence estimate from first encoder/decoder, the image pair, and the second image warped with the estimated flow field
            - outputs are estimates of depth, surface normals, and camera motion
        
    - Iterative Network
        - trained to improve existing depth, normal, and motion estimates through interative estimation. Bootstrap network fails to accurately estimate the scale of the depth. Iterations refine depth prediction and improve the scale of depth values.
        - architecture is identical to bootstrap network, except with additional inputs to the encoder networks
        - encoder1 
            - additional input = optical flow field estimated from depthmap and camera motion ouput of bootstrap or previous interation?
        - encoder2 
            - additional input = depth map estimated from camera motion + optical flow prediction
    - Refinement Network 
        - previous networks operate at 64x48 resolution to reduce parameters and reduce training and test time
        - refinement net upscales the predictions to full input image resolution (256x192, 4:3 ratio)
        - Input is full resolution input image and nearest neighbor upsampled depth and normal field


    - 

# Roadmap
- [x] RGB-D SfM in python
- [x] Depth + Pose Estimation from DeMoN
- [ ] Combine the results
- [ ] Data Capture and formatting of scene for Reconstruction
- Enhancement: Integrate DeMoN pose estimation in place of Registration step

# RGBD SFM Pipeline
SFM standard pipeline:

- [x] Load Images > Steven
- [x] Feature Extraction > Steven
- [x] Find Matching Pairs > Steven
- [x] Registration > Steven
- [x] Spanning Tree > Hojae
- [x] Global Camera Poses > Hojae
- [x] Find Clusters > Hojae
- [x] Find CoM > Hojae
- [ ] Bundle Adjustment > TODO
- [ ] Viewer
  - [x] createPointCloud
  - [x] saveCloud
  - [ ] reduceCloud
- [x] Util functions: as needed

# DeMoN > Alex
- [x] Use pretrained weights (Filetype)
- [ ] Collect test dataset: Waiting on kinect v1
- [ ] Format dataset: scale to use camera intrinsics in SUN3D
- [ ] Calibration parameters (intrinsic & distortion)
- [x] Evaluate on test dataset

# Using Demon
- Photos used in demon must be undistorted and rectified using the camera calibration matrix and a function such as OpenCV's 
```
570.3422047415297129191458225250244140625 0 320
0 570.3422047415297129191458225250244140625 240
0 0 1
```
# Running Demon
- input resolution 256x192 , 4x3 ratio

## Requirements
- tensorflow 1.4.0
- cmake 3.7.1
- python 3.5
- cuda 8.0.61 (required for gpu support)
- VTK 7.1 with python3 interface (required for visualizing point clouds) 

```bash
# create virtualenv
pew new demon_venv
```
```bash
# install python module dependencies
pip3 install tensorflow-gpu # or 'tensorflow' without gpu support
pip3 install pillow         # for reading images
pip3 install matplotlib     # required for visualizing depth maps
pip3 install Cython         # required for visualizing point clouds
```
## Building lmbspecialops
```bash
# clone repo with submodules
git clone --recursive https://github.com/lmb-freiburg/demon.git

# build lmbspecialops
DEMON_DIR=$PWD/demon
mkdir $DEMON_DIR/lmbspecialops/build
cd $DEMON_DIR/lmbspecialops/build
cmake .. # add '-DBUILD_WITH_CUDA=OFF' to build without gpu support
# (optional) run 'ccmake .' here to adjust settings for gpu code generation
make
pew add $DEMON_DIR/lmbspecialops/python # add to python path

# download weights
cd $DEMON_DIR/weights
./download_weights.sh

# run example
cd $DEMON_DIR/examples
python3 example.py # opens a window with the depth map (and the point cloud if vtk is available)
```
## Evaluation 
``` bash
pip install h5py
pip install minieigen
pip install pandas
pip install scipy
pip install scikit-image
pip install xarray
```

- git submodule update --init --recursive 

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
sudo apt-get install cmake-curses-gui
```

## OpenCV3

Followed the instructions [here](https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/) to install version 3.1.0
```
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip
unzip opencv.zip
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip
unzip opencv_contrib.zip
cd ~
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/get-pip.py ~/.cache/pip
echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.bashrc
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc
mkvirtualenv cv -p python3
workon cv
pip install numpy
cd ~/opencv-3.1.0/
mkdir build && cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules \
    -D PYTHON_EXECUTABLE=~/.virtualenvs/cv/bin/python \
    -D BUILD_EXAMPLES=ON ..
make -j4
sudo make install
sudo ldconfig
cd /usr/local/lib/python3.5/site-packages/
sudo mv cv2.cpython-35m-x86_64-linux-gnu.so cv2.so
cd ~/.virtualenvs/cv/lib/python3.5/site-packages/
ln -s /usr/local/lib/python3.5/site-packages/cv2.so cv2.so
```

## PCL
Compile PCL 1.8.1 from source. 

- Need to compile VTK from source too (Used VTK-7.1.1 due to OpenGL errors on parallels).
- Also, ccmake required to configure the PCL installation.

Download VTK-7.1.1 from here: https://www.vtk.org/files/release/7.1/VTK-7.1.1.tar.gz
```
tar xvzf VTK-7.1.1.tar.gz
cd VTK-7.1.1
mkdir build && cd build
cmake ..
make -j4
sudo make install
```

Download pcl-pcl-1.8.1 from here: https://github.com/PointCloudLibrary/pcl/archive/pcl-1.8.1.tar.gz
```
tar xvzf pcl-pcl-1.8.1.tar.gz
cd pcl-pcl-1.8.1
mkdir build && cd build
ccmake ..
make -j4
sudo make install
```
## PCL with python (python-pcl)
```
cd ~
git clone https://github.com/strawlab/python-pcl.git
pip install --upgrade pip
pip install cython==0.25.2
pip install numpy
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
cd $PKG_CONFIG_PATH
```
comment out `pcl_2d-1.8` in line 10 of pcl_features-1.8.pc
```
cd ~/python-pcl
python setup.py build_ext -i
python setup.py install
```
## Ceres
Followed instructions [here](http://ceres-solver.org/installation.html#linux)

