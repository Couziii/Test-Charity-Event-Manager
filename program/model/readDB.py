import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pyrebase


"""
A class to interact with a Firebase Realtime Database, providing methods to retrieve user information,
authenticate users and admins, and manage database queries.
Attributes:
    database: A reference to the Firebase Realtime Database.
Methods:
    get_user_id(user_id):
        Retrieves the user ID and associated information from the database if the user exists.
    
    get_password(user_id):
        Retrieves the password for the specified user ID if the user exists in the database.
    
    authenticate_admin_code(admin_code):
        Authenticates an admin code against the database records.
    
    authenticate_user(user_id, password):
        Authenticates a user by verifying the provided user ID and password.
"""
class Read_db:
    """
    Initializes the Read_db class by configuring and connecting to the Firebase Realtime Database.
    """
    def __init__(self):
        config = {"apiKey": "AIzaSyCzDvjQ_CaezICzS9i0tug_1bXD8qm5HaY",
                    "authDomain": "charityeventapp.firebaseapp.com",
                    "projectId": "charityeventapp",
                    "databaseURL":"https://charityeventapp-default-rtdb.europe-west1.firebasedatabase.app/",
                    "storageBucket": "charityeventapp.firebasestorage.app",
                    "messagingSenderId": "868261173430",
                    "appId": "1:868261173430:web:70433df0ed2d2cf6eeae17",
                    "measurementId": "G-SZDLQ2851E"}
        firebase = pyrebase.initialize_app(config)
        self.database = firebase.database()

    """
    Retrieves the user ID and associated information from the database.
    Args:
        user_id (str): The unique ID of the user to be retrieved.
    Returns:
        tuple: A tuple containing the user ID and associated information if the user exists.
        None: If the user ID does not exist in the database.
    """

    def get_user_id(self, user_id):

        users = self.database.child("Users").get()
        if users.val() is not None:  # Check if there are any users in the database
            for uid, user_info in users.val().items():
                if uid == user_id:  # Compare with the correct variable
                    return uid, user_info
        return None  # Return None if user_id is not found
    
    """
    Retrieves all events in the database collection Events.
    """
    def get_events(self):
        events = self.database.child("Events").get()
        if events.val() is not None:
            # Remove the None value (in the beginning of the events)
            events_list = [event for event in events.val() if event is not None]
            sorted_events = sorted(events_list, key=lambda x: x['date'])

            return sorted_events

        return {}

    """
    Retrieves events that a user has enrolled to. 
    The Users collection has an attribute called enrolled_events, which stores the event ids of enrolled events.
    """
    def get_enrolled_events(self, user_id):
        enrolled_events = self.database.child("Users").child(user_id).get()
        if enrolled_events.val() is not None:
            data = enrolled_events.val()
            if isinstance(data, dict):
                return data.get('enrolled_events', [])
            elif isinstance(data, list):
                return data
            else:
                return []
        else:
            return []
    
    """
    Retrieves the name of a company hosting a specific charity event (specified with event id)
    """
    def get_company_name(self, event_id):
        company_name = self.database.child("Events").child(event_id).get("company_name", "")
        if company_name.val() is not None:
            return company_name.val()
        return ""

    """
    Retrieves the password for a specific user.
    Args:
        user_id (str): The unique ID of the user whose password is to be retrieved.
    Returns:
        str: The password associated with the user ID if the user exists.
        None: If the user ID does not exist in the database.
    """
    def get_password(self, user_id):
        user_data = self.database.child("Users").child(user_id).get()
        if user_data.val() is not None:  # Check if user data exists
            return user_data.val().get("Password")  # Retrieve and return the password
        return None  # Return None if user does not exist

    """
    Authenticates an admin code against the database.
    Args:
        admin_code (str): The admin code to be authenticated.
    Returns:
        bool: True if the admin code is valid, False otherwise.
    """
    def authenticate_admin_code(self, admin_code):
        admn_code = self.database.child("Admin_Codes").get()
        if admn_code.val()is not None:
            for ad_code, code in admn_code.val().items():
                if code == admin_code:
                    return True
        return False
    
    """
    Authenticates a user by verifying the user ID and password.
    Args:
        user_id (str): The unique ID of the user to be authenticated.
        password (str): The password provided for authentication.
    Returns:
        bool: True if the user ID and password match a record in the database, False otherwise.
    """
    def authenticate_user(self, user_id, password):
        users = self.database.child("Users").get()
        if users.val() is not None:  # Check if there are any users in the database
            for uid, user_info in users.val().items():
                if uid == user_id:  # Check if the user_id matches
                    if user_info["Password"] == password:  # Check if the password matches
                        return True
        return False  # Return False if user_id is not found or password doesn't match
