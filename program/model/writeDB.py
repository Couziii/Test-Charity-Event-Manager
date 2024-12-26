import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pyrebase

"""
A class to interact with a Firebase Realtime Database for managing user accounts.
This class provides methods to perform CRUD (Create, Read, Update, Delete) operations
on a Firebase Realtime Database for user accounts.
Attributes:
----------
database : pyrebase.pyrebase.Database
    A reference to the Firebase Realtime Database.
Methods:
-------
__init__():
    Initializes the Firebase connection using the configuration.

insert_new_user(user_id, password, admin):
    Adds a new user to the database with the specified user ID, password, and admin status.

change_user_id(old_user_id, new_user_id):
    Changes the user ID of an existing account by transferring data to a new ID.
change_password(user_id, password):
    Updates the password of a specific user account.
remove_account(user_id):
    Deletes a user account from the database.
"""
class Write_db:
    """
    Initializes the Write_db class and establishes a connection to the Firebase Realtime Database.
    The connection is configured using a predefined dictionary containing API keys and 
    other configuration parameters required by Firebase.
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
    Adds a new user to the database.
    Parameters:
    ----------
    user_id : str
        The unique identifier for the new user.
    password : str
        The password associated with the user account.
    admin : bool
        Specifies if the user has administrative privileges.
    Returns:
    -------
    None
    """
    def insert_new_user(self, user_id, password, admin):
        user_info = {"Password" : password, "Admin" : admin}
        self.database.child("Users").child(user_id).set(user_info)
    
    """
    Registers a user's enrollment to a charity event.
    -> Updates the user's enrolled_events attribute with the new event id.
    -> Updates the event's enrolled_users attribute to hold the logged in user.
    """
    def register_enrollment(self, event_id, user_id):
        try:
            user_data = self.database.child("Users").child(user_id).get()
            event_data = self.database.child("Events").child(event_id).get()

            if user_data.val() is not None and event_data.val() is not None:
                enrolled_events = user_data.val().get("enrolled_events", [])
                enrolled_users = event_data.val().get("enrolled_users", [])

                if event_id not in enrolled_events:
                    enrolled_events.append(event_id)
                    self.database.child("Users").child(user_id).update({"enrolled_events": enrolled_events})

                if user_id not in enrolled_users:
                    enrolled_users.append(user_id)
                    self.database.child("Events").child(event_id).update({"enrolled_users": enrolled_users})
                
                return True
            else:
                return False
        except Exception as e:
            print("Error during enrollment", e)
            return False
    
    """
    Unenrolls a user and withdraws their enrollment to a charity event.
    -> Updates the user's enrolled_events to not hold the event id anymore.
    -> Updates the event's enrolled_users attribute to not hold the logged in user's user id anymore.
    """
    def unenroll(self, event_id, user_id):
        try:
            user_data = self.database.child("Users").child(user_id).get()
            event_data = self.database.child("Events").child(event_id).get()

            if user_data.val() is not None and event_data.val() is not None:
                enrolled_events = user_data.val().get("enrolled_events", [])
                enrolled_users = event_data.val().get("enrolled_users", [])
                            
                if event_id in enrolled_events:
                    enrolled_events.remove(event_id)
                    self.database.child("Users").child(user_id).update({"enrolled_events": enrolled_events})

                if user_id in enrolled_users:
                    enrolled_users.remove(user_id)
                    self.database.child("Events").child(event_id).update({"enrolled_users": enrolled_users})
                
                return True
            else:
                return False
        except Exception as e:
            print("Error during unenrollment", e)
            return False


    """
    Updates a user's ID in the database.
    Transfers all data associated with the old user ID to a new user ID and removes the old ID.
    Parameters:
    ----------
    old_user_id : str
        The current user ID to be changed.
    new_user_id : str
        The new user ID to replace the old ID.
    Returns:
    -------
    None
    """
    def change_user_id(self, old_user_id, new_user_id):
        user_data = self.database.child("Users").child(old_user_id).get()
        if user_data.val() is not None:
            self.database.child("Users").child(new_user_id).set(user_data.val())
            self.database.child("Users").child(old_user_id).remove()

    """
    Updates the password for a specific user.
    Parameters:
    ----------
    user_id : str
        The ID of the user whose password will be updated.
    password : str
        The new password to be set.
    Returns:
    -------
    None
    """
    def change_password(self, user_id, password):
        self.database.child("Users").child(user_id).update({"Password":password})

    """
    Deletes a user account from the database.
    Parameters:
    ----------
    user_id : str
        The ID of the user account to be removed.
    Returns:
    -------
    None
    """
    def remove_account(self, user_id):
        self.database.child("Users").child(user_id).remove()
