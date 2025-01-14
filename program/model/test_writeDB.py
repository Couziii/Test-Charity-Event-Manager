import unittest
from unittest.mock import MagicMock
from writeDB import Write_db


class TestEventEnrollment(unittest.TestCase):

    def setUp(self):
        
        self.mock_database = MagicMock()
        self.mock_users = MagicMock()
        self.mock_events = MagicMock()

        self.mock_database.child.side_effect =  lambda key: self.mock_users if key == "Users" else self.mock_events
        self.write_to_database = Write_db(self.mock_database)


    def test_register_enrollment_success(self):
        user_id = "user123"
        event_id = "event456"
        user_data = {"enrolled_events": []}
        event_data = {"enrolled_users": []}

        self.mock_users.child(user_id).get.return_value.val.return_value = user_data
        self.mock_events.child(event_id).get.return_value.val.return_value = event_data

        result = self.write_to_database.register_enrollment(event_id, user_id)

        self.assertTrue(result)
        self.mock_users.child(user_id).update.assert_called_once_with({"enrolled_events": [event_id]})
        self.mock_events.child(event_id).update.assert_called_once_with({"enrolled_users": [user_id]})


    def test_register_enrollment_user_or_event_not_found(self):
        user_id = "user123"
        event_id = "event456"

        self.mock_database.child("Users").child(user_id).get.return_value.val.return_value = None
        self.mock_database.child("Events").child(event_id).get.return_value.val.return_value = None

        result = self.write_to_database.register_enrollment(event_id, user_id)

        self.assertFalse(result)


    def test_unenroll_success(self):
        user_id = "user123"
        event_id = "event456"
        user_data = {"enrolled_events": [event_id]}
        event_data = {"enrolled_users": [user_id]}

        self.mock_users.child(user_id).get.return_value.val.return_value = user_data
        self.mock_events.child(event_id).get.return_value.val.return_value = event_data

        result = self.write_to_database.unenroll(event_id, user_id)

        self.assertTrue(result)
        self.mock_users.child(user_id).update.assert_called_once_with({"enrolled_events": []})
        self.mock_events.child(event_id).update.assert_called_once_with({"enrolled_users": []})


    def test_unenroll_user_or_event_not_found(self):
        user_id = "user123"
        event_id = "event456"

        self.mock_database.child("Users").child(user_id).get.return_value.val.return_value = None
        self.mock_database.child("Events").child(event_id).get.return_value.val.return_value = None

        result = self.write_to_database.unenroll(event_id, user_id)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
