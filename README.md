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
