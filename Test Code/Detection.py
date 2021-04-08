import cv2
import numpy as np

cap = cv2.VideoCapture('Videos\\pedestrians.avi')                                                  # Loading the Video
fgbg = cv2.createBackgroundSubtractorKNN()                                                         # Background Subtractor
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))                                       # Kernel

while cap.isOpened():
    ret, frame = cap.read()                                                                         # Read the Frame from Video
    if frame is None:                                                                               # If Last frame is read
        break                                                                                            # Exit Loop

    blank_image = np.zeros((frame.shape[:2]), np.uint8)                                             # Creating a Black Image of Same Size
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                                                  # Gray Conversion
    blur = cv2.GaussianBlur(gray, (5, 5), 2)                                                        # Applying Blur
    fgmask = fgbg.apply(blur)                                                                       # Creating Foreground Mask

    diff = blank_image - fgmask                                                                     # Difference Between Mask and Blank Image
    dilated = cv2.dilate(diff, (7, 7), iterations=2)                                                # Dilating the Difference

    diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, (3, 3), iterations=3)                      # Opening ( False Positives Correction )
    diff = cv2.morphologyEx(diff, cv2.MORPH_CROSS, (3, 3), iterations=3)                     # Closing ( False Negatives Correction )

    dilated = cv2.dilate(diff, (3, 3))
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)                 # Finding Contours

    persons = []                                                                                    # List of Detected People

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)                                                    # Coordinates of the Contour

        if cv2.contourArea(contour) < 480:                                                          # If Contour Less than Threshold
            continue                                                                                    # Skip the Contour

        persons.append((x, y, w, h))                                                                # Add the Coordinate to Person List

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)                                # Draw the Bounding Box

    for person in persons:                                                                          # For each person
        x, y, w, h = person                                                                             # Coordinates Unpacking
        centroid = ((x + w//2), (y + h//2))                                                             # Centroid
        cv2.circle(frame, centroid, 2, (0, 0, 255), 2)                                                  # Draw Centroid

    cv2.imshow("Frame", frame)                                                                      # Display Orignal Frame
    cv2.imshow("Dilated", dilated)                                                                  # Display Dilated Frame

    if cv2.waitKey(20) == 27:                                                                       # If Esc Key Pressed
        break                                                                                           # Exit the Loop

cv2.destroyAllWindows()
cap.release()
