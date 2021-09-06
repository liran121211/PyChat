from PyQt5.QtCore import QMargins, Qt, QRectF, QSize
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle, QApplication

# noinspection PyUnresolvedReferences
from Misc import createFont


class OnlineUsersDelegate(QStyledItemDelegate):
    def __init__(self):
        QStyledItemDelegate.__init__(self)
        self.default_margins = QMargins(60, 33, 25, 15)

    def paint(self, painter, option, index) -> None:
        # MouseOver event (background color)
        if option.state & QStyle.State_MouseOver:
            painter.fillRect(option.rect, QBrush(QColor(128, 128, 255, 10)))

        # retrieve the data sent to the model.
        username, username_color, status, = index.model().data(index, Qt.DisplayRole)
        avatar_image = index.model().data(index, Qt.DecorationRole)

        # paint [username] text proprieties
        username_rect = QRectF(option.rect.x() + 60, option.rect.y() + 15, option.rect.width(), option.rect.height())
        R, G, B = username_color[0], username_color[1], username_color[2]
        painter.setPen(QColor(R, G, B))
        painter.setFont(createFont("Eras Medium ITC", 14, False, 50))
        painter.drawText(username_rect, Qt.TextWordWrap, str(username))

        # paint [avatar image] proprieties
        avatar_rect = QRectF(option.rect.x() + 10, option.rect.y() + 10, 40, 40)
        painter.drawImage(avatar_rect, avatar_image)

        # paint [status] proprieties
        status_rect = QRectF(avatar_rect.x() + 10, avatar_rect.y() + 10, 40, 40)
        painter.setPen(QPen(Qt.white, 3, Qt.SolidLine))
        if status == "AVAILABLE":
            painter.setBrush(QBrush(QColor(59, 165, 93), Qt.SolidPattern))
            painter.drawEllipse(status_rect.x() + 15, status_rect.y() + 15, 15, 15)

        if status == "AWAY":
            painter.setBrush(QBrush(QColor(250, 168, 26), Qt.SolidPattern))
            painter.drawEllipse(status_rect.x() + 15, status_rect.y() + 15, 15, 15)

        if status == "UNAVAILABLE":
            painter.setBrush(QBrush(QColor(237, 66, 69), Qt.SolidPattern))
            painter.drawEllipse(status_rect.x() + 15, status_rect.y() + 15, 15, 15)

        # paint [about] text proprieties
        about_rect = QRectF(username_rect.x(), username_rect.y() + 20, 400, 50)
        painter.setFont(createFont("Eras Medium ITC", 10, False, 50))
        painter.setPen(Qt.black)
        about = None

        if status == "AVAILABLE":
            about = "I'm available now :)"

        if status == "AWAY":
            about = "I'll be back soon"

        if status == "UNAVAILABLE":
            about = "Do not disturb me"
        painter.drawText(about_rect, Qt.TextWordWrap, about)

    def sizeHint(self, option, index) -> QSize:
        _, _, about_message = index.model().data(index, Qt.DisplayRole)
        metrics = QApplication.fontMetrics()
        rect = option.rect.marginsRemoved(self.default_margins)
        rect = metrics.boundingRect(rect, Qt.TextWordWrap, about_message)
        rect = rect.marginsAdded(self.default_margins)  # Re add padding for item size.
        return rect.size()
