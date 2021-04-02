# Import Libraries
from PyQt5 import QtWidgets, uic, QtGui
from Home import Home_Window
from SignUp import Register_Window
from qt_material import apply_stylesheet
from Firebase_Operations import user_exists, get_data
from SignUp import message_box
import sys


class Login_Window(QtWidgets.QMainWindow):

    def __init__(self):
        """Load the Login Window and Extract the username, password and run validation"""

        super(Login_Window, self).__init__()                                            # Call the inherited classes __init__ method

        uic.loadUi('UI\\Login_Window.ui', self)                                         # Load the .ui file
        self.setWindowIcon((QtGui.QIcon('UI/Images/Window_Icon.png')))
        self.show()                                                                     # Show the GUI

        self.username_field = self.findChild(QtWidgets.QLineEdit, 'Username_Field')     # Username from UI file
        self.password_field = self.findChild(QtWidgets.QLineEdit, 'Password_Field')     # Password from UI file
        self.invalid_label = self.findChild(QtWidgets.QLabel, 'Invalid_Label')          # Invalid Details Label
        self.invalid_label.setVisible(False)                                            # By Default Hidden

        login_button = self.findChild(QtWidgets.QPushButton, 'Login_Button')            # Login Button
        login_button.clicked.connect(self.login_validation)                             # Call login_validation on Button Press

        register_btn = self.findChild(QtWidgets.QPushButton, 'Register_Button')         # Register Button
        register_btn.clicked.connect(self.register)                                     # Call Register on Button Press

    def login_validation(self):
        """Validate the username and password"""
        username = self.username_field.text()                                           # Extract Username form the Field
        password = self.password_field.text()                                           # Extract Password form the Field

        if username == '' or password == '':                                            # If Either of Fields are Blank
            message_box("Error", "Please Fill all the Details.")                            # Display Error Message

        elif user_exists("Users", username):                                            # If username exists in the database
            if password == get_data(username, "Password"):                              # And Passwords Match as well
                window_stack.setCurrentWidget(home_window)                                  # Changing Window to Home Window
                window_stack.setFixedWidth(950)                                             # Width of Home Window
                window_stack.setFixedHeight(550)                                            # Height of Home Window
                window_stack.setWindowTitle("Home")                                         # Changing Title of Stack to Home

            else:                                                                       # If Password does not match in database
                message_box("Error", "Invalid Password")

        else:                                                                           # If Username doesn't Exist in the Database
            message_box("Error", "Username doesn't exist")

    @staticmethod
    def register():
        window_stack.setCurrentWidget(register_window)                                  # Changing Window to Register Window
        window_stack.setWindowTitle("SignUp")                                           # Changing Title of Stack to Signup
        window_stack.setFixedWidth(720)                                                 # Width of Register Window
        window_stack.setFixedHeight(460)                                                # Height of Register Window


# Driver Code
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)                                              # Main Application
    app.setWindowIcon(QtGui.QIcon("UI\\Images\\Window_Icon"))                           # Setting Application Icon
    apply_stylesheet(app, theme='dark_amber.xml')                                       # Setting Theme of Application

    window_stack = QtWidgets.QStackedWidget()                                           # Window Stack Object for Switching between Windows
    login_window = Login_Window()                                                       # Login Window Object
    home_window = Home_Window(window_stack, login_window)                               # Home Window Object
    register_window = Register_Window(window_stack, login_window)                       # Register Window Object

    window_stack.setWindowTitle("Login")                                                # Setting Title of Stack to Home
    window_stack.setFixedWidth(620)                                                     # Width of Login Window
    window_stack.setFixedHeight(285)                                                    # Height of Login Window

    window_stack.addWidget(login_window)                                                # Adding Login Window to Window Stack
    window_stack.addWidget(home_window)                                                 # Adding Home Window to window stack
    window_stack.addWidget(register_window)                                             # Adding Register Window to Window Stack

    window_stack.show()                                                                 # Displaying the Window Stack

    sys.exit(app.exec_())
