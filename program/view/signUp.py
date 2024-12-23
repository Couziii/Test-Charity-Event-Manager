import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from program.controller.controller import Controller


"""
UI_signup_window
================

This class defines a signup window for a PyQt application, designed to facilitate user registration with validation and appropriate error handling.

Attributes
----------
signal_object : pyqtSignal
    A custom PyQt signal that is emitted when the signup or cancel button is clicked.

controller : Controller
    An instance of the `Controller` class used for managing user-related operations.

btn_cancel : QPushButton
    A button to cancel the signup process and close the window.

btn_signup : QPushButton
    A button to initiate the signup process.

txt_user_id : QLineEdit
    A text input field for entering the user's ID.

txt_password : QLineEdit
    A text input field for entering the user's password.

txt_admin_code : QLineEdit
    A text input field for entering an admin code (if applicable).

lbl_unavailable_user_id : QLabel
    A label to display messages about invalid or unavailable user IDs.

lbl_unauthorized_password : QLabel
    A label to display messages about invalid passwords.

lbl_wrong_admin_code : QLabel
    A label to display messages about incorrect admin codes.

wrong_inputs : bool
    A flag indicating whether the user input is valid or contains errors.

Methods
-------
__init__(parent=None)
    Initializes the UI_signup_window instance, loads the UI file, and connects buttons to their respective slots.

btn_cancel_clicked()
    Handles the behavior when the cancel button is clicked. Clears input fields, emits the signal, and closes the window.

btn_signup_clicked()
    Handles the behavior when the signup button is clicked. Validates input, inserts a new user into the database if valid, and closes the window.

get_window_values()
    Retrieves the current values from the input fields and stores them in class attributes.

check_input()
    Validates user input to prevent SQL injection, checks for required fields, and verifies the uniqueness of the user ID and correctness of the admin code.

clear_window()
    Clears all input fields and resets error labels.
"""
class UI_signup_window(QMainWindow):
  signal_object = pyqtSignal()

  def __init__(self, parent=None):
    super(UI_signup_window, self).__init__(parent)
    uic.loadUi("program/view/uifiles/signup_page.ui", self)
    # uic.loadUi(os.path.join(os.path.dirname(__file__), "uiFiles", "signup_page.ui"), self)

    # For unit testing, the path is different
    # uic.loadUi("uiFiles/signup_page.ui", self)

    # For unit tests
    self.wrong_inputs = False

    self.controller = Controller()
    # accessing widgets
    self.btn_cancel = self.findChild(QPushButton, "btn_cancel")
    self.btn_signup = self.findChild(QPushButton, "btn_signup")

    self.txt_user_id = self.findChild(QLineEdit, "txt_user_id")
    self.txt_password = self.findChild(QLineEdit, "txt_password")
    self.txt_admin_code = self.findChild(QLineEdit, "txt_admin_code")

    self.lbl_unavailable_user_id = self.findChild(QLabel, "lbl_unavailable_user_id")
    self.lbl_unauthorized_password = self.findChild(QLabel, "lbl_unauthorized_password")
    self.lbl_wrong_admin_code = self.findChild(QLabel, "lbl_wrong_admin_code")
    # actions
    self.btn_cancel.clicked.connect(self.btn_cancel_clicked)
    self.btn_signup.clicked.connect(self.btn_signup_clicked)
    # when window open settings

  def btn_cancel_clicked(self):
    self.clear_window()
    self.signal_object.emit()
    self.close()

  def btn_signup_clicked(self):
    self.wrong_inputs = False
    self.check_input()
    if not self.wrong_inputs:
      if self.admin_code.strip() != "":
        self.controller.insert_new_user(self.user_id, self.password, self.admin_code)
      else:
        self.controller.insert_new_user(self.user_id, self.password)
      self.clear_window()
      self.signal_object.emit()
      self.close()

  def get_window_values(self):
    self.user_id = self.txt_user_id.text()
    self.password = self.txt_password.text()
    self.admin_code = self.txt_admin_code.text()

  def check_input(self):
      self.get_window_values()
      forbidden_symbols = ["'", '"', ";", "--", "/*", "*/", "#"]
      if any(symbol in self.user_id for symbol in forbidden_symbols):
        self.lbl_unavailable_user_id.setText("No injection symbols allowed")
        self.wrong_inputs = True
      if any(symbol in self.password for symbol in forbidden_symbols):
        self.lbl_unauthorized_password.setText("No injection symbols allowed")
        self.wrong_inputs = True
      if any(symbol in self.admin_code for symbol in forbidden_symbols):
        self.lbl_wrong_admin_code.setText("No injection symbols allowed")
        self.wrong_inputs = True
      if self.controller.get_user_id(self.user_id) is not None:
        self.lbl_unavailable_user_id.setText("User ID already exist")
        self.wrong_inputs = True
      if self.user_id.strip() == "":
        self.lbl_unavailable_user_id.setText("User ID must not be empty!")
        self.wrong_inputs = True
      if self.password.strip() == "":
        self.lbl_unauthorized_password.setText("Password must not be empty!")
        self.wrong_inputs = True
      if self.admin_code.strip() != "":
        if not self.controller.check_admin_code(self.admin_code):
          self.lbl_wrong_admin_code.setText("Wrong admin code")
          self.wrong_inputs = True
      

  def clear_window(self):
    self.txt_user_id.clear()
    self.txt_password.clear()
    self.txt_admin_code.clear()
    self.lbl_unavailable_user_id.setText("")
    self.lbl_unauthorized_password.setText("")
    self.lbl_wrong_admin_code.setText("")