# © 2021 Liran Smadja. All rights reserved.

import time
import socket
import threading

from Observable import Observable
from Crypto.Cipher import AES
from Protocol import *

# encryption key
SECRET_KEY = b'\x94}a\x1c:L\xa3\xc7\xe1\x86\xd2Oh\x88\x0f3'
IV = b'%\xf0\x01@Q\x8a\xca\xfd\xeb\xdd\xc9\x0b5\x17\xc6D'


def encryptTransmission(msg):
    missing_len = 16 - (len(msg) % 16)
    msg += '&' * missing_len
    encryptor = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    return encryptor.encrypt(msg.encode())


def decryptTransmission(msg):
    decrypter = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    decrypted_message = decrypter.decrypt(msg)
    decoded_message = decrypted_message.decode()
    justify_message = decoded_message.replace('&', '')
    return justify_message


class ClientTCP(Observable):
    def __init__(self):
        Observable.__init__(self)
        self.server_ip = "167.172.181.78"
        self.server_port = 5678
        self.max_msg_length = 2048
        self.client_socket = None
        self.db_waiting_response = True
        self.isTerminated = False
        self.client_db_info = {}

    def setup(self) -> None:
        """
        Initialize Client TCP socket protocol.
        Initialize connection to server.
        :return: None, otherwise raise an error.
        """
        try:
            self.notify("GRAPHICS_LOAD")

            # server connection
            self.notify("CONNECT")
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            self.notify("CONNECTED")

            # client waiting indefinitely to receive messages
            threading.Thread(target=self.recv_msg).start()

            self.notify("CLIENT_DB_CONNECT")
            while self.db_waiting_response:
                self.send_msg(PROTOCOLS["database_status"], "")
                time.sleep(1)

        except ConnectionError:
            self.notify("TIMEOUT")

    def recv_msg(self) -> None:
        """
        Receive messages from server.
        Runs infinitely thorough seperated Thread.
        :return: None
        """
        while not self.isTerminated:
            try:
                msg = self.client_socket.recv(self.max_msg_length).decode()
                self.serverTransmission(self.client_socket, parse_message(msg))
            except ConnectionAbortedError:
                self.isTerminated = True
                self.notify(PROTOCOLS["server_offline"], "")
            except ConnectionResetError:
                self.notify(PROTOCOLS["server_offline"], "")

    def send_msg(self, cmd: typing.AnyStr, msg: typing.AnyStr) -> None:
        """
        Send message to server.
        :param cmd: Identify by protocol with (command)
        :param msg: String that contains the message.
        :return: None
        """
        # if client socket is not closed
        if not self.isTerminated:
            self.client_socket.send(build_message(cmd, msg).encode())

    def serverTransmission(self, client_socket: socket, message) -> None:
        """
        Receive message from server that contains (command) to follow.
        :param client_socket: Client (socket) obj.
        :param message: String message.
        :return: None.
        """
        cmd = message[0]
        msg = message[1]

        if cmd == "DB_CONNECTION_STATUS":
            if msg == "ALIVE":
                self.notify("CLIENT_DB_CONNECTED")
            else:
                self.notify("DB_CONNECTION_ERROR")
            self.db_waiting_response = False

        if cmd == "CLIENT_INFO":
            client_data = split_data(msg, 8)
            self.client_db_info["id"] = client_data[0]
            self.client_db_info["username"] = client_data[1]
            self.client_db_info["password"] = client_data[2]
            self.client_db_info["online"] = client_data[3]
            self.client_db_info["ip_address"] = client_data[4]
            self.client_db_info["avatar"] = client_data[5]
            self.client_db_info["status"] = client_data[6]
            self.client_db_info["room"] = client_data[7]
            self.client_db_info["color"] = client_data[8]

        if cmd == "LOGIN_OK":
            self.notify("LOGIN_OK")

        if cmd == "LOGIN_ERROR":
            self.notify("LOGIN_ERROR")

        if cmd == "ONLINE_USERS":
            self.notify("ONLINE_USERS", msg)

        if cmd == "MESSAGE_TO_CLIENT":
            self.notify("MESSAGE_TO_CLIENT", msg)

        if cmd == "CHAT_ROOMS_NAMES":
            self.notify("CHAT_ROOMS_NAMES", msg)

        if cmd == "CHAT_ROOMS_INFO":
            self.notify("CHAT_ROOMS_INFO", msg)

        if cmd == "BOT_USER_LOGGED_IN":
            self.notify("BOT_USER_LOGGED_IN", msg)

        if cmd == "BOT_USER_LOGGED_OUT":
            self.notify("BOT_USER_LOGGED_OUT", msg)

        if cmd == "REPLACE_USER_AVATAR":
            self.notify("REPLACE_USER_AVATAR", msg)

        if cmd == "REPLACE_USERNAME_COLOR":
            self.notify("REPLACE_USERNAME_COLOR", msg)

        if cmd == "REPLACE_USER_STATUS":
            self.notify("REPLACE_USER_STATUS", msg)

        if cmd == "REGISTER_USER":
            self.notify("REGISTER_USER", msg)

        if cmd == "IS_SERVER_RUNNING":
            pass


if __name__ == "__main__":
    client = ClientTCP()
    client.setup()

# © 2021 Liran Smadja. All rights reserved.
