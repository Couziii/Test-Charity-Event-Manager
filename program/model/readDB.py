import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pyrebase

class Read_db:
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

    def get_user_id(self, user_id):
        users = self.database.child("Users").get()
        if users.val() is not None:  # Check if there are any users in the database
            for uid, user_info in users.val().items():
                if uid == user_id:  # Compare with the correct variable
                    return uid, user_info
        return None  # Return None if user_id is not found
    
    def get_password(self, user_id):
        user_data = self.database.child("Users").child(user_id).get()
        if user_data.val() is not None:  # Check if user data exists
            return user_data.val().get("Password")  # Retrieve and return the password
        return None  # Return None if user does not exist

    
    def authenticate_admin_code(self, admin_code):
        admn_code = self.database.child("Admin_Codes").get()
        if admn_code.val()is not None:
            for ad_code, code in admn_code.val().items():
                if code == admin_code:
                    return True
        return False
    
    def authenticate_user(self, user_id, password):
        users = self.database.child("Users").get()
        if users.val() is not None:  # Check if there are any users in the database
            for uid, user_info in users.val().items():
                if uid == user_id:  # Check if the user_id matches
                    if user_info["Password"] == password:  # Check if the password matches
                        return True
        return False  # Return False if user_id is not found or password doesn't match
