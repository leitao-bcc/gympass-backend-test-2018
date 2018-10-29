"""
functions to support log parser
"""


def split_log_line(line):
    """ Clears and divides a log line
    :param line: string
    :return: list of string
    """
    line = line.replace('\t', ' ')
    line = line.replace('\n', ' ')
    return [item for item in line.split() if item and item != '–']
