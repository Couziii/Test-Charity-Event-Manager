import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from program.controller.controller import Controller

class UI_main_window(QMainWindow):
    signal_object = pyqtSignal()

    def __init__(self, parent=None, user_id=None,initial_tab_index=0):
        super(UI_main_window, self).__init__(parent)
        uic.loadUi("program/view/uifiles/main_page.ui", self)

        self.user_id = user_id
        self.controller= Controller()

        # accessing widgets
        # main window
        self.tab_widget = self.findChild(QTabWidget, "tab_main_window")
        self.btn_logout = self.findChild(QPushButton, "btn_logout")
        # account details tab
        self.btn_ad_change_user_id = self.findChild(QPushButton, "btn_ad_change_user_id")
        self.btn_ad_change_password = self.findChild(QPushButton, "btn_ad_change_password")
        self.btn_ad_withdraw_event = self.findChild(QPushButton, "btn_ad_withdraw_event")

        self.txt_ad_user_id = self.findChild(QLineEdit, "txt_ad_user_id")
        self.txt_ad_password = self.findChild(QLineEdit, "txt_ad_password")

        self.lbl_ad_unavailable_user_id = self.findChild(QLabel, "lbl_ad_unavailable_user_id")
        self.lbl_ad_unauthorized_password = self.findChild(QLabel, "lbl_ad_unauthorized_password")

        self.list_widget_ad_charities = self.findChild(QListWidget, "list_widget_ad_charities")
        self.list_widget_ad_events = self.findChild(QListWidget, "list_widget_ad_events")
        # main window tab

        # actions
        # main window
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        self.btn_logout.clicked.connect(self.btn_logout_clicked)
        # account details tab
        self.btn_ad_change_user_id.clicked.connect(self.btn_ad_change_user_id_clicked)
        self.btn_ad_change_password.clicked.connect(self.btn_ad_change_password_clicked)
        self.btn_ad_withdraw_event.clicked.connect(self.btn_ad_withdraw_event_clicked)
        # main window tab

        # when window open settings
        self.tab_widget.setCurrentIndex(initial_tab_index)

    def on_tab_changed(self, index):
        if index == 1:
            self.clear_account_detals_tab()

    def btn_logout_clicked(self):
        self.clear_account_detals_tab()
        self.signal_object.emit()
        self.close()

    def btn_ad_change_user_id_clicked(self):
        self.wrong_inputs = False
        self.check_input()
        if not self.wrong_inputs:
           pass
        
    def btn_ad_change_password_clicked(self):
        self.wrong_inputs = False
        self.check_input()
        if not self.wrong_inputs:
           pass
        
    def btn_ad_withdraw_event_clicked(self):
        pass

    def get_window_values(self):
        self.user_id = self.txt_ad_user_id.text()
        self.password = self.txt_ad_password.text()

    def check_input(self):
        self.get_window_values()
        forbidden_symbols = ["'", '"', ";", "--", "/*", "*/", "#"]
        if any(symbol in self.user_id for symbol in forbidden_symbols):
          self.lbl_ad_unavailable_user_id.setText("No injection symbols allowed")
          self.wrong_inputs = True
        elif any(symbol in self.password for symbol in forbidden_symbols):
          self.lbl_ad_unauthorized_password.setText("No injection symbols allowed")
          self.wrong_inputs = True
        elif self.controller.get_user_id(self.user_id):
          self.lbl_ad_unavailable_user_id.setText("User ID already exist")
          self.wrong_inputs = True
        elif self.user_id.strip() == "":
            self.lbl_ad_unavailable_user_id.setText("User ID must not be empty!")
            self.wrong_inputs = True
        elif self.password.strip() == "":
            self.lbl_ad_unauthorized_password.setText("Password must not be empty!")
            self.wrong_inputs = True
        
    def clear_account_detals_tab(self):
        self.txt_ad_user_id.clear()
        self.txt_ad_password.clear()
        self.lbl_ad_unavailable_user_id.setText("")
        self.lbl_ad_unauthorized_password.setText("")
        self.list_widget_ad_charities.clear()
        self.list_widget_ad_charities.clear()