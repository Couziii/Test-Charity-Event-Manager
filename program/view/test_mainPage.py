import unittest
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication, QListWidgetItem
from mainPage import UI_main_window, List_item_widget


class TestUI_main_window(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])


    def setUp(self):
        self.window = UI_main_window()
        self.window.controller = MagicMock()
        self.window.txt_ad_user_id.setText("test_user")


    def test_btn_logout_clicked(self):
        mock_function = MagicMock()
        self.window.signal_object.connect(mock_function)

        with patch.object(UI_main_window, 'close', MagicMock()) as mock_close:
            self.window.btn_logout_clicked()

            mock_close.assert_called_once()


    def test_reset_account_detail_tab(self):
        self.window.controller.get_password.return_value = "password123"

        self.window.reset_account_detail_tab()

        self.assertFalse(self.window.change_user_id_clicked)
        self.assertFalse(self.window.change_password_clicked)
        self.assertEqual(self.window.txt_ad_user_id.text(), "test_user")
        self.assertEqual(self.window.txt_ad_password.text(), "password123")
        self.assertFalse(self.window.txt_ad_user_id.isEnabled())
        self.assertFalse(self.window.txt_ad_password.isEnabled())
    

    def test_update_withdraw_button_state(self):
        self.window.list_widget_ad_events.addItem(QListWidgetItem("Event 1"))
        self.window.list_widget_ad_events.setCurrentRow(0)

        self.window.update_withdraw_button_state()

        self.assertTrue(self.window.btn_ad_withdraw_event.isEnabled())


    def test_btn_ad_change_user_id_clicked(self):
        
        self.window.btn_ad_change_user_id_clicked()

        self.assertTrue(self.window.change_user_id_clicked)
        self.assertTrue(self.window.txt_ad_user_id.isEnabled())
        self.assertFalse(self.window.btn_ad_change_password.isEnabled())
        self.assertTrue(self.window.btn_ad_confirm_changes.isEnabled())


    def test_btn_ad_change_password_clicked(self):
        
        self.window.btn_ad_change_password_clicked()

        self.assertTrue(self.window.change_password_clicked)
        self.assertTrue(self.window.txt_ad_password.isEnabled())
        self.assertFalse(self.window.btn_ad_change_user_id.isEnabled())
        self.assertTrue(self.window.btn_ad_confirm_changes.isEnabled())


    def test_check_input_valid(self):

        self.window.txt_ad_user_id.setText("new_user")
        self.window.txt_ad_password.setText("valid_password")
        self.window.controller.get_user_id.return_value = None

        self.window.check_input()

        self.assertFalse(self.window.wrong_inputs)
        self.assertEqual(self.window.lbl_ad_unavailable_user_id.text(), "")
        self.assertEqual(self.window.lbl_ad_unauthorized_password.text(), "")


    def test_check_input_invalid(self):

        self.window.txt_ad_user_id.setText("invalid_user;")
        self.window.txt_ad_password.setText("")

        self.window.check_input()

        self.assertTrue(self.window.wrong_inputs)
        self.assertEqual(self.window.lbl_ad_unavailable_user_id.text(), "No injection symbols allowed")


    def test_get_enrolled_events_by_company(self):

        enrolled_events = [1, 2, 3]
        self.window.controller.get_company_name.side_effect = [
            {"company_name": "Company A"},
            {"company_name": "Company B"},
            {"company_name": "Company A"},
        ]

        result = self.window.get_enrolled_events_by_company("Company A", enrolled_events)

        self.assertEqual(len(result), 2)
        for event in result:
            self.assertEqual(event["company_name"], "Company A")


    def test_load_charities(self):

        self.window.controller.get_enrolled_events.return_value = ["event1", "event2"]
        self.window.controller.get_company_name.side_effect = [
            {"company_name": "Charity A"},
            {"company_name": "Charity B"}
        ]

        self.window.load_charities()

        self.assertEqual(self.window.list_widget_ad_charities.count(), 2)
        self.assertEqual(self.window.list_widget_ad_charities.item(0).text(), "Charity A")
        self.assertEqual(self.window.list_widget_ad_charities.item(1).text(), "Charity B")


    def test_charity_name_selected(self):

        self.window.controller.get_enrolled_events.return_value = [1, 2]
        self.window.controller.get_company_name.side_effect = [
            {"company_name": "Charity A", "event_id": 1, "name": "Event 1"},
            {"company_name": "Charity A", "event_id": 2, "name": "Event 2"},
        ]

        mock_item = MagicMock()
        mock_item.text.return_value = "Charity A"

        self.window.charity_name_selected(mock_item)

        self.assertEqual(self.window.list_widget_ad_events.count(), 2)
        self.assertEqual(self.window.list_widget_ad_events.item(0).text(), "Event 1")
        self.assertEqual(self.window.list_widget_ad_events.item(1).text(), "Event 2")


    def test_load_events(self):

        self.window.controller.get_events.return_value = [
            {"event_id": 1, "name": "Event 1", "date": "2025-01-11T08:00:00"},
            {"event_id": 2, "name": "Event 2", "date": "2025-03-11T09:00:00"},
        ]

        self.window.load_events()

        self.assertEqual(self.window.event_list_area.count(), 2)


    @classmethod
    def tearDownClass(cls):
        cls.app.quit()



class TestList_item_widget(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])


    def setUp(self):

        self.controller_mock = MagicMock()
        self.event_data = {
            "date": "2024-12-28T15:30:00",
            "company_name": "Charity A",
            "address": "123 Main St",
            "name": "Event A",
            "short_description": "Short Desc",
            "description": "Full Description",
            "event_id": "event123"
        }
        self.widget = List_item_widget(self.event_data, "test_user", self.controller_mock, enrolled_events=["event123"])


    def test_format_event_date(self):

        formatted_date = self.widget.format_event_date("2024-12-28T15:30:00")
        self.assertEqual(formatted_date, "Saturday 28.12.2024")


    def test_enroll(self):

        self.controller_mock.register_enrollment.return_value = True
        self.widget.enroll(self.event_data)

        self.assertFalse(self.widget.enroll_btn.isEnabled())
        self.assertEqual(self.widget.enroll_btn.text(), "Enrolled")


    @classmethod
    def tearDownClass(cls):
        cls.app.quit()


if __name__ == "__main__":
    unittest.main()
