import psycopg2
from Protocol import *


class DBConnection:
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
            debugMessages("DB_CONNECT")
            self.conn = psycopg2.connect(
                host="127.0.0.1",
                database="OnlineChat",
                user="postgres",
                password="",
                port=5432)

        except (Exception, psycopg2.OperationalError):
            debugMessages("DB_CONNECTION_ERROR")

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
            debugMessages("DB_CONNECTED")

        except (Exception, psycopg2.DatabaseError):
            debugMessages("DB_OPERATION_ERROR")

    def user_authentication(self, username, password):
        """
        Validate login details of the client.
        :param username: client (String) username
        :param password: client (String) password
        :return: success message (Protocol), otherwise error message.
        """
        sql_auth = "SELECT * FROM online_chat_db.users WHERE username = %s AND password = %s"
        self.cursor.execute(sql_auth, (username, password))
        sql_query_result = self.cursor.fetchall()

        # check if given data exists in sql table
        if len(sql_query_result) == 0:
            return PROTOCOLS["login_failed_msg"], []
        return PROTOCOLS["login_ok_msg"], sql_query_result[0]

    def sql_query(self, request):
        if request == "CLIENT_INFO":
            pass

    def close_connection(self):
        """
        Close connection to the PostgreSQL database.
        :return: None.
        """
        self.cursor.close()
        self.conn.close()
