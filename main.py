import cv2 as cv

img = cv.imread("road.webp")

cv.imshow('Road',img)

cv.waitKey(0)