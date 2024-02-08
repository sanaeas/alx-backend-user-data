#!/usr/bin/env python3
""" A module that filters logs """
import re
import logging
from typing import List


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
