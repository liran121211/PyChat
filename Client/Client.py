import socket
import threading
import time
from Observable import Observable
from Protocol import *
import LoadingScreen, LoginScreen


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
            self.gui.LoginWindow.close()

        if cmd == "LOGIN_ERROR":
            debugMessages("NOT_AUTHENTICATED")

        if cmd == "DB_CONNECTION_STATUS":
            if msg == "ALIVE":
                self.notify("CLIENT_DB_CONNECTED")
                # client login screen
                time.sleep(0.5)
                self.threads["LOGIN_SCREEN"] = threading.Thread(target=self.LoginGUI)
                self.threads["LOGIN_SCREEN"].start()

            else:
                self.notify("DB_CONNECTION_ERROR")

    def LoadingGUI(self):
        """
        Graphic Interface of the Client.
        :return: None
        """
        app = LoadingScreen.QtWidgets.QApplication(LoadingScreen.sys.argv)
        LoadingWindow = LoadingScreen.QtWidgets.QMainWindow()
        LoadingWindow.setWindowFlags(LoadingScreen.QtCore.Qt.FramelessWindowHint)
        self.gui = LoadingScreen.LoadingScreen()
        self.gui.setupUi(LoadingWindow)
        self.attach(self.gui)  # Attach LoadingScreen observer
        self.notify("GRAPHICS_LOAD")
        LoadingWindow.show()
        LoadingScreen.sys.exit(app.exec_())

    def LoginGUI(self):
        app = LoginScreen.QtWidgets.QApplication(LoginScreen.sys.argv)
        LoginWindow = LoginScreen.QtWidgets.QMainWindow()
        LoginWindow.setWindowFlags(LoginScreen.QtCore.Qt.FramelessWindowHint)
        self.gui = LoginScreen.LoginScreen()
        self.gui.setupUi(LoginWindow)
        self.gui.attach(self)  # Attach Client observer to LoginScreen
        LoginWindow.show()
        LoginScreen.sys.exit(app.exec_())

    def update(self, observable, msg):
        if isinstance(msg, list):
            if len(msg) > 0:
                if msg[0] == "LOGIN":
                    self.send_msg(msg[0], msg[1] + "#" + msg[2])

if __name__ == "__main__":
    client = ClientTCP()
    client.setup()
