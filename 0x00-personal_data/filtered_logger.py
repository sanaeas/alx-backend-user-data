#!/usr/bin/env python3
""" A module that filters logs """
import re
import os
import logging
from mysql.connector.connection import MySQLConnection
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """Return the log message obfuscated"""
    for field in fields:
        message = re.sub(r"{}=[^{}]+".format(field, separator),
                         r"{}={}".format(field, redaction), message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum"""
        message = super().format(record)
        return filter_datum(self.fields,
                            self.REDACTION,
                            message,
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Create logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_db() -> MySQLConnection:
    """Return a connector to the database"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    dbname = os.getenv("PERSONAL_DATA_DB_NAME")

    return MySQLConnection(
        user=username,
        password=password,
        host=host,
        database=dbname
    )


def main():
    """Read and filter data"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()

    for row in cursor:
        logger.info("name={}; email={}; phone={}; ssn={}; password={}; \
ip={}; last_login={}; user_agent={};".format(row[0], row[1], row[2],
                                             row[3], row[4], row[5],
                                             row[6], row[7]))
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
