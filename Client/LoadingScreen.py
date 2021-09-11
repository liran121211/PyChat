import random
import threading
import time
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

import Client
from Misc import fetchAppIcon
from ThreadWorker import ThreadWorker
from Protocol import debugMessages
import LoginScreen

# noinspection PyUnresolvedReferences
import StyleSheets.loading_screen_css


class LoadingScreen(object):
    def __init__(self):
        self.client = Client.ClientTCP()
        self.thread_worker = ThreadWorker()
        self.client.attach(self)

    def setupUi(self, LoadingWindow):
        self.main_window = LoadingWindow
        LoadingWindow.setObjectName("LoadingWindow")
        LoadingWindow.setStyleSheet("")
        LoadingWindow.setFixedSize(672, 395)
        LoadingWindow.setWindowIcon(fetchAppIcon())
        LoadingWindow.setWindowFlags(Qt.FramelessWindowHint)
        LoadingWindow.setAttribute(Qt.WA_TranslucentBackground)
        self.centralwidget = QtWidgets.QWidget(LoadingWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.background_image_label = QtWidgets.QLabel(self.centralwidget)
        self.background_image_label.setGeometry(QtCore.QRect(0, 0, 671, 381))
        self.background_image_label.setStyleSheet("background-image: url(:/logo/pychat_logo.png);")
        self.background_image_label.setText("")
        self.background_image_label.setObjectName("background_image_label")

        self.loading_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.loading_bar.setGeometry(QtCore.QRect(180, 270, 311, 21))
        self.loading_bar.setProperty("value", 0)
        self.loading_bar.setTextVisible(False)
        self.loading_bar.setInvertedAppearance(False)
        self.loading_bar.setObjectName("loading_bar")
        self.loading_bar.setStyleSheet(
            """#loading_bar::chunk {background-color: #2196F3;width: 10px; margin: 0.5px;}""")

        self.loading_label = QtWidgets.QLabel(self.centralwidget)
        self.loading_label.setGeometry(QtCore.QRect(180, 300, 500, 21))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(10)
        self.loading_label.setFont(font)
        self.loading_label.setObjectName("loading_label")
        LoadingWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(LoadingWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 677, 21))
        self.menubar.setObjectName("menubar")
        LoadingWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(LoadingWindow)
        self.statusbar.setObjectName("statusbar")
        LoadingWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoadingWindow)
        QtCore.QMetaObject.connectSlotsByName(LoadingWindow)

        threading.Thread(target=self.client.setup, daemon=True).start()
        self.initProgressBar()

    # noinspection PyUnresolvedReferences
    def initProgressBar(self):
        def setProgressVal(val):
            self.loading_bar.setValue(val)

        def finishedProgressBar():
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
        self.loading_label.setText(_translate("LoadingWindow", "Loading text area....."))

    # noinspection PyUnresolvedReferences
    def update(self, notif, data):
        time.sleep(random.uniform(0.2, 1))
        if notif == "GRAPHICS_LOAD":
            self.thread_worker.progress.emit(10)
            self.loading_label.setText(debugMessages(notif))

        if notif == "CONNECT":
            self.thread_worker.progress.emit(50)
            self.loading_label.setText(debugMessages(notif))

        if notif == "TIMEOUT":
            # noinspection PyUnresolvedReferences
            self.thread_worker.progress.emit(50)
            self.loading_label.setText(debugMessages(notif))

        if notif == "CONNECTED":
            self.thread_worker.progress.emit(70)
            self.loading_label.setText(debugMessages(notif))

        if notif == "CLIENT_DB_CONNECT":
            self.thread_worker.progress.emit(90)
            self.loading_label.setText(debugMessages(notif))


        if notif == "RETRY_DB_CONNECTION":
            self.thread_worker.progress.emit(90)
            self.loading_label.setText(debugMessages(notif))

        if notif == "DB_CONNECTION_ERROR":
            self.thread_worker.progress.emit(90)
            self.loading_label.setText(debugMessages(notif))

        if notif == "CLIENT_DB_CONNECTED":
            self.loading_label.setText(debugMessages(notif))
            self.thread_worker.finished.emit(100)


def run():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    LSF = LoadingScreen()
    LSF.setupUi(window)
    window.show()
    sys.exit(app.exec_())

def restart():
    window = QtWidgets.QMainWindow()
    LSF = LoadingScreen()
    LSF.setupUi(window)
    window.show()

if __name__ == "__main__":
    run()
