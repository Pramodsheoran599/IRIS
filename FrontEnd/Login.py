# Import Libraries
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton

from BackEnd.Firebase_Operations import user_exists, get_user_data, generate_log
from Alerts_and_Messages import Message


class Login_Window(QMainWindow):

    def __init__(self, window_stack = None, home_window = None):
        """Load the Login Window and Extract the username, password and run validation"""

        super(Login_Window, self).__init__()
        uic.loadUi(r'Ui Files\Login_Window.ui', self)                                   # Load the .ui file

        self.home_window = home_window
        self.window_stack = window_stack
        self.username_field = self.findChild(QLineEdit, 'Username_Field')               # Username Field
        self.password_field = self.findChild(QLineEdit, 'Password_Field')               # Password Field

        login_button = self.findChild(QPushButton, 'Login_Button')                      # Login Button
        login_button.setShortcut('Return')                                              # Shortcut Key for Login Button
        login_button.clicked.connect(self.login_validation)                             # Call login_validation on Button Press

        sign_up_btn = self.findChild(QPushButton, 'SignUp_Button')                      # Register Button
        sign_up_btn.clicked.connect(self.register)                                      # Call Register on Button Press

    def login_validation(self):
        """Validate the username and password"""
        username = self.username_field.text()                                           # Extract Username form the Field
        password = self.password_field.text()                                           # Extract Password form the Field

        if username == '' or password == '':                                            # If Either of Fields are Blank
            Message(self, "Error", "Please Fill all the Details.")                            # Display Error Message

        elif user_exists(username):                                                     # If username exists in the database
            if password == get_user_data(username, "Password"):                               # And Passwords Match as well
                generate_log(username, "Sign-in")                                             # Create a Log in database that a User has signed in

                self.home_window.username = username                                          # Passing Username to Home Window
                self.home_window.name_tag.setText(f"Welcome {username}")                      # Setting Name Tag of Home Window
                self.window_stack.setCurrentIndex(1)                                          # Changing Window to Home Window
                self.window_stack.resize(950, 550)                                            # Dimensions of Home Window
                self.window_stack.setWindowTitle("Home")                                      # Changing Title of Stack to Home

            else:                                                                       # If Password does not match in database
                Message(self, "Error", "Invalid Password")
        else:                                                                           # If Username doesn't Exist in the Database
            Message(self, "Error", "Username Does not Exist.")

    def register(self):
        """Change the Current Window to Register Window"""
        self.window_stack.setCurrentIndex(2)                                            # Changing Window to Register Window
        self.window_stack.setWindowTitle("SignUp")                                      # Changing Title of Stack to Signup
        self.window_stack.resize(720, 460)                                              # Dimensions of Home Window


# Testing Code
if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_window = Login_Window()
    login_window.show()

    sys.exit(app.exec_())
