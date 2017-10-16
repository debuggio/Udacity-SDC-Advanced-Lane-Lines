## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/undistorted.jpg "Undistorted"
[image2]: ./output_images/undistorted_0.jpg "Road Transformed"
[image3]: ./output_images/processed_0.jpg "Binary Example"
[image4]: ./output_images/warped_5.jpg "Warp Example"
[image5]: ./output_images/lines_0.jpg "Fit Visual"
[video1]: ./project_video_processed.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the second code cell of the IPython notebook located in "result.ipynb" 

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![undistorted][image1]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![undistorted testimage][image2]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

Istarted using combination of color and gradient thresholds to generate a binary image (color thresholding happens in method `color_threshold`, gradient - `abs_sobel_thresh`). But then found that it doesn't work quite well. So I'm using only color threshhold and trying to find yellow and white lines separately and then merge results. Whole process happens in method `process_image`  Here's an example of my output for this step.  (note: this is not actually from one of the test images)

![Binary Example][image3]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `warp_image`.  The `warp_image` function takes as inputs an initial image (`raw_image`), as well as processed_image (`processed_image`). I'm calculating source and destination points, using hardcoded percentage values to identify "region of interest" (excluding car hood). in the following manner:

```hardcoded values to set region of interest
    bot_width = .76
    mid_width = .16
    height_pct = .66
    bottom_trim = 1
    offset = image_size[1]*.33
```

This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 538, 475      | 237, 0        | 
| 742, 475      | 1042, 0       |
| 1126, 720     | 1042, 720     |
| 153, 720      | 237, 720      |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image. At first I excluded rectangle with car hood, but sometimes right line in presented only by small square on top of the hood, so I decided to keep this ares

![Warp Example][image4]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

`find_lane_lines` method finds lines, and do draw them on initial image:
`window_width` and `window_height` are chosen imperically but took some time to find the best value 
`xm_per_pixel` and `ym_per_pixel` are used to convert distance from pixels to meters 

1) at first I take a histogram of the 3/4 of an image. Then I'm looking for peaks on the left and right sides of the histogram. At first I impelemnted it with centroids but results were not that good and sometimes lines were not detected
Image is devided to 9 vertical images and for each image I'm storing left and right coordinates of lane line, and then I'm concatinating results

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

It happens in `find_lane_lines` method starting from line `yvals = range(0, warped.shape[0])` 
I calculated the position of the vehicle with respect to center in next 10 lines and then I apply result data to output image video frame

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

![Fit Visual][image5]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video_processed.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.

Initially, using gradients to detect lane lines failed. Gradients took too much noise, especially from shadows and from pavements. Then I tried to use c combination of gradient and color thresholds, but again, sometimes (especially on a bright road with a massive shadow from pavement or from car) results were not good. As a result I ended up using color spaces (RGB + HSV) to find white and yellow lines. These is still a field of improvement, but for now it solves project video and shows quite good results on challenging video, but sometimes it fails to detect anything, so it should be improved later
I also faced issues when I tried to find centroids and now I'm using histogram to identify where lane lines are

My current implementations fails to solve challenging videos even it shows good results in project video. I think if investigate more how to get rid of a gradient noise and improve color space detection (maybe using other olor spaces or tune parameters). I'll be able to solve challenge videos

In the end I found (thanks for reviewer) that radius of curvature was not correct, so I did some investigation and found out that my warped image is about 10 meters, so I changed my `ym_per_pixels` to appropriate value and results become much more realistic 