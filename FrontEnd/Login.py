# Import Libraries
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLineEdit, QPushButton
from qt_material import apply_stylesheet
from Home import Home_Window
from SignUp import Register_Window
from BackEnd.Firebase_Operations import user_exists, get_data, generate_log
from SignUp import message_box
import sys


class Login_Window(QMainWindow):

    def __init__(self):
        """Load the Login Window and Extract the username, password and run validation"""

        super(Login_Window, self).__init__()                                            # Call the inherited classes __init__ method
        uic.loadUi('Ui Files\\Login_Window.ui', self)                                   # Load the .ui file

        self.username_field = self.findChild(QLineEdit, 'Username_Field')               # Username from Ui Files file
        self.password_field = self.findChild(QLineEdit, 'Password_Field')               # Password from Ui Files file

        login_button = self.findChild(QPushButton, 'Login_Button')                      # Login Button
        login_button.clicked.connect(self.login_validation)                             # Call login_validation on Button Press

        sign_up_btn = self.findChild(QPushButton, 'SignUp_Button')                      # Register Button
        sign_up_btn.clicked.connect(self.register)                                      # Call Register on Button Press

    def login_validation(self):
        """Validate the username and password"""
        username = self.username_field.text()                                           # Extract Username form the Field
        password = self.password_field.text()                                           # Extract Password form the Field

        if username == '' or password == '':                                            # If Either of Fields are Blank
            message_box("Error", "Please Fill all the Details.")                            # Display Error Message

        elif user_exists("Users", username):                                            # If username exists in the database
            if password == get_data(username, "Password"):                              # And Passwords Match as well
                generate_log(username, "Sign-in")                                           # Create a Log in database that a User has signed in
                home_window.username = username                                             # Passing Username to Home Window
                home_window.name_tag.setText(f"Welcome {username}")                         # Setting Name Tag of Home Window
                window_stack.setCurrentIndex(1)                                             # Changing Window to Home Window
                window_stack.resize(950, 550)                                               # Dimensions of Home Window
                window_stack.setWindowTitle("Home")                                         # Changing Title of Stack to Home

            else:                                                                       # If Password does not match in database
                message_box("Error", "Invalid Password")
        else:                                                                           # If Username doesn't Exist in the Database
            message_box("Error", "Username doesn't exist")

    @staticmethod
    def register():
        """Change the Current Window to Register Window"""
        window_stack.setCurrentIndex(2)                                                 # Changing Window to Register Window
        window_stack.setWindowTitle("SignUp")                                           # Changing Title of Stack to Signup
        window_stack.resize(720, 460)                                                   # Dimensions of Home Window


# Driver Code
if __name__ == "__main__":
    app = QApplication(sys.argv)                                                        # Main Application
    app.setWindowIcon(QtGui.QIcon("Ui Files\\Images\\Window_Icon"))                     # Setting Application Icon
    apply_stylesheet(app, theme='dark_amber.xml')                                       # Setting Theme of Application

    window_stack = QStackedWidget()                                                     # Window Stack Object for Switching between Windows
    login_window = Login_Window()                                                       # Login Window Object
    home_window = Home_Window(window_stack)                                             # Home Window Object
    register_window = Register_Window(window_stack)                                     # Register Window Object

    window_stack.setWindowTitle("Login")                                                # Setting Title of Stack to Home
    window_stack.resize(640, 240)                                                       # Dimensions of Login Window

    window_stack.addWidget(login_window)                                                # Adding Login Window to Window Stack
    window_stack.addWidget(home_window)                                                 # Adding Home Window to window stack
    window_stack.addWidget(register_window)                                             # Adding Register Window to Window Stack

    window_stack.show()                                                                 # Displaying the Window Stack

    sys.exit(app.exec_())
