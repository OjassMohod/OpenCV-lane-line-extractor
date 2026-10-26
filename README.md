Lane edge extractor

What the program does

The program reads road.webp. It selects white and yellow pixels, blurs small
specks, finds edges with Canny, and keeps edges inside a road-shaped region.
It saves each stage and a comparison with the original image in results/.

The final image contains edge pixels, not fitted lane lines.

Functions in main.py

filter_lane_colors(image): Converts the image to HSV and makes a mask of white and yellow pixels
blur_color_mask(colors): Smooths that mask before edge detection
detect_edges(blurred): Uses Canny to find edges in the blurred mask
road_roi_mask(shape): Makes a road-shaped polygon mask the same size as the image
make_comparison(image, roi_edges): Places the original and final edge image side by side
main(): Loads the image, runs the functions in order, applies the road mask, and saves the images
