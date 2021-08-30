import socket
import threading
import time

from PyQt5.QtCore import QThread

from Observable import Observable
from Protocol import *
import LoadingScreen, LoginScreen, MainChatScreen


class ClientTCP(Observable):
    def __init__(self):
        Observable.__init__(self)
        self.server_ip = "167.172.181.78"
        self.server_port = 5678
        self.max_msg_length = 1024
        self.client_socket = None
        self.client_db_info = {}
        self.threads = {}
        self.gui = None

    def setup(self):
        """
        Initialize Client GUI.
        Initialize connection to server.
        :return: None, otherwise raise an error.
        """
        # client loading screen
        self.threads["LOADING_SCREEN"] = threading.Thread(target=self.LoadingGUI)
        self.threads["LOADING_SCREEN"].start()
        # Wait for graphics to be loaded.
        time.sleep(1)

        try:
            # server connection
            self.notify("CONNECT")
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            self.notify("CONNECTED")
            time.sleep(1)

            # client waiting indefinitely to receive messages
            self.threads["RECEIVE_MESSAGES"] = threading.Thread(target=self.recv_msg)
            self.threads["RECEIVE_MESSAGES"].start()

            self.notify("CLIENT_DB_CONNECT")
            self.send_msg(PROTOCOLS["database_status"], "")

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
            time.sleep(0.5)  # let client lookup for server responses every 0.5 sec

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

        if cmd == "CLIENT_INFO":
            client_data = split_data(msg, 2)
            self.client_db_info["id"] = client_data[0]
            self.client_db_info["username"] = client_data[1]
            self.client_db_info["password"] = client_data[2]

        if cmd == "LOGIN_OK":
            self.gui.LoginWindow.close()
            self.threads["CHAT_SCREEN"] = threading.Thread(target=self.ChatGUI)
            self.threads["CHAT_SCREEN"].start()

        if cmd == "LOGIN_ERROR":
            self.gui.login_result.setText("Invalid username or password.")
            self.gui.login_result.setStyleSheet("color: rgb(236, 31, 39);")
            debugMessages("NOT_AUTHENTICATED")

        if cmd == "DB_CONNECTION_STATUS":
            if msg == "ALIVE":
                self.notify("CLIENT_DB_CONNECTED")
                # move to client login screen
                self.threads["LOGIN_SCREEN"] = threading.Thread(target=self.LoginGUI)
                self.threads["LOGIN_SCREEN"].start()

            else:
                self.notify("DB_CONNECTION_ERROR")

        if cmd == "MESSAGE_TO_CLIENT":
            self.gui.chat_update(msg)




    def LoadingGUI(self):
        """
        Graphic Interface of the Client.
        :return: None
        """
        app = LoadingScreen.QtWidgets.QApplication(LoadingScreen.sys.argv)
        LoadingWindow = LoadingScreen.QtWidgets.QMainWindow()
        LoadingWindow.setWindowFlags(LoadingScreen.QtCore.Qt.FramelessWindowHint)
        LoadingWindow.setAttribute(LoadingScreen.QtCore.Qt.WA_TranslucentBackground)
        self.gui = LoadingScreen.LoadingScreen()
        self.gui.setupUi(LoadingWindow)
        self.attach(self.gui)  # Attach LoadingScreen observer
        self.notify("GRAPHICS_LOAD")
        LoadingWindow.show()
        LoadingScreen.sys.exit(app.exec_())

    def LoginGUI(self):
        time.sleep(0.5)
        app = LoginScreen.QtWidgets.QApplication(LoginScreen.sys.argv)
        LoginWindow = LoginScreen.QtWidgets.QMainWindow()
        LoginWindow.setWindowFlags(LoginScreen.QtCore.Qt.FramelessWindowHint)
        self.gui = LoginScreen.LoginScreen()
        self.gui.setupUi(LoginWindow)
        self.gui.attach(self)  # Attach Client observer to LoginScreen
        LoginWindow.show()
        LoginScreen.sys.exit(app.exec_())

    def ChatGUI(self):
        time.sleep(0.5)
        while len(self.client_db_info) == 0:
            pass
        app = MainChatScreen.QtWidgets.QApplication(MainChatScreen.sys.argv)
        MainChatWindow = MainChatScreen.QtWidgets.QMainWindow()
        self.gui = MainChatScreen.MainChatScreen()
        self.gui.client_data = self.client_db_info
        self.gui.setupUi(MainChatWindow)
        self.gui.attach(self)  # Attach Client observer to MainChatScreen
        MainChatWindow.show()
        MainChatScreen.sys.exit(app.exec_())

    def update(self, observable, data):
        if isinstance(data, list):
            if len(data) > 0:
                if data[0] == "LOGIN":
                    self.send_msg(data[0], data[1] + "#" + data[2])

        if "MESSAGE_TO_SERVER" in data:
            cmd, msg = parse_message(data)
            self.send_msg(cmd, msg)


if __name__ == "__main__":
    client = ClientTCP()
    client.setup()
