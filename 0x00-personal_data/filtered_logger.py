#!/usr/bin/env python3
""" A module that filters logs """
import re
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
