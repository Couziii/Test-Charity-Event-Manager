import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from program.controller.controller import Controller
from datetime import datetime

"""
UI_main_window Class

This class represents the main window of a PyQt-based application. It manages the user interface 
elements and provides the logic for user interactions, such as managing account details, logging out, 
and switching tabs. The class is initialized with user-specific data and supports dynamic UI updates.

Attributes:
-----------

signal_object : pyqtSignal
    Signal emitted when the user logs out of the application.

user_id : str
    The ID of the current user logged into the application.

controller : Controller
    Instance of a `Controller` class to handle backend operations like changing passwords, 
    updating user IDs, and removing accounts.

tab_widget : QTabWidget
    Reference to the tab widget controlling the main window tabs.

btn_logout : QPushButton
    Button to log out of the application.


Account details tab widgets:
----------------------------

btn_ad_change_user_id : QPushButton
    Button to enable user ID editing.

btn_ad_change_password : QPushButton
    Button to enable password editing.

btn_ad_cancel_changes : QPushButton
    Button to cancel account detail changes.

btn_ad_confirm_changes : QPushButton
    Button to confirm account detail changes.

btn_ad_withdraw_event : QPushButton
    Button to withdraw from an event.

btn_ad_remove_account : QPushButton
    Button to remove the current user account.

txt_ad_user_id : QLineEdit
    Text input field for user ID.

txt_ad_password : QLineEdit
    Text input field for password.

lbl_ad_unavailable_user_id : QLabel
    Label displaying messages related to invalid or unavailable user IDs.

lbl_ad_unauthorized_password : QLabel
    Label displaying messages related to invalid passwords.

list_widget_ad_charities : QListWidget
    List widget displaying user-associated charities.

list_widget_ad_events : QListWidget
    List widget displaying user-associated events.


Methods:
--------

__init__(self, parent=None, user_id=None, initial_tab_index=0):
    Initializes the main window and connects the UI elements with their respective actions.

on_tab_changed(self, index):
    Callback function executed when the current tab is changed.

btn_logout_clicked(self):
    Handles the logout process and emits the logout signal.

reset_account_detail_tab(self):
    Resets the account details tab to its initial state.

btn_ad_change_user_id_clicked(self):
    Enables user ID editing and disables password editing.

btn_ad_change_password_clicked(self):
    Enables password editing and disables user ID editing.

btn_ad_cancel_changes_clicked(self):
    Cancels any changes made to the account details and resets the tab.

btn_ad_confirm_changes_clicked(self):
    Validates and confirms changes to the user ID or password, and triggers the logout process.

update_withdraw_button_state(self):
    Sets the withdraw button enabled/disabled depending on user interaction with the program.

btn_ad_withdraw_event_clicked(self):
    Withdraws the logged in users enrollment from the selected event.

btn_ad_remove_account_clicked(self):
    Removes the current user's account and triggers the logout process.

get_window_values(self):
    Retrieves the current values from the account details tab's input fields.

check_input(self):
    Validates user input for user ID and password, checking for empty fields and forbidden symbols.

clear_account_detals_tab(self):
    Clears all fields and messages in the account details tab.

load_charities(self):
    Fetches the names of the charity companies the user has enrolled to.

charity_name_selected(self, item):
    Displays the events of the charity that the user selected in the charities list.

get_enrolled_events_by_company(self, company_name, enrolled_events):
    Supplies the events of a specific company to the charity_name_selected method. 

load_events(self):
    Gets all charity events saved in the database.

add_event_to_main(self, event_data):
    Creates a list widget for each event and displays them in the main window.

"""


class UI_main_window(QMainWindow):

    signal_object = pyqtSignal()

    def __init__(self, parent=None, user_id=None, initial_tab_index=0):

        super(UI_main_window, self).__init__(parent)

        # uic.loadUi("program/view/uifiles/main_page.ui", self)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "uiFiles", "main_page.ui"), self)

        self.user_id = user_id

        self.controller= Controller()

        # accessing widgets

        # main window

        self.tab_widget = self.findChild(QTabWidget, "tab_main_window")

        self.btn_logout = self.findChild(QPushButton, "btn_logout")

        self.event_list_area = self.findChild(QListWidget, "event_list_area")

        self.load_events() # Loading events to the event list
        

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

        self.list_widget_ad_events.itemSelectionChanged.connect(self.update_withdraw_button_state)
        self.load_charities()

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

        self.list_widget_ad_charities.itemClicked.connect(self.charity_name_selected)

        # main window tab


        # when window open settings
        self.reset_account_detail_tab()

        self.tab_widget.setCurrentIndex(initial_tab_index)


    ####### CLASS METHODS #######


    def on_tab_changed(self, index):

        if index == 1:
            self.load_charities()
        else:
            pass


    def btn_logout_clicked(self):

        self.clear_account_detals_tab()

        self.signal_object.emit()
        
        self.close()


    ##### ACCOUNT DETAILS METHODS #####

    def reset_account_detail_tab(self):

        self.change_user_id_clicked = False

        self.change_password_clicked = False

        self.txt_ad_user_id.setText(self.user_id)

        self.txt_ad_user_id.setEnabled(False)

        self.txt_ad_password.setText(self.controller.get_password(self.user_id))

        self.txt_ad_password.setEnabled(False)

        self.btn_ad_confirm_changes.setEnabled(False)

        self.btn_ad_withdraw_event.setEnabled(False)


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
    

    def update_withdraw_button_state(self):

        if self.list_widget_ad_events.currentItem():
            self.btn_ad_withdraw_event.setEnabled(True)

        else:
            self.btn_ad_withdraw_event.setEnabled(False)
        

    def btn_ad_withdraw_event_clicked(self):

        selected_event = self.list_widget_ad_events.currentItem()

        if not selected_event:
            return

        event_id = selected_event.data(Qt.UserRole)

        success = self.controller.unenroll(event_id, self.user_id)

        if success:
            selected_charity = self.list_widget_ad_charities.currentItem()

            if selected_charity:
                self.charity_name_selected(selected_charity.text())

            self.load_events()
            self.load_charities()
        
        self.update_withdraw_button_state()


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

        self.list_widget_ad_events.clear()
    

    def load_charities(self):

        company_names = []
        
        enrolled_events_data = self.controller.get_enrolled_events(self.user_id)
        
        if isinstance(enrolled_events_data, dict):
            enrolled_events = enrolled_events_data.get('enrolled_events', [])

        elif isinstance(enrolled_events_data, list):
            enrolled_events = enrolled_events_data

        else:
            return

        for event_id in enrolled_events:
            company_data = self.controller.get_company_name(event_id)
            company_name = company_data.get('company_name', '')

            if company_name not in company_names:
                company_names.append(company_name)

        self.list_widget_ad_charities.clear()

        for name in company_names:
            self.list_widget_ad_charities.addItem(name)
    


    def charity_name_selected(self, item):

        if isinstance(item, str):
            company_name = item

        else:
            company_name = item.text()

        enrolled_events_data = self.controller.get_enrolled_events(self.user_id)

        if isinstance(enrolled_events_data, dict):
            enrolled_events = enrolled_events_data.get('enrolled_events', [])

        elif isinstance(enrolled_events_data, list):
            enrolled_events = enrolled_events_data

        else:
            return

        events_by_company = self.get_enrolled_events_by_company(company_name, enrolled_events)

        self.list_widget_ad_events.clear()

        for event in events_by_company:
            item = QListWidgetItem(event['name'])
            item.setData(Qt.UserRole, event['event_id'])  # Store event id for btn_ad_withdraw_event_clicked()
            self.list_widget_ad_events.addItem(item)


    def get_enrolled_events_by_company(self, company_name, enrolled_events):

        events_by_company = []

        for event_id in enrolled_events:
            event_data = self.controller.get_company_name(event_id)

            if event_data:
                name = event_data.get('company_name', '')

                if name == company_name:
                    events_by_company.append(event_data)
        
        return events_by_company


    ##### MAIN WINDOW METHODS ######


    def load_events(self):

        self.event_list_area.clear()

        events = self.controller.get_events()

        for event_data in events:
            self.add_event_to_main(event_data)


    def add_event_to_main(self, event_data):

        if not event_data:
            return
        
        enrolled_events = self.controller.get_enrolled_events(self.user_id)

        event_widget = List_item_widget(event_data, self.user_id, self.controller, enrolled_events)

        list_item = QListWidgetItem(self.event_list_area)

        custom_height = event_widget.sizeHint().height() + 400

        list_item.setSizeHint(QSize(self.event_list_area.width(), custom_height))

        self.event_list_area.addItem(list_item)

        self.event_list_area.setItemWidget(list_item, event_widget)


class List_item_widget(QWidget):

    def __init__(self, data, user_id, controller, enrolled_events, parent=None):

        super(List_item_widget, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "uiFiles", "event_list_item.ui"), self)

        self.user_id = user_id

        self.controller = controller


        self.event_widget = self.findChild(QWidget, "event_widget")

        self.date_lbl = self.findChild(QLabel, "date_label")

        self.address_lbl = self.findChild(QLabel, "address_label")

        self.company_name_lbl = self.findChild(QLabel, "company_name_label")

        self.event_name_lbl = self.findChild(QLabel, "event_name_label")

        self.short_desc_lbl = self.findChild(QLabel, "short_description_label")

        self.desc_lbl = self.findChild(QLabel, "description_label")

        self.enroll_btn = self.findChild(QPushButton, "enroll_button")


        formatted_date = self.format_event_date(data["date"])
        self.date_lbl.setText(formatted_date)

        self.company_name_lbl.setText(data.get("company_name", ""))

        self.address_lbl.setText(data.get("address", ""))

        self.event_name_lbl.setText(data.get("name", ""))

        self.short_desc_lbl.setText(data.get("short_description", ""))

        self.desc_lbl.setText(data.get("description", ""))

        if data["event_id"] in enrolled_events:
            self.enroll_btn.setEnabled(False)
            self.enroll_btn.setText('Enrolled')
            self.event_widget.setStyleSheet('background:lightgreen;')

        self.enroll_btn.clicked.connect(lambda: self.enroll(data))
    

    def enroll(self, data):

        event_id = data.get("event_id")

        if not event_id:
            print('Invalid event id')
            return

        if not self.user_id:
            print('Invalid user id')
            return
    
        success = self.controller.register_enrollment(event_id, self.user_id)

        if success:
            self.enroll_btn.setEnabled(False) # Disable enroll button (avoid multiple enrollments)
            self.enroll_btn.setText("Enrolled")
            self.event_widget.setStyleSheet('background:lightgreen;')

            if hasattr(self.controller, 'main_window'):
                self.controller.main_window.load_charities()
    

    def format_event_date(self, date_str):

        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

        return date_obj.strftime("%A %d.%m.%Y")
