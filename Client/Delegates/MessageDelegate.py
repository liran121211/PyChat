from PyQt5.QtCore import QMargins, QRectF, Qt, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QStyledItemDelegate, QApplication


class MessageDelegate(QStyledItemDelegate):
    def __init__(self):
        QStyledItemDelegate.__init__(self)
        self.default_margins = QMargins(60, 33, 25, 15)

    def paint(self, painter, option, index):
        # retrieve the data sent to the model.
        username, username_color, current_time, text_message, = index.model().data(index, Qt.DisplayRole)
        avatar_image = index.model().data(index, Qt.DecorationRole)

        # paint username text proprieties
        username_rect = QRectF(option.rect.x() + 60, option.rect.y() + 15, option.rect.width(), option.rect.height())
        R, G, B = username_color[0], username_color[1], username_color[2]
        painter.setPen(QColor(R, G, B))
        username_painter = painter.drawText(username_rect, Qt.TextWordWrap, str(username))

        # paint time text proprieties
        time_rect = QRectF(username_painter.width() + 65, username_rect.y(), username_rect.width(),
                           username_rect.height())
        painter.setPen(Qt.gray)
        painter.drawText(time_rect, Qt.TextWordWrap, current_time)

        # paint message text proprieties
        text_message_rect = option.rect.marginsRemoved(self.default_margins)
        painter.setPen(Qt.black)
        painter.drawText(text_message_rect, Qt.TextWordWrap, str(text_message))

        # paint avatar image proprieties
        avatar_rect = QRectF(option.rect.x() + 10, option.rect.y() + 10, 40, 40)
        painter.drawImage(avatar_rect, avatar_image)

    def sizeHint(self, option, index) -> QSize:
        _, _, _, text_message = index.model().data(index, Qt.DisplayRole)
        metrics = QApplication.fontMetrics()
        rect = option.rect.marginsRemoved(self.default_margins)
        rect = metrics.boundingRect(rect, Qt.TextWordWrap, text_message)
        rect = rect.marginsAdded(self.default_margins)  # Re add padding for item size.
        return rect.size()
