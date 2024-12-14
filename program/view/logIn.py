import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from program.view.mainPage import UI_main_window
from program.view.signUp import UI_signup_window
from program.controller.controller import Controller


"""
UI_login_window: A class representing the login window of the application.

This class is responsible for managing the login functionality, including handling
user input, validating credentials, and transitioning to other windows within the
application. It uses PyQt5 for the graphical interface.

Attributes:
-----------
btn_login : QPushButton
    The button for triggering the login action.

txt_user_id : QLineEdit
    The text field for entering the user ID.

txt_password : QLineEdit
    The text field for entering the user password.

lbl_wrong_input : QLabel
    A label for displaying error messages related to user input or login failure.

lbl_signup : QLabel
    A clickable label for transitioning to the signup window.

controller : Controller
    A controller object for managing user authentication.

Methods:
--------
__init__(parent=None)
    Initializes the login window, connects signals to actions, and displays the UI.

btn_login_clicked()
    Handles the login button click, validates inputs, and transitions to the main window on success.

lbl_signup_clicked(event=None)
    Handles clicks on the signup label and transitions to the signup window.

get_window_values()
    Retrieves the values entered in the user ID and password fields.

check_input()
    Validates the user input for forbidden symbols and authenticates credentials.

clear_window()
    Clears all input fields and resets error messages.
"""
class UI_login_window(QMainWindow):
    def __init__(self, parent=None):
        super(UI_login_window, self).__init__(parent)
        uic.loadUi("program/view/uifiles/login_page.ui", self)
        # uic.loadUi(os.path.join(os.path.dirname(__file__), "uiFiles", "login_page.ui"), self)

        # For unit testing, the path is different
        # uic.loadUi("uiFiles/login_page.ui", self)

        # For unit tests
        self.wrong_inputs = False

        self.controller = Controller()

        # accessing widgets
        self.btn_login = self.findChild(QPushButton, "btn_login")

        self.txt_user_id = self.findChild(QLineEdit, "txt_user_id")
        self.txt_password = self.findChild(QLineEdit, "txt_password")

        self.lbl_wrong_input = self.findChild(QLabel, "lbl_wrong_input")
        self.lbl_signup = self.findChild(QLabel, "lbl_signup")

        # actions
        self.btn_login.clicked.connect(self.btn_login_clicked)

        # Make lbl_signup clickable
        self.lbl_signup.mousePressEvent = self.lbl_signup_clicked

        self.show()

    def btn_login_clicked(self):
        self.user_id = self.txt_user_id.text()# this line will be deleted
        self.wrong_inputs = False
        self.check_input()
        if not self.wrong_inputs:
            self.UI_main_window = UI_main_window(self, self.user_id)
            self.UI_main_window.signal_object.connect(self.show)
            self.clear_window()
            self.close()
            self.UI_main_window.show()

        

    def lbl_signup_clicked(self, event=None): # Accept event for mousePressEvent
        self.UI_singup_window = UI_signup_window(self)
        self.UI_singup_window.signal_object.connect(self.show)
        self.clear_window()
        self.close()
        self.UI_singup_window.show()

    def get_window_values(self):
        self.user_id = self.txt_user_id.text()
        self.password = self.txt_password.text()

    def check_input(self):
        self.get_window_values()
        forbidden_symbols = ["'", '"', ";", "--", "/*", "*/", "#"]
        if any(symbol in self.user_id for symbol in forbidden_symbols):
            self.lbl_wrong_input.setText("No injection symbols allowed")
            self.wrong_inputs = True
        elif any(symbol in self.password for symbol in forbidden_symbols):
            self.lbl_wrong_input.setText("No injection symbols allowed")
            self.wrong_inputs = True
        if not self.controller.authenticate_user(self.user_id, self.password):
            self.lbl_wrong_input.setText("Wrong credentials")
            self.wrong_inputs = True

    def clear_window(self):
        self.txt_user_id.clear()
        self.txt_password.clear()
        self.lbl_wrong_input.setText("")