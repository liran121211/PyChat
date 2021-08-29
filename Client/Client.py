import socket
import threading
import time
from Observable import Observable
from Protocol import *
import LoadingScreen


class ClientTCP(Observable):
    def __init__(self):
        Observable.__init__(self)
        self.server_ip = "167.172.181.78"
        self.server_port = 5678
        self.max_msg_length = 1024
        self.client_socket = None
        self.username = ""
        self.threads = {}
        self.gui = None

    def setup(self):
        """
        Initialize Client GUI.
        Initialize connection to server.
        :return: None, otherwise raise an error.
        """
        # client loading screen
        self.threads["LOADING_SCREEN"] = threading.Thread(target=self.show)
        self.threads["LOADING_SCREEN"].start()
        # Wait for graphics to be loaded.
        time.sleep(1)

        try:
            # server connection
            self.notify(None, "CONNECT")
            time.sleep(1)
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            self.notify(None, "CONNECTED")
            time.sleep(1)

            # client waiting indefinitely to receive messages
            self.threads["RECEIVE_MESSAGES"] = threading.Thread(target=self.recv_msg)
            self.threads["RECEIVE_MESSAGES"].start()

            self.notify(None, "CLIENT_DB_CONNECT")
            time.sleep(0.5)
            self.send_msg(PROTOCOLS["database_status"], "")
            time.sleep(1)

            self.send_msg(PROTOCOLS["login_request"], "liran#123456")

        except ConnectionError:
            self.notify(None, "TIMEOUT")
            exit(0)

    def recv_msg(self):
        """
        Receive messages from server.
        Runs infinitely thorough seperated Thread.
        :return: None
        """
        while True:
            msg = self.client_socket.recv(self.max_msg_length).decode()
            self.clientEvents(self.client_socket, parse_message(msg))
            time.sleep(0.5)  # let client lookup for server responses every 1 sec

    def send_msg(self, cmd, msg):
        """
        Send message to server.
        :param cmd: Identify by protocol with (command)
        :param msg: String that contains the message.
        :return: None
        """
        self.client_socket.send(build_message(cmd, msg).encode())

    def clientEvents(self, client_socket, message):
        """
        Receive message from server that contains (command) to follow.
        :param client_socket: Client socket obj.
        :param message: String message.
        :return: None.
        """
        cmd = message[0]
        msg = message[1]

        if cmd == "LOGIN_OK":
            debugMessages("AUTHENTICATED")

        if cmd == "LOGIN_ERROR":
            debugMessages("NOT_AUTHENTICATED")

        if cmd == "LOGIN_ERROR":
            debugMessages("NOT_AUTHENTICATED")

        if cmd == "DB_CONNECTION_STATUS":
            if msg == "ALIVE":
                self.notify(None, "CLIENT_DB_CONNECTED")
            else:
                self.notify(None, "DB_CONNECTION_ERROR")

    def show(self):
        """
        Graphic Interface of the Client.
        :return: None
        """
        app = LoadingScreen.QtWidgets.QApplication(LoadingScreen.sys.argv)
        LoadingWindow = LoadingScreen.QtWidgets.QMainWindow()
        LoadingWindow.setWindowFlags(LoadingScreen.QtCore.Qt.FramelessWindowHint)
        self.gui = LoadingScreen.Ui_LoadingWindow()
        self.gui.setupUi(LoadingWindow)
        self.attach(self.gui)
        self.notify(None, "GRAPHICS_LOAD")
        LoadingWindow.show()
        LoadingScreen.sys.exit(app.exec_())


if __name__ == "__main__":
    client = ClientTCP()
    client.setup()
