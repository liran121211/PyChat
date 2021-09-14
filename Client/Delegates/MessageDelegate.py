# © 2021 Liran Smadja. All rights reserved.

from PyQt5.QtCore import QMargins, QRectF, Qt, QSize
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QStyledItemDelegate, QApplication

# noinspection PyUnresolvedReferences
from Misc import createFont


class MessageDelegate(QStyledItemDelegate):
    def __init__(self):
        QStyledItemDelegate.__init__(self)
        self.default_margins = QMargins(60, 33, 25, 15)
        self.font = createFont("Eras Medium ITC", 12, True, 40)

    def paint(self, painter, option, index):
        # retrieve the data sent to the model.
        username, username_color, current_time, text_direction, text_message = index.model().data(index, Qt.DisplayRole)
        avatar_image = index.model().data(index, Qt.DecorationRole)

        if text_direction == 'True':
            # paint username text proprieties
            name_rect = QRectF(option.rect.x() + 60, option.rect.y() + 15, option.rect.width(), option.rect.height())
            R, G, B = username_color[0], username_color[1], username_color[2]
            painter.setFont(self.font)
            painter.setPen(QColor(R, G, B))
            username_painter = painter.drawText(name_rect, Qt.TextWordWrap, str(username))

            # paint time text proprieties
            time_rect = QRectF(username_painter.width() + 65, name_rect.y(), name_rect.width(), name_rect.height())
            painter.setFont(self.font)
            painter.setPen(Qt.gray)
            painter.drawText(time_rect, Qt.TextWordWrap, current_time)

            # paint message text proprieties
            message_rect = QRectF(option.rect.x() + 60, option.rect.y() + 30, option.rect.width(), option.rect.height())
            painter.setFont(self.font)
            painter.setPen(Qt.black)
            painter.drawText(message_rect, Qt.TextWordWrap, str(text_message))

            # paint avatar image proprieties
            avatar_rect = QRectF(option.rect.x() + 10, option.rect.y() + 10, 40, 40)
            painter.drawImage(avatar_rect, avatar_image)

        else:
            # paint username text proprieties
            name_rect = QRectF(option.rect.x() - 55, option.rect.y() + 15, option.rect.width(), option.rect.height())
            R, G, B = username_color[0], username_color[1], username_color[2]
            painter.setFont(self.font)
            painter.setPen(QColor(R, G, B))
            username_painter = painter.drawText(name_rect, Qt.AlignRight, str(username))

            # paint time text proprieties
            time_rect = QRectF(username_painter.x() -140 , name_rect.y(), name_rect.width(), name_rect.height())
            painter.setFont(self.font)
            painter.setPen(Qt.gray)
            painter.drawText(time_rect, Qt.TextWordWrap, current_time)

            # paint message text proprieties
            message_rect = QRectF(option.rect.x()-55, option.rect.y() + 30, option.rect.width(),
                                  option.rect.height())
            painter.setFont(self.font)
            painter.setPen(Qt.black)
            painter.drawText(message_rect,Qt.AlignRight, str(text_message))

            # paint avatar image proprieties
            avatar_rect = QRectF(option.rect.x() +950, option.rect.y() + 10, 40, 40)
            painter.drawImage(avatar_rect, avatar_image)

        if username == "PyBOT":
            painter.fillRect(option.rect, QBrush(QColor(0, 56, 255, 10)))

    def sizeHint(self, option, index) -> QSize:
        _, _, _, _, text_message = index.model().data(index, Qt.DisplayRole)
        metrics = QApplication.fontMetrics()
        rect = option.rect.marginsRemoved(self.default_margins)
        rect = metrics.boundingRect(rect, Qt.TextWordWrap, text_message)
        rect = rect.marginsAdded(self.default_margins)
        return rect.size()

# © 2021 Liran Smadja. All rights reserved.