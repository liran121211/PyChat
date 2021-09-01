import psycopg2
from Protocol import *

DATABASE_ADDRESS = "127.0.0.1"
DATABASE_NAME = "OnlineChat"
DATABASE_SCHEME = "online_chat_db"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = ""
DATABASE_PORT = 5432


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
        self.update(table="users", column="online", new_value=True, filter_key="id", filter_value=sql_query_result[0][0])

        # update current client ip to the logged-in user
        ip_address = client_address[0] + ":" + str(client_address[1])
        self.update(table="users", column="ip_address", new_value=ip_address, filter_key="id",filter_value=sql_query_result[0][0])

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

        if len(self.query(table, filter_key, filter_value, column)) != 0:
            debugMessages("DB_UPDATE_QUERY_SUCCESS")
        else:
            debugMessages("DB_UPDATE_QUERY_FAIL")

    def query(self, table, filter_key, filter_value, column= None):
        """
        Retrieve record from the database.
        :param table: database table name
        :param column: database column name
        :param filter_key: database column name to filter records. (Default: unique column)
        :param filter_value: database row value to filter records
        :return: None
        """
        if column is None:
            sql_auth = "SELECT * FROM {0}.{1} WHERE {2}='{3}'". \
                format(DATABASE_SCHEME, table, filter_key, filter_value)
            self.cursor.execute(sql_auth)
            sql_query_result = self.cursor.fetchall()
            return sql_query_result

        else:
            sql_auth = "SELECT {0} FROM {1}.{2} WHERE {3}='{4}'". \
                format(column, DATABASE_SCHEME, table, filter_key, filter_value)
            self.cursor.execute(sql_auth)
            sql_query_result = self.cursor.fetchall()
            return sql_query_result

    def close_connection(self):
        """
        Close connection to the PostgreSQL database.
        :return: None.
        """
        self.cursor.close()
        self.conn.close()

