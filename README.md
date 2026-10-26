Lane edge extractor

What the program does:-

Loads a static road image using OpenCV.

Uses HSV color filtering to isolate white and yellow lane markings.

Applies Gaussian blur to reduce image noise.

Uses Canny edge detection to identify lane-marking boundaries.

Applies a Region of Interest (ROI) mask to retain edges within the road area.

Saves the processed images for viewing and comparison.


Functions in main.py

filter_lane_colors(image): Converts the image to HSV and makes a mask of white and yellow pixels

blur_color_mask(colors): Smooths that mask before edge detection

detect_edges(blurred): Uses Canny to find edges in the blurred mask

road_roi_mask(shape): Makes a road-shaped polygon mask the same size as the image

make_comparison(image, roi_edges): Places the original and final edge image side by side

main(): Loads the image, runs the functions in order, applies the road mask, and saves the images
