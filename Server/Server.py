import sys
import time
import random
import socket
import select
import requests
import threading
import DBConnection as DBConn

from sys import exit
from Protocol import *
from Crypto.Cipher import AES
from string import ascii_letters
from multiavatar.multiavatar import multiavatar



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

    def setup(self) -> None:
        """
        Initialize PostgreSQL connection.
        Initialize server socket binding.
        :return: None, otherwise raise an error.
        """
        # Setup server connection
        debugMessages("START_SERVER", True)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen()
        debugMessages("SERVER_STARTED", True)

        # Setup database connection
        self.database = DBConn.DBConnection()
        threading.Thread(target=self.database.connect).start()

        # Sub-Main Thread.
        threading.Thread(target=self.run).start()

    def run(self) -> None:
        """
        Initialize clients connections.
        Loop infinitely to receive requests from clients.
        :return:
        """
        while True:
            self.ready_to_read, self.ready_to_write, in_error = select.select(
                [self.server_socket] + list(self.clients_sockets.keys()), list(self.clients_sockets.keys()), [])

            for current_socket in self.ready_to_read:
                # add new client ip:port the the server listeners.
                if current_socket is self.server_socket:
                    client_socket, client_address = current_socket.accept()
                    self.clients_sockets[client_socket] = client_address
                    print("New client has joined the server: ", client_address)
                else:
                    try:
                        # reply to exist client with the following the PROTOCOL
                        encrypted_data = current_socket.recv(self.max_msg_length)
                        decrypted_data = decryptTransmission(encrypted_data)
                        self.clientTransmission(current_socket, decrypted_data)

                    # in case the customer disconnected
                    except ConnectionError:
                        ip = self.clients_sockets[current_socket][0]
                        port = self.clients_sockets[current_socket][1]
                        ip_address = ip + ":" + str(port)

                        # update online status to (False) of Client.
                        self.database.update("users", "online", "False", "ip_address", ip_address)
                        self.database.update("users", "room", "General", "ip_address", ip_address)

                        # notify all online users who left the chat with bot message.
                        offline_username = self.database.query("users", "ip_address", ip_address, "username")

                        if len(offline_username) != 0:
                            username = offline_username[0][0]
                            self.clientTransmission(current_socket, (PROTOCOLS["bot_user_logged_out"], username))

                        # update client with changed list of users
                        threading.Thread(target=self.online_users).start()

                        print(self.clients_sockets[current_socket], "Disconnected from the server.")
                        self.clients_sockets.pop(current_socket)
                        current_socket.close()

                    except UnicodeDecodeError:
                        pass

            # messages waiting in queue to be delivered (responding to available clients only).
            try:
                for message in self.messages_to_send:
                    current_socket, _ = message
                    # dispatch message to client and remove from queue
                    if current_socket in self.ready_to_write:
                        if current_socket.fileno() != -1:
                            encryptTransmission(message)
                        self.messages_to_send.remove(message)
            except (BrokenPipeError, IOError):
                exit(1)

    def clientTransmission(self, client_socket, message):
        print("SERVER REQUEST: ", message)
        """
        Receive message from client that contains (command) to follow.
        :param client_socket: Client socket obj.
        :param message: encoded (String) message.
        :return: None.
        """
        cmd = message[0]
        msg = message[1]

        if cmd == "DB_CONNECTION_STATUS":
            if self.database.conn is not None:
                if self.database.conn.closed == 0:
                    dispatch = build_message(PROTOCOLS["database_status"], "ALIVE")
                    self.messages_to_send.append((client_socket, dispatch))
            else:
                dispatch = build_message(PROTOCOLS["database_status"], "DEAD")
                self.messages_to_send.append((client_socket, dispatch))

        if cmd == "LOGIN":
            if self.database.conn is not None:
                username, password = msg.split('#')
                client_ip = self.clients_sockets[client_socket]
                cmd_result, data_result = self.database.user_authentication(username, password, client_ip)

                # if user successfully authenticated, send current user data from db.
                if len(data_result) != 0:
                    dispatch = build_message(PROTOCOLS["client_db_info"], join_data(data_result))
                    self.messages_to_send.append((client_socket, dispatch))

                # send authentication result to client
                dispatch = build_message(cmd_result, "")
                self.messages_to_send.append((client_socket, dispatch))

        if cmd == "MESSAGE_TO_SERVER":

            # sender room name , list with all users that belongs to the same room name.
            room_name = msg.split('#')[2]
            query_result = self.database.query("users", "room", room_name, 'ip_address')

            # iterate thorough available clients only.
            for client in self.ready_to_write:
                ip, port = client.getpeername()
                socket_ip = "{0}:{1}".format(ip, str(port))

                # send message to qualified users only.
                for ip_address in query_result:
                    if ip_address[0] == socket_ip:
                        dispatch = build_message(PROTOCOLS["server_message"], msg)
                        self.messages_to_send.append((client, dispatch))

        if cmd == "ONLINE_USERS":
            threading.Thread(target=self.online_users).start()

        if cmd == "CHAT_ROOMS_NAMES":
            query_result = self.database.query(table="rooms", filter_key=None, filter_value=None)
            data = [(value[1], value[2]) for value in query_result]
            encoded_data = '##'.join(['#'.join(value) for value in data])

            dispatch = build_message(PROTOCOLS["chat_rooms_names"], encoded_data)
            self.messages_to_send.append((client_socket, dispatch))

        if cmd == "CHANGE_USER_ROOM":
            room_name, username = msg.split('#')
            self.database.update('users', 'room', room_name, 'username', username)
            threading.Thread(target=self.rooms_info).start()

        if cmd == "BOT_USER_LOGGED_IN":
            # send to all client that new user has joined the chat.
            username = "PyBOT"
            text_direction = "True"
            room_name = "General"
            message = " has now joined the chat!"
            bot_message = "{0}#{1}#{2}#{3}".format(username, text_direction, room_name, message)

            for client in self.ready_to_write:
                if client is not client_socket:
                    dispatch = build_message(PROTOCOLS["bot_user_logged_in"], bot_message)
                    self.messages_to_send.append((client, dispatch))

        if cmd == "BOT_USER_LOGGED_OUT":
            # send to all client that new user has joined the chat.
            username = "PyBOT"
            text_direction = "True"
            room_name = "General"
            message = " has now left the chat!"
            bot_message = "{0}#{1}#{2}#{3}".format(username, text_direction, room_name, message)

            for client in self.ready_to_write:
                if client is not client_socket:
                    dispatch = build_message(PROTOCOLS["bot_user_logged_out"], bot_message)
                    self.messages_to_send.append((client, dispatch))

        if cmd == "REPLACE_USER_AVATAR":
            # real-time user avatar updating
            threading.Thread(target=replaceAvatar, args=(client_socket, msg)).start()

        if cmd == "REPLACE_USERNAME_COLOR":
            color, username = msg.split('#')
            self.database.update('users', 'color', color, 'username', username)
            dispatch = build_message(PROTOCOLS["replace_username_color"], "SUCCESS")
            self.messages_to_send.append((client_socket, dispatch))

        if cmd == "REPLACE_USER_STATUS":
            status, username = msg.split('#')
            self.database.update('users', 'status', status, 'username', username)
            dispatch = build_message(PROTOCOLS["replace_user_status"], "SUCCESS")
            self.messages_to_send.append((client_socket, dispatch))

        if cmd == "REFRESH_CLIENT_INFO":
            username, password = msg.split('#')
            client_ip = self.clients_sockets[client_socket]
            login_cmd_result, login_data_result = self.database.user_authentication(username, password, client_ip)

            # if user successfully authenticated, send current user data from db.
            if len(login_data_result) != 0:
                dispatch = build_message(PROTOCOLS["client_db_info"], join_data(login_data_result))
                self.messages_to_send.append((client_socket, dispatch))

        if cmd == "IS_SERVER_RUNNING":
            dispatch = build_message(PROTOCOLS["is_server_running"], "ALIVE")
            self.messages_to_send.append((client_socket, dispatch))

        if cmd == "REGISTER_USER":
            decoded_data = msg.split('#')

            # return registration result to client
            result = self.database.insert("NEW_USER", decoded_data)

            if result[0] == "#USERNAME_EXIST#":
                dispatch = build_message(PROTOCOLS["register_user"], "USERNAME_EXIST")
                self.messages_to_send.append((client_socket, dispatch))

            elif len(result) != 0:
                # fetch new avatar for new user
                replaceAvatar(current_socket=client_socket, username=decoded_data[0])

                # send confirmation of registration
                dispatch = build_message(PROTOCOLS["register_user"], "SUCCESS")
                self.messages_to_send.append((client_socket, dispatch))
            else:
                # send error upon registration
                dispatch = build_message(PROTOCOLS["register_user"], "FAIL")
                self.messages_to_send.append((client_socket, dispatch))

    def online_users(self):
        # check if database is reachable.
        if self.database.conn is not None:

            if self.database.conn.closed == 0:
                query_result = self.database.query(table="users")

                # convert (query_result) to protocol transmission.
                users = [[str(_[1]), str(_[3]), str(_[5]), str(_[6]), str(_[8])] for _ in query_result]
                encoded_users = '##'.join(['#'.join(value) for value in users])

                # check if there are clients available for an update.
                for available_client in self.ready_to_write:

                    # make sure client socket is not closed.
                    if available_client.fileno() != -1:
                        dispatch = build_message(PROTOCOLS["online_users"], encoded_users)
                        self.messages_to_send.append((available_client, dispatch))

    def rooms_info(self):
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
                        dispatch = build_message(PROTOCOLS["chat_rooms_info"], encoded_data)
                        self.messages_to_send.append((available_client, dispatch))


def decryptTransmission(data: typing.AnyStr) -> tuple:
    """
    Decrypt data from client.
    :param data: encrypted string (bytes)
    :return: (cmd, msg) tuple.
    """
    # create decrypter
    decrypter = AES.new(DBConn.SECRET_KEY, AES.MODE_CBC, DBConn.IV)

    # decrypt--> decode--> parse data
    try:
        decrypted_data = decrypter.decrypt(data)
        decoded_data = decrypted_data.decode('cp424')
        justify_data = decoded_data.replace('~', '')
        parsed_data = parse_message(justify_data)
    except ValueError:
        sys.exit(1)
    return parsed_data


def encryptTransmission(message: tuple) -> None:
    """
    Encrypt data and send it to client.
    :param message: tuple(client_socket,msg)
    :return: None
    """
    current_socket, data = message

    # complete for missing bytes
    missing_len = 16 - (len(data) % 16)
    data += '~' * missing_len

    # create encryptor
    encryptor = AES.new(DBConn.SECRET_KEY, AES.MODE_CBC, DBConn.IV)

    # send encoded message --> encrypted message to client.
    try:
        encoded_message = data.encode('cp424')
        encrypted_message = encryptor.encrypt(encoded_message)
        current_socket.send(encrypted_message)
    except ValueError:
        sys.exit(1)


def replaceAvatar(current_socket, username) -> None:
    """
    Fetch unique avatar image from online resource
    :param username: username (String) who requested to change the avatar.
    :param current_socket: client socket.
    """
    random_string = ''.join(random.choice(ascii_letters) for _ in range(15))

    svg_data = str(multiavatar(random_string, None, None)).encode(encoding='UTF-8')
    open('../var/www/html/avatars/{0}.svg'.format(username), 'wb').write(svg_data)

    dispatch = build_message(PROTOCOLS["replace_user_avatar"], "SUCCESS")
    server.messages_to_send.append((current_socket, dispatch))


SERVER_STARTED = False
while True:
    try:
        if not SERVER_STARTED:
            server = MultipleTCP()
            server.setup()
            SERVER_STARTED = True

    except Exception as error:
        print(error)
        SERVER_STARTED = False
        time.sleep(5)
