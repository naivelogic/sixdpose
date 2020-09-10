# sixdpose

## Introduction and Background on BOP: Benchmark for 6D Object Pose Estimation 



## Approach with Pix2Pose

For the purposes of learning the depth and breath of topics that goes into solving the 6D Pose estimation problem, we utilized the Pix2Pose method addresses the challenge of the problem by:
1.	Occlusion: estimating the 3D coordinates per-pixel and generative adversarial training
2.	Symmetry: introducing a novel L1-based transformer loss
3.	Lack of precise 3D object models: using RGB images without textured models during training phase. 

The full 6D pose is obtained by employing PnP and RANSAC over the predicted 3D coordinates. 
This is a regression based method in which we:
•	Input an RGB image
•	Input pre-processing (default = none) (contribution) augmentation to minimize overfitting
•	Training data on both real and synthetic data
•	Regression parameter using the 3D translation (x = (x, y, z))
•	Regressor Training (L1) 
•	Trained regressor (CNN)
•	Refinement step = PnP & RANSAC
•	Filtering = default none
•	Instance level
