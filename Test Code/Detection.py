import cv2
import numpy as np

cap = cv2.VideoCapture('..\\Videos\\Abuse001_x264.mp4')
fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=60, detectShadows=False)

while cap.isOpened():
    ret, frame = cap.read()
    if frame is None:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    fgmask = fgbg.apply(blur)

    dilated = cv2.dilate(fgmask, (3, 3), iterations=1)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 80:
            continue

        # x = roi.shape[:]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    cv2.imshow("Dilated", dilated)

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
