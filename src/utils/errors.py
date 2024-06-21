import os
from termcolor import colored
import re
import sys

def clean_text(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    text = ansi_escape.sub('', text)
    text = re.sub(r'[\r\n\t]', ' ', text)
    return text

def error(type, message, code, stop=False):
    try:
        columns, _ = os.get_terminal_size()
    except OSError:
        columns = 80  

    message = clean_text(message)
    code = clean_text(code)

    if len(code) > 40:
        code = code[:47] + '...'

    code = "On: \x1B[3m" + code + "\x1B[23m"

    details = [
        colored(type, 'yellow', attrs=['bold']) + ": ",
        message,
        code
    ]

    max_width = columns - 4
    width = min(max(len(clean_text(detail)) for detail in details), max_width)

    top_left = '╔'
    top_right = '╗'
    bottom_left = '╚'
    bottom_right = '╝'
    horizontal = '═'
    vertical = '║'

    border_horizontal = top_left + (horizontal * (width + 2)) + top_right
    print(colored(border_horizontal, 'red'))

    for detail in details:
        clean_detail = clean_text(detail)
        if len(clean_detail) > width:
            detail = detail[:width - 3] + '...'

        print(colored(vertical + ' ', 'red'), end='')
        print(detail.ljust(width + len(detail) - len(clean_detail)), end='')
        print(colored(' ' + vertical, 'red'))

    border_horizontal = bottom_left + (horizontal * (width + 2)) + bottom_right
    print(colored(border_horizontal, 'red'))

    if stop:
        sys.exit(1)
