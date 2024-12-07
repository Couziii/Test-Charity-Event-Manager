import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from program.controller.controller import Controller

class UI_main_window(QMainWindow):
    signal_object = pyqtSignal()

    def __init__(self, parent=None, user_id=None, initial_tab_index=0):
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
        self.btn_ad_cancel_changes = self.findChild(QPushButton, "btn_ad_cancel_changes")
        self.btn_ad_confirm_changes = self.findChild(QPushButton, "btn_ad_confirm_changes")
        self.btn_ad_withdraw_event = self.findChild(QPushButton, "btn_ad_withdraw_event")
        self.btn_ad_remove_account = self.findChild(QPushButton, "btn_ad_remove_account")

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
        self.btn_ad_cancel_changes.clicked.connect(self.btn_ad_cancel_changes_clicked)
        self.btn_ad_confirm_changes.clicked.connect(self.btn_ad_confirm_changes_clicked)
        self.btn_ad_remove_account.clicked.connect(self.btn_ad_remove_account_clicked)
        # main window tab

        # when window open settings
        self.reset_account_detail_tab()
        self.tab_widget.setCurrentIndex(initial_tab_index)

    def reset_account_detail_tab(self):
        self.change_user_id_clicked = False
        self.change_password_clicked = False
        self.txt_ad_user_id.setText(self.user_id)
        self.txt_ad_user_id.setEnabled(False)
        self.txt_ad_password.setText(self.controller.get_password(self.user_id))
        self.txt_ad_password.setEnabled(False)
        self.btn_ad_confirm_changes.setEnabled(False)

    def on_tab_changed(self, index):
        if index == 1:
            pass
        else:
            pass

    def btn_logout_clicked(self):
        self.clear_account_detals_tab()
        self.signal_object.emit()
        self.close()

    def btn_ad_change_user_id_clicked(self):
        self.change_user_id_clicked = True
        self.txt_ad_user_id.setEnabled(True)
        self.btn_ad_change_password.setEnabled(False)
        self.btn_ad_confirm_changes.setEnabled(True)
        
    def btn_ad_change_password_clicked(self):
        self.change_password_clicked = True
        self.txt_ad_password.setEnabled(True)
        self.btn_ad_change_user_id.setEnabled(False)
        self.btn_ad_confirm_changes.setEnabled(True)

        self.wrong_inputs = False
        self.check_input()
        if not self.wrong_inputs:
           self.controller.change_password(self. user_id, self.password)
           self.btn_logout_clicked()

    def btn_ad_cancel_changes_clicked(self):
        self.reset_account_detail_tab()

    def btn_ad_confirm_changes_clicked(self):
        if self.change_user_id_clicked:
            self.wrong_inputs = False
            self.check_input()
            if not self.wrong_inputs:
                self.controller.change_user_id(self.user_id, self.user_id_new)
                self.btn_logout_clicked()
        elif self.change_password_clicked:
            self.wrong_inputs = False
            self.check_input()
            if not self.wrong_inputs:
               self.controller.change_password(self. user_id, self.password)
               self.btn_logout_clicked()
        
    def btn_ad_withdraw_event_clicked(self):
        pass

    def btn_ad_remove_account_clicked(self):
        self.controller.remove_account(self.user_id)
        self.btn_logout_clicked()

    def get_window_values(self):
        self.user_id_new = self.txt_ad_user_id.text()
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
        elif self.controller.get_user_id(self.user_id_new):
          self.lbl_ad_unavailable_user_id.setText("User ID already exist")
          self.wrong_inputs = True
        elif self.user_id_new.strip() == "":
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