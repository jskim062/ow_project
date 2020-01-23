import numpy as np
import argparse
#import cv2
#import mss 
import matplotlib.pyplot as plt
import skimage.io
import skimage.segmentation
#import mss
import cv2, time, sys, random, mss
import pyautogui as pag

import win32gui, win32api, win32con, ctypes



class Mouse:
    #"""It simulates the mouse"""
    MOUSEEVENTF_MOVE = 0x0001 # mouse move 
    MOUSEEVENTF_LEFTDOWN = 0x0002 # left button down 
    MOUSEEVENTF_LEFTUP = 0x0004 # left button up 
    MOUSEEVENTF_RIGHTDOWN = 0x0008 # right button down 
    MOUSEEVENTF_RIGHTUP = 0x0010 # right button up 
    MOUSEEVENTF_MIDDLEDOWN = 0x0020 # middle button down 
    MOUSEEVENTF_MIDDLEUP = 0x0040 # middle button up 
    MOUSEEVENTF_WHEEL = 0x0800 # wheel button rolled 
    MOUSEEVENTF_ABSOLUTE = 0x8000 # absolute move 
    SM_CXSCREEN = 0
    SM_CYSCREEN = 1

    def _do_event(self, flags, x_pos, y_pos, data, extra_info):
        #"""generate a mouse event"""
        x_calc = int(65536 * x_pos / ctypes.windll.user32.GetSystemMetrics(self.SM_CXSCREEN) + 1)
        y_calc = int(65536 * y_pos / ctypes.windll.user32.GetSystemMetrics(self.SM_CYSCREEN) + 1)
        return ctypes.windll.user32.mouse_event(flags, x_calc, y_calc, data, extra_info)

    def _get_button_value(self, button_name, button_up=False):
        #"""convert the name of the button into the corresponding value"""
        buttons = 0
        if button_name.find("right") >= 0:
            buttons = self.MOUSEEVENTF_RIGHTDOWN
        if button_name.find("left") >= 0:
            buttons = buttons + self.MOUSEEVENTF_LEFTDOWN
        if button_name.find("middle") >= 0:
            buttons = buttons + self.MOUSEEVENTF_MIDDLEDOWN
        if button_up:
            buttons = buttons << 1
        return buttons

    def move_mouse(self, pos):
        #"""move the mouse to the specified coordinates"""
        (x, y) = pos
        old_pos = self.get_position()
        x =  x if (x != -1) else old_pos[0]
        y =  y if (y != -1) else old_pos[1]    
        self._do_event(self.MOUSEEVENTF_MOVE + self.MOUSEEVENTF_ABSOLUTE, x, y, 0, 0)

    def press_button(self, pos=(-1, -1), button_name="left", button_up=False):
        #"""push a button of the mouse"""
        self.move_mouse(pos)
        self._do_event(self.get_button_value(button_name, button_up), 0, 0, 0, 0)

    def click(self, pos=(-1, -1), button_name= "left"):
        #"""Click at the specified placed"""
        self.move_mouse(pos)
        self._do_event(self._get_button_value(button_name, False)+self._get_button_value(button_name, True), 0, 0, 0, 0)

    def double_click (self, pos=(-1, -1), button_name="left"):
        #"""Double click at the specifed placed"""
        for i in xrange(2): 
            self.click(pos, button_name)

    def get_position(self):
        #"""get mouse position"""
        return win32api.GetCursorPos()


def _sendMouseEvent(ev, x, y, dwData=0):
    assert x != None and y != None, 'x and y cannot be set to None'
    width, height = _size()
    convertedX = 65536 * x // width + 1
    convertedY = 65536 * y // height + 1
    ctypes.windll.user32.mouse_event(ev, ctypes.c_long(convertedX), ctypes.c_long(convertedY), dwData, 0)

#mouse = Mouse()
#mouse.click((20, 10), "left")
#mouse.move_mouse((100,100))
#time.sleep(2.0)
#mouse.move_mouse((200,200))
#mouse.click((100, 100), "right")

#mouse = Mouse()
#mouse.click((x = 412 + cX,y = 391 + cY), "left")
#mouse.move_mouse((100,100))

xx = 1
yy = 1

while True:
	time.sleep(5)
	#print(xx)
	#print(yy)
	aim = {'left':700, 'top': 250, 'width': 500, 'height': 500}
	#plt.imshow(aim),plt.show()
	with mss.mss() as sct:
		aim_poision = np.array(sct.grab(aim))[:,:,:3]


	plt.imshow(aim_poision),plt.show()


	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", help = "Pocketmon_source.jpg")
	args = vars(ap.parse_args())
	
	# load the image
	#image = cv2.imread(args["image"])
	#image = cv2.imread(aim_poision)
	#image = cv2.imread("Pocketmon_source.jpg")
	image = aim_poision

	boundaries = [
		([20, 20, 110], [50, 50, 160])
		#([86, 31, 4], [220, 88, 50]),
		#([25, 146, 190], [62, 174, 250]),
		#([103, 86, 65], [145, 133, 128])
	]


	for (lower, upper) in boundaries:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")

		# find the colors within the specified boundaries and apply
		# the mask
		mask = cv2.inRange(image, lower, upper)
		output = cv2.bitwise_and(image, image, mask = mask)

		#plt.imshow(output),plt.show()

		#output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

		#cv2.imwrite('test_image.jpg', output)
		
		#print(output.shape)
		
		#im = output[:, :, ::-1]
		
		#print(im.shape)
		
		gray_image = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
	
		# convert the grayscale image to binary image
		ret,thresh = cv2.threshold(gray_image,0,255,0)
		
		# calculate moments of binary image
		M = cv2.moments(thresh)
		
		# calculate x,y coordinate of center
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		
		print(cX)
		print(cY)
		
		# put text and highlight the center
		cv2.circle(output, (cX, cY), 5, (255, 255, 255), -1)
		cv2.putText(output, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
		
		# display the image
		cv2.imshow("Image", output)
		cv2.waitKey(0)
		#pag.click(x=843 + cX, y=391 + cY)
		#pag.moveTo(x = 412 + cX, y = 228 + cY)
		mouse = Mouse()
		#mouse.click((x = 412 + cX,y = 391 + cY), "left")
		mouse.move_mouse((cX,cY))
		#xx = xx + 1
		#yy = yy + 1
		#time.sleep(2.0)
		
		time.sleep(1)

