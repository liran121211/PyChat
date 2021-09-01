# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainChatScreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from Protocol import *
from Observable import Observable
import CSS.main_chat_screen_css


class MainChatScreen(Observable):
    def __init__(self):
        Observable.__init__(self)
        self.client_data = None
        self.chat_history = ""
        self.threads = {}

    def setupUi(self, MainChatWindow):
        MainChatWindow.setObjectName("MainChatWindow")
        MainChatWindow.resize(1574, 832)
        MainChatWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainChatWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_chat_textbox = QtWidgets.QTextBrowser(self.centralwidget)
        self.main_chat_textbox.setEnabled(True)
        self.main_chat_textbox.setGeometry(QtCore.QRect(330, 60, 1001, 631))
        self.main_chat_textbox.setObjectName("main_chat_textbox")
        self.online_users_list = QtWidgets.QListView(self.centralwidget)
        self.online_users_list.setGeometry(QtCore.QRect(1340, 60, 221, 631))
        self.online_users_list.setObjectName("online_users_list")
        self.chat_rooms_list = QtWidgets.QListView(self.centralwidget)
        self.chat_rooms_list.setGeometry(QtCore.QRect(10, 60, 311, 631))
        self.chat_rooms_list.setObjectName("chat_rooms_list")
        self.message_textfield = QtWidgets.QLineEdit(self.centralwidget)
        self.message_textfield.setGeometry(QtCore.QRect(330, 700, 991, 41))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.message_textfield.setFont(font)
        self.message_textfield.setStyleSheet("background-color: rgb(243, 243, 243);\n"
                                             "border-radius: 10px;\n"
                                             "color: rgb(95, 95, 95);")
        self.message_textfield.setClearButtonEnabled(False)
        self.message_textfield.setObjectName("message_textfield")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 710, 61, 41))
        self.label.setStyleSheet("background-image: url(\"static.thenounproject.com/png/373675-200.png\")")
        self.label.setObjectName("label")
        self.username_label = QtWidgets.QLabel(self.centralwidget)
        self.username_label.setGeometry(QtCore.QRect(80, 710, 61, 41))
        self.username_label.setObjectName("username_label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(150, 720, 61, 21))
        self.label_3.setObjectName("label_3")
        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_button.setGeometry(QtCore.QRect(1280, 710, 31, 21))
        self.send_button.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.send_button.setStyleSheet("image: url(:/send_button/send_button1.png);\n"
                                       "background-color: rgb(243, 243, 243);\n"
                                       "border: 0px;\n"
                                       "")
        self.send_button.setText("")
        self.send_button.setAutoDefault(False)
        self.send_button.setObjectName("send_button")
        MainChatWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainChatWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1574, 21))
        self.menubar.setObjectName("menubar")
        MainChatWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainChatWindow)
        self.statusbar.setObjectName("statusbar")
        MainChatWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainChatWindow)
        QtCore.QMetaObject.connectSlotsByName(MainChatWindow)

        # other specifications
        self.username_label.setText(self.client_data["username"])
        self.send_button.clicked.connect(self.sendMessage)
        self.message_textfield.textEdited.connect(self.messageFieldStatus)
        MainChatWindow.keyPressEvent = self.keyPressEvent

        self.model = QStandardItemModel(self.online_users_list)

    def retranslateUi(self, MainChatWindow):
        _translate = QtCore.QCoreApplication.translate
        MainChatWindow.setWindowTitle(_translate("MainChatWindow", "MainWindow"))
        self.label.setText(_translate("MainChatWindow", "UserImage"))
        self.username_label.setText(_translate("MainChatWindow", "username..."))
        self.label_3.setText(_translate("MainChatWindow", "tools images"))

    def updateChat(self, data):
        def threadWorker():
            self.chat_history += self.main_chat_textbox.toPlainText()
            self.main_chat_textbox.append(data)

        self.threads["UPDATE_CHAT"] = threading.Thread(target=threadWorker)
        self.threads["UPDATE_CHAT"].start()

    def sendMessage(self):
        self.send_button.setHidden(True)
        self.notify(build_message(PROTOCOLS["client_message"], self.message_textfield.text()))
        self.message_textfield.setText("")

    def messageFieldStatus(self):
        if self.message_textfield.text() != "":
            self.send_button.setVisible(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and self.message_textfield.hasFocus() == True:
            self.sendMessage()

    def updateUserList(self, user_lst):
        def threadWorker():
            self.model.clear()
            for username in user_lst:
                item = QStandardItem(username)
                item.setCheckable(True)
                self.model.appendRow(item)
            self.online_users_list.setModel(self.model)
            self.online_users_list.update()

        self.threads["UPDATE_USERS_LIST"] = threading.Thread(target=threadWorker)
        self.threads["UPDATE_USERS_LIST"].start()

# class WorkThread(QtCore.QThread):
#     update_chat_box = QtCore.pyqtSignal(object)
#     def __init__(self):
#         super().__init__()
#         self.info = None
#
#     def run(self):
#         self.statusMessage.emit(self.info)
