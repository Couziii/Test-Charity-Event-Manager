import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pyrebase

class Write_db:
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

    def insert_new_user(self, user_id, password, admin):
        user_info = {"Password" : password, "Admin" : admin}
        self.database.child("Users").child(user_id).set(user_info)

    def change_user_id(self, old_user_id, new_user_id):
        user_data = self.database.child("Users").child(old_user_id).get()
        if user_data.val() is not None:
            self.database.child("Users").child(new_user_id).set(user_data.val())
            self.database.child("Users").child(old_user_id).remove()

    def change_password(self, user_id, password):
        self.database.child("Users").child(user_id).update({"Password":password})

    def remove_account(self, user_id):
        self.database.child("Users").child(user_id).remove()
