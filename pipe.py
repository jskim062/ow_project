import cv2
import numpy as np
rgb_img = cv2.imread('pipe.jpg')
gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
height, width = gray_img.shape


white_padding = np.zeros((50, width, 3))
white_padding[:, :] = [255, 255, 255]
rgb_img = np.row_stack((white_padding, rgb_img))

gray_img = 255 - gray_img
gray_img[gray_img > 100] = 255
gray_img[gray_img <= 100] = 0
black_padding = np.zeros((50, width))
gray_img = np.row_stack((black_padding, gray_img))

kernel = np.ones((30, 30), np.uint8)
closing = cv2.morphologyEx(gray_img, cv2.MORPH_CLOSE, kernel)

closing = np.uint8(closing)

edges = cv2.Canny(closing, 100, 200)

minLineLength = 500
maxLineGap = 10
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, None, 50, 100)
all_lines = lines[0]
for x1,y1,x2,y2 in lines[0]:
    cv2.line(rgb_img,(x1,y1),(x2,y2),(0,0,255),2)

all_lines_x_sorted = sorted(all_lines, key=lambda k: (-k[2], -k[0]))
for x1,y1,x2,y2 in all_lines_x_sorted[1:3]:
    cv2.line(rgb_img,(x1,y1),(x2,y2),(0,0,255),2)
all_lines_y_sorted = sorted(all_lines, key=lambda k: (-k[1]))
for x1,y1,x2,y2 in all_lines_y_sorted[:2]:
    cv2.line(rgb_img,(x1,y1),(x2,y2),(0,0,255),2)

final_lines = all_lines_x_sorted[1:3] + all_lines_y_sorted[:2]
#print(type(final_lines))
print(final_lines)
