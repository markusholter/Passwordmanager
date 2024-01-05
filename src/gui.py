from kontroller import Kontroller
from functools import partial

from PyQt6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, 
                             QLineEdit, QPushButton, QWidget,
                             QLabel, QVBoxLayout, QGridLayout,
                             QScrollArea, QMessageBox, QToolBar)

from PyQt6.QtGui import QMouseEvent, QFontMetrics
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):

    # Initialize the window to the log in screen
    def __init__(self, kontroller):
        super().__init__()

        # Initialize all variables that will be saved to self
        self.KONTROLLER: Kontroller = kontroller
        self.my_layout = QGridLayout()
        self.user_line = QLineEdit()
        self.master_password_line = QLineEdit()
        self.main_widget = QWidget()
        self.under_widget = QWidget()
        self.services = {}
        self.item_window = QWidget()
        self.toolbar = None

        self.setWindowTitle("Passwordmanager")
        self.setMaxByPercentage(0.3, 0.5)

        # Make and add the labels and editable lines to the layout
        user_instruction = QLabel("Username:")
        self.my_layout.addWidget(user_instruction, 1, 1)

        user_instruction = QLabel("Password:")
        self.my_layout.addWidget(user_instruction, 2, 1)

        self.my_layout.addWidget(self.user_line, 1, 2)

        self.master_password_line.setEchoMode(QLineEdit.EchoMode.Password)
        self.my_layout.addWidget(self.master_password_line, 2, 2)


        # Make, configure and add a "register" and "log in" button to the layout
        buttons = QHBoxLayout()
        register = QPushButton("Register")
        log_in = QPushButton("Log in")

        register.clicked.connect(self.register)
        log_in.clicked.connect(self.log_in)
        self.master_password_line.returnPressed.connect(self.log_in)
        self.user_line.returnPressed.connect(self.log_in)


        buttons.addWidget(register)
        buttons.addWidget(log_in)

        self.my_layout.addLayout(buttons, 3, 2)

        self.main_widget.setLayout(self.my_layout)

        # Add the main widget to the window
        self.setCentralWidget(self.main_widget)

    # Build main window again after succesful login
    def loggedIn(self):
        self.services = self.KONTROLLER.getNamesAndUsernames()
        self.toolbar = QToolBar("Toolbar")
        self.buildManager()
        self.resize(self.under_widget.width() + 20, self.under_widget.height() + self.toolbar.heightMM())

        self.toolbar.setMovable(False)
        
        # Configure the toolbar with search an "add item" button
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

    # Build the main widget
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

    # Lists all saved services for the user with buttons for details and password copy
    def listServices(self, services):
        i = 0
        for service in services:
            service_space = QVBoxLayout()

            # Configure the service name label
            q_service = QLabel(service)
            q_service.setStyleSheet("font-size: 13pt;")
            q_service.setMaximumWidth(200)
            font_metrics = QFontMetrics(q_service.font())
            elided_service = font_metrics.elidedText(q_service.text(), Qt.TextElideMode.ElideMiddle, q_service.maximumWidth() - 60)
            q_service.setText(elided_service)
            q_service.setAlignment(Qt.AlignmentFlag.AlignBottom)
            service_space.addWidget(q_service)

            # Configure username widget as LineEdit, so that it can be selected and copied
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

            #Configure the buttons "Details" and "Copy password"
            show_details = QPushButton("Details")
            show_details.clicked.connect(partial(self.showDetails, q_service.text()))
            self.my_layout.addWidget(show_details, i, 1)

            copy_password = QPushButton("Copy password")
            copy_password.clicked.connect(partial(self.copyPassword, q_service.text()))
            self.my_layout.addWidget(copy_password, i, 2)

            i += 1

    # Set the max window size in relation to screen size
    def setMaxByPercentage(self, w, h):
        screen = QApplication.primaryScreen()
        screenGeometry = screen.availableGeometry()
        minw = int(screenGeometry.width() * w)
        minh = int(screenGeometry.height() * h)
        self.setMaximumSize(minw, minh)


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

    # Add or edit the message at the log in screen
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


    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        if self.focusWidget():
            self.focusWidget().clearFocus()
        return super().mousePressEvent(a0)
    

    def copyPassword(self, service):
        clipboard = QApplication.clipboard()
        password = self.KONTROLLER.getPassword(service)
        clipboard.setText(password)

        QMessageBox.information(self, "Clipboard", "Password copied to clipboard!")

    # Initialize a new window to add an Item
    def addItem(self):
        self.item_window.close()
        self.item_window = AddItemWindow(self, self.KONTROLLER)
        self.item_window.show()

    # Close the secondary window and add the new Item
    def addPassword(self, name, username, new_password):
        self.KONTROLLER.addPassword(name, username, new_password)
        self.buildManager()
        self.services = self.KONTROLLER.getNamesAndUsernames()

    # Initialize a new window for details and editing
    def showDetails(self, service):
        self.item_window.close()
        self.item_window = DetailsItemWindow(self, service, self.services[service], self.KONTROLLER.getPassword(service), self.KONTROLLER)
        self.item_window.show()


# An abstract class with the common UI of addItemWindow and DetailsItemWindow 
class ItemWindow(QWidget):
    def __init__(self, main_window: MainWindow, kontroller: Kontroller):
        super().__init__()

        # Initialize all variables that will be saved to self
        self.main_window = main_window
        self.KONTROLLER = kontroller
        self.my_layout = QGridLayout()
        self.name = QLineEdit()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.button_layout = QHBoxLayout()
        self.show_password = QPushButton("Show password")

        # Make and add all labels to the layout
        name_label = QLabel("Service: ")
        self.my_layout.addWidget(name_label, 0, 0)
        self.my_layout.addWidget(self.name, 0, 1)

        username_label = QLabel("Username: ")
        self.my_layout.addWidget(username_label, 1, 0)
        self.my_layout.addWidget(self.username, 1, 1)

        password_label = QLabel("Password: ")
        self.my_layout.addWidget(password_label, 2, 0)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.my_layout.addWidget(self.password, 2, 1)

        self.my_layout.addLayout(self.button_layout, 3, 1)

        # Add layout to the window
        self.setLayout(self.my_layout)

    # Change between showing and hiding the password
    def showPassword(self):
        self.show_password.setFixedSize(self.show_password.size())

        if self.password.echoMode() == QLineEdit.EchoMode.Password:
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_password.setText("Hide password")
        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_password.setText("Show password")


    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        if self.focusWidget():
            self.focusWidget().clearFocus()
        return super().mousePressEvent(a0)

# Window for adding items
class AddItemWindow(ItemWindow):
    def __init__(self, main_window: MainWindow, kontroller):
        super().__init__(main_window, kontroller)

        # Connect the action of pressing "Enter" to being done
        self.name.returnPressed.connect(self.done)
        self.username.returnPressed.connect(self.done)
        self.password.returnPressed.connect(self.done)

        # Configure buttons
        self.show_password.clicked.connect(self.showPassword)
        self.button_layout.addWidget(self.show_password)

        done = QPushButton("Done")
        done.clicked.connect(self.done)
        self.button_layout.addWidget(done)

    # Save new item and close window
    def done(self):
        name = self.name.text()
        username = self.username.text()
        password = self.password.text()
        self.main_window.addPassword(name, username, password)
        self.close()

# Window for showing details and editing items
class DetailsItemWindow(ItemWindow):
    def __init__(self, main_window, service, username, password, kontroller):
        super().__init__(main_window, kontroller)
        self.v_mini_button_layout = QVBoxLayout()
        self.h_mini_button_layout = QVBoxLayout()
        self.copy_password = QPushButton("Copy password")
        self.delete_button = QPushButton("Delete")
        self.edit_button = QPushButton("Edit")

        # Configure and add buttons to button layouts
        self.show_password.clicked.connect(self.showPassword)
        self.v_mini_button_layout.addWidget(self.show_password)

        self.v_mini_button_layout.addWidget(self.edit_button)
        self.edit_button.clicked.connect(self.edit)
        self.button_layout.addLayout(self.v_mini_button_layout)


        self.h_mini_button_layout.addWidget(self.copy_password)
        self.copy_password.clicked.connect(partial(self.copyPassword, service))

        self.h_mini_button_layout.addWidget(self.delete_button)
        self.delete_button.clicked.connect(self.delete)
        self.button_layout.addLayout(self.h_mini_button_layout)

        # Set the lines to show the data and to read only
        self.name.setText(service)
        self.name.setReadOnly(True)

        self.username.setText(username)
        self.username.setReadOnly(True)

        self.password.setText(password)
        self.password.setReadOnly(True)


    def copyPassword(self, service):
        self.main_window.copyPassword(service)

    # Reconfigure window to allow for editing details
    def edit(self):

        # Remove buttons unnecessary for editing
        self.v_mini_button_layout.removeWidget(self.edit_button)
        self.edit_button.deleteLater()
        self.h_mini_button_layout.removeWidget(self.delete_button)
        self.delete_button.deleteLater()
        
        # Make lines editable
        self.name.setReadOnly(False)
        self.username.setReadOnly(False)
        self.password.setReadOnly(False)

        # Configure "Done"-button at the place of "Copy_password"
        self.copy_password.setText("Done")
        self.copy_password.clicked.disconnect()
        self.copy_password.clicked.connect(partial(self.done, self.name.text(), self.username.text(), self.password.text()))

    # Save changed details and close window
    def done(self, original_name, original_username, original_password):
        new_name = self.name.text()
        new_username = self.username.text()
        new_password = self.password.text()

        if new_name != original_name:
            self.KONTROLLER.editServicename(original_name, new_name)
        if new_username != original_username:
            self.KONTROLLER.editUsername(new_name, new_username)
        if new_password != original_password:
            self.KONTROLLER.editPassword(new_name, new_password)

        self.main_window.services = self.KONTROLLER.getNamesAndUsernames()

        self.main_window.buildManager()
        self.close()
        

    def delete(self):
        self.KONTROLLER.deleteItem(self.name.text())
        self.main_window.buildManager()
        self.close()
        

def start(kontroller):
    app = QApplication([])
    w = MainWindow(kontroller)
    w.show()
    app.exec()
