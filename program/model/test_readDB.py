import unittest
from unittest.mock import MagicMock
from readDB import Read_db


class TestReadDB(unittest.TestCase):

    def setUp(self):
        
        self.mock_database = MagicMock()
        self.read_db = Read_db()
        self.read_db.database = self.mock_database


    def test_get_events(self):
        
        mock_events = [
            None,
            {"date": "2024-01-01", "name": "Event A"},
            {"date": "2024-01-03", "name": "Event C"},
            {"date": "2024-01-02", "name": "Event B"}
        ]
        self.mock_database.child("Events").get.return_value.val.return_value = mock_events

        result = self.read_db.get_events()

        expected = [
            {"date": "2024-01-01", "name": "Event A"},
            {"date": "2024-01-02", "name": "Event B"},
            {"date": "2024-01-03", "name": "Event C"}
        ]

        self.assertEqual(result, expected)
        self.mock_database.child("Events").get.assert_called_once()


    def test_get_enrolled_events_dict(self):

        mock_user_data = {"enrolled_events": ["event1", "event2"]}
        self.mock_database.child("Users").child("user123").get.return_value.val.return_value = mock_user_data

        result = self.read_db.get_enrolled_events("user123")

        expected = ["event1", "event2"]

        self.assertEqual(result, expected)
        self.mock_database.child("Users").child("user123").get.assert_called_once()


    def test_get_enrolled_events_list(self):

        mock_user_data = ["event1", "event2"]
        self.mock_database.child("Users").child("user123").get.return_value.val.return_value = mock_user_data

        result = self.read_db.get_enrolled_events("user123")

        expected = ["event1", "event2"]

        self.assertEqual(result, expected)
        self.mock_database.child("Users").child("user123").get.assert_called_once()


    def test_get_company_name(self):

        mock_company_name = "Charity Co."
        self.mock_database.child("Events").child("event123").get.return_value.val.return_value = mock_company_name

        result = self.read_db.get_company_name("event123")

        expected = "Charity Co."

        self.assertEqual(result, expected)
        self.mock_database.child("Events").child("event123").get.assert_called_once()


if __name__ == "__main__":
    unittest.main()
