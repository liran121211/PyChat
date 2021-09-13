from PyQt5.QtWidgets import QLabel, QWidget, QProgressBar, QMenuBar, QStatusBar, QApplication, QMainWindow
from PyQt5.QtCore import Qt

from Misc import fetchWindowIcon, createFont
from ThreadWorker import ThreadWorker
from Protocol import debugMessages
from Misc import fetchSound, fetchImages

import random
import threading
import time
import sys
import LoginScreen
import Client
import typing

# noinspection PyUnresolvedReferences
from StyleSheets.loading_screen_css import *


class LoadingScreen(object):
    def __init__(self):
        self.client = Client.ClientTCP()
        self.thread_worker = ThreadWorker()
        self.client.attach(self)
        self.window_loaded = False

    def setupUi(self, LoadingWindow):
        self.main_window = LoadingWindow

        LoadingWindow.setObjectName("LoadingWindow")
        LoadingWindow.setFixedSize(672, 395)
        LoadingWindow.setWindowIcon(fetchWindowIcon())
        LoadingWindow.setWindowFlags(Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        LoadingWindow.setAttribute(Qt.WA_TranslucentBackground, True)

        self.centralwidget = QWidget(LoadingWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.background_image = QLabel(self.centralwidget)
        self.background_image.setGeometry(QtCore.QRect(0, 0, 671, 381))
        self.background_image.setStyleSheet("background-image: url(:/logo/pychat_logo.png);")
        self.background_image.setObjectName("background_image")

        self.loading_bar = QProgressBar(self.centralwidget)
        self.loading_bar.setGeometry(QtCore.QRect(180, 270, 311, 21))
        self.loading_bar.setInvertedAppearance(False)
        self.loading_bar.setObjectName("loading_bar")
        self.loading_bar.setStyleSheet(LOADING_CSS)
        self.loading_bar.setProperty("value", 0)
        self.loading_bar.setTextVisible(False)

        self.loading_label = QLabel(self.centralwidget)
        self.loading_label.setGeometry(QtCore.QRect(180, 300, 500, 21))
        self.loading_label.setFont(createFont("Arial Rounded MT Bold", 10, False, 40))
        self.loading_label.setObjectName("loading_label")
        LoadingWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(LoadingWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 677, 21))
        self.menubar.setObjectName("menubar")
        LoadingWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(LoadingWindow)
        self.statusbar.setObjectName("statusbar")
        LoadingWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoadingWindow)
        QtCore.QMetaObject.connectSlotsByName(LoadingWindow)

        # Misc...
        threading.Thread(target=self.client.setup, daemon=True).start()
        self.initProgressBar()

    # noinspection PyUnresolvedReferences
    def initProgressBar(self):
        def setProgressVal(val):
            self.loading_bar.setValue(val)

        def finishedProgressBar():
            if self.window_loaded is False:
                self.window_loaded = True
                self.loading_bar.setValue(100)
                self.thread_worker.terminate()
                self.main_window.close()
                self.client.detach(self)
                LoginScreen.run(ClientTCP=self.client)

        self.thread_worker.progress.connect(setProgressVal)
        self.thread_worker.finished.connect(finishedProgressBar)
        self.thread_worker.start()

    def retranslateUi(self, LoadingWindow):
        _translate = QtCore.QCoreApplication.translate
        LoadingWindow.setWindowTitle(_translate("Initializing PyChat...", "Initializing PyChat..."))
        self.loading_label.setText(_translate("LoadingWindow", "Loading sound files....."))

    # noinspection PyUnresolvedReferences
    def update(self, notif: typing.AnyStr, data: typing.AnyStr) -> None:
        """
        Get notifications from client TCP module.
        :param notif: cmd (String) of command.
        :param data: message with data (String)
        :return: None
        """
        time.sleep(random.uniform(0.2, 1))
        if notif == "GRAPHICS_LOAD":
            fetchSound()
            fetchImages()
            self.thread_worker.progress.emit(10)
            self.loading_label.setText(debugMessages(notif, False))

        if notif == "CONNECT":
            self.thread_worker.progress.emit(50)
            self.loading_label.setText(debugMessages(notif, False))

        if notif == "TIMEOUT":
            # noinspection PyUnresolvedReferences
            self.thread_worker.progress.emit(50)
            self.loading_label.setText(debugMessages(notif, False))

        if notif == "CONNECTED":
            self.thread_worker.progress.emit(70)
            self.loading_label.setText(debugMessages(notif, False))

        if notif == "CLIENT_DB_CONNECT":
            self.thread_worker.progress.emit(90)
            self.loading_label.setText(debugMessages(notif, False))

        if notif == "RETRY_DB_CONNECTION":
            self.thread_worker.progress.emit(90)
            self.loading_label.setText(debugMessages(notif, False))

        if notif == "DB_CONNECTION_ERROR":
            self.thread_worker.progress.emit(90)
            self.loading_label.setText(debugMessages(notif, False))

        if notif == "CLIENT_DB_CONNECTED":
            self.loading_label.setText(debugMessages(notif, False))
            self.thread_worker.finished.emit(100)


def run() -> None:
    """
    Main function, Initializing the GUI Process.
    :return: None
    """
    app = QApplication(sys.argv)
    window = QMainWindow()
    next_window = LoadingScreen()
    next_window.setupUi(window)
    window.show()
    sys.exit(app.exec_())


def restart() -> None:
    """
    Restart application.
    :return: None
    """
    window = QMainWindow()
    next_window = LoadingScreen()
    next_window.setupUi(window)
    window.show()
