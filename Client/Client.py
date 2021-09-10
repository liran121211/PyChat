import socket
import threading
import time

from Observable import Observable
from Protocol import *


class ClientTCP(Observable):
    def __init__(self):
        Observable.__init__(self)
        self.server_ip = "167.172.181.78"
        self.server_port = 5678
        self.max_msg_length = 2048
        self.client_socket = None
        self.client_db_info = {}
        self.db_waiting_response = True

    def setup(self):
        """
        Initialize Client GUI.
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
            exit(0)

    def recv_msg(self):
        """
        Receive messages from server.
        Runs infinitely thorough seperated Thread.
        :return: None
        """
        while True:
            msg = self.client_socket.recv(self.max_msg_length).decode()
            self.serverTransmission(self.client_socket, parse_message(msg))

    def send_msg(self, cmd, msg):
        """
        Send message to server.
        :param cmd: Identify by protocol with (command)
        :param msg: String that contains the message.
        :return: None
        """
        self.client_socket.send(build_message(cmd, msg).encode())

    def serverTransmission(self, client_socket, message):
        """
        Receive message from server that contains (command) to follow.
        :param client_socket: Client socket obj.
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
            debugMessages("AUTHENTICATED")

        if cmd == "LOGIN_ERROR":
            self.notify("LOGIN_ERROR")
            debugMessages("NOT_AUTHENTICATED")

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

if __name__ == "__main__":
    client = ClientTCP()
    client.setup()
