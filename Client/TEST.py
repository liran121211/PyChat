"""
TODO: handle changing data.
"""

import sys
import typing

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QModelIndex, Qt, QRect, QMetaObject, QCoreApplication, QAbstractItemModel
from PyQt5.QtWidgets import QWidget, QMenuBar, QStatusBar
from Models.ChatRoomsModel import ChatRoomsModel, ChatRoomItem
from Delegates.ChatRoomsDelegate import ChatRoomsDelegate
from MainChatScreen import fetchAvatar


class Ui_MainWindow(object):
    def __init__(self):
        self.nodes = []
        self.rooms_list = ['-----General-----', '-----NadezdaLand-----', '-----Entshuldi?-----',
                           '-----TovAzBye...Bye!!-----']
        # Set some random data:
        for room in self.rooms_list:
            self.nodes.append(ChatRoomItem(room))
        self.nodes[0].addChild(ChatRoomItem(['@Extarminator']))
        self.nodes[0].addChild(ChatRoomItem(['@Tamar']))

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.tw = QtWidgets.QTreeView(self.centralwidget)
        self.tw.setGeometry(QtCore.QRect(10, 0, 311, 691))
        self.tw.setStyleSheet("background-color: rgb(243, 243, 243);\n"
                              "border-radius: 10px;\ncolor: rgb(95, 95, 95);\n")
        self.tw.setItemDelegate(ChatRoomsDelegate())
        self.tw_model = ChatRoomsModel(self.nodes)
        self.tw.setModel(self.tw_model)
        self.tw.setHeaderHidden(True)

        self.button = QtWidgets.QPushButton(self.centralwidget)
        self.button.setGeometry(QtCore.QRect(400, 0, 100, 50))
        self.button.setText("ADD ITEM")
        self.button.clicked.connect(self.insertData)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def insertData(self):
        rootIdx = self.tw_model.index(0, 0, QtCore.QModelIndex())
        # Pick an insert location for a new node. This should be based on some input. For example
        # the location of a mouse click or the last element if we are appending. In this example
        # I have hard coded a value.
        position = 3
        # Create a new node called and give it a name
        new = ChatRoomItem("new")
        # Add a child node to the node which contains the value we want to display.
        # new.addChild(ChatRoomItem(['1', '2', '3']))

        # self.tw_model.beginInsertRows(rootIdx, 3, 0)
        # self.tw_model.addChild(ChatRoomItem(['1']), self.tw_model.index(1,0,QtCore.QModelIndex()))
        # self.tw_model.endInsertRows()
        # self.tw_model.addRoom(ChatRoomItem(['1']))
        #self.tw_model.addUser(ChatRoomItem("nigga"), "-----General1-----")
        self.tw_model.removeUser("@Extarminator")
        self.tw_model.removeUser("@Tamar")

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
    # retranslateUi


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
LSF = Ui_MainWindow()
LSF.setupUi(window)
window.show()
sys.exit(app.exec_())
