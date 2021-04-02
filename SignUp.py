from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QMessageBox
from Firebase_Operations import push_user_to_database


def message_box(code, message):
    msgBox = QMessageBox()
    msgBox.setWindowIcon((QtGui.QIcon('UI/Images/Window_Icon.png')))
    msgBox.setText(message)
    msgBox.setWindowTitle("QMessageBox Example")
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()


class Register_Window(QtWidgets.QMainWindow):
    def __init__(self, window_stack, login_window):
        """Load SignUp UI and Extract all the user data"""
        super(Register_Window, self).__init__()

        uic.loadUi('UI\\SignUp_Window.ui', self)
        self.show()

        self.window_stack = window_stack
        self.login_window = login_window

        self.first_name = self.findChild(QtWidgets.QLineEdit, 'First_Name_Field')
        self.last_name = self.findChild(QtWidgets.QLineEdit, 'Last_Name_Field')
        self.email = self.findChild(QtWidgets.QLineEdit, 'Email_Field')
        self.contact = self.findChild(QtWidgets.QLineEdit, 'Contact_Field')
        self.username = self.findChild(QtWidgets.QLineEdit, 'Username_Field')
        self.password = self.findChild(QtWidgets.QLineEdit, 'Password_Field')
        self.con_password = self.findChild(QtWidgets.QLineEdit, 'Confirm_Pass_Field')

        self.register_btn = self.findChild(QtWidgets.QPushButton, 'Register_Button')
        self.clear_btn = self.findChild(QtWidgets.QPushButton, 'Clear_Button')
        self.exit_btn = self.findChild(QtWidgets.QPushButton, 'Exit_Button')

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
        self.window_stack.setFixedWidth(620)  # Width of Login Window
        self.window_stack.setFixedHeight(285)  # Height of Login Window
        self.window_stack.setCurrentWidget(self.login_window)  # Adding Login Window to Window Stack
