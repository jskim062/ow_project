import cv2 as cv
import numpy as np

c = np.uint8([[[113,99,255 ]]])
hsv_c = cv.cvtColor(c,cv.COLOR_BGR2HSV)
print( hsv_c )

c = np.uint8([[[67,53,158 ]]])
hsv_c = cv.cvtColor(c,cv.COLOR_BGR2HSV)
print( hsv_c )