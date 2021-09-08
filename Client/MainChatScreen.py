# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainChatScreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QFrame, QMessageBox

from Delegates.MessageDelegate import MessageDelegate
from Delegates.OnlineUsersDelegate import OnlineUsersDelegate
from Delegates.ChatRoomsDelegate import ChatRoomsDelegate
from Models.MessagesModel import MessagesModel
from Models.OnlineUsersModel import OnlineUsersModel
from Models.ChatRoomsModel import ChatRoomsModel, ChatRoomItem
from Misc import randomColor, createFont, timeStamp, fetchAvatar, fetchIcon
from ThreadWorker import ThreadWorker
from Protocol import *
from Observable import Observable

# noinspection PyUnresolvedReferences
import StyleSheets.main_chat_screen_css


class MainChatScreen(Observable):
    def __init__(self, ClientTCP):
        Observable.__init__(self)
        self.client = ClientTCP
        self.client.attach(self)
        self.threads = {}
        self.thread_worker = ThreadWorker()
        self.finished_loading = False

    def setupUi(self, MainChatWindow):
        self.main_window = MainChatWindow
        MainChatWindow.setObjectName("MainChatWindow")
        MainChatWindow.resize(1574, 832)
        MainChatWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainChatWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.settings_frame = QFrame(self.centralwidget)
        self.settings_frame.setObjectName(u"settings_frame")
        self.settings_frame.setGeometry(QtCore.QRect(10, 700, 311, 41))
        self.settings_frame.setFrameShape(QFrame.Box)
        self.settings_frame.setFrameShadow(QFrame.Raised)
        self.settings_frame.setStyleSheet("background-color: rgb(243, 243, 243);\n"
                                          "border-radius: 10px;\ncolor: rgb(95, 95, 95);")

        self.main_chat = QtWidgets.QListView(self.centralwidget)
        self.main_chat.setGeometry(QtCore.QRect(330, 60, 1001, 631))
        self.main_chat.setObjectName("main_chat")
        self.main_chat.setItemDelegate(MessageDelegate())
        self.main_chat_model = MessagesModel()
        self.main_chat.setModel(self.main_chat_model)

        self.users_list = QtWidgets.QListView(self.centralwidget)
        self.users_list.setGeometry(QtCore.QRect(1340, 95, 221, 647))
        self.users_list.setObjectName("users_list")
        self.users_list.setItemDelegate(OnlineUsersDelegate())
        self.users_list_model = OnlineUsersModel()
        self.users_list.setModel(self.users_list_model)
        self.users_list.setStyleSheet("background-color: rgb(243, 243, 243);\n"
                                      "border-radius: 10px;\ncolor: rgb(95, 95, 95);\n")

        self.users_list_label = QtWidgets.QLabel(self.centralwidget)
        self.users_list_label.setObjectName(u"users_list_label")
        self.users_list_label.setText("-----------Online Users-----------")
        self.users_list_label.setAlignment(Qt.AlignCenter)
        self.users_list_label.setFont(createFont("Eras Medium ITC", 15, False, 50))
        self.users_list_label.setGeometry(QtCore.QRect(1340, 60, 221, 50))
        self.users_list_label.setStyleSheet(u"background-color: rgb(243, 243, 243);\n"
                                                 "border-radius: 10px;\n"
                                                 "color: rgb(95, 95, 95);")

        self.chat_rooms_list = QtWidgets.QTreeView(self.centralwidget)
        self.chat_rooms_list.setGeometry(QtCore.QRect(10, 50, 311, 641))
        self.chat_rooms_list.setObjectName("chat_rooms_list")
        self.chat_rooms_list.setItemDelegate(ChatRoomsDelegate())
        self.chat_rooms_list.setHeaderHidden(True)
        self.chat_rooms_list.doubleClicked.connect(self.userChangedRoom)
        self.chat_rooms_list.setStyleSheet("background-color: rgb(243, 243, 243);\n"
                                           "border-radius: 10px;\ncolor: rgb(95, 95, 95);\n")

        self.chat_rooms_list_label = QtWidgets.QLabel(self.centralwidget)
        self.chat_rooms_list_label.setObjectName(u"chat_rooms_list_label")
        self.chat_rooms_list_label.setText("--------------------Chat Rooms--------------------")
        self.chat_rooms_list_label.setAlignment(Qt.AlignCenter)
        self.chat_rooms_list_label.setFont(createFont("Eras Medium ITC", 15, False, 50))
        self.chat_rooms_list_label.setGeometry(QtCore.QRect(10, 0, 311, 65))
        self.chat_rooms_list_label.setStyleSheet(u"background-color: rgb(243, 243, 243);\n"
                                                 "border-radius: 10px;\n"
                                                 "color: rgb(95, 95, 95);")

        self.message_textfield = QtWidgets.QLineEdit(self.centralwidget)
        self.message_textfield.setGeometry(QtCore.QRect(350, 700, 931, 41))
        self.message_textfield.setStyleSheet("background-color: rgb(243, 243, 243);\n"
                                             "border-radius: 10px;\n"
                                             "color: rgb(95, 95, 95);")
        self.message_textfield.setClearButtonEnabled(False)
        self.message_textfield.setObjectName("message_textfield")
        self.message_textfield.setFont(createFont("Eras Medium ITC", 13, False, 50))

        self.user_avatar = QSvgWidget(self.settings_frame)
        self.user_avatar.setGeometry(10, 7, 30, 30)
        self.user_avatar.setObjectName("user_avatar")

        self.username_label = QtWidgets.QLabel(self.settings_frame)
        self.username_label.setGeometry(QtCore.QRect(50, 10, 121, 21))
        self.username_label.setObjectName("username_label")
        self.username_label.setFont(createFont("Eras Medium ITC", 14, False, 50))

        self.settings_button = QtWidgets.QPushButton(self.settings_frame)
        self.settings_button.setObjectName(u"settings_button")
        self.settings_button.setGeometry(QtCore.QRect(265, 6, 41, 31))
        self.settings_button.setStyleSheet("image: url(:/settings_button/settings2.png);")

        self.sound_button = QtWidgets.QPushButton(self.settings_frame)
        self.sound_button.setObjectName(u"settings_button")
        self.sound_button.setGeometry(QtCore.QRect(220, 6, 41, 31))
        self.sound_button.setStyleSheet("image: url(:/main_volume/volume.png);")
        self.sound_button.clicked.connect(self.soundButtonStatus)

        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_button.setGeometry(QtCore.QRect(1290, 710, 31, 21))
        self.send_button.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.send_button.setStyleSheet("image: url(:/send_button/send_button1.png);\n"
                                       "background-color: rgb(243, 243, 243);\n"
                                       "border: 0px;\n"
                                       "")
        self.send_button.setAutoDefault(False)
        self.send_button.setObjectName("send_button")

        self.textfield_label_right = QtWidgets.QLabel(self.centralwidget)
        self.textfield_label_right.setObjectName(u"textfield_label_right")
        self.textfield_label_right.setGeometry(QtCore.QRect(1270, 700, 61, 41))
        self.textfield_label_right.setStyleSheet(u"background-color: rgb(243, 243, 243);\n"
                                                 "border-radius: 10px;\n"
                                                 "color: rgb(95, 95, 95);")
        self.textfield_label_right.setFrameShape(QFrame.NoFrame)
        self.textfield_label_left = QtWidgets.QLabel(self.centralwidget)
        self.textfield_label_left.setObjectName(u"textfield_label_left")
        self.textfield_label_left.setFrameShape(QFrame.NoFrame)
        self.textfield_label_left.setGeometry(QtCore.QRect(330, 700, 61, 41))
        self.textfield_label_left.setStyleSheet(u"background-color: rgb(243, 243, 243);\n"
                                                "border-radius: 10px;\n"
                                                "color: rgb(95, 95, 95);")

        self.toolbar_frame = QFrame(self.centralwidget)
        self.toolbar_frame.setObjectName(u"toolbar_frame")
        self.toolbar_frame.setGeometry(QtCore.QRect(330, 0, 1231, 51))
        self.toolbar_frame.setFrameShape(QFrame.Box)
        self.toolbar_frame.setFrameShadow(QFrame.Raised)

        self.message_textfield.raise_()
        self.main_chat.raise_()
        self.chat_rooms_list.raise_()
        self.users_list.raise_()
        self.send_button.raise_()
        self.user_avatar.raise_()
        self.username_label.raise_()
        self.settings_button.raise_()

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
        self.main_window.closeEvent = self.closeEvent
        self.client.send_msg(PROTOCOLS["chat_rooms_names"], "")
        self.username_label.setText(self.client.client_db_info["username"])
        self.user_avatar.renderer().load(fetchAvatar(username=self.client.client_db_info["username"], obj_type="SVG"))
        self.send_button.clicked.connect(self.sendMessage)
        self.message_textfield.textEdited.connect(self.messageFieldStatus)
        MainChatWindow.keyPressEvent = self.keyPressEvent
        self.finished_loading = True

    def retranslateUi(self, MainChatWindow):
        _translate = QtCore.QCoreApplication.translate
        MainChatWindow.setWindowTitle(_translate("MainChatWindow", "MainWindow"))
        self.username_label.setText(_translate("MainChatWindow", "username..."))

    def update(self, notif, data=None):
        """
        Get notification from client interface
        :param notif: client command protocol
        :param data: client data.
        :return: None
        """
        if notif == "ONLINE_USERS":
            if self.finished_loading is True:
                self.updateUserList(data)

        if notif == "MESSAGE_TO_CLIENT":
            if self.finished_loading is True:
                self.updateChat(data)

        if notif == "CHAT_ROOMS_NAMES":
            self.initRoomsList(data)

        if notif == "CHAT_ROOMS_INFO":
            self.updateRoomsList(data)

        if notif == "BOT_USER_LOGGED_IN":
            self.updateChat(data)

        if notif == "BOT_USER_LOGGED_OUT":
            self.updateChat(data)

    def updateChat(self, data):
        username, message = data.split('#')
        model_index = self.main_chat_model.index(self.main_chat_model.rowCount(), 0)
        self.main_chat_model.insertData(model_index, (username, [180, 20, 50], timeStamp(), message))

    def sendMessage(self):
        if self.message_textfield.text() != "":
            dispatch_data = self.client.client_db_info["username"] + '#' + self.message_textfield.text().replace('#',
                                                                                                                 '')
            self.sendButtonStatus(False)
            self.client.send_msg(PROTOCOLS["client_message"], dispatch_data)
            self.message_textfield.setText("")

    def messageFieldStatus(self):
        if self.message_textfield.text() == "":
            self.sendButtonStatus(False)
        else:
            self.sendButtonStatus(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and self.message_textfield.hasFocus() is True:
            self.sendMessage()

    def updateUserList(self, online_users):
        """
        Update QListView widget and show the online users only.
        :param online_users: list of users that have ('online'=True) in the database
        :return: None
        """
        # decode users to list
        decoded_users = online_users.split('##')
        for user in decoded_users:
            # decode user data to list
            decoded_user = user.split('#')
            username, online, avatar, status = decoded_user[0], decoded_user[1], decoded_user[2], decoded_user[3]

            # if username exist, do not fetch an avatar again.
            if username not in self.users_list_model.users_avatars.keys():
                self.users_list_model.users_avatars[username] = fetchAvatar(username, 'QIMAGE')

            # if user connected to chat add to [online users]
            if online == 'True':
                model_index = self.users_list_model.index(self.users_list_model.rowCount(), 0)
                value = [username, randomColor(), status]
                self.users_list_model.insertData(model_index, value)

            # if user disconnected from chat remove from [online users]
            elif online == 'False':
                self.users_list_model.removeData(username)

    def initRoomsList(self, data):
        """
        Load chat rooms list with their icons.
        :param data: pair room name and icon list.
        :return: None
        """
        # init data structures.
        rooms_nodes = []
        rooms_icons = {}

        # decode data into lists
        decoded_data = [value.split('#') for value in data.split('##')]

        # for each room name create (ChatRoomItem) node, fetch room icon.
        for row in decoded_data:
            rooms_nodes.append(ChatRoomItem(row[0]))
            rooms_icons[row[0]] = fetchIcon(row[1])

        # init model and send the data.
        self.chat_rooms_list_model = ChatRoomsModel(rooms_nodes)
        self.chat_rooms_list_model.rooms_icons = rooms_icons
        self.chat_rooms_list.setModel(self.chat_rooms_list_model)

    def updateRoomsList(self, data):
        """
        Update the entire chat rooms from the updated data given by the server.
        :param data:  encoded (user, room) tuples.
        :return: None
        """
        try:
            # decode data into lists
            decoded_data = [value.split('#') for value in data.split('##')]

            # move each user the the room that is specified in the (data) given.
            for row in decoded_data:
                if self.chat_rooms_list_model.findUser(row[0], row[1]) is None:
                    self.chat_rooms_list_model.removeUser(row[0])
                    self.chat_rooms_list_model.addUser(ChatRoomItem(row[0]), row[1])
        except AttributeError:
            pass

    def userChangedRoom(self, index):
        """
        Moving a user to a room that has been double-clicked.
        :param index: current clicked node (ChatRoomItem) object.
        :return: None
        """
        clicked_item = index.data(0)[0]
        if self.chat_rooms_list_model.findRoom(clicked_item) is not None:
            self.client.send_msg(PROTOCOLS["change_user_room"], clicked_item + '#' + self.username_label.text())

    def sendButtonStatus(self, mode):
        if mode:
            self.send_button.setStyleSheet("image: url(:/send_button/send_button1.png);\n"
                                           "background-color: rgb(243, 243, 243);\n"
                                           "border: 0px;\n"
                                           "")
        else:
            self.send_button.setStyleSheet("image: url(:/send_button_disabled/send_button_disabled.png);\n"
                                           "background-color: rgb(243, 243, 243);\n"
                                           "border: 0px;\n"
                                           "")

    def soundButtonStatus(self):
        if "volume" in self.sound_button.styleSheet():
            self.sound_button.setStyleSheet("image: url(:/main_mute/mute.png);")
        else:
            self.sound_button.setStyleSheet("image: url(:/main_volume/volume.png);")

    def closeEvent(self, event):
        msgBox = QMessageBox()
        msgBox.setText("You will no longer be a part of the chat, Are you sure? ")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.Yes)
        if msgBox.exec_() == QMessageBox.Yes:
            self.client.send_msg(PROTOCOLS["bot_user_logged_out"], self.client.client_db_info["username"])
            event.accept()
        else:
            event.ignore()



def run(ClientTCP):
    window = QtWidgets.QMainWindow()
    MCS = MainChatScreen(ClientTCP=ClientTCP)
    MCS.setupUi(window)
    window.show()
