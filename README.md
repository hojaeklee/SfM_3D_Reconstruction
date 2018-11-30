# Structure from Motion
RGB-D structure from motion with DeMoN predicted Depth information. 

# Roadmap
- [ ] RGB-D SfM in python
- [ ] Depth Estimation from DeMoN
- [ ] Combine the results
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
- Calibration parameters (intrinsic & distortion)
- Evaluate on test dataset

# Running Demon
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


