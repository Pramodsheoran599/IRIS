from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
import os
import cv2


class Home_Window(QtWidgets.QMainWindow):

    def __init__(self, window_stack, login_window):
        """Load the Home Window"""
        super(Home_Window, self).__init__()                                                             # Call the inherited classes __init__ method

        uic.loadUi('UI\\Monitoring_Window.ui', self)                                                    # Load the .ui file
        self.show()                                                                                     # Show the GUI

        self.window_stack = window_stack
        self.login_window = login_window

        self.live_feed_section = self.findChild(QtWidgets.QLabel, 'video')                              # Live Video Feed Display Section
        self.start_monitor_btn = self.findChild(QtWidgets.QPushButton, 'Monitor_Button')                    # Start Monitoring Button
        self.rec_btn = self.findChild(QtWidgets.QPushButton, 'Record_Button')                               # Record Button
        self.prev_rec_btn = self.findChild(QtWidgets.QPushButton, 'Prev_Rec_Button')                        # Previous Recordings Button
        self.logout_btn = self.findChild(QtWidgets.QPushButton, 'Logout_Button')                            # Logout Button
        self.name_tag = self.findChild(QtWidgets.QLabel, 'Name_Label')
        self.name_tag.setText(f"Welcome {login_window.username_field.text()}")

        self.timer = QTimer()                                                                           # Creating a Timer
        self.timer.timeout.connect(self.viewCam)                                                        # Set Timer Timeout callback function

        self.start_monitor_btn.clicked.connect(self.controlTimer)                                       # set control_bt callback clicked  function
        self.rec_btn.clicked.connect(self.record_live_feed)                                             # Record the Live Feed

        # connect method accepts only functions and not function calls(passing arguments)
        # In order to pass arguments to connect method Lambda is used to generate a Function which calls the
        '''https://stackoverflow.com/questions/40982518/argument-1-has-unexpected-type-nonetype'''
        self.prev_rec_btn.clicked.connect(lambda: os.startfile("Recordings"))                           # Open previous Recordings Folder
        self.logout_btn.clicked.connect(self.logout)

    def controlTimer(self):
        """Load the Login Window and Extract the username, password and run validation"""
        if not self.timer.isActive():                                                                   # if timer is stopped
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)                                               # Create video capture
            self.timer.start(20)                                                                        # start timer
            self.start_monitor_btn.setText("Stop Monitoring")                                           # update Button Text

        else:                                                                                           # if timer is started
            self.timer.stop()                                                                           # stop timer
            cv2.destroyAllWindows()
            self.cap.release()                                                                          # Release video capture
            self.start_monitor_btn.setText("Start Monitoring")                                          # Update Button Text

    def viewCam(self):
        ret, image = self.cap.read()                                                                    # read image in BGR format

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)                                                  # convert image to RGB format
        flipped_image = cv2.flip(image, 1)
        height, width, channel = flipped_image.shape                                                    # get image info
        step = channel * width

        q_img = QImage(flipped_image.data, width, height, step, QImage.Format_RGB888)                   # create QImage from image

        self.live_feed_section.setPixmap(QPixmap.fromImage(q_img))                                      # show image in img_label

    def record_live_feed(self, frame):
        if self.cap.isOpened() is False:
            print("Unable to read camera feed")
        else:
            frame_width = int(self.cap.get(3))
            frame_height = int(self.cap.get(4))
            out = cv2.VideoWriter('Recordings/output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

            while True:
                ret, frame = self.cap.read()
                if ret:
                    out.write(frame)

                    # if self.rec_btn.clicked():
                    #     print("ss")
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                else:
                    break
            out.release()

    def logout(self):
        self.window_stack.setCurrentWidget(self.login_window)
        self.window_stack.setFixedWidth(620)
        self.window_stack.setFixedHeight(285)

