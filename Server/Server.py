import socket
import select
import time

import DBConnection as DBConn
import threading
from Protocol import *


class MultipleTCP:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = "0.0.0.0"
        self.server_port = 5678
        self.max_msg_length = 2048
        self.database = None
        self.clients_sockets = {}
        self.messages_to_send = []
        self.ready_to_write = []
        self.ready_to_read = []

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
        threading.Thread(target=self.database.connect).start()

        # Sub-Main Thread.
        threading.Thread(target=self.run).start()

        # Online user list.
        threading.Thread(target=self.online_users).start()

        # real-time room chats info update
        threading.Thread(target=self.rooms_info).start()

    def run(self):
        """
        Initialize clients connections.
        Loop infinitely to receive requests from clients.
        :return:
        """
        while True:
            self.ready_to_read, self.ready_to_write, in_error = select.select(
                [self.server_socket] + list(self.clients_sockets.keys()), list(self.clients_sockets.keys()), [])

            for current_socket in self.ready_to_read:
                if current_socket is self.server_socket:
                    client_socket, client_address = current_socket.accept()
                    self.clients_sockets[client_socket] = client_address
                    print("New client has joined the server: ", client_address)

                else:
                    try:
                        client_msg = parse_message(current_socket.recv(self.max_msg_length).decode())
                        self.client_transmission(current_socket, client_msg)

                    except ConnectionError:
                        ip = self.clients_sockets[current_socket][0]
                        port = self.clients_sockets[current_socket][1]
                        ip_address = ip + ":" + str(port)
                        # update online status to (False) of Client.
                        self.database.update(table="users", column="online", new_value=False, filter_key="ip_address",
                                             filter_value=ip_address)

                        print(self.clients_sockets[current_socket], debugMessages("DISCONNECTED"))
                        self.clients_sockets.pop(current_socket)
                        current_socket.close()

            # responding to available clients only.
            for message in self.messages_to_send:
                current_socket, data = message
                if current_socket in self.ready_to_write:
                    current_socket.send(data.encode())
                    self.messages_to_send.remove(message)

    def client_transmission(self, client_socket, message):
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
                client_ip = self.clients_sockets[client_socket]
                login_cmd_result, login_data_result = self.database.user_authentication(username, password, client_ip)

                # if user successfully authenticated, send current user data from db.
                if len(login_data_result) != 0:
                    client_socket.send(
                        build_message(PROTOCOLS["client_db_info"], join_data(login_data_result)).encode())

                # send authentication result to client
                client_socket.send(build_message(login_cmd_result, "").encode())

        if cmd == "DB_CONNECTION_STATUS":
            if self.database.conn is not None:
                if self.database.conn.closed == 0:
                    client_socket.send(build_message(PROTOCOLS["database_status"], "ALIVE").encode())
            else:
                client_socket.send(build_message(PROTOCOLS["database_status"], "DEAD").encode())

        if cmd == "MESSAGE_TO_SERVER":
            for client in self.ready_to_write:
                client.send(build_message(PROTOCOLS["server_message"], msg).encode())

        if cmd == "CHAT_ROOMS_NAMES":
            query_result = self.database.query(table="rooms", filter_key=None, filter_value=None)
            data = [(value[1], value[2]) for value in query_result]
            encoded_data = '##'.join(['#'.join(value) for value in data])
            client_socket.send(build_message(PROTOCOLS["chat_rooms_names"], encoded_data).encode())

        if cmd == "CHANGE_USER_ROOM":
            room_name,username = msg.split('#')
            self.database.update(table='users', column='room', new_value=room_name, filter_key='username', filter_value=username)

    def online_users(self):
        while True:
            # check if database is reachable.
            if self.database.conn is not None:

                if self.database.conn.closed == 0:
                    query_result = self.database.query(table="users")

                    # convert (query_result) to protocol transmission.
                    users = [[str(value[1]), str(value[3]), str(value[5]), str(value[6])] for value in query_result]
                    encoded_users = '##'.join(['#'.join(value) for value in users])

                    # check if there are clients available for an update.
                    for available_client in self.ready_to_write:

                        # make sure client socket is not closed.
                        if available_client.fileno() != -1:
                            available_client.send(build_message(PROTOCOLS["online_users"], encoded_users).encode())
            time.sleep(2)

    def rooms_info(self):
        while True:
            # check if database is reachable.
            if self.database.conn is not None:

                if self.database.conn.closed == 0:
                    query_result = self.database.query(table="users", filter_key=None, filter_value=None)
                    data = [(value[1], value[7]) for value in query_result]
                    encoded_data = '##'.join(['#'.join(value) for value in data])

                    # check if there are clients available for an update.
                    for available_client in self.ready_to_write:

                        # make sure client socket is not closed.
                        if available_client.fileno() != -1:
                            available_client.send(build_message(PROTOCOLS["chat_rooms_info"], encoded_data).encode())
            time.sleep(1)

server = MultipleTCP()
server.setup()
