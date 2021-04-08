# # -*- coding: utf-8 -*-
#
# import cv2
#
# video_src = 'Videos\\people-walking.mp4'
#
# cap = cv2.VideoCapture(video_src)
# fgbg = cv2.bgsegm_BackgroundSubtractorGSOC()
# person_cascade = cv2.CascadeClassifier('pedestrian.xml')
#
# while True:
#     ret, img = cap.read()
#
#     if img is None:
#         break
#
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     fgmask = fgbg.apply(gray)
#     person = person_cascade.detectMultiScale(gray, 1.3, 2)
#
#     for (a, b, c, d) in person:
#         cv2.rectangle(img, (a, b), (a + c, b + d), (0, 255, 210), 4)
#
#     cv2.imshow('video', img)
#     # cv2.imshow('mask', fgmask)
#
#     if cv2.waitKey(10) == 27:
#         break
#
# cv2.destroyAllWindows()


# Standard imports
import cv2
import numpy as np;

# Read image
im = cv2.imread("blob.jpg", cv2.IMREAD_GRAYSCALE)

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector()

# Detect blobs.
keypoints = detector.detect(im)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
