import random
import sys
import typing
from datetime import datetime
import requests
from PyQt5.QtGui import QFont, QPixmap, QIcon


def randomColor():
    R = random.randint(0, 244)
    G = random.randint(0, 244)
    B = random.randint(0, 244)
    return str(R), str(G), str(B)


def createFont(fontFamily=None, PointSize=None, Bold=None, Weight=None):
    """
    Create new Font object.
    :param fontFamily: name of the font.
    :param PointSize: size of font.
    :param Bold: True/False value.
    :param Weight: N/A
    :return: QFont object.
    """
    font = QFont()
    font.setFamily(fontFamily)
    font.setPointSize(PointSize)
    font.setBold(Bold)
    font.setWeight(Weight)
    return font


def timeStamp():
    return "Today at " + datetime.now().strftime("%I:%M %p")


def fetchAvatar(username: str, obj_type: typing.Any):
    """
    Fetch unique avatar image for every user from online resource
    :param username: username (String)
    :param obj_type: type of obj to be returned.
    :return: QIcon obj, svg (ByteArray)
    """
    image_url = 'http://167.172.181.78/avatars/{0}.svg'.format(username)
    pixmap_obj = QPixmap()
    svg_data = requests.get(image_url).content
    pixmap_obj.loadFromData(svg_data)

    if obj_type == "QICON":
        return QIcon(pixmap_obj)

    if obj_type == "SVG":
        return bytearray(svg_data.decode(), encoding='utf-8')

    if obj_type == "QIMAGE":
        return pixmap_obj.toImage()

    if obj_type == "PIXMAP":
        return pixmap_obj

    if obj_type is None:
        return svg_data


def fetchIcon(name):
    """
    Fetch unique avatar image for every user from online resource
    :param name: icon (String) name.
    :return: QImage
    """
    image_url = 'http://167.172.181.78/chat_icons/{0}'.format(name)
    svg_data = requests.get(image_url).content
    pixmap_obj = QPixmap()
    pixmap_obj.loadFromData(svg_data)
    return pixmap_obj.toImage()


def fetchAppIcon() -> QIcon:
    """
    Fetch app icon for every window created.
    :return: QIcon
    """
    image_url = 'http://167.172.181.78/app_icon/pyc-32x32.png'
    svg_data = requests.get(image_url).content
    pixmap_obj = QPixmap()
    pixmap_obj.loadFromData(svg_data)
    return QIcon(pixmap_obj)


def toRGB(hex_color: str) -> tuple:
    # credits to : https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def toHex(r: str, g: str, b: str) -> str:
    return '%02x%02x%02x' % (int(r), int(g), int(b))


def catchErrors(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
