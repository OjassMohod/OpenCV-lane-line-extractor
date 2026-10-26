# Extract white/yellow road-marking edges from a static image

import os

import cv2 as cv
import numpy as np

INPUT_IMAGE = "road.webp"
OUTPUT_DIR = "results"
SHOW_IMAGE = True  # For OpenCV window

# Hue is 0-179; saturation and brightness are 0-255
WHITE_LOWER = np.array([0, 0, 180], dtype=np.uint8)
WHITE_UPPER = np.array([179, 70, 255], dtype=np.uint8)
YELLOW_LOWER = np.array([15, 70, 100], dtype=np.uint8)
YELLOW_UPPER = np.array([40, 255, 255], dtype=np.uint8)

BLUR_KERNEL_SIZE = 5
CANNY_LOW = 50
CANNY_HIGH = 150

def filter_lane_colors(image):
    # Keeps white and yellow pixels in a one-channel mask
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    white_mask = cv.inRange(hsv,WHITE_LOWER, WHITE_UPPER)
    yellow_mask = cv.inRange(hsv,YELLOW_LOWER, YELLOW_UPPER)
    return cv.bitwise_or(white_mask,yellow_mask)


def blur_color_mask(colors):
    # Smoothens small specks before finding edges
    return cv.GaussianBlur(colors,(BLUR_KERNEL_SIZE,BLUR_KERNEL_SIZE),0)

def detect_edges(blurred):
    #Finds boundaries in the smoothed mask
    return cv.Canny(blurred, CANNY_LOW, CANNY_HIGH)

def road_roi_mask(shape):
    #Marks the road-shaped region to keep
    height, width = shape[:2]
    vertices = np.array(
        [[
            (int(0.02 * width), int(0.92 * height)),
            (int(0.38 * width), int(0.30 * height)),
            (int(0.67 * width), int(0.30 * height)),
            (int(0.98 * width), int(0.92 * height)),
        ]],
        dtype=np.int32,
    )
    mask = np.zeros((height, width), dtype=np.uint8)
    cv.fillPoly(mask, vertices, 255)
    return mask

def make_comparison(image,roi_edges):
    #Places the original next to the extracted edge pixels
    edge_panel = cv.cvtColor(roi_edges, cv.COLOR_GRAY2BGR)
    comparison = cv.hconcat([image, edge_panel])
    cv.putText(comparison, "Original", (8, 20), cv.FONT_HERSHEY_SIMPLEX,
               0.5, (0, 0, 255), 1, cv.LINE_AA)
    cv.putText(comparison, "ROI edge pixels", (image.shape[1] + 8, 20),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)
    return comparison

def main():
    #Writing Paths relative to this script, so VS Code can run it from any folder
    project_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(project_dir, INPUT_IMAGE)
    output_dir = os.path.join(project_dir, OUTPUT_DIR)

    #Loading the road photo
    image = cv.imread(input_path)
    colors = filter_lane_colors(image)
    blurred = blur_color_mask(colors)
    edges = detect_edges(blurred)
    roi_mask = road_roi_mask(image.shape)
    roi_edges = cv.bitwise_and(edges, roi_mask)

    results = {
        "01_color_mask.png": colors,
        "02_blurred.png": blurred,
        "03_canny_edges.png": edges,
        "04_roi_mask.png": roi_mask,
        "05_roi_edges.png": roi_edges,
    }
    os.makedirs(output_dir, exist_ok=True)
    for filename, result in results.items():
        cv.imwrite(os.path.join(output_dir, filename), result)
    comparison = make_comparison(image, roi_edges)
    cv.imwrite(os.path.join(output_dir, "06_comparison.png"), comparison)

    print(f"Saved 6 images to {output_dir}")
    if SHOW_IMAGE:
        cv.imshow("Original and ROI edge pixels", comparison)
        cv.waitKey(0)
        cv.destroyAllWindows()

main()
