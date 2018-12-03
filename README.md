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
- [ ] RGB-D SfM in python
- [ ] Depth + Pose Estimation from DeMoN
- [ ] Combine the results
- [ ] Data Capture and formatting of scene for Reconstruction
- Enhancement: Integrate DeMoN pose estimation in place of Registration step

# RGBD SFM Pipeline
SFM standard pipeline:

- Step 0: Load Images > Steven
- Step 1: Feature Extraction > Steven
- Step 2: Find Matching Pairs > Steven
- Step 3: Registration > Steven
- Step 4: Spanning Tree > Hojae
- Step 5: Global Camera Poses > Hojae
- Step 6: Find Clusters > Hojae
- Step 7: Find CoM > Hojae
- Step 8: Bundle Adjustment > Hojae
- Viewer:
- Util functions:

# DeMoN > Alex
- Use pretrained weights (Filetype)
- Collect test dataset
- Format dataset - scale to use camera instrinsics in SUN3d
- Calibration parameters (intrinsic & distortion)
- Evaluate on test dataset

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


