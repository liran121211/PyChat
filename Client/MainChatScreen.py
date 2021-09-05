# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainChatScreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import threading
import random
import typing
from datetime import datetime

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QModelIndex, QAbstractListModel, QSize, QMargins, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon, QColor, QBrush, QPen
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QFrame, QApplication, QStyledItemDelegate, QStyle

from ThreadWorker import ThreadWorker
from Protocol import *
from Observable import Observable
import CSS.main_chat_screen_css


class MainChatScreen(Observable):

    def __init__(self, ClientTCP):
        Observable.__init__(self)
        self.client = ClientTCP
        self.client.attach(self)
        self.chat_history = ""
        self.threads = {}
        self.thread_worker = ThreadWorker()

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
        self.users_list.setGeometry(QtCore.QRect(1340, 60, 221, 681))
        self.users_list.setObjectName("users_list")
        self.users_list.setItemDelegate(OnlineUsersDelegate())
        self.users_list_model = OnlineUsersModel()
        self.users_list.setModel(self.users_list_model)
        self.users_list.setStyleSheet("background-color: rgb(243, 243, 243);\n"
                                      "border-radius: 10px;\ncolor: rgb(95, 95, 95);\n")

        self.chat_rooms_list = QtWidgets.QListView(self.centralwidget)
        self.chat_rooms_list.setGeometry(QtCore.QRect(10, 0, 311, 691))
        self.chat_rooms_list.setObjectName("chat_rooms_list")

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
        self.client.send_msg(PROTOCOLS["chat_rooms_list"], "")
        self.username_label.setText(self.client.client_db_info["username"])
        self.user_avatar.renderer().load(fetchAvatar(username=self.client.client_db_info["username"], obj_type="SVG"))
        self.send_button.clicked.connect(self.sendMessage)
        self.message_textfield.textEdited.connect(self.messageFieldStatus)
        MainChatWindow.keyPressEvent = self.keyPressEvent

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
            self.updateUserList(data)

        if notif == "MESSAGE_TO_CLIENT":
            self.updateChat(data)

        if notif == "CHAT_ROOMS_LIST":
            self.updateRoomsList(data.split("#"))

    def updateChat(self, data):
        username, message = data.split('#')
        self.main_chat_model.add_message(username, [180, 20, 50], message)

    def sendMessage(self):
        if self.message_textfield.text() != "":
            dispatch_data = self.username_label.text() + '#' + self.message_textfield.text().replace('#','')
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
        decoded_users = online_users.split('##')
        for user in decoded_users:
            decoded_user = user.split('#')
            username, avatar, status = decoded_user[0], decoded_user[1], decoded_user[2]
            self.users_list_model.add_user(username=username, username_color=randomColor(), status=status)

    def updateRoomsList(self, rooms):
        """
        Update QListView widget and show the available chat rooms.
        :param rooms: list of rooms in the database
        :return: None
        """
        self.chat_rooms_list_model = QStandardItemModel(self.chat_rooms_list)  # define model structure for QListView
        font = QtGui.QFont()
        font.setFamily("Eras Medium ITC")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.chat_rooms_list.setFont(font)
        for room in rooms:
            self.chat_rooms_list_model.appendRow(QStandardItem(room))

        self.chat_rooms_list.setModel(self.chat_rooms_list_model)
        self.chat_rooms_list.update()

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


class MessageDelegate(QStyledItemDelegate):
    def __init__(self):
        QStyledItemDelegate.__init__(self)
        self.default_margins = QMargins(60, 33, 25, 15)

    def paint(self, painter, option, index):
        # retrieve the data sent to the model.
        username, username_color, current_time, text_message, = index.model().data(index, Qt.DisplayRole)
        avatar_image = index.model().data(index, Qt.DecorationRole)

        # paint username text proprieties
        username_rect = QtCore.QRectF(option.rect.x() + 60, option.rect.y() + 15, option.rect.width(),
                                      option.rect.height())
        R, G, B = username_color[0], username_color[1], username_color[2]
        painter.setPen(QColor(R, G, B))
        username_painter = painter.drawText(username_rect, Qt.TextWordWrap, str(username))

        # paint time text proprieties
        time_rect = QtCore.QRectF(username_painter.width() + 65, username_rect.y(), username_rect.width(),
                                  username_rect.height())
        painter.setPen(Qt.gray)
        painter.drawText(time_rect, Qt.TextWordWrap, current_time)

        # paint message text proprieties
        text_message_rect = option.rect.marginsRemoved(self.default_margins)
        painter.setPen(Qt.black)
        painter.drawText(text_message_rect, Qt.TextWordWrap, str(text_message))

        # paint avatar image proprieties
        avatar_rect = QtCore.QRectF(option.rect.x() + 10, option.rect.y() + 10, 40, 40)
        painter.drawImage(avatar_rect, avatar_image)

    def sizeHint(self, option, index) -> QSize:
        _, _, _, text_message = index.model().data(index, Qt.DisplayRole)
        metrics = QApplication.fontMetrics()
        rect = option.rect.marginsRemoved(self.default_margins)
        rect = metrics.boundingRect(rect, Qt.TextWordWrap, text_message)
        rect = rect.marginsAdded(self.default_margins)  # Re add padding for item size.
        return rect.size()


class OnlineUsersDelegate(QStyledItemDelegate):
    def __init__(self):
        QStyledItemDelegate.__init__(self)
        self.default_margins = QMargins(60, 33, 25, 15)

    def paint(self, painter, option, index) -> None:
        # MouseOver event (background color)
        if option.state & QStyle.State_MouseOver:
            painter.fillRect(option.rect, QBrush(QColor(128, 128, 255, 10)))

        # retrieve the data sent to the model.
        username, username_color, status, = index.model().data(index, Qt.DisplayRole)
        avatar_image = index.model().data(index, Qt.DecorationRole)

        # paint [username] text proprieties
        username_rect = QtCore.QRectF(option.rect.x() + 60, option.rect.y() + 15, option.rect.width(),
                                      option.rect.height())
        R, G, B = username_color[0], username_color[1], username_color[2]
        painter.setPen(QColor(R, G, B))
        painter.setFont(createFont("Eras Medium ITC", 14, False, 50))
        painter.drawText(username_rect, Qt.TextWordWrap, str(username))

        # paint [avatar image] proprieties
        avatar_rect = QtCore.QRectF(option.rect.x() + 10, option.rect.y() + 10, 40, 40)
        painter.drawImage(avatar_rect, avatar_image)

        # paint [status] proprieties
        status_rect = QtCore.QRectF(avatar_rect.x() + 10, avatar_rect.y() + 10, 40, 40)
        painter.setPen(QPen(Qt.white, 3, Qt.SolidLine))
        if status == "AVAILABLE":
            painter.setBrush(QBrush(QColor(59, 165, 93), Qt.SolidPattern))
            painter.drawEllipse(status_rect.x() + 15, status_rect.y() + 15, 15, 15)

        if status == "AWAY":
            painter.setBrush(QBrush(QColor(250, 168, 26), Qt.SolidPattern))
            painter.drawEllipse(status_rect.x() + 15, status_rect.y() + 15, 15, 15)

        if status == "UNAVAILABLE":
            painter.setBrush(QBrush(QColor(237, 66, 69), Qt.SolidPattern))
            painter.drawEllipse(status_rect.x() + 15, status_rect.y() + 15, 15, 15)

        # paint [about] text proprieties
        about_rect = QtCore.QRectF(username_rect.x(), username_rect.y() + 20, 400, 50)
        painter.setFont(createFont("Eras Medium ITC", 10, False, 50))
        painter.setPen(Qt.gray)
        about = None

        if status == "AVAILABLE":
            about = "I'm available now :)"

        if status == "AWAY":
            about = "I'll be back soon"

        if status == "UNAVAILABLE":
            about = "Do not disturb me"
        painter.drawText(about_rect, Qt.TextWordWrap, about)

    def sizeHint(self, option, index) -> QSize:
        _, _, about_message = index.model().data(index, Qt.DisplayRole)
        metrics = QApplication.fontMetrics()
        rect = option.rect.marginsRemoved(self.default_margins)
        rect = metrics.boundingRect(rect, Qt.TextWordWrap, about_message)
        rect = rect.marginsAdded(self.default_margins)  # Re add padding for item size.
        return rect.size()


class MessagesModel(QAbstractListModel):
    layoutChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(MessagesModel, self).__init__(*args, **kwargs)
        self.messages_data = []

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            return self.messages_data[index.row()]

        if role == Qt.DecorationRole:
            username = self.messages_data[index.row()][0]
            return fetchAvatar(username=username, obj_type="QIMAGE", k=0).smoothScaled(40, 40)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.messages_data)

    def add_message(self, username: str, username_color: list, message: str):
        if message:
            self.messages_data.append((username, username_color, timeStamp(), message))

            # trigger refresh of model.
            self.layoutChanged.emit()


class OnlineUsersModel(QAbstractListModel):
    layoutChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(OnlineUsersModel, self).__init__(*args, **kwargs)
        self.users_data = []
        self.avatar = fetchAvatar("Extarminator", "QIMAGE", 1).smoothScaled(40, 40)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            return self.users_data[index.row()]

        if role == Qt.DecorationRole:
            return self.avatar

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.users_data)

    def add_user(self, username: str, username_color: list, status: str):
        if not any(username in users for users in self.users_data):
            self.users_data.append((username, username_color, status))

            # trigger refresh of model.
            self.layoutChanged.emit()

    def remove_user(self, index):
        self.users_data.pop(index)
        self.layoutChanged.emit()


def fetchAvatar(username: str, obj_type: typing.Any, k=0):
    """
    Fetch unique avatar image for every user from online resource
    :param k: API_KEYS index of item
    :param username: username (String)
    :param obj_type: type of obj to be returned.
    :return: QIcon obj, svg (ByteArray)
    """
    IMAGE_LIMIT_REACHED = 'Limit reached'
    image_url = 'http://167.172.181.78/avatars/{0}.svg'.format(username)
    pixmap_obj = QPixmap()
    svg_data = requests.get(image_url).content

    if IMAGE_LIMIT_REACHED in svg_data.decode():
        try:
            svg_data = fetchAvatar(username, None, k + 1)
        except IndexError:
            svg_data = fetchAvatar(username, None, 0)

    pixmap_obj.loadFromData(svg_data)

    if obj_type == "QICON":
        return QIcon(pixmap_obj)

    if obj_type == "SVG":
        return bytearray(svg_data.decode(), encoding='utf-8')

    if obj_type == "QIMAGE":
        return pixmap_obj.toImage()

    if obj_type is None:
        return svg_data


def randomColor():
    rgb_color = [
        [255, 85, 127],
        [255, 85, 0],
        [85, 170, 127],
        [32, 147, 121],
        [38, 60, 83],
        [228, 151, 77],
        [107, 130, 199],
        [128, 64, 64],
        [128, 128, 64],
        [234, 209, 555],
    ]
    return rgb_color[random.randint(0, 9)]


def createFont(fontFamily=None, PointSize=None, Bold=None, Weight=None):
    """
    Create new Font object.
    :param fontFamily: name of the font.
    :param PointSize: size of font.
    :param Bold: True/False value.
    :param Weight: N/A
    :return: QFont object.
    """
    font = QtGui.QFont()
    font.setFamily(fontFamily)
    font.setPointSize(PointSize)
    font.setBold(Bold)
    font.setWeight(Weight)
    return font


def timeStamp():
    return "Today at " + datetime.now().strftime("%I:%M %p")


def run(ClientTCP):
    window = QtWidgets.QMainWindow()
    MCS = MainChatScreen(ClientTCP=ClientTCP)
    MCS.setupUi(window)
    window.show()
