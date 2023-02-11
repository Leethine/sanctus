import cv2, base64
import sys, os

class FaceCropper:
  def __init__(self) -> None:
    print()
    self._CASCADE = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    self._ZOOM_FACTOR = 1.6

    self._CROPPED_IMG = 0

  def detect_image(self, input_img :str) -> None:
    img = cv2.imread(input_img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = self._CASCADE.detectMultiScale(gray, 1.2, 4)
    x_c = 0
    y_c = 0
    w_c = 0
    h_c = 0

    for (x, y, w, h) in faces:
      if w * h > w_c * h_c:
        x_c = x
        y_c = y
        w_c = w
        h_c = h

    center_x = x_c + w_c / 2
    center_y = y_c + h_c / 2

    h = int(h_c * self._ZOOM_FACTOR)
    w = int(h_c * (4 / 3) * self._ZOOM_FACTOR)
    y = int(center_y - h / 2)
    x = int(center_x - w / 2)

    self._CROPPED_IMG = img[y:y+h,x:x+w]

  def write_result(self, output_image: str) -> None:
    cv2.imwrite(output_image, self._CROPPED_IMG)
  
  def encode_result(self) -> str:
    (x, buffer) = cv2.imencode('.png', self._CROPPED_IMG)
    return base64.b64encode(buffer).decode('ascii')
  
  def decode_result(self, buffer: str, out_image='decoded.png') -> str:
    with open(out_image, 'wb') as f_output:
      f_output.write(base64.b64decode(buffer))


if __name__ == '__main__':
  f = FaceCropper()
  f.detect_image(str(sys.argv[1]))
  f.write_result(str(sys.argv[2]))
