from PyQt5.QtWidgets import QFrame, QLabel, QLineEdit, QPushButton, QCommandLinkButton
from PyQt5.QtWidgets import QStatusBar, QWidget, QMenuBar, QMainWindow
from PyQt5.QtCore import QRect, QSize
from PyQt5.QtGui import QFont
from PyQt5.Qt import Qt

from Misc import fetchWindowIcon, createFont
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
        LoginWindow.setWindowFlags(Qt.FramelessWindowHint)
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
        self.username_textfield.setGeometry(QRect(90, 110, 231, 31))
        self.username_textfield.setFont(font)
        self.username_textfield.setMaxLength(100)
        self.username_textfield.setFrame(False)
        self.username_textfield.setEchoMode(QLineEdit.Normal)
        self.username_textfield.setClearButtonEnabled(True)
        self.username_textfield.setObjectName("username_textfield")
        self.username_textfield.mousePressEvent = self.mousePressEvent

        self.password_textfield = QLineEdit(self.background_frame)
        self.password_textfield.setGeometry(QRect(90, 170, 231, 31))
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
        self.cancel_button.clicked.connect(exit)

        self.forgot_password_link_button = QCommandLinkButton(self.background_frame)
        self.forgot_password_link_button.setGeometry(QtCore.QRect(80, 320, 201, 41))
        self.forgot_password_link_button.setObjectName("forgot_password_link_button")

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

        font = QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        self.login_result = QLabel(self.background_frame)
        self.login_result.setGeometry(QtCore.QRect(90, 210, 221, 16))
        self.login_result.setFont(font)
        self.login_result.setObjectName("login_result")

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
        self.username_textfield.setText("Extarminator")
        self.password_textfield.setText("GreatPassword")

        threading.Thread(target=self.client.recv_msg, daemon=True).start()
        self.thread_worker.finished.connect(self.loadMainChatWindow)
        self.thread_worker.start()

    def retranslateUi(self, login_screen):
        _translate = QtCore.QCoreApplication.translate
        login_screen.setWindowTitle(_translate("Welcome to PyChat", "Welcome to PyChat"))
        self.headline_label.setText(_translate("MainWindow", "Login Zone"))
        self.username_textfield.setText(_translate("MainWindow", "Your Username..."))
        self.password_textfield.setText(_translate("MainWindow", "password"))
        self.login_button.setText(_translate("MainWindow", "Login"))
        self.forgot_password_link_button.setText(_translate("MainWindow", "Forgot Your Password?"))
        self.signin_label.setText(_translate("MainWindow", "Sign In With:"))
        self.cancel_button.setText(_translate("MainWindow", "Cancel"))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and self.username_textfield.hasFocus() is True:
            self.login_button.click()

        if event.key() == Qt.Key_Return and self.password_textfield.hasFocus() is True:
            self.login_button.click()

        if event.key() == Qt.Key_Enter and self.username_textfield.hasFocus() is True:
            self.login_button.click()

        if event.key() == Qt.Key_Enter and self.password_textfield.hasFocus() is True:
            self.login_button.click()

        if event.key() == Qt.Key_Escape:
            exit(0)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.username_textfield.hasFocus() is True:
            self.username_textfield.setText("")

        if event.button() == Qt.LeftButton and self.password_textfield.hasFocus() is True:
            self.password_textfield.setText("")

    def login(self):
        username = self.username_textfield.text()
        password = self.password_textfield.text()
        self.client.send_msg(PROTOCOLS["login_request"], username + "#" + password)
        self.login_button.setDisabled(True)

    def update(self, notif, data):
        if notif == "LOGIN_ERROR":
            time.sleep(0.5)
            self.login_result.setText("Invalid username or password.")
            self.login_result.setStyleSheet("color: rgb(236, 31, 39);")
            self.login_result.setText(" ")
            self.login_button.setEnabled(True)

        if notif == "LOGIN_OK":
            # notification to BOT
            self.client.send_msg(PROTOCOLS["bot_user_logged_in"], self.username_textfield.text())

            # Send beacon to load the MainChatScreen
            self.thread_worker.finished.emit(100)

    def loadMainChatWindow(self):
        self.thread_worker.terminate()
        self.main_window.close()
        self.client.detach(self)
        MainChatScreen.run(ClientTCP=self.client)


def run(ClientTCP):
    window = QMainWindow()
    next_screen = LoginScreen(ClientTCP=ClientTCP)
    next_screen.setupUi(window)
    window.show()
