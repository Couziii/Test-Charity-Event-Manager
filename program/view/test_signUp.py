import unittest # Python module for creating and running unit tests
from unittest.mock import MagicMock # Used for creating mock inputs for testing without real implementations
from PyQt5.QtWidgets import QApplication # required for running PyQt5 applications
from signUp import UI_signup_window # the class being tested

class TestUISignupWindow(unittest.TestCase):
    '''Test case class for functionality in the UI_signup_window that inherits from the unittest.TestCase'''

    @classmethod
    def setUpClass(cls):
        '''Class-level setup. Creating an instance of the QApplication class, which is mandatory for using PyQt5 widgets.'''
        cls.app = QApplication([])


    def setUp(self):
        '''Test-level setUp that runs before every test.'''

        # Creating an instance of the signup window for the tests
        self.window = UI_signup_window()

        # Initating a mock version of the controller to avoid errors related to the database (backend connection errors)
        self.window.controller = MagicMock()
        
        # The UI_signup_window initializes a signal_object that reacts to the signup and cancel buttons
        # For testing, the signal is mocked to avoid external (backend) connection errors
        self.signal_mock = MagicMock()

        # Connecting the mocked signal to the signal_object created in the UI_signup_window class
        self.window.signal_object.connect(self.signal_mock)


    def tearDown(self):
        '''Method that runs after each test and closes the window instance.'''
        self.window.close()


    ### UNIT TESTS ###
    def test_btn_cancel_clicked(self):
        '''Test for the 'cancel' button functionality.'''

        # Setting the signup input values as some values
        self.window.txt_user_id.setText("testuser")
        self.window.txt_password.setText("password123")
        self.window.txt_admin_code.setText("admincode")

        # Calling the method being tested
        self.window.btn_cancel_clicked()

        # After cancel is pressed, the input fields should be cleared
        # The unit tests are checking that each input field corresponds to an empty string
        self.assertEqual(self.window.txt_user_id.text(), "")
        self.assertEqual(self.window.txt_password.text(), "")
        self.assertEqual(self.window.txt_admin_code.text(), "")

        # Verify that the mocked signal_object was called (the signal is called when cancel button is pressed)
        self.signal_mock.assert_called_once()

        # Verify that the window is closed, since the user wanted to cancel
        self.assertFalse(self.window.isVisible())


    def test_btn_signup_clicked_valid_input(self):
        '''Test for the 'signup' button functionality when the input is valid.'''

        # Setting the signup input values as some values (must be valid)
        self.window.txt_user_id.setText("validuser")
        self.window.txt_password.setText("validpassword")
        self.window.txt_admin_code.setText("")

        # Since the test will not actually implement a connection to the database, mock responses are set here
        self.window.controller.get_user_id.return_value = None
        self.window.controller.check_admin_code.return_value = True

        # Call the method being tested
        self.window.btn_signup_clicked()

        # Verify that the method allowed the new user to be added to the system, since the input was valid
        self.window.controller.insert_new_user.assert_called_once_with("validuser", "validpassword")
        
        # Verify that a signal is emitted
        self.signal_mock.assert_called_once()

        # Lastly, verify that the window closes
        self.assertFalse(self.window.isVisible())


    def test_btn_signup_clicked_invalid_input(self):
        '''Test for the 'signup' button functionality when the input is invalid.'''

        # Setting the input values as some values (notice the injection symbol in user id, missing password, and invalid admin code)
        self.window.txt_user_id.setText("invalid'user")
        self.window.txt_password.setText("")
        self.window.txt_admin_code.setText("wrongcode")

        # Mocked database connection that simulates a response to an invalid signup attempt
        self.window.controller.get_user_id.return_value = None
        self.window.controller.check_admin_code.return_value = False

        # Call the tested method
        self.window.btn_signup_clicked()

        # Verify that the method found the errors in user id, password, and admin code
        self.assertEqual(self.window.lbl_unavailable_user_id.text(), "No injection symbols allowed")
        self.assertEqual(self.window.lbl_unauthorized_password.text(), "Password must not be empty!")
        self.assertEqual(self.window.lbl_wrong_admin_code.text(), "Wrong admin code")
        
        # Verify that wrong_input was set to True due to the errors in the input
        self.assertTrue(self.window.wrong_inputs)
        
        # Verify that the insert_new_user method was not called due to disallowed user input
        self.window.controller.insert_new_user.assert_not_called()
        
        # Verify that no signal was emitted
        self.signal_mock.assert_not_called()


    def test_clear_window(self):
        '''Test for the clear_window method that resets input fields and error messages.'''

        # Inputting some values into the input fields
        self.window.txt_user_id.setText("user")
        self.window.txt_password.setText("pass")
        self.window.txt_admin_code.setText("code")

        # Setting some values into the labels that carry error messages
        self.window.lbl_unavailable_user_id.setText("Error")
        self.window.lbl_unauthorized_password.setText("Error")
        self.window.lbl_wrong_admin_code.setText("Error")

        # Call the tested method
        self.window.clear_window()

        # Verify that the clear_window method set all fields to empty strings
        self.assertEqual(self.window.txt_user_id.text(), "")
        self.assertEqual(self.window.txt_password.text(), "")
        self.assertEqual(self.window.txt_admin_code.text(), "")
        self.assertEqual(self.window.lbl_unavailable_user_id.text(), "")
        self.assertEqual(self.window.lbl_unauthorized_password.text(), "")
        self.assertEqual(self.window.lbl_wrong_admin_code.text(), "")


    def test_check_input_valid(self):
        '''Test for input validation functionality with valid data.'''

        # Inputting some values into the signup fields
        self.window.txt_user_id.setText("validuser")
        self.window.txt_password.setText("validpassword")
        self.window.txt_admin_code.setText("")

        # Mocking a database response to get_user_id (user not found --> id allowed for new user)
        self.window.controller.get_user_id.return_value = None

        # Calling the tested method
        self.window.check_input()

        # Verify that wrong_input is False, since the input was valid
        self.assertFalse(self.window.wrong_inputs)

        # Verify that the error messages carried in labels are empty, since no error should occur
        self.assertEqual(self.window.lbl_unavailable_user_id.text(), "")
        self.assertEqual(self.window.lbl_unauthorized_password.text(), "")
        self.assertEqual(self.window.lbl_wrong_admin_code.text(), "")


    def test_check_input_invalid(self):
        '''Test for input validation functionality with invalid data.'''

        # Inputting some invalid values into the signup fields
        self.window.txt_user_id.setText("invalid'user")
        self.window.txt_password.setText("")
        self.window.txt_admin_code.setText("wrongcode")

        # Mocking a database response to get_user_id and check_admin_code
        # User exists --> a new user cannot use the same id
        self.window.controller.get_user_id.return_value = "exists"

        # The input admin code was invalid
        self.window.controller.check_admin_code.return_value = False

        # Call the tested method
        self.window.check_input()

        # Verify that the wrong_inputs is True, since the inputs were invalid
        self.assertTrue(self.window.wrong_inputs)

        # Verify that the error messages carried in labels are updated correctly
        self.assertEqual(self.window.lbl_unavailable_user_id.text(), "User ID already exist")
        self.assertEqual(self.window.lbl_unauthorized_password.text(), "Password must not be empty!")
        self.assertEqual(self.window.lbl_wrong_admin_code.text(), "Wrong admin code")


if __name__ == "__main__":
    unittest.main()
