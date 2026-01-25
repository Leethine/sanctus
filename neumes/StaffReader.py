import cv2 as cv
import numpy as np
import math

from CVTools import horizontal_median_filter

class StaffReader:
  def __init__(self, impath: str):
    self.__img = cv.imread(impath, cv.IMREAD_GRAYSCALE)
    self.__imrgb = cv.imread(impath, cv.IMREAD_COLOR_RGB)
    assert self.__img is not None, "Image could not be read, check the path provided"
    
    self.CANNY_TH1 = 50
    self.CANNY_TH2 = 200
    self.MORTH_KERNEL_SIZE = 5
    self.MEDIAN_FILTER_KERNEL_SIZE = 15
    self.HOUGH_TH = 1000
  
  def detectStaff(self):
    self.__edge = cv.Canny(self.__img, self.CANNY_TH1, self.CANNY_TH2, None, 3)
    self.__edge = cv.dilate(self.__edge, np.ones((self.MORTH_KERNEL_SIZE, self.MORTH_KERNEL_SIZE), np.uint8), iterations=3)
    self.__edge = cv.erode(self.__edge, np.ones((self.MORTH_KERNEL_SIZE, self.MORTH_KERNEL_SIZE), np.uint8), iterations=3)
    self.__edge = horizontal_median_filter(self.__edge, self.MEDIAN_FILTER_KERNEL_SIZE)
    lines = cv.HoughLines(self.__edge, 1, np.pi / 180, self.HOUGH_TH, None, 0, 0)
    line_ypos = []
    if lines is not None:
      for i in range(0, len(lines)):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt = (int(x0 - 10000*(-b)), int(y0 - 10000*(a)))
        line_ypos.append(pt[1])
    self._staffline_ypos.sort(reverse=True)
    ydiff = np.array(self.staffline_ypos[1:]) - np.array(self.staffline_ypos[:-1])
    self._staffline_ydiff = ydiff.tolist()
    
  def verifyStaff(self):
    DIFF_RATIO_TH = 0.9
    line_distance = min(self._staffline_ydiff)
    for i in range(len(self._staffline_ydiff)):
      if i % 3 == 0:
        pass
      else:
        if float(self._staffline_ydiff[i] / line_distance) < DIFF_RATIO_TH or \
           float(self._staffline_ydiff[i] / line_distance) > 1. / DIFF_RATIO_TH :
          print(f"On line {i}, line distance check failed")
          return False
    return True
  
  def getAverageLineDistance(self):
    DIFF_RATIO_TH = 0.9
    line_distance = min(self._staffline_ydiff)
    diffs = []
    for diff in self._staffline_ydiff:
      if float(diff / line_distance) > DIFF_RATIO_TH and \
         float(diff / line_distance) < 1. / DIFF_RATIO_TH :
        diffs.append(diff)
    average_distance = sum(diffs) / len(diffs)
    return average_distance

  def detectDoClef(self):
    #TODO testing
    distance = self.getAverageLineDistance()
    template = cv.imread('clef-do.png', cv.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]
    scale_ratio = 2. * distance / h
    template_n = cv.resize(template, (int(w*scale_ratio), int(h*scale_ratio)))
    res = cv.matchTemplate(self.__img, template_n, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + int(w*scale_ratio), top_left[1] + int(h*scale_ratio))
    rec = cv.rectangle(self.__img, top_left, bottom_right, (0,0,0), 2)
    cv.imwrite('result.png', rec)

