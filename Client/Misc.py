# © 2021 Liran Smadja. All rights reserved.

import os
import random
import sys
import typing
import requests

from datetime import datetime
from urllib.request import urlretrieve
from PyQt5.QtGui import QFont, QPixmap, QIcon, QImage

SERVER_URL = 'http://167.172.181.78'


def randomColor() -> tuple:
    """
    Generate ramdom RGB color
    :return: tuple (r,g,b) color.
    """
    R = random.randint(1, 244)
    G = random.randint(1, 244)
    B = random.randint(1, 244)
    return str(R), str(G), str(B)


def createFont(fontFamily=None, PointSize=None, Bold=None, Weight=None) -> QFont:
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


def timeStamp() -> typing.AnyStr:
    """
    Create customized (String) time stamp.
    :return: time stamp (String)
    """
    return "Today at " + datetime.now().strftime("%I:%M %p")


def fetchAvatar(username: str, obj_type: typing.Any) -> QIcon or typing.ByteString or QImage or QPixmap:
    """
    Fetch unique avatar image for every user from online resource
    :param username: username (String)
    :param obj_type: type of obj to be returned.
    :return: QIcon, svg (ByteArray), QImage, QPixmap
    """
    image_url = '{0}/avatars/{1}.svg'.format(SERVER_URL, username)
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


def fetchRoomIcon(name: str, obj_type: typing.Any) -> QImage or QPixmap:
    """
    Fetch unique avatar image for every user from online resource
    :param obj_type: object name (QIMAGE, QPIXMAP)
    :param name: icon (String) name.
    :return: QImage, QPixmap
    """
    image_url = '{0}/chat_icons/{1}'.format(SERVER_URL, name)
    svg_data = requests.get(image_url).content
    pixmap_obj = QPixmap()
    pixmap_obj.loadFromData(svg_data)

    if obj_type == "QIMAGE":
        return pixmap_obj.toImage()

    if obj_type == "QPIXMAP":
        return pixmap_obj


def fetchWindowIcon() -> QIcon:
    """
    Fetch app icon for every window created.
    :return: QIcon
    """
    image_url = '{0}/app_icon/pyc-32x32.png'.format(SERVER_URL)
    svg_data = requests.get(image_url).content
    pixmap_obj = QPixmap()
    pixmap_obj.loadFromData(svg_data)
    return QIcon(pixmap_obj)


def fetchCredits() -> typing.AnyStr:
    """
    Fetch credits info from server.
    :return: HTML decoded (String)
    """
    url_file = '{0}/credits.html'.format(SERVER_URL)
    return requests.get(url_file).content.decode()


def fetchSound() -> None:
    """
    Fetch all sounds files locally.
    :return: None
    """
    try:
        if not os.path.isfile('sounds/login_sound.mp3'):
            urlretrieve('{0}/sounds/login_sound.mp3'.format(SERVER_URL), 'sounds/login_sound.mp3')
        if not os.path.isfile('sounds/logout_sound.mp3'):
            urlretrieve('{0}/sounds/logout_sound.mp3'.format(SERVER_URL), 'sounds/logout_sound.mp3')
        if not os.path.isfile('sounds/new_message.mp3'):
            urlretrieve('{0}/sounds/new_message.mp3'.format(SERVER_URL), 'sounds/new_message.mp3')

    except PermissionError:
        fetchSound()
    except FileNotFoundError:
        os.mkdir('Sounds')
        fetchSound()


def toRGB(hex_color: str) -> tuple:
    """
    Convert hex format string to rgb format string.
    :param hex_color: string (#FFFFFF)
    :return: tuple of (R,G,B)
    """
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def toHex(r: str, g: str, b: str) -> str:
    """
    Convert rgb format string to hex format string.
    :param b: (0-255) color code
    :param g: (0-255) color code
    :param r: (0-255) color code
    :return: string of (#FFFFFF)
    """
    return '%02x%02x%02x' % (int(r), int(g), int(b))


def fetchImages() -> None:
    """
    Fetch all images files locally.
    :return: None
    """
    try:
        if not os.path.isfile('Images/loading.gif'):
            urlretrieve('{0}/misc/loading_data_.gif'.format(SERVER_URL), 'Images/loading.gif')
    except PermissionError:
        fetchImages()
    except FileNotFoundError:
        os.mkdir('Images')
        fetchImages()


def catchErrors(exctype, value, traceback) -> None:
    """
    Catch the errors of PyQt and print them in the terminal.
    :param exctype: Error type
    :param value: the error by String.
    :param traceback: chain of error.
    :return: string detailed error.
    """
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# © 2021 Liran Smadja. All rights reserved.