import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PyQt5.QtWidgets import QApplication
from program.view.logIn import UI_login_window


def main():
    app = QApplication(sys.argv)
    main_window = UI_login_window()
    app.exec_()


if __name__ == "__main__":
    main()