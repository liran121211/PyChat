import typing
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, pyqtSignal
# noinspection PyUnresolvedReferences
from Misc import fetchAvatar


class MessagesModel(QAbstractListModel):
    layoutChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(MessagesModel, self).__init__(*args, **kwargs)
        self.messages_data = []
        self.users_avatars = {}

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            return self.messages_data[index.row()]

        if role == Qt.DecorationRole:
            username = self.messages_data[index.row()][0]
            try:
                return self.users_avatars[username]
            except KeyError:
                self.users_avatars[username] = fetchAvatar(username=username, obj_type="QIMAGE", k=0).smoothScaled(40,                                                                                                   40)
                return self.users_avatars[username]

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.messages_data)

    def insertData(self, index: QModelIndex, value: typing.Any) -> None:
        self.beginInsertRows(index, self.rowCount(), self.rowCount())
        if value[0]:
            self.messages_data.append((value[0], value[1], value[2], value[3]))
        self.endInsertRows()
