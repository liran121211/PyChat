import random
import typing
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt

# noinspection PyUnresolvedReferences
from Misc import fetchAvatar, fetchIcon


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


class ChatRoomsModel(QAbstractItemModel):
    def __init__(self, nodes):
        QAbstractItemModel.__init__(self)
        self.chat_rooms_icons = {}
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
        node = index.internalPointer()
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
            try:
                if node.data(0) in rooms_data.keys():
                    return self.chat_rooms_icons[node.data(0)]
            except KeyError:
                self.chat_rooms_icons[node.data(0)] = fetchIcon(index=random.randint(0, 35))
                return self.chat_rooms_icons[node.data(0)]
