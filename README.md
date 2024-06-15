# Surface-Recontruction-Using-Colmap
Utility scripts for correcting fisheye distortion, generation and injection of camera intrinsic values into COLMAP database.

The primary goal of this project is to explore the implementation of COLMAP on the BRUTUS Dataset. The data presented is 24 HD video files from which we extract a frame (say frame 0) for every video and attempt to make a 3D scene from the acquired images. The frames we acquire should be taken from the same timestamp to avoid “pixel motion”. The final goal is obtaining a dense representation (using MVS) of images from the BRUTUS Dataset.


## COLMAP Pipeline
COLMAP is a graphical and command-line interfaced general-purpose Structure-from-Motion (SFM) and Multi-View Stereo (MVS) pipeline. It has a variety of features for reassembling ordered and unordered image collections. Using Structure-from-Motion, image-based 3D reconstruction from images traditionally recovers a sparse representation of the scene and the camera poses of the input images first. This output is fed into Multi-View Stereo to create a dense scene representation. [^1]

## Brutus Dataset
Brutus is a multi-camera mid-range system for recording panoramic light field video content. The proposed system captures light fields with a wide baseline (0.9 meters), high resolution (>20 pixels per degree), and a large field of view (>220) at 60 frames per second. The array consists of 24 time-synchronized cameras distributed across the surface of a hemispherical plastic dome 60cm in diameter. We use Z CAM E2 professional cinema cameras mounted to the dome's exterior with 3D printed brackets. The dome, mounts, triggering hardware, and cameras are all reasonably priced, and the array is simple to build. Using the recently developed Deep-View Video pipeline, we can record and render subjects as close to the cameras as 50cm.[^2]

## Script Descriptions
### Extract frames: 
Extract_frames.py will extract frames from all video files in the directory passed onto it on the command line. For example, if you run the following command in the command line (in the Utility Scripts directory)
 
Note: I’m using forward slash to escape all special characters. The output will be generated in the Directory passed in a directory called Frames.

### Undistort frames:
Undistort_frames.py will undistort frames using FOV and POV parameters (which I have approximated and taken from BRUTUS[^2] ). For the Brutus dataset, it is recommended that you undistort the frames right after you run the extract frames script as the Brutus Data set has very high distortion. We do not have the camera intrinsic to support proper un-distortion in COLMAP. So instead of trying to undistort images in COLMAP which crops them to an unusable extent, we will use this script to first undistort the images to a usable extent and then use a SIMPLE_RADIAL_FISHEYE camera model in COLMAP to attempt further to undistort images before dense reconstruction. Usage:
 
### Export Intrinsic to text:
You won’t need this in most cases. If you have the intrinsic data available in JSON format this script will allow you to load it into Python, then export it in txt format; this text file is styled according to COLMAP Database parameters. Which is “Camera_ID Camera_Type Width Height Focal_length Principal_Point_x Principal_Point_y Distortion_coefficient_1 Distortion_coefficient_2”. Then we can either manually use this to update the database in COLMAP or use a Python script to do so. The structure of the JSON file should be of the following format:
 
If you have intrinsic data for a rig at hand, then it is recommended to use it to create a better sparse model from the images. Further information can be found in the COLMAP Documentation. [^3]

### Undistort Using Intrinsic Information
The ‘undistort_using_intrinsic_information.py’ Python script will undistort images using the aforementioned JSON file’s intrinsic information. It is recommended to use this if you have the intrinsic at hand (at the time of making this project I did not). This will help you undistort images before you feed them into the COLMAP pipeline. Alternatively, you can also try feeding the intrinsic parameters directly into COLMAP and observe the difference.


# Demo
[Video Demo](https://youtu.be/o3DYzf60YBM)

![Presentation](Resources/Presentation.pdf)

[Technical Report](Resources/TechnicalReport.pdf)


<a href="http://www.youtube.com/watch?feature=player_embedded&v=o3DYzf60YBM
" target="_blank"><img src="http://img.youtube.com/vi/o3DYzf60YBM/0.jpg" 
alt="Colmap on Brutus Dataset" width="240" height="180"/></a>


# References
[^1]: Johannes L. Schönberger, “COLMAP Source Code,” https://github.com/colmap/colmap Github.
[^2]: M. Broxton et al., “A Low Cost Multi-Camera Array for Panoramic Light Field Video Capture,” in SIGGRAPH Asia 2019 Posters, New York, NY, USA: ACM, Nov. 2019, pp. 1–2. doi: 10.1145/3355056.3364593.
[^3]: “COLMAP Documentation,” https://colmap.github.io/index.html. GithubIO (accessed Apr. 08, 2023).