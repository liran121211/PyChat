from PyQt5 import QtCore
from PyQt5.QtCore import QMargins, Qt, QRectF, QSize
from PyQt5.QtWidgets import QStyledItemDelegate, QApplication, QWidget

# noinspection PyUnresolvedReferences
from Misc import createFont


class ChatRoomsDelegate(QStyledItemDelegate):
    def __init__(self):
        QStyledItemDelegate.__init__(self)
        self.default_margins = QMargins(0, 0, 0, 15)

    def paint(self, painter, option, index):
        # retrieve the data sent to the model.
        current_data, rooms_list = index.model().data(index, Qt.DisplayRole)
        avatar = index.model().data(index, Qt.DecorationRole)

        # paint username text proprieties
        painter.setPen(Qt.black)
        room_rect = QRectF(option.rect.x() + 25, option.rect.y(), option.rect.width()+20, option.rect.height())
        painter.setFont(createFont("Eras Medium ITC", 14, False, 50))
        painter.drawText(room_rect, Qt.TextWordWrap, str(current_data))

        # paint avatar image proprieties
        if current_data in rooms_list:
            avatar_rect = QRectF(option.rect.x(), option.rect.y() + 5, 20, 20)
            painter.drawImage(avatar_rect, avatar)

    def sizeHint(self, option, index) -> QSize:
        room_name,rooms_list = index.model().data(index, Qt.DisplayRole)
        metrics = QApplication.fontMetrics()
        rect = option.rect.marginsRemoved(self.default_margins)
        rect = metrics.boundingRect(rect, Qt.TextWordWrap, room_name)
        rect = rect.marginsAdded(self.default_margins)  # Re add padding for item size.
        return rect.size()
