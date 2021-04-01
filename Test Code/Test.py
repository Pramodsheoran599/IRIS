import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if cap.isOpened():
    ret, frame = cap.read()

else:
    ret = False

while ret:
    ret, frame = cap.read()
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.

    cv2.imshow("", frame)
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()

cap.release()