from brukeradministrasjon import Brukeradministrasjon
from passordadministrasjon import Passordadministrasjon
import sys

from PyQt6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, 
                             QLineEdit, QPushButton, QWidget,
                             QLabel, QVBoxLayout, QGridLayout)

from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Passwordmanager")

        self.layout = QGridLayout()

        user_instruction = QLabel("Username:")
        self.layout.addWidget(user_instruction, 1, 1)

        user_instruction = QLabel("Password:")
        self.layout.addWidget(user_instruction, 2, 1)

        user = QLineEdit()
        self.layout.addWidget(user, 1, 2)

        master_password = QLineEdit()
        master_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(master_password, 2, 2)


        buttons = QHBoxLayout()
        register = QPushButton("Register")
        log_in = QPushButton("Log in")

        register.clicked.connect(self.register)
        log_in.clicked.connect(self.log_in)
        master_password.returnPressed.connect(self.log_in)
        user.returnPressed.connect(self.log_in)


        buttons.addWidget(register)
        buttons.addWidget(log_in)

        self.layout.addLayout(buttons, 3, 2)

        main = QWidget()
        main.setLayout(self.layout)

        self.setCentralWidget(main)


    def setMinByPercentage(self, w, h):
        screen = QApplication.primaryScreen()
        screenGeometry = screen.availableGeometry()
        minw = int(screenGeometry.width() * w)
        minh = int(screenGeometry.height() * h)
        self.setMinimumSize(minw, minh)

    def register(self):
        print("Reg")

    def log_in(self):
        print("Log")

    def addLoginError(self):
        error_message = QLabel()
        self.layout.addWidget(error_message, 0, 2, Qt.AlignmentFlag.AlignCenter)


app = QApplication([])
w = MainWindow()
w.show()
app.exec()