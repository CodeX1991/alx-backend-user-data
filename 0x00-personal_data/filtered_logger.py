#!/usr/bin/env python3
""" Regex-ing"""


from typing import List
import re
import logging


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
