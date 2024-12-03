import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from program.view.mainPage import UI_main_window
from program.view.signUp import UI_signup_window
from program.controller.controller import Controller


class UI_login_window(QMainWindow):

    def __init__(self, parent=None):
        super(UI_login_window, self).__init__(parent)
        uic.loadUi("program/view/uifiles/login_page.ui", self)

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

        # when window open settings
        self.lbl_signup.setTextFormat(Qt.RichText)  # Enables rich text, like HTML
        self.lbl_signup.setOpenExternalLinks(False)  # Keeps click handling within the application
        self.lbl_signup.setStyleSheet("""
        QLabel {
            color: blue; 
            text-decoration: underline;  /* Makes it look like a hyperlink */
        }
        QLabel:hover {
            color: darkblue;  /* Changes the color when hovering */
        }
        """)

        # Set the cursor to a pointing hand cursor
        self.lbl_signup.setCursor(Qt.PointingHandCursor)

        self.show()

    def btn_login_clicked(self):
        self.user_id = self.txt_user_id.text()# this line will be deleted
        # self.wrong_inputs = False
        # self.check_input()
        # if not self.wrong_inputs:
        self.UI_main_window = UI_main_window(self, self.user_id)
        self.UI_main_window.signal_object.connect(self.show)
        self.clear_window()
        self.close()
        self.UI_main_window.show()

        

    def lbl_signup_clicked(self, event=None): # Accept event for mousePressEvent
        self.UI_main_window = UI_signup_window(self)
        self.UI_main_window.signal_object.connect(self.show)
        self.clear_window()
        self.close()
        self.UI_main_window.show()

    def get_window_values(self):
        self.user_id = self.txt_user_id.text()
        self.password = self.txt_password.text()

    def check_input(self):
        self.get_window_values()
        if not self.controller.authenticate_user(self.user_id, self.password):
            self.lbl_wrong_input.setText("Wrong credentials")
            self.wrong_inputs = True

    def clear_window(self):
        self.txt_user_id.clear()
        self.txt_password.clear()
        self.lbl_wrong_input.setText("")