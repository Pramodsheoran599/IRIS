# Importing Libraries
import sys

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, QLineEdit, QPushButton

from BackEnd.Firebase_Operations import push_user_to_database


def message_box(code, message):
    msg_box = QMessageBox()
    msg_box.setWindowIcon((QtGui.QIcon(r'Ui Files\Images\Window_Icon.png')))
    msg_box.setText(message)
    msg_box.setWindowTitle("QMessageBox Example")
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()


class SignUp_Window(QMainWindow):
    def __init__(self, window_stack = None):
        """Load SignUp Ui Files and Extract all the user data"""
        super(SignUp_Window, self).__init__()

        uic.loadUi(r'Ui Files\SignUp_Window.ui', self)

        self.window_stack = window_stack

        self.first_name = self.findChild(QLineEdit, 'First_Name_Field')
        self.last_name = self.findChild(QLineEdit, 'Last_Name_Field')
        self.email = self.findChild(QLineEdit, 'Email_Field')
        self.contact = self.findChild(QLineEdit, 'Contact_Field')
        self.username = self.findChild(QLineEdit, 'Username_Field')
        self.password = self.findChild(QLineEdit, 'Password_Field')
        self.con_password = self.findChild(QLineEdit, 'Confirm_Pass_Field')

        self.register_btn = self.findChild(QPushButton, 'Register_Button')
        self.clear_btn = self.findChild(QPushButton, 'Clear_Button')
        self.exit_btn = self.findChild(QPushButton, 'Exit_Button')

        self.register_btn.clicked.connect(self.validation)
        self.clear_btn.clicked.connect(self.clear_fields)
        self.exit_btn.clicked.connect(self.exit)

    def validation(self):

        new_user = {
            "Username": self.username.text(),
            "Password": self.password.text(),
            "First Name": self.first_name.text(),
            "Last Name": self.last_name.text(),
            "Email ID": self.email.text(),
            "Contact": self.contact.text()
        }

        if "" in new_user.values():
            message_box("Error", "Please Fill All the Details")

        elif self.password.text() == self.con_password.text():
            if push_user_to_database(new_user):
                message_box("Success", "You Have Successfully Registered with the IRIS System.")
            else:
                message_box("Error", "You are Already Registered with the IRIS System.")

        else:
            message_box("Error", "Passwords Do not Match.")

    def clear_fields(self):
        self.first_name.clear()
        self.last_name.clear()
        self.email.clear()
        self.contact.clear()
        self.username.clear()
        self.password.clear()
        self.con_password.clear()

    def exit(self):
        self.window_stack.setWindowTitle("Login")  # Setting Title of Stack to Home
        self.window_stack.resize(640, 240)
        self.window_stack.setCurrentIndex(0)  # Adding Login Window to Window Stack


if __name__ == "__main__":
    app = QApplication(sys.argv)

    signup_window = SignUp_Window()
    signup_window.show()

    sys.exit(app.exec_())
