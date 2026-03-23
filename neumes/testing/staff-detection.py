import cv2 as cv
import numpy as np
import math

def horizontal_median_filter(image, kernel_size):
  if kernel_size % 2 == 0 or kernel_size <= 1:
    raise ValueError("kernel_size must be an odd integer greater than 1.")
  filtered_image = np.zeros_like(image)
  for i in range(image.shape[0]):
    filtered_image[i, :] = cv.medianBlur(image[i:i+1, :], kernel_size)[0, :]
  return filtered_image

# Edge detection
in_img = cv.imread('sample.png', cv.IMREAD_GRAYSCALE)
out_img = cv.Canny(in_img, 50, 200, None, 3)
out_img = cv.dilate(out_img, np.ones((5, 5), np.uint8), iterations=3)
out_img = cv.erode(out_img, np.ones((5, 5), np.uint8), iterations=3)
out_img = horizontal_median_filter(out_img, 15)

# line detection
HOUGH_TH = 1000
lines = cv.HoughLines(out_img, 1, np.pi / 180, HOUGH_TH, None, 0, 0)
cdst = cv.cvtColor(in_img, cv.COLOR_GRAY2BGR)

line_ypos = []

if lines is not None:
  for i in range(0, len(lines)):
    rho = lines[i][0][0]
    theta = lines[i][0][1]
    a = math.cos(theta)
    b = math.sin(theta)
    x0 = a * rho
    y0 = b * rho
    pt1 = (int(x0 + 10000*(-b)), int(y0 + 10000*(a)))
    pt2 = (int(x0 - 10000*(-b)), int(y0 - 10000*(a)))
    # Check if rotation needed
    line_ypos.append(pt2[1])
    cv.line(cdst, pt1, pt2, (0,0,255), 3, cv.LINE_AA)

cv.imwrite("result.png", cdst)
line_ypos.sort(reverse=True)
print(line_ypos)
line_ydiff = np.array(line_ypos[:-1]) - np.array(line_ypos[1:])
print(line_ydiff.tolist())
