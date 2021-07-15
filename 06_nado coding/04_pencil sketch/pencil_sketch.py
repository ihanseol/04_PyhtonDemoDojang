# pip install opencv-python

import cv2

img_location = 'c:/Users/minhwasoo/Desktop/'
filename = 'puppy.jpg'

img = cv2.imread(img_location+filename)

# convert the image to gray scale

gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

inverted_gray_image = 255 - gray_image
# blurred_img = cv2.GaussianBlur(inverted_gray_image, (21, 21), 0)
# blurred_img = cv2.GaussianBlur(inverted_gray_image, (11, 11), 0)
blurred_img = cv2.GaussianBlur(inverted_gray_image, (21, 21), 6)
inverted_blurred_img = 255 - blurred_img
pencil_sketch_img = cv2.divide(gray_image, inverted_blurred_img, scale=256.0)

cv2.imshow('original image', img)
# cv2.imshow('new image', gray_image)
# cv2.imshow('inverted image', inverted_gray_image)
# cv2.imshow('inverted image', blurred_img)
cv2.imshow('inverted image', pencil_sketch_img)


cv2.imwrite(img_location + 'converted2.jpg', pencil_sketch_img)
cv2.waitKey(0)


