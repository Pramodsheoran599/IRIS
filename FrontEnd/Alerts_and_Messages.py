# Importing Libraries

from PyQt5 import uic
from PyQt5.QtCore import QRect, QPropertyAnimation
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QPlainTextEdit, QRadioButton, qApp

from BackEnd.Firebase_Operations import generate_alert


class Alert(QMainWindow):
    def __init__(self, username):
        super(Alert, self).__init__()

        uic.loadUi(r"Ui Files\Alert_Window.ui", self)                                           # Load Alert_Window UI File

        self.username = username                                                                # Username of currently Signed-in User
        self.screenshot = QPixmap("../Recordings/Image Evidence/screenshot.jpg")                # Read Evidence Screenshot
        self.comment_section = self.findChild(QPlainTextEdit, "Comment_Section")                # Comment Section
        self.evidence = self.findChild(QLabel, "Screenshot")                                    # Evidence Display Area

        self.sus_radio_btn = self.findChild(QRadioButton, "Suspicious_Radio_Button")            # Suspicious Radio Button
        self.false_radio_btn = self.findChild(QRadioButton, "False_Alarm_Radio_Button")         # False Alarm Radio Button
        self.submit_btn = self.findChild(QPushButton, "Submit_Button")                          # Submit Button

        self.evidence.setPixmap(self.screenshot)                                                # Display Screenshot in Evidence Section

        self.submit_btn.setShortcut('Return')                                                   # Shortcut Key for Submit Button
        self.submit_btn.clicked.connect(self.create_alert)                                      # On Click Generate Alert


    def create_alert(self):
        """Create an Alert and Store it in the Database"""

        if self.sus_radio_btn.isChecked():
            detection = "Suspicious Activity"

        else:
            detection = "False Alarm"

        comment = self.comment_section.toPlainText()                    # Get Comment from Comment Section

        self.anim = QPropertyAnimation(self.submit_btn, b"geometry")
        self.anim.setDuration(5)
        self.anim.setStartValue(QRect(590, 360, 161, 51))
        self.anim.setEndValue(QRect(540, 360, 261, 51))
        self.anim.start()
        self.submit_btn.setText("Uploading Evidence...")                # Setting Button Text
        qApp.processEvents()                                            # Forcing GUI update to display above text before generate alert execution

        generate_alert(self.username, detection, comment)               # Push Alert to Cloud

        Message(self, "Success", "Evidence Uploaded")
        self.close()


class Message_Box(QMainWindow):
    def __init__(self):
        super(Message_Box, self).__init__()

        uic.loadUi(r"Ui Files\Message_Box.ui", self)                                            # Load Message Box UI File

        self.message_icon = self.findChild(QLabel, "Message_Icon")                              # Message Icon
        self.message_label = self.findChild(QLabel, "Message_Label")                            # Message Label
        self.ok_btn = self.findChild(QPushButton, "OK_Button")                                  # OK Button

        self.ok_btn.setShortcut('Return')                                                       # Shortcut Key for OK Button
        self.ok_btn.clicked.connect(lambda: self.close())                                       # Close Window on OK button click

    def set_up(self, code, message):
        """Set-Up Message Icon and the Message"""

        if code == "Success":
            pixmap = QPixmap(r"Ui Files\Images\Success_Icon.png")

        else:
            pixmap = QPixmap(r"Ui Files\Images\Error_Icon.png")

        self.message_icon.setPixmap(pixmap)
        self.message_label.setText(message)


def Message(self, code, message):
    """Create Message Box Object and Display it"""

    self.message_box = Message_Box()
    self.message_box.set_up(code, message)
    self.message_box.show()
