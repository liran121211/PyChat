import time

from Protocol import debugMessages
from PyQt5 import QtCore, QtGui, QtWidgets
import CSS.loading_screen_css

class LoadingScreen(object):
    def __init__(self):
        self.name = "LoadingWindow"
        self.LoadingWindow = None

    def setupUi(self, LoadingWindow):
        LoadingWindow.setObjectName("LoadingWindow")
        LoadingWindow.setStyleSheet("")
        LoadingWindow.setFixedSize(672, 395)

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
        self.loading_bar.setStyleSheet("""#loading_bar::chunk {background-color: #2196F3;width: 10px; margin: 0.5px;}""")

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
        self.LoadingWindow = LoadingWindow

    def retranslateUi(self, LoadingWindow):
        _translate = QtCore.QCoreApplication.translate
        LoadingWindow.setWindowTitle(_translate("LoadingWindow", "MainWindow"))
        self.loading_label.setText(_translate("LoadingWindow", "Loading text area....."))

    def update(self, observable, cmd):
        if cmd == "GRAPHICS_LOAD":
            self.loading_bar.setValue(10)
            self.loading_label.setText(debugMessages(cmd))

        if cmd == "CONNECT":
            self.loading_bar.setValue(50)
            self.loading_label.setText(debugMessages(cmd))

        if cmd == "TIMEOUT":
            self.loading_bar.setValue(50)
            self.loading_label.setText(debugMessages(cmd))

        if cmd == "CONNECTED":
            self.loading_bar.setValue(70)
            self.loading_label.setText(debugMessages(cmd))

        if cmd == "CLIENT_DB_CONNECT":
            self.loading_bar.setValue(90)
            self.loading_label.setText(debugMessages(cmd))

        if cmd == "DB_CONNECTION_ERROR":
            self.loading_bar.setValue(90)
            self.loading_label.setText(debugMessages(cmd))

        if cmd == "CLIENT_DB_CONNECTED":
            self.loading_bar.setValue(99)
            self.loading_label.setText(debugMessages(cmd))
            time.sleep(0.5)
            self.LoadingWindow.close()