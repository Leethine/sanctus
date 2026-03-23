import cv2 as cv
import numpy as np
#from skimage.feature import match_template

img = cv.imread('all.png', cv.IMREAD_GRAYSCALE)
template = cv.imread('clef-do.png', cv.IMREAD_GRAYSCALE)

"""
result = match_template(img, template)
ij = np.unravel_index(np.argmax(result), result.shape)
x, y = ij[::-1]
rec = cv.rectangle(img, (x, y), (x+10, y+10), (0, 255, 0), 2)
cv.imwrite('result.png', rec)
print(result)
"""


w, h = template.shape[::-1]
#for scale_ratio in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]:
scale_ratio = 64. / h
if True:
#for scale_ratio in [0.2,0.3,0.4]:
  template_n = cv.resize(template, (int(w*scale_ratio), int(h*scale_ratio)))
  res = cv.matchTemplate(img, template_n, cv.TM_CCOEFF_NORMED)
  min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
  top_left = max_loc
  bottom_right = (top_left[0] + int(w*scale_ratio), top_left[1] + int(h*scale_ratio))
  rec = cv.rectangle(img, top_left, bottom_right, (0,0,0), 2)
  cv.imwrite('result.png', rec)


#threshold = 0.8
#loc = np.where(res >= threshold)
#for pt in zip(*loc[::-1]):
#  print(pt)
#  rec = cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), 255, 2)
