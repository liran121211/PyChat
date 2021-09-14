# © 2021 Liran Smadja. All rights reserved.

import threading
from pathlib import Path

import typing
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRect, QRegExp, QSize, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QColor, QMovie, QKeyEvent
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QFrame, QMessageBox, QPushButton, QLabel
from PyQt5.QtWidgets import QLineEdit, QCommandLinkButton, QComboBox, QTextEdit

import LoadingScreen
import Client
from Models.OnlineUsersFilterModel import OnlineUsersFilterModel
from Delegates.MessageDelegate import MessageDelegate
from Delegates.OnlineUsersDelegate import OnlineUsersDelegate
from Delegates.ChatRoomsDelegate import ChatRoomsDelegate
from Models.MessagesModel import MessagesModel
from Models.OnlineUsersModel import OnlineUsersModel
from Models.ChatRoomsModel import ChatRoomsModel, ChatRoomItem
from Misc import createFont, timeStamp, fetchAvatar, fetchWindowIcon
from Misc import toRGB, randomColor, toHex, fetchRoomIcon, fetchCredits
from ThreadWorker import ThreadWorker
from Observable import Observable
from playsound2 import playsound
from Protocol import *

# noinspection PyUnresolvedReferences
from StyleSheets.main_chat_screen_css import *

LOGIN_SOUND = str(Path(__file__).parent.resolve()) + "\\Sounds\\login_sound.mp3"
LOGOUT_SOUND = str(Path(__file__).parent.resolve()) + "\\Sounds\\logout_sound.mp3"
NEW_MESSAGE_SOUND = str(Path(__file__).parent.resolve()) + "\\Sounds\\new_message.mp3"
LOADING_GIF = str(Path(__file__).parent.resolve()) + "\\Images\\loading.gif"


class MainChatScreen(Observable):
    def __init__(self, ClientTCP):
        Observable.__init__(self)
        self.client = ClientTCP
        self.client.attach(self)
        self.window_loaded = False
        self.require_restart = False
        self.sound_enabled = True
        self.thread_worker = ThreadWorker()
        self.threads = {}

    def setupUi(self, MainChatWindow):
        self.main_window = MainChatWindow
        MainChatWindow.setFixedSize(1574, 782)
        MainChatWindow.setObjectName("MainChatWindow")
        MainChatWindow.setWindowIcon(fetchWindowIcon())
        MainChatWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        MainChatWindow.setWindowTitle("PyChat - Communicate with People")
        MainChatWindow.keyPressEvent = self.keyPressEvent
        MainChatWindow.closeEvent = lambda event: event.accept()

        self.centralwidget = QtWidgets.QWidget(MainChatWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.settings_frame = QFrame(self.centralwidget)
        self.settings_frame.setGeometry(QtCore.QRect(10, 700, 311, 41))
        self.settings_frame.setObjectName("settings_frame")
        self.settings_frame.setFrameShape(QFrame.Box)
        self.settings_frame.setFrameShadow(QFrame.Raised)
        self.settings_frame.setStyleSheet(COMMON_STYLESHEET)

        self.main_chat = QtWidgets.QListView(self.centralwidget)
        self.main_chat.setGeometry(QtCore.QRect(330, 60, 1001, 631))
        self.main_chat.setObjectName("main_chat")
        self.main_chat.setItemDelegate(MessageDelegate())
        self.main_chat_model = MessagesModel()
        self.main_chat.setModel(self.main_chat_model)
        self.main_chat.verticalScrollBar().setStyleSheet(SCROLL_BAR_CSS)

        self.users_list = QtWidgets.QListView(self.centralwidget)
        self.users_list.setGeometry(QtCore.QRect(1340, 95, 221, 647))
        self.users_list.setObjectName("users_list")
        self.users_list.setItemDelegate(OnlineUsersDelegate())
        self.users_list_model = OnlineUsersModel()
        self.users_list_proxy_model = OnlineUsersFilterModel()
        self.users_list_proxy_model.setSourceModel(self.users_list_model)
        self.users_list.setModel(self.users_list_proxy_model)
        self.users_list.setStyleSheet(COMMON_STYLESHEET)
        self.users_list.verticalScrollBar().setStyleSheet(SCROLL_BAR_CSS)

        self.users_list_label = QtWidgets.QLabel(self.centralwidget)
        self.users_list_label.setGeometry(QtCore.QRect(1340, 60, 221, 50))
        self.users_list_label.setObjectName("users_list_label")
        self.users_list_label.setText("-----------Online Users-----------")
        self.users_list_label.setAlignment(Qt.AlignCenter)
        self.users_list_label.setFont(createFont("Eras Medium ITC", 15, False, 50))
        self.users_list_label.setStyleSheet(COMMON_STYLESHEET)

        self.chat_rooms_list = QtWidgets.QTreeView(self.centralwidget)
        self.chat_rooms_list.setGeometry(QtCore.QRect(10, 50, 311, 641))
        self.chat_rooms_list.setObjectName("chat_rooms_list")
        self.chat_rooms_list.setItemDelegate(ChatRoomsDelegate())
        self.chat_rooms_list.setHeaderHidden(True)
        self.chat_rooms_list.doubleClicked.connect(self.userChangedRoom)
        self.chat_rooms_list.setStyleSheet(COMMON_STYLESHEET)
        self.chat_rooms_list.verticalScrollBar().setStyleSheet(SCROLL_BAR_CSS)

        self.chat_rooms_list_label = QtWidgets.QLabel(self.centralwidget)
        self.chat_rooms_list_label.setGeometry(QtCore.QRect(10, 0, 311, 65))
        self.chat_rooms_list_label.setObjectName("chat_rooms_list_label")
        self.chat_rooms_list_label.setText("--------------------Chat Rooms--------------------")
        self.chat_rooms_list_label.setAlignment(Qt.AlignCenter)
        self.chat_rooms_list_label.setFont(createFont("Eras Medium ITC", 15, False, 50))
        self.chat_rooms_list_label.setStyleSheet(COMMON_STYLESHEET)

        self.message_textfield = QtWidgets.QLineEdit(self.centralwidget)
        self.message_textfield.setGeometry(QtCore.QRect(350, 700, 931, 41))
        self.message_textfield.setObjectName("message_textfield")
        self.message_textfield.setStyleSheet(COMMON_STYLESHEET)
        self.message_textfield.setClearButtonEnabled(False)
        self.message_textfield.setFont(createFont("Eras Medium ITC", 13, False, 50))
        self.message_textfield.textEdited.connect(self.messageFieldStatus)

        self.user_avatar = QSvgWidget(self.settings_frame)
        self.user_avatar.setGeometry(10, 7, 30, 30)
        self.user_avatar.setObjectName("user_avatar")
        self.user_avatar.renderer().load(fetchAvatar(self.client.client_db_info["username"], "SVG"))

        self.username_label = QtWidgets.QLabel(self.settings_frame)
        self.username_label.setGeometry(QtCore.QRect(50, 10, 121, 21))
        self.username_label.setObjectName("username_label")
        self.username_label.setFont(createFont("Eras Medium ITC", 14, False, 50))
        self.username_label.setText(self.client.client_db_info["username"])

        self.settings_button = QtWidgets.QPushButton(self.settings_frame)
        self.settings_button.setGeometry(QtCore.QRect(265, 6, 41, 31))
        self.settings_button.setObjectName("settings_button")
        self.settings_button.clicked.connect(self.settingsPanel)
        self.settings_button.setStyleSheet("image: url(:/settings_button/settings2.png);")

        self.sound_button = QtWidgets.QPushButton(self.settings_frame)
        self.sound_button.setGeometry(QtCore.QRect(223, 6, 41, 31))
        self.sound_button.setObjectName("settings_button")
        self.sound_button.setStyleSheet("image: url(:/main_volume/volume.png);")
        self.sound_button.clicked.connect(self.soundButtonStatus)

        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_button.setGeometry(QtCore.QRect(1290, 710, 31, 21))
        self.send_button.setObjectName("send_button")
        self.send_button.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.send_button.clicked.connect(self.sendMessage)
        self.send_button.setStyleSheet(SEND_BTN_CSS)
        self.send_button.setAutoDefault(False)

        self.textfield_label_right = QtWidgets.QLabel(self.centralwidget)
        self.textfield_label_right.setObjectName("textfield_label_right")
        self.textfield_label_right.setGeometry(QtCore.QRect(1270, 700, 61, 41))
        self.textfield_label_right.setStyleSheet(COMMON_STYLESHEET)
        self.textfield_label_right.setFrameShape(QFrame.NoFrame)

        self.textfield_label_left = QtWidgets.QLabel(self.centralwidget)
        self.textfield_label_left.setGeometry(QtCore.QRect(330, 700, 61, 41))
        self.textfield_label_left.setObjectName("textfield_label_left")
        self.textfield_label_left.setFrameShape(QFrame.NoFrame)
        self.textfield_label_left.setStyleSheet(COMMON_STYLESHEET)

        self.toolbar_frame = QFrame(self.centralwidget)
        self.toolbar_frame.setGeometry(QtCore.QRect(330, 0, 1231, 51))
        self.toolbar_frame.setObjectName("toolbar_frame")
        self.toolbar_frame.setFrameShape(QFrame.Box)
        self.toolbar_frame.setFrameShadow(QFrame.Raised)
        self.toolbar_frame.setStyleSheet(COMMON_STYLESHEET)

        self.search_button = QPushButton(self.toolbar_frame)
        self.search_button.setGeometry(QRect(1185, 12, 41, 23))
        self.search_button.setObjectName("search_button")
        self.search_button.setStyleSheet("image: url(:/search/search_icon.png);\n" + COMMON_STYLESHEET)
        self.search_button.clicked.connect(self.searchOnlineUser)

        self.search_line = QLabel(self.toolbar_frame)
        self.search_line.setGeometry(QRect(1052, 22, 141, 16))
        self.search_line.setObjectName("search_line")
        self.search_line.setText("__________________________")

        self.search_textbox = QLineEdit(self.toolbar_frame)
        self.search_textbox.setGeometry(QRect(1052, 12, 143, 20))
        self.search_textbox.setObjectName("search_textbox")
        self.search_textbox.setText("Look up for user...")
        self.search_textbox.mousePressEvent = lambda event: self.search_textbox.setText("")

        self.settings_panel = QFrame(self.centralwidget)
        self.settings_panel.setGeometry(
            QRect((self.main_window.width() / 2) - 200, (self.main_window.height() / 2) - 200, 400, 415))
        self.settings_panel.setObjectName("settings_panel")
        self.settings_panel.setFrameShape(QFrame.Box)
        self.settings_panel.setFrameShadow(QFrame.Raised)
        self.settings_panel.hide()

        self.settings_panel_avatar = QLabel(self.settings_panel)
        self.settings_panel_avatar.setObjectName("settings_panel_avatar")

        self.settings_panel_username = QLabel(self.settings_panel)
        self.settings_panel_username.setObjectName("settings_panel_username")

        self.replace_avatar = QCommandLinkButton(self.settings_panel)
        self.replace_avatar.setObjectName("replace_avatar_")

        self.replace_username_color = QCommandLinkButton(self.settings_panel)
        self.replace_username_color.setObjectName("replace_username_color")

        self.logout_button = QCommandLinkButton(self.settings_panel)
        self.logout_button.setObjectName("logout_button")

        self.server_offline_label = QLabel(self.centralwidget)
        self.server_offline_label.setGeometry(QRect(540, 280, 581, 91))
        self.server_offline_label.setObjectName("server_offline_label")
        self.server_offline_label.setText("Server is offline now!")
        self.server_offline_label.setTextFormat(Qt.PlainText)
        self.server_offline_label.setFont(createFont("Eras Medium ITC", 42, False, 50))
        self.server_offline_label.setStyleSheet("color: rgb(255,0,0)")
        self.server_offline_label.setAlignment(Qt.AlignCenter)
        self.server_offline_label.hide()

        self.current_user_chat_room = QLabel(self.toolbar_frame)
        self.current_user_chat_room.setGeometry(QRect(10, 10, 250, 30))
        self.current_user_chat_room.setObjectName("current_user_chat_room")
        self.current_user_chat_room.setFont(createFont("Eras Medium ITC", 16, False, 40))
        self.current_user_chat_room.setText('# ' + self.client.client_db_info["room"])

        self.about_panel = QFrame(self.centralwidget)
        self.about_panel.setGeometry(
            QRect((self.main_window.width() / 2) - 200, (self.main_window.height() / 2) - 200, 400, 400))
        self.about_panel.setObjectName("about_panel")
        self.about_panel.setFrameShape(QFrame.Box)
        self.about_panel.setFrameShadow(QFrame.Raised)
        self.about_panel.hide()

        self.about_button = QPushButton(self.settings_frame)
        self.about_button.setGeometry(QRect(180, 6, 41, 31))
        self.about_button.setObjectName(u"about_button")
        self.about_button.setStyleSheet(u"image: url(:/about/about.png);")
        self.about_button.clicked.connect(self.aboutPanel)

        self.about_credits_text = QTextEdit(self.about_panel)
        self.about_credits_text.setGeometry(QRect(10, 10, 380, 380))
        self.about_credits_text.setObjectName(u"about_credits_text")
        self.about_credits_text.setText(fetchCredits())
        self.about_credits_text.verticalScrollBar().setStyleSheet(SCROLL_BAR_CSS)

        self.loading_users_gif = None
        self.loading_users_label = QLabel(self.centralwidget)
        self.loading_users_label.setGeometry(QtCore.QRect(1420, 300, 140, 140))

        self.loading_rooms_gif = None
        self.loading_rooms_label = QLabel(self.centralwidget)
        self.loading_rooms_label.setGeometry(QtCore.QRect(130, 260, 140, 140))

        self.replace_user_status = QComboBox(self.settings_panel)
        self.replace_user_status.setObjectName("replace_user_status")
        self.replace_user_status.addItem("")
        self.replace_user_status.addItem("")
        self.replace_user_status.addItem("")

        self.search_textbox.raise_()
        self.search_button.raise_()
        self.message_textfield.raise_()
        self.chat_rooms_list.raise_()
        self.users_list.raise_()
        self.send_button.raise_()
        self.user_avatar.raise_()
        self.username_label.raise_()
        self.settings_button.raise_()
        self.server_offline_label.raise_()
        self.current_user_chat_room.raise_()
        self.loading_rooms_label.raise_()
        self.loading_users_label.raise_()

        MainChatWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainChatWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1574, 21))
        self.menubar.setObjectName("menubar")
        MainChatWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainChatWindow)
        self.statusbar.setObjectName("statusbar")
        MainChatWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainChatWindow)

        # Misc...
        self.users_list_loaded = False
        self.rooms_list_loaded = False
        self.initImages()
        self.initLists()
        self.initSettingsPanel()
        self.serverStatus()

        self.window_loaded = True
        self.main_window.show()

    def update(self, notif: typing.AnyStr, data: typing.AnyStr) -> None:
        """
        Get notifications from client TCP module.
        :param notif: cmd (String) of command.
        :param data: message with data (String)
        :return: None
        """
        if notif == "ONLINE_USERS":
            self.users_list_loaded = True
            self.threads["ONLINE_USERS"] = threading.Thread(target=self.updateUserList, args=(data,))
            self.threads["ONLINE_USERS"].start()
            self.loading_users_gif.stop()
            self.loading_users_label.hide()

        if notif == "MESSAGE_TO_CLIENT":
            if self.window_loaded is True:
                self.threads["MESSAGE_TO_CLIENT"] = threading.Thread(target=self.updateChat, args=(data,))
                self.threads["MESSAGE_TO_CLIENT"].start()

                if self.sound_enabled:
                    self.threads["SOUND_MESSAGE"] = threading.Thread(target=playsound, args=(NEW_MESSAGE_SOUND,))
                    self.threads["SOUND_MESSAGE"].start()

        if notif == "CHAT_ROOMS_NAMES":
            self.rooms_list_loaded = True
            self.threads["CHAT_ROOMS_NAMES"] = threading.Thread(target=self.initRoomsList, args=(data,))
            self.threads["CHAT_ROOMS_NAMES"].start()
            self.loading_rooms_gif.stop()
            self.loading_rooms_label.hide()

        if notif == "CHAT_ROOMS_INFO":
            self.threads["CHAT_ROOMS_INFO"] = threading.Thread(target=self.updateRoomsList, args=(data,))
            self.threads["CHAT_ROOMS_INFO"].start()

        if notif == "BOT_USER_LOGGED_IN":
            self.threads["BOT_USER_LOGGED_IN"] = threading.Thread(target=self.updateChat, args=(data,))
            self.threads["BOT_USER_LOGGED_IN"].start()

            if self.sound_enabled:
                self.threads["LOGIN_SOUND"] = threading.Thread(target=playsound, args=(LOGIN_SOUND,))
                self.threads["LOGIN_SOUND"].start()

        if notif == "BOT_USER_LOGGED_OUT":
            self.threads["BOT_USER_LOGGED_OUT"] = threading.Thread(target=self.updateChat, args=(data,))
            self.threads["BOT_USER_LOGGED_OUT"].start()

            if self.sound_enabled:
                self.threads["LOGOUT_SOUND"] = threading.Thread(target=playsound, args=(LOGOUT_SOUND,))
                self.threads["LOGOUT_SOUND"].start()

        if notif == "REPLACE_USER_AVATAR":
            if data == "SUCCESS":
                self.block_replaceUserAvatar = False
                username = self.client.client_db_info["username"]
                self.settings_panel_avatar.setPixmap(fetchAvatar(username, "PIXMAP").scaled(150, 150))
                self.replace_avatar.setEnabled(True)
                self.require_restart = True

        if notif == "REPLACE_USERNAME_COLOR":
            if data == "SUCCESS":
                self.replace_username_color.setEnabled(True)
                self.require_restart = True

        if notif == "REPLACE_USER_STATUS":
            if data == "SUCCESS":
                self.replace_user_status.setEnabled(True)
                self.require_restart = True

        if notif == "SERVER_OFFLINE":
            self.main_window.setDisabled(True)
            self.main_chat.setDisabled(True)
            self.server_offline_label.show()

    def updateChat(self, data: typing.AnyStr) -> None:
        """
        Update chat (QListView) with the current data sent from the server.
        :param data: decoded (String) data.
        :return: None
        """
        username, text_direction, message = data.split('#')
        model_index = self.main_chat_model.index(self.main_chat_model.rowCount(), 0)
        self.main_chat_model.insertData(model_index, (username, [180, 20, 50], timeStamp(), text_direction, message))

    def sendMessage(self) -> None:
        """
        Gather data from the (message_textfield) and dispatch it to the server.
        Avoid server overload when the (message_textfield) is empty.
        :return: None
        """
        if self.message_textfield.text() != "" and self.message_textfield.text() != '#':
            username = self.client.client_db_info["username"]
            text_direction = str(self.message_textfield.isLeftToRight())
            text_message = self.message_textfield.text().replace('#', '')

            dispatch_data = username + '#' + text_direction + '#' + text_message
            self.client.send_msg(PROTOCOLS["client_message"], dispatch_data)
            self.message_textfield.setText("")
            self.send_button.setStyleSheet(DISABLED_BTN_CSS)

    def messageFieldStatus(self) -> None:
        """
        Change StyleSheet of (message_textfield) when it's  empty/not empty.
        :return: None
        """
        if self.message_textfield.text() == "":
            self.send_button.setStyleSheet(DISABLED_BTN_CSS)
        else:
            self.send_button.setStyleSheet(ENABLED_BTN_CSS)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Triggered when key is pressed in GUI window.
        :param event: (QKeyEvent) object
        :return: None
        """
        if event.key() == Qt.Key_Return and self.message_textfield.hasFocus() is True:
            self.sendMessage()

        if event.key() == Qt.Key_Enter and self.message_textfield.hasFocus() is True:
            self.sendMessage()

        if event.key() == Qt.Key_Return and self.search_textbox.hasFocus() is True:
            self.search_button.click()

        if event.key() == Qt.Key_Enter and self.search_textbox.hasFocus() is True:
            self.search_button.click()

    def updateUserList(self, online_users: typing.AnyStr) -> None:
        """
        Update QListView widget and show the online users only.
        :param online_users: encoded filtered list of users with ('online'=True) in the database.
        :return: None
        """
        # decode users to list
        decoded_users = online_users.split('##')

        # decode user data to list
        for user in decoded_users:
            decoded_user = user.split('#')
            username, online, avatar = decoded_user[0], decoded_user[1], decoded_user[2]
            status, color = decoded_user[3], decoded_user[4]

            # if username exist, do not fetch an avatar again.
            if username not in self.users_list_model.users_avatars.keys():
                self.users_list_model.users_avatars[username] = fetchAvatar(username, 'QIMAGE')

            # if user connected to chat add to [online users]
            if online == 'True':
                model_index = self.users_list_model.index(self.users_list_model.rowCount(), 0)
                value = [username, toRGB(color), status]
                self.users_list_model.insertData(model_index, value)

            # if user disconnected from chat remove from [online users]
            elif online == 'False':
                self.users_list_model.removeData(username)

    def initRoomsList(self, data: typing.AnyStr) -> None:
        """
        Load chat rooms list, for each room (item) load the icon.
        :param data: [room name, icon] list.
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
            rooms_icons[row[0]] = fetchRoomIcon(row[1], "QIMAGE")

        # init model and send the data.
        self.chat_rooms_list_model = ChatRoomsModel(rooms_nodes)
        self.chat_rooms_list_model.rooms_icons = rooms_icons
        self.chat_rooms_list.setModel(self.chat_rooms_list_model)

    def updateRoomsList(self, data: typing.AnyStr) -> None:
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

    def userChangedRoom(self, index: ChatRoomItem) -> None:
        """
        Transfer a user to a room that has been double-clicked.
        :param index: current clicked node (ChatRoomItem) object.
        :return: None
        """
        clicked_room = index.data(0)[0]
        username = self.client.client_db_info["username"]
        if self.chat_rooms_list_model.findRoom(clicked_room) is not None:
            self.current_user_chat_room.setText('# ' + clicked_room)
            self.client.send_msg(PROTOCOLS["change_user_room"], clicked_room + '#' + username)

    def soundButtonStatus(self) -> None:
        """
        Disable/Enable sound effects of the chat.
        :return: None
        """
        if self.sound_enabled:
            self.sound_button.setStyleSheet("image: url(:/main_mute/mute.png);")
            self.sound_enabled = False
        else:
            self.sound_button.setStyleSheet("image: url(:/main_volume/volume.png);")
            self.sound_enabled = True

    def searchOnlineUser(self) -> None:
        """
        Narrow down the online users list by (username) keyword.
        :return: None
        """
        syntax = QRegExp.PatternSyntax(QRegExp.RegExp)
        caseSensitivity = Qt.CaseInsensitive
        regExp = QRegExp(self.search_textbox.text(), caseSensitivity, syntax)

        self.users_list.setModel(self.users_list_proxy_model)
        self.users_list_proxy_model.setFilterRegExp(regExp)

    def settingsPanel(self):
        """
        Reload settings panel window on click, or hide it.
        :return:
        """
        if self.settings_panel.isHidden():
            self.initSettingsPanel()
            self.settings_panel.show()
        else:
            if self.require_restart:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText("Restart to apply changes.")
                msgBox.setWindowTitle("Information")
                msgBox.setWindowFlags(
                    Qt.WindowTitleHint | Qt.Dialog | Qt.WindowMaximizeButtonHint | Qt.CustomizeWindowHint)
                msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                if msgBox.exec_() == QMessageBox.Ok:
                    # terminate client socket, close it, and restart the process of MainChatWindow Gui.
                    self.client.isTerminated = True
                    self.client.client_socket.close()
                    self.main_window.close()
                    LoadingScreen.restart()
            else:
                self.settings_panel.hide()

    def aboutPanel(self) -> None:
        """
        Show copyright of all contributors used to create this application.
        :return: None
        """
        if self.about_panel.isHidden():
            self.about_panel.show()
        else:
            self.about_panel.hide()

    def initSettingsPanel(self):
        """
        Fetch all needed data for the settings panel window.
        :return:
        """
        # refresh client data from database.
        username, password = self.client.client_db_info["username"], self.client.client_db_info["password"]
        self.client.send_msg(PROTOCOLS["refresh_client_info"], username + "#" + password)

        self.block_replaceUserAvatar = False
        x_loc = self.settings_panel.width() / 2
        username = self.client.client_db_info["username"]
        self.settings_panel_avatar.setGeometry(x_loc - 75, 50, 150, 150)
        self.settings_panel_avatar.setPixmap(fetchAvatar(username, "PIXMAP").scaled(150, 150))

        self.settings_panel_username.setGeometry(x_loc - 75, 210, 150, 30)
        self.settings_panel_username.setAlignment(Qt.AlignCenter)
        self.settings_panel_username.setText('@' + username)
        self.settings_panel_username.setFont(createFont("Eras Medium ITC", 15, True, 50))
        self.settings_panel_username.setStyleSheet("color: #" + self.client.client_db_info["color"] + ";")

        avatar_icon = QIcon()
        avatar_icon.addFile(":/replace_avatar/replace_avatar.png", QSize(), QIcon.Normal, QIcon.Off)
        self.replace_avatar.setGeometry(QRect(15, 275, 250, 51))
        self.replace_avatar.setIcon(avatar_icon)
        self.replace_avatar.setIconSize(QSize(32, 32))
        self.replace_avatar.setText("Replace Current Avatar")
        self.replace_avatar.setFont(createFont("Eras Medium ITC", 13, True, 50))
        self.replace_avatar.clicked.connect(self.replaceUserAvatar)
        self.replace_avatar.setStyleSheet(REPLACE_AVATAR_CSS)

        username_icon = QIcon()
        username_icon.addFile(":/change_username_color/change_username_color.png", QSize(), QIcon.Normal, QIcon.Off)
        self.replace_username_color.setGeometry(QRect(15, 315, 250, 51))
        self.replace_username_color.setIcon(username_icon)
        self.replace_username_color.setIconSize(QSize(32, 32))
        self.replace_username_color.setText("Replace Username Color")
        self.replace_username_color.setFont(createFont("Eras Medium ITC", 13, True, 50))
        self.replace_username_color.clicked.connect(self.replaceUserColor)
        self.replace_username_color.setStyleSheet(REPLACE_USERNAME_CSS)

        logout_icon = QIcon()
        logout_icon.addFile(":/logout/logout.png", QSize(), QIcon.Normal, QIcon.Off)
        self.logout_button.setGeometry(QRect(15, 355, 250, 51))
        self.logout_button.setIcon(logout_icon)
        self.logout_button.setIconSize(QSize(32, 32))
        self.logout_button.setText("Logout")
        self.logout_button.setFont(createFont("Eras Medium ITC", 13, True, 50))
        self.logout_button.clicked.connect(self.logout)
        self.logout_button.setStyleSheet(LOGOUT_CSS)

        self.replace_user_status.setGeometry(x_loc - 75, 240, 158, 30)
        self.replace_user_status.setFont(createFont("Eras Medium ITC", 13, True, 50))
        self.replace_user_status.setStyleSheet(COMBO_BOX_CSS)
        status_dict = {"Available": (59, 165, 93, 0), "Away": (250, 168, 26, 1), "Unavailable": (237, 66, 69, 2)}

        for status, color in status_dict.items():
            R, G, B = color[0], color[1], color[2]
            index = color[3]
            icon = QPixmap(20, 20)
            icon.fill(QColor(R, G, B))
            self.replace_user_status.setItemIcon(index, QIcon(icon))
            self.replace_user_status.setItemData(index, status, Qt.DisplayRole)

        if self.client.client_db_info["status"] == "AVAILABLE":
            self.replace_user_status.setCurrentIndex(0)
        elif self.client.client_db_info["status"] == "AWAY":
            self.replace_user_status.setCurrentIndex(1)
        elif self.client.client_db_info["status"] == "UNAVAILABLE":
            self.replace_user_status.setCurrentIndex(2)

        self.replace_user_status.currentIndexChanged.connect(self.replaceUserStatus)

    def replaceUserColor(self) -> None:
        """
        Replace username color on user demand.
        :return: None
        """
        R, G, B = randomColor()
        CSS = "color:rgb({0},{1},{2})".format(R, G, B)
        msg = toHex(R, G, B).upper() + '#' + self.client.client_db_info["username"]
        self.settings_panel_username.setStyleSheet(CSS)
        self.replace_username_color.setDisabled(True)
        self.client.send_msg(PROTOCOLS["replace_username_color"], msg)

    def replaceUserAvatar(self) -> None:
        """
        Replace user Avatar on user demand.
        :return: None
        """
        if self.block_replaceUserAvatar is False:
            self.client.send_msg(PROTOCOLS["replace_user_avatar"], self.client.client_db_info["username"])
            self.replace_avatar.setDisabled(True)
            self.block_replaceUserAvatar = True

    def replaceUserStatus(self) -> None:
        """
        Replace user status on user demand.
        :return: None
        """
        self.replace_user_status.setEnabled(False)
        status = str(self.replace_user_status.currentData(Qt.DisplayRole)).upper()
        username = self.client.client_db_info["username"]
        self.client.send_msg(PROTOCOLS["replace_user_status"], status + '#' + username)

    def logout(self) -> None:
        """
        Logout from the chat, and return to login screen.
        :return: None
        """
        self.client.isTerminated = True
        self.client.client_socket.close()
        self.main_window.close()
        LoadingScreen.restart()

    def serverStatus(self) -> None:
        """
        Retrieve server status: Online/Offline, by sending message and waiting for reply.
        :return: None
        """
        self.client.send_msg(PROTOCOLS["is_server_running"], "")
        QTimer.singleShot(5000, lambda: self.serverStatus())

    def initLists(self) -> None:
        """
        Initialize for the first time the Online Users List and Chat Rooms List.
        :return: None
        """
        if self.users_list_loaded is False:
            self.client.send_msg(PROTOCOLS["online_users"], "")
            QTimer.singleShot(2000, lambda: self.initLists())

        if self.rooms_list_loaded is False:
            self.client.send_msg(PROTOCOLS["chat_rooms_names"], "")
            QTimer.singleShot(2000, lambda: self.initLists())

    def initImages(self) -> None:
        """
        Loading data of lists (Rooms, Users) gif animation.
        :return: None
        """
        self.loading_users_gif = QMovie(LOADING_GIF)
        self.loading_users_label.setMovie(self.loading_users_gif)
        self.loading_users_label.setStyleSheet(COMMON_STYLESHEET)
        self.loading_users_gif.start()

        self.loading_rooms_gif = QMovie(LOADING_GIF)
        self.loading_rooms_label.setMovie(self.loading_rooms_gif)
        self.loading_rooms_label.setStyleSheet(COMMON_STYLESHEET)
        self.loading_rooms_gif.start()


def run(ClientTCP: Client.ClientTCP) -> None:
    """
    Main function, Initializing the GUI Process.
    :param ClientTCP: Client module.
    :return: None
    """
    window = QtWidgets.QMainWindow()
    MCS = MainChatScreen(ClientTCP=ClientTCP)
    MCS.setupUi(window)

# © 2021 Liran Smadja. All rights reserved.