import unittest # Python framework for testing
from unittest.mock import patch, MagicMock # Mock creates 'fake' objects (inputs) to use in the testing of a program
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton # Widgets that are used in the login window
from logIn import UI_login_window # The classes being tested
from signUp import UI_signup_window

class TestUILoginWindow(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        '''Class-level setup. In order to use the PyQt5 widgets, a QApplication instance must be created.'''
        
        cls.app = QApplication([])


    def setUp(self):
        '''Test-level setup. Initializing a login window for the session and creating the mock inputs.
        This method runs before each test.'''
        
        # Create an instance of the UI_login_window class for the test
        self.window = UI_login_window()

        # Mock widgets that correspond to the PyQt widgets
        self.window.txt_user_id = MagicMock(spec=QLineEdit)
        self.window.txt_password = MagicMock(spec=QLineEdit)
        self.window.lbl_wrong_input = MagicMock(spec=QLabel)
        self.window.btn_login = MagicMock(spec=QPushButton)
        self.window.lbl_signup = MagicMock(spec=QLabel)

        # Initating a mock version of the controller to avoid errors related to the database (backend connection errors)
        self.window.controller = MagicMock()


    ### UNIT TESTS ###
    def test_widgets_loaded_correctly(self):
        '''Test for determining that the widgets have been loaded correctly at program start.'''
        
        # Checking that none of the mocked widgets are None
        self.assertIsNotNone(self.window.btn_login, "btn_login not loaded")
        self.assertIsNotNone(self.window.txt_user_id, "txt_user_id not loaded")
        self.assertIsNotNone(self.window.txt_password, "txt_password not loaded")
        self.assertIsNotNone(self.window.lbl_wrong_input, "lbl_wrong_input not loaded")
        self.assertIsNotNone(self.window.lbl_signup, "lbl_signup not loaded")


    def test_widget_connections(self):
        '''Test for verifying the connection between the btn_login button and the btn_login_clicked method.'''
        
        # Save a mock signal that a button was clicked into a variable
        with patch.object(self.window.btn_login, "clicked") as mock_signal:

            # Find the login button in the login window and connect to it's method
            self.window.btn_login.clicked.connect(self.window.btn_login_clicked)

            # Mock that the login button has been clicked and check that the connected method was called once and only once (not 0 or multiple calls)
            mock_signal.connect.assert_called_once_with(self.window.btn_login_clicked)
    

    def test_btn_login_clicked_success(self):
        '''Test for the program's behavior after valid login inputs are provided and the login button is clicked.'''

        self.window.wrong_inputs = False

        # Mock is used here to track the check_input, clear_window, and close calls
        self.window.check_input = MagicMock()
        self.window.clear_window = MagicMock()
        self.window.close = MagicMock()
        
        # The UI_main_window is mocked, instead of initiating the actual main window (then cannot mock inputs)
        with patch("logIn.UI_main_window") as MockMainWindow:
            mock_instance = MockMainWindow.return_value
            mock_instance.signal_object.connect = MagicMock()

            # Calling the method this test is for
            self.window.btn_login_clicked()

            # Verify check_input was called after the login button was 'clicked' (once)
            self.window.check_input.assert_called_once()

            # Verify UI_main_window is instantiated after the input was verified
            MockMainWindow.assert_called_once_with(self.window, self.window.user_id)

            # Verify that the main window is called to show
            mock_instance.signal_object.connect.assert_called_once_with(self.window.show)
            
            # Verify that the methods (clear_window, close, show) are called correctly when valid user information was provided
            self.window.clear_window.assert_called_once()
            self.window.close.assert_called_once()
            mock_instance.show.assert_called_once()


    def test_lbl_signup_clicked(self):
        '''Test for determining the program's behavior after the signup button is clicked.'''

        # Mock to track clear_window and close calls (so assert_called_once method can be used for testing)
        self.window.clear_window = MagicMock()
        self.window.close = MagicMock()

        # Mock UI_signup_window to avoid instantiating the actual window
        with patch("logIn.UI_signup_window") as MockSignupWindow:
            mock_instance = MockSignupWindow.return_value
            mock_instance.signal_object.connect = MagicMock()

            # Calling the method this test is for
            self.window.lbl_signup_clicked()

            # Verify UI_signup_window was created after the signup button was 'clicked'
            MockSignupWindow.assert_called_once_with(self.window)

            # Verify the UI_signup_window shows after initiation
            mock_instance.signal_object.connect.assert_called_once_with(self.window.show)

            # Verify associated methods are called correctly
            self.window.clear_window.assert_called_once()
            self.window.close.assert_called_once()
            mock_instance.show.assert_called_once()


    def test_get_window_values(self):
        '''Test for verifying the correct functionality of the get_window_values method.'''
        
        # Mock some values for text fields
        self.window.txt_user_id.text.return_value = "test_user"
        self.window.txt_password.text.return_value = "test_password"

        # Call the method the test is for
        self.window.get_window_values()

        # Check that the mocked values are the ones the method retrieved
        self.assertEqual(self.window.user_id, "test_user")
        self.assertEqual(self.window.password, "test_password")


    def test_check_input_valid(self):
        '''Test for the program's behavior when the login input values are valid.'''
        
        # The check_input method reads the user inputs from the window, which we don't have for this test --> mock
        self.window.get_window_values = MagicMock()

        # Set the user id and password to some values (cannot include injection symbols)
        self.window.user_id = "valid_user"
        self.window.password = "valid_password"

        # Creating a mock database response to an authentication request (for testing purposes)
        self.window.controller.authenticate_user.return_value = True

        # Calling the method being tested
        self.window.check_input()

        # Verify wrong_inputs returns False
        # The method check_input checks for hidden symbols and then authenticates the user through the controller
        self.assertFalse(self.window.wrong_inputs)


    def test_check_input_invalid(self):
        '''Test for the program's behavior when the login input values are invalid.'''
        
        # The check_input method reads the user inputs from the window, which we don't have for this test --> mock
        self.window.get_window_values = MagicMock()
        
        # Set the user id and password to some values --> notice the ' in the user id (injection symbol)
        self.window.user_id = "invalid'"
        self.window.password = "valid_password"

        # Calling the method being tested
        self.window.check_input()

        # Verify lbl_wrong_input is updated in the check_input method
        self.window.lbl_wrong_input.setText.assert_called_once_with("No injection symbols allowed")
        
        # Verify wrong_inputs returns True
        self.assertTrue(self.window.wrong_inputs)


    def test_clear_window(self):
        '''Test for verifying the correct functionality of the clear_window method.'''
        
        # Calling the tested method
        self.window.clear_window()

        # Checking that clear is called for user id and password fields
        self.window.txt_user_id.clear.assert_called_once()
        self.window.txt_password.clear.assert_called_once()

        # Verifying that the lbl_wrong_input is reset to an empty string
        self.window.lbl_wrong_input.setText.assert_called_once_with("")


    @classmethod
    def tearDownClass(cls):
        cls.app.quit()


if __name__ == "__main__":
    unittest.main()
