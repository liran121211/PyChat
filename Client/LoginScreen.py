# © 2021 Liran Smadja. All rights reserved.

import sys
import typing

from PyQt5.QtWidgets import QFrame, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QStatusBar, QWidget, QMenuBar, QMainWindow
from PyQt5.QtCore import QRect, QSize
from PyQt5.QtGui import QFont, QKeyEvent, QMouseEvent
from PyQt5.Qt import Qt

import Client
from Misc import fetchWindowIcon, createFont, randomColor, toHex
from ThreadWorker import ThreadWorker
from Observable import Observable
from Protocol import PROTOCOLS

import MainChatScreen
import threading
import time

# noinspection PyUnresolvedReferences
from StyleSheets.login_screen_css import *


class LoginScreen(Observable):
    def __init__(self, ClientTCP):
        Observable.__init__(self)
        self.client = ClientTCP
        self.client.attach(self)
        self.thread_worker = ThreadWorker()

    def setupUi(self, LoginWindow):
        self.main_window = LoginWindow

        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.setFixedSize(678, 582)
        LoginWindow.setWindowIcon(fetchWindowIcon())
        LoginWindow.setAttribute(Qt.WA_TranslucentBackground, True)
        LoginWindow.setWindowFlags(Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        LoginWindow.keyPressEvent = self.keyPressEvent

        self.centralwidget = QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.background_frame = QFrame(self.centralwidget)
        self.background_frame.setObjectName(u"background_frame")
        self.background_frame.setGeometry(QRect(0, 0, 670, 542))
        self.background_frame.setFrameShape(QFrame.Box)
        self.background_frame.setFrameShadow(QFrame.Raised)
        self.background_frame.setStyleSheet("""background-color: rgb(255, 255, 255);""")

        self.logo_background = QLabel(self.background_frame)
        self.logo_background.setGeometry(QRect(337, 2, 331, 521))
        self.logo_background.setStyleSheet("image: url(:/window_logo/login_logo.png);")

        self.headline_label = QLabel(self.background_frame)
        self.headline_label.setGeometry(QRect(100, 20, 191, 51))
        self.headline_label.setFont(createFont("Comic Sans MS", 28, False, 40))
        self.headline_label.setObjectName("headline_label")

        font = QFont()
        font.setFamily("Comic Sans MS")
        font.setStyleStrategy(QFont.PreferDefault)
        self.username_textfield = QLineEdit(self.background_frame)
        self.username_textfield.setGeometry(QRect(90, 110, 231, 29))
        self.username_textfield.setFont(font)
        self.username_textfield.setMaxLength(100)
        self.username_textfield.setFrame(False)
        self.username_textfield.setEchoMode(QLineEdit.Normal)
        self.username_textfield.setClearButtonEnabled(True)
        self.username_textfield.setObjectName("username_textfield")
        self.username_textfield.mousePressEvent = self.mousePressEvent

        self.password_textfield = QLineEdit(self.background_frame)
        self.password_textfield.setGeometry(QRect(90, 170, 231, 29))
        self.password_textfield.setFrame(False)
        self.password_textfield.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password_textfield.setClearButtonEnabled(True)
        self.password_textfield.setObjectName("password_textfield")
        self.password_textfield.mousePressEvent = self.mousePressEvent

        self.password_icon_label = QLabel(self.background_frame)
        self.password_icon_label.setGeometry(QRect(30, 160, 61, 41))
        self.password_icon_label.setStyleSheet("image: url(:/password_icon/password_icon1.png);")
        self.password_icon_label.setText("")
        self.password_icon_label.setObjectName("password_icon_label")

        self.username_icon_label = QLabel(self.background_frame)
        self.username_icon_label.setGeometry(QRect(40, 100, 51, 41))
        self.username_icon_label.setStyleSheet("image: url(:/username_icon/username_icon1.png);")
        self.username_icon_label.setText("")
        self.username_icon_label.setObjectName("username_icon_label")

        font = QFont()
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.username_line = QFrame(self.background_frame)
        self.username_line.setFrameShape(QFrame.HLine)
        self.username_line.setFrameShadow(QFrame.Sunken)
        self.username_line.setGeometry(QRect(90, 130, 231, 20))
        self.username_line.setObjectName("username_line")
        self.username_line.setEnabled(True)
        self.username_line.setFont(font)
        self.username_line.setLineWidth(1)

        self.login_button = QPushButton(self.background_frame)
        self.login_button.setGeometry(QRect(70, 250, 111, 41))
        self.login_button.setStyleSheet(LOGIN_BTN)
        self.login_button.setObjectName("login_button")
        self.login_button.clicked.connect(self.login)

        self.cancel_button = QPushButton(self.background_frame)
        self.cancel_button.setGeometry(QRect(190, 250, 111, 41))
        self.cancel_button.setStyleSheet(CANCEL_BTN)
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.clicked.connect(lambda: sys.exit(1))

        self.register_button = QPushButton(self.background_frame)
        self.register_button.setGeometry(QtCore.QRect(228, 210, 71, 21))
        self.register_button.setObjectName("register_button")
        self.register_button.setStyleSheet(TO_REGISTRATION_BTN)
        self.register_button.setFont(createFont("MS Shell Dlg 2", 8, False, 20))
        self.register_button.clicked.connect(self.registerForm)

        self.google_logo_label = QLabel(self.background_frame)
        self.google_logo_label.setGeometry(QRect(20, 470, 71, 51))
        self.google_logo_label.setStyleSheet("image: url(:/fast_login_icons/google_login_logo.png);")
        self.google_logo_label.setText("")
        self.google_logo_label.setObjectName("google_logo_label")

        self.facebook_logo_label = QLabel(self.background_frame)
        self.facebook_logo_label.setGeometry(QRect(90, 470, 71, 51))
        self.facebook_logo_label.setStyleSheet("image: url(:/fast_login_icons/facebook_login_logo.png);")
        self.facebook_logo_label.setText("")
        self.facebook_logo_label.setObjectName("facebook_logo_label")

        self.linkedin_logo_label = QLabel(self.background_frame)
        self.linkedin_logo_label.setGeometry(QRect(160, 470, 71, 51))
        self.linkedin_logo_label.setStyleSheet("image: url(:/fast_login_icons/linkedin_login_logo.png);")
        self.linkedin_logo_label.setText("")
        self.linkedin_logo_label.setObjectName("linkedin_logo_label")

        self.twitter_logo_label = QLabel(self.background_frame)
        self.twitter_logo_label.setGeometry(QRect(230, 470, 71, 51))
        self.twitter_logo_label.setStyleSheet("image: url(:/fast_login_icons/twitter_login_logo.png);")
        self.twitter_logo_label.setText("")
        self.twitter_logo_label.setObjectName("twitter_logo_label")

        font = QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.signin_label = QLabel(self.background_frame)
        self.signin_label.setGeometry(QRect(30, 430, 111, 31))
        self.signin_label.setFont(font)
        self.signin_label.setObjectName("signin_label")

        font = QFont()
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.password_line = QFrame(self.background_frame)
        self.password_line.setEnabled(True)
        self.password_line.setGeometry(QRect(90, 190, 231, 20))
        self.password_line.setFont(font)
        self.password_line.setLineWidth(1)
        self.password_line.setFrameShape(QFrame.HLine)
        self.password_line.setFrameShadow(QFrame.Sunken)
        self.password_line.setObjectName("password_line")

        self.password_register_line = QFrame(self.background_frame)
        self.password_register_line.setEnabled(True)
        self.password_register_line.setGeometry(QRect(90, 250, 231, 20))
        self.password_register_line.setFont(font)
        self.password_register_line.setLineWidth(1)
        self.password_register_line.setFrameShape(QFrame.HLine)
        self.password_register_line.setFrameShadow(QFrame.Sunken)
        self.password_register_line.setObjectName("password_register_line")
        self.password_register_line.hide()

        self.password_register_textfield = QLineEdit(self.background_frame)
        self.password_register_textfield.setGeometry(QRect(90, 230, 231, 29))
        self.password_register_textfield.setFrame(False)
        self.password_register_textfield.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password_register_textfield.setClearButtonEnabled(True)
        self.password_register_textfield.setObjectName("password_register_textfield")
        self.password_register_textfield.mousePressEvent = self.mousePressEvent
        self.password_register_textfield.hide()

        self.password_register_icon_label = QLabel(self.background_frame)
        self.password_register_icon_label.setGeometry(QRect(30, 230, 61, 41))
        self.password_register_icon_label.setStyleSheet("image: url(:/password_icon/password_icon1.png);")
        self.password_register_icon_label.setText("")
        self.password_register_icon_label.setObjectName("password_icon_label")
        self.password_register_icon_label.hide()

        font = QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.register_text_label = QLabel(self.background_frame)
        self.register_text_label.setGeometry(QtCore.QRect(80, 210, 149, 21))
        self.register_text_label.setFont(font)
        self.register_text_label.setObjectName("register_text_label")
        self.register_text_label.setText("Don't have a PyChat Account?")

        self.login_result = QLabel(self.background_frame)
        self.login_result.setGeometry(QtCore.QRect(75, 310, 221, 25))
        self.login_result.setFont(createFont("MS Shell Dlg 2", 10, False, 20))
        self.login_result.setObjectName("login_result")
        self.login_result.setAlignment(Qt.AlignCenter)
        self.login_result.hide()

        font = QFont()
        font.setUnderline(False)
        self.line = QFrame(self.background_frame)
        self.line.setFont(font)
        self.line.setGeometry(QRect(330, 11, 20, 527))
        self.line.setMinimumSize(QSize(0, 527))
        self.line.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.line.setFrameShadow(QFrame.Raised)
        self.line.setLineWidth(0)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setObjectName("line")

        LoginWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(LoginWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 678, 21))
        self.menubar.setObjectName("menubar")
        LoginWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(LoginWindow)
        self.statusbar.setObjectName("statusbar")
        LoginWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

        # Manual components settings
        self.username_textfield.setText("Enter your username...")
        self.password_textfield.setText("Password")

        threading.Thread(target=self.client.recv_msg, daemon=True).start()
        self.thread_worker.finished.connect(self.loadMainChatWindow)
        self.thread_worker.start()

        self.login_result.raise_()
        self.username_textfield.raise_()
        self.password_textfield.raise_()

    def retranslateUi(self, login_screen):
        _translate = QtCore.QCoreApplication.translate
        login_screen.setWindowTitle(_translate("Welcome to PyChat", "Welcome to PyChat"))
        self.headline_label.setText(_translate("MainWindow", "Login Zone"))
        self.username_textfield.setText(_translate("MainWindow", "Your Username..."))
        self.password_textfield.setText(_translate("MainWindow", "password"))
        self.login_button.setText(_translate("MainWindow", "Login"))
        self.register_button.setText(_translate("MainWindow", "Register now"))
        self.signin_label.setText(_translate("MainWindow", "Sign In With:"))
        self.cancel_button.setText(_translate("MainWindow", "Cancel"))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Triggered when key is pressed in GUI window.
        :param event: (QKeyEvent) object
        :return: None
        """
        if event.key() == Qt.Key_Return and self.username_textfield.hasFocus() is True:
            self.login_button.click()

        if event.key() == Qt.Key_Return and self.password_textfield.hasFocus() is True:
            self.login_button.click()

        if event.key() == Qt.Key_Enter and self.username_textfield.hasFocus() is True:
            self.login_button.click()

        if event.key() == Qt.Key_Enter and self.password_textfield.hasFocus() is True:
            self.login_button.click()

        if event.key() == Qt.Key_Escape:
            sys.exit(1)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Triggered when mouse key is pressed in GUI window.
        :param event: (QMouseEvent) object.
        :return: None
        """
        if event.button() == Qt.LeftButton and self.username_textfield.hasFocus() is True:
            self.username_textfield.setText("")

        if event.button() == Qt.LeftButton and self.password_textfield.hasFocus() is True:
            self.password_textfield.setText("")

        if event.button() == Qt.LeftButton and self.password_register_textfield.hasFocus() is True:
            self.password_register_textfield.setText("")

    def login(self) -> None:
        """
        Send authentication request to the server.
        :return: None
        """
        username = self.username_textfield.text().replace('#', '')
        password = self.password_textfield.text().replace('#', '')
        self.client.send_msg(PROTOCOLS["login_request"], username + "#" + password)
        self.login_button.setEnabled(False)

    def update(self, notif: typing.AnyStr, data: typing.AnyStr) -> None:
        """
        Get notifications from client TCP module.
        :param notif: cmd (String) of command.
        :param data: message with data (String)
        :return: None
        """
        if notif == "LOGIN_ERROR":
            self.login_result.hide()
            self.login_button.setEnabled(True)
            self.login_result.setStyleSheet(ERROR_LOGIN_LABEL_CSS)
            self.login_result.setText("Invalid username or password")
            self.login_result.show()
            time.sleep(2)
            self.login_result.hide()

        if notif == "LOGIN_OK":
            # Send beacon to load the MainChatScreen
            self.thread_worker.finished.emit(100)

        if notif == "REGISTER_USER":
            if data == "SUCCESS":
                self.cancel_button.click()
                self.login_result.setStyleSheet(SUCCESS_REGISTRATION_LABEL_CSS)
                self.login_result.setText("You have successfully signed up for PyChat")
                self.register_button.setEnabled(False)
                self.login_result.show()

            elif data == "FAIL":
                self.cancel_button.click()
                self.login_result.setStyleSheet(ERROR_LOGIN_LABEL_CSS)
                self.login_result.setText("Something went wrong...")
                self.login_result.show()

            elif data == "USERNAME_EXIST":
                self.login_button.setEnabled(True)
                self.login_button.setText("Register")
                self.login_result.setStyleSheet(ERROR_LOGIN_LABEL_CSS)
                self.login_result.setText("Username already exists!")
                self.login_result.show()

    def loadMainChatWindow(self) -> None:
        """
        Load next window (MainChatWindow).
        Detach Client TCP object from the current GUI.
        :return: None
        """

        # notification to BOT
        self.client.send_msg(PROTOCOLS["bot_user_logged_in"], self.username_textfield.text())

        self.thread_worker.terminate()
        self.main_window.close()
        self.client.detach(self)
        MainChatScreen.run(ClientTCP=self.client)

    def registerForm(self) -> None:
        """
        Load Registration Form and replace the current Login Form.
        :return: None
        """
        font = QFont()
        font.setFamily("Comic Sans MS")

        self.login_button.hide()
        self.cancel_button.hide()
        self.register_button.hide()
        self.register_text_label.hide()
        self.login_button.setText("Register")
        self.login_button.clicked.disconnect()
        self.login_button.clicked.connect(self.registerProcess)
        self.cancel_button.clicked.disconnect()
        self.cancel_button.clicked.connect(self.LoginForm)

        self.login_result.setGeometry(QtCore.QRect(41, 350, 280, 25))
        self.login_button.setGeometry(QtCore.QRect(70, 290, 111, 41))
        self.cancel_button.setGeometry(QtCore.QRect(190, 290, 111, 41))

        self.login_button.setStyleSheet(REGISTER_BTN_CSS)
        self.login_result.setStyleSheet(ERROR_LOGIN_LABEL_CSS)

        self.password_textfield.setEchoMode(QLineEdit.Normal)
        self.password_register_textfield.setEchoMode(QLineEdit.Normal)

        self.password_textfield.setFont(font)
        self.password_register_textfield.setFont(font)
        self.username_textfield.setText("Enter a username...")
        self.password_textfield.setText("Enter your password...")
        self.password_register_textfield.setText("Enter your password again...")

        self.login_button.show()
        self.cancel_button.show()
        self.password_register_line.show()
        self.password_register_textfield.show()
        self.password_register_icon_label.show()

    def registerProcess(self) -> None:
        """
        Gather all required data and send the registration form to the server.
        :return: None
        """

        # validate data before preceding with the registration process.
        validation = self.formValidator()

        if validation == "VALIDATED":
            self.login_button.setEnabled(False)
            self.login_button.setText("Registering...")

            R, G, B = randomColor()
            username = self.username_textfield.text().replace('#', '') + '#'
            password = self.password_textfield.text().replace('#', '') + '#'
            online = "False#"
            ip_address = "0.0.0.0:00000#"
            avatar = "{0}.svg#".format(self.username_textfield.text())
            status = "AVAILABLE#"
            room = "GENERAL#"
            color = toHex(R, G, B)
            data = username + password + online + ip_address + avatar + status + room + color
            self.client.send_msg(PROTOCOLS["register_user"], data)
        else:
            self.login_button.setEnabled(True)
            self.login_result.setText(validation)
            self.login_result.show()

    def LoginForm(self) -> None:
        """
        Load Login Form and replace the current Registration Form.
        :return: None
        """
        self.login_button.setEnabled(True)

        self.login_button.hide()
        self.cancel_button.hide()
        self.register_text_label.hide()
        self.register_button.hide()

        self.login_result.setGeometry(QtCore.QRect(50, 310, 260, 25))
        self.login_button.setGeometry(QRect(73, 250, 111, 41))
        self.cancel_button.setGeometry(QRect(190, 250, 111, 41))

        self.login_button.setStyleSheet(LOGIN_BTN)
        self.password_textfield.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        font = QFont()
        font.setFamily("Comic Sans MS")
        self.password_textfield.setFont(font)
        self.password_register_textfield.setFont(font)
        self.username_textfield.setText("Enter your username...")
        self.password_textfield.setText("Password")
        self.login_button.setText("Login")

        self.login_button.clicked.disconnect()
        self.login_button.clicked.connect(self.login)
        self.cancel_button.clicked.disconnect()
        self.cancel_button.clicked.connect(lambda: sys.exit(1))

        self.password_register_line.hide()
        self.password_register_textfield.hide()
        self.password_register_icon_label.hide()
        self.login_button.show()
        self.cancel_button.show()
        self.register_text_label.show()
        self.register_button.show()


    def formValidator(self) -> typing.AnyStr:
        """
        Avoid invalid data and look up for errors before dispatching the Registration Form.
        :return: None
        """
        if len(self.username_textfield.text()) > 12:
            return "Username contains more than 12 characters."

        if ' ' in self.username_textfield.text():
            return "Username can not contain spaces."

        if '#' in self.username_textfield.text():
            return "Username can not contain (#) character."

        if self.password_textfield.text() != self.password_register_textfield.text():
            return "Passwords do not match."

        if len(self.password_textfield.text()) > 12 or len(self.password_register_textfield.text()) > 12:
            return "Password contains more than 12 characters."

        if ' ' in self.password_textfield.text() or ' ' in self.password_register_textfield.text():
            return "Password can not contain spaces."

        if '#' in self.password_textfield.text() or '#' in self.password_register_textfield.text():
            return "Password can not contain (#) character."

        return "VALIDATED"


def run(ClientTCP: Client.ClientTCP) -> None:
    """
    Main function, Initializing the GUI Process.
    :param ClientTCP: Client module.
    :return: None
    """
    window = QMainWindow()
    next_screen = LoginScreen(ClientTCP=ClientTCP)
    next_screen.setupUi(window)
    window.show()

# © 2021 Liran Smadja. All rights reserved.