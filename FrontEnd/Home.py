# Importing Libraries
import cv2
import os
import sys
import numpy as np
from collections import deque

from tensorflow import keras
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from qt_material import apply_stylesheet

from Alerts_and_Messages import Alert, Message
from BackEnd.Firebase_Operations import generate_log


def run_once(f):
    def wrapper(*args, **kwargs):

            if not f.has_run:
                f.has_run = True
                return f(*args, **kwargs)

    f.has_run = False
    return wrapper


class Home_Window(QMainWindow):

    def __init__(self, window_stack = None):
        """Load the Home Window"""

        super(Home_Window, self).__init__()
        uic.loadUi(r'Ui Files\Monitoring_Window.ui', self)                                              # Load the .ui file

        self.window_stack = window_stack                                                                # Accepting Window Stack
        self.cap = None                                                                 # Initializing Capture Variable

        self.window_size = 25
        self.model = keras.models.load_model('../ML/Models/Hockey_nofight_fight_Accuracy_98.9.h5')
        self.classes_list = ["Normal", "Abnormal"]
        self.predicted_labels_probabilities_deque = deque(maxlen=self.window_size)

        self.username = None                                                                            # Initializing Username
        self.name_tag = self.findChild(QLabel, 'Name_Label')                                   # Name Tag
        self.live_feed_section = self.findChild (QLabel, 'video')                              # Live Video Feed Display Section

        self.start_monitor_btn = self.findChild (QPushButton, 'Monitor_Button')                # Start Monitoring Button
        self.rec_btn = self.findChild (QPushButton, 'Record_Button')                           # Record Button
        self.prev_rec_btn = self.findChild (QPushButton, 'Prev_Rec_Button')                    # Previous Recordings Button
        self.logout_btn = self.findChild (QPushButton, 'Logout_Button')                        # Logout Button
        self.alert_btn = self.findChild (QPushButton, 'Alert_Button')

        self.timer = QTimer()                                                                           # Creating a Timer

        self.timer.timeout.connect(self.viewCam)                                                        # Set Timer Timeout callback function
        self.start_monitor_btn.clicked.connect(self.controlTimer)                                       # set control_bt callback clicked  function
        self.rec_btn.clicked.connect(self.record_live_feed)                                             # Record the Live Feed
        self.prev_rec_btn.clicked.connect(lambda: os.startfile(r"..\Recordings"))                           # Open previous Recordings Folder
        self.logout_btn.clicked.connect(self.logout)
        self.alert_btn.clicked.connect(self.alert)

    def controlTimer(self):
        if not self.timer.isActive():                                                                   # if timer is stopped
            self.cap = cv2.VideoCapture(r"C:\Users\JiN\Desktop\IRIS\Videos\V_1.mp4")                                              # Create video capture
            self.timer.start(20)                                                                        # start timer
            self.live_feed_section.setVisible(True)
            self.start_monitor_btn.setText("Stop Monitoring")                                           # update Button Text

        else:                                                                                           # if timer is started
            self.timer.stop()                                                                           # stop timer
            cv2.destroyAllWindows()
            self.cap.release()                                                                          # Release video capture
            self.live_feed_section.setVisible(False)
            self.start_monitor_btn.setText("Start Monitoring")                                          # Update Button Text

    def viewCam(self):
        ret, image = self.cap.read()                                                                    # read image in BGR format

        if ret:
            resized_frame = cv2.resize(image, (64, 64))
            normalized_frame = resized_frame / 255

            predicted_labels_probabilities = self.model.predict(np.expand_dims(normalized_frame, axis=0))[0]
            # decimal_pred = list(map(decimal_str, predicted_labels_probabilities))
            # # print(decimal_pred)

            self.predicted_labels_probabilities_deque.append(predicted_labels_probabilities)

            if len(self.predicted_labels_probabilities_deque) == self.window_size:
                predicted_labels_probabilities_np = np.array(self.predicted_labels_probabilities_deque)
                predicted_labels_probabilities_averaged = predicted_labels_probabilities_np.mean(axis=0)
                predicted_label = np.argmax(predicted_labels_probabilities_averaged)
                predicted_class_name = self.classes_list[predicted_label]

                cv2.putText(image, predicted_class_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                print(predicted_class_name)
                if predicted_class_name == "Abnormal":
                    self.alert()
                    print(predicted_labels_probabilities_averaged[1])
                    # self.timer.stop()


            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)                                                  # convert image to RGB format
            # flipped_image = cv2.flip(image, 1)                                                              # Flipping the Image
            height, width, channel = image.shape                                                    # get image info
            step = channel * width

            q_img = QImage(image.data, width, height, step, QImage.Format_RGB888)                   # create QImage from image
            self.live_feed_section.setPixmap(QPixmap.fromImage(q_img))                                      # show image in img_label

        else:
            self.timer.stop()  # stop timer
            cv2.destroyAllWindows()
            self.cap.release()  # Release video capture
            self.live_feed_section.setVisible(False)
            self.start_monitor_btn.setText("Start Monitoring")  # Update Button Text


    def record_live_feed(self):
        if (self.cap is None) or (self.cap.isOpened() is False):
            Message(self, "Error", "Unable to read camera feed")                                        ###### NEED MORE WORK HERE

        else:
            frame_width = int(self.cap.get(3))
            frame_height = int(self.cap.get(4))
            out = cv2.VideoWriter(r'Recordings\output.avi', cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), 20, (frame_width, frame_height))

            while True:
                ret, frame = self.cap.read()
                if ret:
                    out.write(frame)

                    if self.rec_btn.clicked():
                        self.rec_btn.setText("Stop Recording")
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                else:
                    break
            out.release()

    def logout(self):
        generate_log(self.username, "Sign-out")
        self.window_stack.setCurrentIndex(0)
        self.window_stack.resize(640, 240)

    @run_once
    def alert(self):
        ret, screenshot = self.cap.read()
        screenshot = cv2.flip(screenshot, 1)
        cv2.imwrite("../Recordings/Image Evidence/screenshot.jpg", screenshot)

        self.alert_window = Alert(self.username)
        self.alert_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_amber.xml')
    home_window = Home_Window()
    home_window.show()

    sys.exit(app.exec_())
