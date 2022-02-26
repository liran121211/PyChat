import time

import psycopg2
from Protocol import *
import threading

DATABASE_ADDRESS = "NONE"
DATABASE_NAME = "NONE"
DATABASE_SCHEME = "NONE"
DATABASE_USER = "NONE"
DATABASE_PASSWORD = "NONE"
DATABASE_PORT = "NONE"
SECRET_KEY = b'\xf8[\xd6\t<\xd8\x04a5siif\x93\xdc\xe0'
IV = b'\x8e;\xf21bB\x0c\x95\x93\xce\xe9J3,\x04\xdd'

class DBConnection():
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.log = ""

    def connect(self):
        """
        Establish connection to PostgreSQL server.
        :return: None, otherwise raise an error.
        """
        try:
            debugMessages("DB_CONNECT", True)
            self.conn = psycopg2.connect(
                host=DATABASE_ADDRESS,
                database=DATABASE_NAME,
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                port=DATABASE_PORT)

        except (Exception, psycopg2.OperationalError):
            debugMessages("DB_CONNECTION_ERROR", True)

        try:
            # connect to the PostgreSQL server
            self.log += 'Connecting to the PostgreSQL database...\n'

            # create a cursor
            self.cursor = self.conn.cursor()

            # execute a statement
            self.log += 'PostgreSQL database version:\n'
            self.cursor.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = self.cursor.fetchone()
            self.log += str(db_version) + "\n"
            debugMessages("DB_CONNECTED", True)

        except (Exception, psycopg2.DatabaseError):
            debugMessages("DB_OPERATION_ERROR", True)

    def user_authentication(self, username, password, client_address):
        """
        Validate login details of the client.
        :param username: client (String) username
        :param password: client (String) password
        :param client_address: IP:PORT of client.
        :return: success message (Protocol), otherwise error message.
        """
        sql_auth = "SELECT * FROM online_chat_db.users WHERE username = %s AND password = %s"
        self.cursor.execute(sql_auth, (username, password))
        sql_query_result = self.cursor.fetchall()

        # check if given data exists in sql table
        if len(sql_query_result) == 0:
            return PROTOCOLS["login_failed_msg"], []

        # update online status to (True) of Client.
        self.update(table="users", column="online", new_value=True, filter_key="id",
                    filter_value=sql_query_result[0][0])

        # attach current socket ip to the logged-in user
        ip_address = "{0}:{1}".format(client_address[0], str(client_address[1]))
        self.update(table="users", column="ip_address", new_value=ip_address, filter_key="id",
                    filter_value=sql_query_result[0][0])

        return PROTOCOLS["login_ok_msg"], sql_query_result[0]

    def update(self, table, column, new_value, filter_key, filter_value):
        """
        Update record in the database
        :param table: database table name
        :param column: database column name
        :param filter_key: database column name to filter records. (Default: unique column)
        :param filter_value: database row value to filter records
        :param new_value: new data to update.
        :return: None
        """
        sql_query = "UPDATE {0}.{1} SET {2}='{3}' WHERE {4}='{5}'". \
            format(DATABASE_SCHEME, table, column, new_value, filter_key, filter_value)
        self.cursor.execute(sql_query)
        self.conn.commit()

        if len(self.query(table, filter_key, filter_value, column)) == 0:
            debugMessages("DB_UPDATE_QUERY_FAIL", True)

    def query(self, table, filter_key=None, filter_value=None, column=None):
        """
            Retrieve record from the database.
            :param table: database table name
            :param column: database column name
            :param filter_key: database column name to filter records. (Default: unique column)
            :param filter_value: database row value to filter records
            :return: None
            """
        if column is None and filter_key is not None and filter_value is not None:
            sql_auth = "SELECT * FROM {0}.{1} WHERE {2}='{3}'". \
                format(DATABASE_SCHEME, table, filter_key, filter_value)
            self.cursor.execute(sql_auth)
            sql_query_result = self.cursor.fetchall()
            return sql_query_result

        if column is not None and filter_key is None and filter_value is None:
            sql_auth = "SELECT {0} FROM {1}.{2}".format(column, DATABASE_SCHEME, table)
            self.cursor.execute(sql_auth)
            sql_query_result = self.cursor.fetchall()
            return sql_query_result

        if column is not None and filter_key is not None and filter_value is not None:
            sql_auth = "SELECT {0} FROM {1}.{2} WHERE {3}='{4}'". \
                format(column, DATABASE_SCHEME, table, filter_key, filter_value)
            self.cursor.execute(sql_auth)
            sql_query_result = self.cursor.fetchall()
            return sql_query_result

        if column is None and filter_key is None and filter_value is None:
            print("{} table called from DB".format(table))
            sql_auth = "SELECT * FROM {0}.{1}".format(DATABASE_SCHEME, table)
            self.cursor.execute(sql_auth)
            sql_query_result = self.cursor.fetchall()
            return sql_query_result

    def insert(self, cmd, data):
        if cmd == "NEW_USER":
            # organize data to variables.
            username, password, online, ip_address, avatar = data[0], data[1], data[2], data[3], data[4]
            status, room, color = data[5], data[6], data[7]

            # check if username exist
            search_username = self.query(table='users', filter_key='username', filter_value=username, column='username')

            if len(search_username) == 0:
                # create user id in chronological order.
                self.cursor.execute("SELECT MAX(id)+1 FROM online_chat_db.users")
                new_id = self.cursor.fetchall()[0][0]

                # organize data for sql execution.
                columns = "id, username, password, online, ip_address,avatar, status, room, color"
                values = "{0},'{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}'". \
                    format(new_id, username, password, online, ip_address, avatar, status, room, color)

                self.cursor.execute("INSERT INTO online_chat_db.users({0}) VALUES ({1})".format(columns, values))
                self.conn.commit()

                # check if record was successfully inserted
                return self.query(table='users', filter_key='username', filter_value=username, column='username')

            else:
                return ["#USERNAME_EXIST#"]

    def close_connection(self):
        """
        Close connection to the PostgreSQL database.
        :return: None.
        """
        self.cursor.close()
        self.conn.close()
