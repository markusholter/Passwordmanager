import sys
from kontroller import Kontroller
from functools import partial

from PyQt6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, 
                             QLineEdit, QPushButton, QWidget,
                             QLabel, QVBoxLayout, QGridLayout,
                             QScrollArea, QMessageBox, QToolBar)

from PyQt6.QtGui import QMouseEvent, QFontMetrics
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, kontroller):
        super().__init__()
        self.KONTROLLER: Kontroller = kontroller
        self.my_layout = QGridLayout()
        self.user_line = QLineEdit()
        self.master_password_line = QLineEdit()
        self.main_widget = QWidget()
        self.under_widget = QWidget()
        self.services = {}
        self.toolbar = None

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

    def loggedIn(self):
        self.services = self.KONTROLLER.getNamesAndUsernames()
        self.toolbar = QToolBar("Toolbar")
        self.buildManager()
        self.resize(self.under_widget.width() + 20, self.under_widget.height() + self.toolbar.heightMM())

        self.toolbar.setMovable(False)
        
        add_item = QPushButton("Add item")
        add_item.clicked.connect(self.addItem)
        self.toolbar.addWidget(add_item)

        self.toolbar.addSeparator()

        search_label = QLabel("Search: ")
        self.toolbar.addWidget(search_label)

        search = QLineEdit()
        search.textEdited.connect(self.search)
        self.toolbar.addWidget(search)

        self.addToolBar(self.toolbar)

    def buildManager(self, search=""):
        self.main_widget = QScrollArea()
        self.my_layout = QGridLayout(self.main_widget)
        self.under_widget = QWidget()
        services = self.KONTROLLER.getNamesAndUsernames(search)

        self.my_layout.setHorizontalSpacing(5)
        self.under_widget.setLayout(self.my_layout)

        self.listServices(services)

        self.main_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.main_widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.main_widget.setWidget(self.under_widget)
        self.setCentralWidget(self.main_widget)

    def listServices(self, services):
        i = 0
        for service in services:
            service_space = QVBoxLayout()

            q_service = QLabel(service)
            q_service.setStyleSheet("font-size: 13pt;")
            q_service.setMaximumWidth(200)
            font_metrics = QFontMetrics(q_service.font())
            elided_service = font_metrics.elidedText(q_service.text(), Qt.TextElideMode.ElideMiddle, q_service.maximumWidth() - 60)
            q_service.setText(elided_service)
            q_service.setAlignment(Qt.AlignmentFlag.AlignBottom)
            service_space.addWidget(q_service)

            username = QLineEdit(services[service])
            username.setStyleSheet("font-style: italic; background-color: transparent; border: 0px;")
            username.setMaximumWidth(200)
            font_metrics = QFontMetrics(username.font())
            elided_service = font_metrics.elidedText(username.text(), Qt.TextElideMode.ElideMiddle, username.maximumWidth() - 60)
            username.setText(elided_service)
            username.setAlignment(Qt.AlignmentFlag.AlignTop)
            username.setReadOnly(True)
            service_space.addWidget(username)

            self.my_layout.addLayout(service_space, i, 0)


            show_details = QPushButton("Details")
            show_details.clicked.connect(self.showDetails)
            self.my_layout.addWidget(show_details, i, 1)

            copy_password = QPushButton("Copy password")
            copy_password.clicked.connect(partial(self.copyPassword, q_service.text()))
            self.my_layout.addWidget(copy_password, i, 2)

            i += 1


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

        self.loggedIn()


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


    def search(self, s):
        self.buildManager(s)

    def showDetails(self):
        pass

    def mousePressEvent(self, a0: QMouseEvent | None) -> None: # For at den blå borderen rundt knapper skal forsvinne når man klikker et annet sted
        if self.focusWidget():
            self.focusWidget().clearFocus()
        return super().mousePressEvent(a0)
    

    def copyPassword(self, service):
        clipboard = QApplication.clipboard()
        password = self.KONTROLLER.getPassword(service)
        clipboard.setText(password)

        QMessageBox.information(self, "Clipboard", "Password copied to clipboard!")

    def addItem(self):
        pass


def start(kontroller):
    app = QApplication([])
    w = MainWindow(kontroller)
    w.show()
    app.exec()
