#!/usr/bin/env python3
""" Regex-ing"""


from typing import List
import re
import logging
import os
import mysql.connector
import mysql.connector


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    log message obfuscated

    Args:
        fields (str): a list of strings representing all fields to obfuscate
        redaction (str): a string representing by what
        the field will be obfuscated
        message (str): a string representing the log line
        separator (str): a string representing by which character
        is separating all fields in the log line (message)
    Returns:
        the log message obfuscated:
    """
    pattern = r'({})=[^{}]*'.format('|'.join(fields), separator)
    return re.sub(pattern, lambda m: "{}={}".format(
        m.group(1), redaction), message)


def get_logger() -> logging.Logger:
    """Returns logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a streamhandler for console output
    handler = logging.StreamHandler()

    # Create and set the formatter
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to a MySQL database using credentials from env variables

    Returns:
        a connector to the database
    """
    # Retrieve database credentials from env variables
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    # Connect to the database with the credentials above
    db_connection = mysql.connector.connect(
            username=username,
            password=password,
            host=host,
            database=database
            )

    return db_connection


def main() -> None:
    """Obtain a database connection get_db and retrieve all rows in the users
    table and display each row under a filtered format
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    for row in rows:
        row_str = "; ".join(["{}={}".format(key, value)
                            for key, value in row.items()])
        logger.info(row_str)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
