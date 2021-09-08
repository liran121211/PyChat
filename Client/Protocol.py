# Protocol Constants
CMD_FIELD_LENGTH = 16  # Exact length of command field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages
# In this dictionary we will have all the client and server command names

PROTOCOLS = {
    "login_request": "LOGIN",
    "logout_request": "LOGOUT",
    "client_message": "MESSAGE_TO_SERVER",
    "server_message": "MESSAGE_TO_CLIENT",
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "LOGIN_ERROR",
    "database_status": "DB_CONNECTION_STATUS",
    "client_db_info": "CLIENT_INFO",
    "online_users": "ONLINE_USERS",
    "chat_rooms_names": "CHAT_ROOMS_NAMES",
    "chat_rooms_info": "CHAT_ROOMS_INFO",
    "change_user_room": "CHANGE_USER_ROOM",
    "bot_user_logged_in": "BOT_USER_LOGGED_IN",
    "bot_user_logged_out": "BOT_USER_LOGGED_OUT",

}  # .. Add more commands if needed

# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occurred
    """
    full_msg = None
    for item in PROTOCOLS.values():
        if cmd == item:
            C = cmd + (" " * (CMD_FIELD_LENGTH - len(cmd)))
            L = ("0" * (LENGTH_FIELD_LENGTH - len(str(len(data))))) + str(len(data))
            M = data
            full_msg = C + DELIMITER + L + DELIMITER + M

    return full_msg


def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occurred, returns None, None
    """
    split_by_delimiter = data.split(DELIMITER)
    cmd = split_by_delimiter[0]
    msg = split_by_delimiter[-1]

    if len(split_by_delimiter) != 3:
        return None, None

    if len(split_by_delimiter[1]) != 4:
        return None, None

    try:
        if int(split_by_delimiter[1]) != len(msg):
            return None, None
    except ValueError:
        return None, None

    for char in split_by_delimiter[1]:
        if char != " ":
            if not char.isalnum():
                return None, None

    cmd = cmd.strip()

    return cmd, msg


def split_data(msg, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occurred, returns None
    """
    count_delimiters = 0
    for delimiter in msg:
        if delimiter == DATA_DELIMITER:
            count_delimiters += 1
    if count_delimiters == expected_fields:
        return msg.split(DATA_DELIMITER)
    return [None]


def join_data(msg_fields):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
    Returns: string that looks like cell1#cell2#cell3
    """
    msg = ""
    for word in msg_fields:
        msg += DATA_DELIMITER + str(word)

    return msg[1:]


def debugMessages(key):
    msg_dict = {
        "GRAPHICS_LOAD": "Loading client graphices...",
        "CONNECT": "Establishing a connection to the server...",
        "CONNECTED": "Client is successfully connected to the server.",
        "AUTHENTICATED": "Client authenticated successfully!",
        "NOT_AUTHENTICATED": "Username or Password incorrect, please try again.",
        "DISCONNECTED": "Client disconnected from the server.",
        "TIMEOUT": "There is a problem connecting to the server, please try again later.",
        "DB_CONNECT": "Establishing a connection to database...",
        "DB_CONNECTED": "Server is successfully connected to the database.",
        "DB_CONNECTION_ERROR": "Connection to database could not be established.",
        "DB_OPERATION_ERROR": "Something went wrong with the database, try again later.",
        "CLIENT_DB_CONNECT": "Checking if database is up and running...",
        "CLIENT_DB_CONNECTED": "Everything is ready!",
        "DB_UPDATE_QUERY_SUCCESS": "Database record updated successfully.",
        "DB_UPDATE_QUERY_FAIL": "Database record could not be updated.",

    }
    print(msg_dict[key])

    return msg_dict[key]
