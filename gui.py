import sys
from kontroller import Kontroller

from PyQt6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, 
                             QLineEdit, QPushButton, QWidget,
                             QLabel, QVBoxLayout, QGridLayout,
                             QScrollArea)

from PyQt6.QtGui import QAction, QMouseEvent
from PyQt6.QtCore import Qt, QSize

class MainWindow(QMainWindow):
    def __init__(self, kontroller):
        super().__init__()
        self.KONTROLLER: Kontroller = kontroller
        self.my_layout = QGridLayout()
        self.user_line = QLineEdit()
        self.master_password_line = QLineEdit()
        self.main_widget = QWidget()
        self.services = {}

        self.setWindowTitle("Passwordmanager")
        self.setMaxByPercentage(0.3, 0.5)

        user_instruction = QLabel("Username:")
        self.my_layout.addWidget(user_instruction, 1, 1)

        user_instruction = QLabel("Password:")
        self.my_layout.addWidget(user_instruction, 2, 1)

        self.my_layout.addWidget(self.user_line, 1, 2)

        self.master_password_line.setEchoMode(QLineEdit.EchoMode.Password)
        self.my_layout.addWidget(self.master_password_line, 2, 2)


        buttons = QHBoxLayout()
        register = QPushButton("Register")
        log_in = QPushButton("Log in")

        register.clicked.connect(self.register)
        log_in.clicked.connect(self.log_in)
        self.master_password_line.returnPressed.connect(self.log_in) # For at man skal kunne trykke enter fo å logge inn.
        self.user_line.returnPressed.connect(self.log_in)


        buttons.addWidget(register)
        buttons.addWidget(log_in)

        self.my_layout.addLayout(buttons, 3, 2)

        self.main_widget.setLayout(self.my_layout)

        self.setCentralWidget(self.main_widget)


    def setMaxByPercentage(self, w, h):
        screen = QApplication.primaryScreen()
        screenGeometry = screen.availableGeometry()
        minw = int(screenGeometry.width() * w)
        minh = int(screenGeometry.height() * h)
        self.setMaximumSize(minw, minh)

    def setMinByPercentage(self, w, h):
        screen = QApplication.primaryScreen()
        screenGeometry = screen.availableGeometry()
        minw = int(screenGeometry.width() * w)
        minh = int(screenGeometry.height() * h)
        self.setMinimumSize(minw, minh)


    def register(self):
        user = self.user_line.text()
        master_password = self.master_password_line.text()

        if self.KONTROLLER.checkIfTaken(user):
            self.addLoginMessage("Username is taken", error=True)
            return
    
        self.KONTROLLER.createUser(user, master_password)
        self.addLoginMessage("New user created!")
        self.master_password_line.clear()


    def log_in(self):
        user = self.user_line.text()
        master_password = self.master_password_line.text()

        if not self.KONTROLLER.checkIfTaken( user):
            self.addLoginMessage("Wrong username", error=True)
            return
        
        if not self.KONTROLLER.getUser(user, master_password):
            self.addLoginMessage("Wrong password", error=True)
            self.master_password_line.clear()
            return

        self.buildManager()


    def addLoginMessage(self, string, error=False):
        message = self.my_layout.itemAtPosition(0, 2)
        if message:
            message = message.widget()
        else:
            message = QLabel()
            self.my_layout.addWidget(message, 0, 2, Qt.AlignmentFlag.AlignCenter)

        message.setText(string)
        if error: message.setStyleSheet("color: red;")
        else: message.setStyleSheet("")


    def buildManager(self):
        scroll_area = QScrollArea()
        self.my_layout = QGridLayout(scroll_area)
        self.main_widget = QWidget()
        self.services = self.KONTROLLER.getNamesAndUsernames()

        self.my_layout.setHorizontalSpacing(5)
        self.main_widget.setLayout(self.my_layout)

        i = 0
        for service in self.services:
            service_space = QVBoxLayout()

            q_service = QLabel(service)
            q_service.setStyleSheet("font-size: 15pt")
            q_service.setAlignment(Qt.AlignmentFlag.AlignBottom)
            service_space.addWidget(q_service)

            username = QLineEdit(self.services[service])
            username.setStyleSheet("font-style: italic; background-color: transparent; border: 0px;")
            username.setAlignment(Qt.AlignmentFlag.AlignTop)
            username.setReadOnly(True)
            service_space.addWidget(username)

            self.my_layout.addLayout(service_space, i, 0)


            show_details = QPushButton("Details")
            show_details.clicked.connect(self.showDetails)
            self.my_layout.addWidget(show_details, i, 1)

            copy_password = QPushButton("Copy password")
            self.my_layout.addWidget(copy_password, i, 2)

            i += 1

        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setWidget(self.main_widget)
        self.resize(self.main_widget.width() + 10, self.main_widget.height())
        self.setCentralWidget(scroll_area)


    def showDetails(self):
        pass

    def mousePressEvent(self, a0: QMouseEvent | None) -> None: # For at den blå borderen rundt knapper skal forsvinne når man klikker et annet sted
        if self.focusWidget():
            self.focusWidget().clearFocus()
        return super().mousePressEvent(a0)

def start(kontroller):
    app = QApplication([])
    w = MainWindow(kontroller)
    w.show()
    app.exec()
