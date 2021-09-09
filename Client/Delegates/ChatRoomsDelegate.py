from PyQt5.QtCore import QMargins, Qt, QRectF, QSize
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QStyledItemDelegate, QApplication, QStyle

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

        # MouseOver event (background color)
        if option.state & QStyle.State_MouseOver:
            painter.fillRect(option.rect, QBrush(QColor(128, 128, 255, 10)))

        # paint username text proprieties
        painter.setPen(Qt.black)
        room_rect = QRectF(option.rect.x() + 33, option.rect.y() + 8, option.rect.width(), option.rect.height())
        painter.setFont(createFont("Eras Medium ITC", 14, False, 50))
        if current_data not in rooms_list:
            painter.drawText(room_rect, Qt.TextWordWrap, '@' + str(current_data))
        else:
            painter.drawText(room_rect, Qt.TextWordWrap, str(current_data))

        # paint avatar image proprieties
        if current_data in rooms_list:
            avatar_rect = QRectF(option.rect.x(), option.rect.y() + 5, 30, 30)
            painter.drawImage(avatar_rect, avatar)

    def sizeHint(self, option, index) -> QSize:
        _, _ = index.model().data(index, Qt.DisplayRole)
        metrics = QApplication.fontMetrics()
        rect = option.rect.marginsRemoved(self.default_margins)
        rect = metrics.boundingRect(rect, Qt.TextWordWrap, "Chamber Of Secrets")
        rect = rect.marginsAdded(self.default_margins)  # Re add padding for item size.
        return rect.size()
