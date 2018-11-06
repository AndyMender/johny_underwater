"""
    Utility functions for general use

    author: Andy Mender <andymenderunix@gmail.com>
    date: 2018-11-06
"""

import time


def timestamp_now():
    """Get a Unix timestamp for the current time, rounded to seconds."""

    return round(time.time())
