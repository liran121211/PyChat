import typing
from PyQt5.QtCore import QSortFilterProxyModel, QModelIndex


class OnlineUsersFilterModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(OnlineUsersFilterModel, self).__init__(parent)

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        index = self.mapFromSource(self.sourceModel().index(source_row, 0, source_parent))
        return self.filterRegExp().indexIn(self.sourceModel().data(index, 0)[0]) >= 0

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        return self.sourceModel().data(self.mapToSource(index), role)
