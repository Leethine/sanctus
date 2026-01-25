import cv2 as cv
import numpy as np

def horizontal_median_filter(image: np.array, kernel_size: int) -> np.array:
  if kernel_size % 2 == 0 or kernel_size <= 1:
    raise ValueError("kernel_size must be an odd integer greater than 1.")
  filtered_image = np.zeros_like(image)
  for i in range(image.shape[0]):
    filtered_image[i, :] = cv.medianBlur(image[i:i+1, :], kernel_size)[0, :]
  return filtered_image

