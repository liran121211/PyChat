# © 2021 Liran Smadja. All rights reserved.

import typing
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, pyqtSignal


class OnlineUsersModel(QAbstractListModel):
    layoutChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(OnlineUsersModel, self).__init__(*args, **kwargs)
        self.users_data = []
        self.users_avatars = {}

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            return self.users_data[index.row()]

        if role == Qt.DecorationRole:
            username = self.users_data[index.row()][0]
            return self.users_avatars[username]

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.users_data)

    def insertData(self, index: QModelIndex, value: typing.Any) -> None:
        if not any(value[0] in users for users in self.users_data):
            self.beginInsertRows(index, self.rowCount(), self.rowCount())
            self.users_data.append((value[0], value[1], value[2]))
            self.endInsertRows()

    def removeData(self, value: typing.Any) -> None:
        for row in range(0, len(self.users_data)):
            if self.users_data[row][0] == value:
                self.beginRemoveRows(QModelIndex(), row, row)
                self.users_avatars.pop(self.users_data[row][0])
                self.users_data.pop(row)
                self.endRemoveRows()
                break

# © 2021 Liran Smadja. All rights reserved.