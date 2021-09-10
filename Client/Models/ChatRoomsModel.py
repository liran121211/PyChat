import sys
import typing
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt

# noinspection PyUnresolvedReferences
from Misc import catchErrors

sys._excepthook = sys.excepthook
sys.excepthook = catchErrors


class ChatRoomItem(object):
    def __init__(self, data):
        self._children = []
        self._parent = None
        self._row = 0
        self._data = data
        if type(data) is str or not hasattr(data, '__getitem__'):
            self._data = [data]
        self._columns_count = len(self._data)

    def data(self, column):
        if 0 <= column < len(self._data):
            return self._data[column]

    def columnCount(self):
        return self._columns_count

    def childCount(self):
        return len(self._children)

    def child(self, row):
        if 0 <= row < self.childCount():
            return self._children[row]

    def children(self):
        return self._children

    def parent(self):
        return self._parent

    def row(self):
        return self._row

    def addChild(self, child):
        child._parent = self
        child._row = len(self._children)
        self._children.append(child)
        self._columns_count = max(child.columnCount(), self._columns_count)

    def removeChild(self, child):
        self._row = len(self._children) - 1
        self._children.remove(child)
        self._columns_count = max(child.columnCount(), self._columns_count)
        child._parent = None


class ChatRoomsModel(QAbstractItemModel):
    def __init__(self, nodes):
        QAbstractItemModel.__init__(self)
        self.rooms_icons = {}
        self._root = ChatRoomItem(None)
        for node in nodes:
            self._root.addChild(node)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        if parent.isValid():
            return parent.internalPointer().childCount()
        return self._root.childCount()

    def addChild(self, node, _parent):
        if not _parent or not _parent.isValid():
            parent = self._root
        else:
            parent = _parent.internalPointer()
        parent.addChild(node)

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        if not parent or not parent.isValid():
            parent = self._root
        else:
            parent = parent.internalPointer()

        if not QAbstractItemModel.hasIndex(self, row, column):
            return QModelIndex()
        child = parent.child(row)

        if child:
            return QAbstractItemModel.createIndex(self, row, column, child)
        else:
            return QModelIndex()

    def parent(self, child: QModelIndex) -> QModelIndex:
        if child.isValid():
            p = child.internalPointer().parent()
            if p:
                return QAbstractItemModel.createIndex(self, p.row(), 0, p)
        return QModelIndex()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        if parent.isValid():
            return parent.internalPointer().columnCount()
        return self._root.columnCount()

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        # Rooms Nodes: self._root.
        # Users Nodes in room (x): self._root.child(x)

        # current (MouseOver) data.
        node = index.internalPointer()

        # create dictionary of [room: users]
        rooms_data = {}
        for room in range(self._root.childCount()):
            users = []
            room_name = self._root.child(room).data(0)
            for user in range(self._root.child(room).childCount()):
                users.append(self._root.child(room).child(user).data(0))
            rooms_data[room_name] = users

        if role == Qt.DisplayRole:
            return node.data(index.column()), rooms_data

        if role == Qt.DecorationRole:
            # filter Decoration if the (node) is username, and accept only room names.
            try:
                return self.rooms_icons[node.data(0)]
            except KeyError:
                return None

    def addRoom(self, node: ChatRoomItem) -> ChatRoomItem:
        """
        Add new room to the rooms list.
        :param node: room (ChatRoomItem).
        :return: room (node) itself.
        """
        self.beginInsertRows(QModelIndex(), self._root.childCount(), self._root.childCount())
        self.addChild(node, QModelIndex())
        self.endInsertRows()
        return node

    def findRoom(self, room_name: str) -> ChatRoomItem or None:
        """
        Find room (node) by its name.
        :param room_name: String room name.
        :return: room (ChatRoomItem)
        """
        for index in range(self._root.childCount()):
            if room_name == self._root.child(index).data(0):
                return self._root.child(index)
        return None

    def addUser(self, node: ChatRoomItem, room_name: str) -> None:
        """
        Add user to the given room (node) parameter.
        :param node: user (node).
        :param room_name: (String) room name.
        :return: None.
        """
        selected_room = self.findRoom(room_name)
        self.beginInsertRows(QModelIndex(), selected_room.childCount(), selected_room.childCount())
        selected_room.addChild(node)
        self.endInsertRows()

    def findUser(self, username: str, room_name: str = None) -> (ChatRoomItem, int) or None:
        """
        Find user by given (username) parameter.
        :param username: (String) username.
        :param room_name: (String) room name.
        :return: user (ChatRoomItem), index (int).
        """

        # search user in all rooms available.
        if room_name is None:
            for room_index in range(self._root.childCount()):
                users_count = self._root.child(room_index).childCount()
                for user_index in range(users_count):
                    user_node = self._root.child(room_index).child(user_index)
                    if username == user_node.data(0):
                        return user_node, user_index
        else:
            # search user inside the given room name.
            room_node = self.findRoom(room_name)
            users_count = room_node.childCount()
            for user_index in range(users_count):
                user_node = room_node.child(user_index)
                if username == user_node.data(0):
                    return user_node, user_index
        return None

    def removeUser(self, username: str) -> None:
        """
        Remove user from the current room.
        :param username: (String) username
        :return: None
        """
        if self.findUser(username) is not None:
            user_node, user_index = self.findUser(username)
            self.beginRemoveRows(QModelIndex(), user_index, user_index)
            user_node.parent().removeChild(user_node)
            self.endRemoveRows()
