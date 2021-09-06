import random
import typing
from datetime import datetime
import requests
from PyQt5.QtGui import QFont, QPixmap, QIcon, QImage


def randomColor():
    rgb_color = [
        [255, 85, 127],
        [255, 85, 0],
        [85, 170, 127],
        [32, 147, 121],
        [38, 60, 83],
        [228, 151, 77],
        [107, 130, 199],
        [128, 64, 64],
        [128, 128, 64],
        [234, 209, 555],
    ]
    return rgb_color[random.randint(0, 9)]


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


def fetchAvatar(username: str, obj_type: typing.Any, k=0):
    """
    Fetch unique avatar image for every user from online resource
    :param k: API_KEYS index of item
    :param username: username (String)
    :param obj_type: type of obj to be returned.
    :return: QIcon obj, svg (ByteArray)
    """
    IMAGE_LIMIT_REACHED = 'Limit reached'
    image_url = 'http://167.172.181.78/avatars/{0}.svg'.format(username)
    pixmap_obj = QPixmap()
    svg_data = requests.get(image_url).content

    if IMAGE_LIMIT_REACHED in svg_data.decode():
        try:
            svg_data = fetchAvatar(username, None, k + 1)
        except IndexError:
            svg_data = fetchAvatar(username, None, 0)

    pixmap_obj.loadFromData(svg_data)

    if obj_type == "QICON":
        return QIcon(pixmap_obj)

    if obj_type == "SVG":
        return bytearray(svg_data.decode(), encoding='utf-8')

    if obj_type == "QIMAGE":
        return pixmap_obj.toImage()

    if obj_type is None:
        return svg_data


def fetchIcon(index=None):
    """
    Fetch unique avatar image for every user from online resource
    :param index: icon (int) index.
    :return: QImage
    """
    ICONS_LIST = ['Candy Cane', 'Christmas Ball', 'Christmas Candle', 'Christmas Candy', 'Christmas Gift',
                  'Christmas Mitten', 'Christmas Penguin', 'Christmas Star', 'Christmas Stocking', 'Christmas Tree',
                  'Church', 'Cinnamon Sticks', 'Cookies', 'Cruse', 'Dreidel', 'Fireplace', 'Firework',
                  'Gingerbread House', 'Gingerbread Man', 'Hanukkah Donut', 'Hanukkah Gelt', 'Hanukkah Glass',
                  'Hanukkah', 'Holy Bible', 'Ice Skate', 'Jingle Bell', 'Lantern', 'Pie', 'Reindeer', 'Santa', 'Scarf',
                  'Skiing', 'Sled', 'Sleigh', 'Snow Storm', 'Snowman', 'Star of Bethlehem', 'Star of David',
                  'Synagogue' 'Winter']

    image_url = 'http://167.172.181.78/chat_icons/{0}.svg'.format(ICONS_LIST[index])
    svg_data = requests.get(image_url).content
    pixmap_obj = QPixmap()
    pixmap_obj.loadFromData(svg_data)
    return pixmap_obj.toImage()
