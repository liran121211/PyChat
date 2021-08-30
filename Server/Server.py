import socket
import select
import DBConnection as DBConn
import threading
from Protocol import *


class MultipleTCP:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = "0.0.0.0"
        self.server_port = 5678
        self.max_msg_length = 1024
        self.clients_sockets = {}
        self.messages_to_send = []
        self.database = None
        self.ready_to_write = None
        self.ready_to_read = None

    def setup(self):
        """
        Initialize PostgreSQL connection.
        Initialize server socket binding.
        :return: None, otherwise raise an error.
        """
        # Setup server connection
        print("Initializing server...")
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen()
        print("Server is up and running.")

        # Setup database connection
        self.database = DBConn.DBConnection()
        threading.Thread(target=self.database.connect()).start()

    def run(self):
        """
        Initialize clients connections.
        Loop infinitely to receive requests from clients.
        :return:
        """
        while True:
            self.ready_to_read, self.ready_to_write , in_error = select.select(
                [self.server_socket] + list(self.clients_sockets.keys()), list(self.clients_sockets.keys()), [])

            for current_socket in self.ready_to_read:
                if current_socket is self.server_socket:
                    client_socket, client_address = current_socket.accept()
                    self.clients_sockets[client_socket] = client_address
                    print("New client has joined the server: ", client_address)
                    self.messages_to_send.append((client_socket, "<----- WELCOME TO ALIEN SERVER ----->"))

                else:
                    try:
                        client_msg = parse_message(current_socket.recv(self.max_msg_length).decode())
                        self.clientTransmission(current_socket, client_msg)

                    except ConnectionError:
                        print("Client: ", self.clients_sockets[current_socket], " is now disconnected.")
                        self.clients_sockets.pop(current_socket)
                        current_socket.close()

            # responding to available clients only.
            for message in self.messages_to_send:
                current_socket, data = message
                if current_socket in self.ready_to_write:
                    current_socket.send(data.encode())
                    self.messages_to_send.remove(message)

    def clientTransmission(self, client_socket, message):
        """
        Receive message from client that contains (command) to follow.
        :param client_socket: Client socket obj.
        :param message: String message.
        :return: None.
        """
        cmd = message[0]
        msg = message[1]

        if cmd == "LOGIN":
            if self.database.conn is not None:
                username, password = msg.split('#')
                login_result, login_fetched_data = self.database.user_authentication(username, password)
                client_socket.send(build_message(login_result, "").encode())

                # if user successfully authenticated, send current user data from db.
                if len(login_fetched_data) != 0:
                    client_socket.send(build_message(PROTOCOLS["client_db_info"], join_data(login_fetched_data)).encode())

        if cmd == "DB_CONNECTION_STATUS":
            if self.database.conn is not None:
                if self.database.conn.closed == 0:
                    client_socket.send(build_message(PROTOCOLS["database_status"], "ALIVE").encode())
            else:
                client_socket.send(build_message(PROTOCOLS["database_status"], "DEAD").encode())

        if cmd == "MESSAGE_TO_SERVER":
            for client in self.ready_to_write:
                client.send(build_message(PROTOCOLS["server_message"], msg).encode())

server = MultipleTCP()
server.setup()
server.run()
