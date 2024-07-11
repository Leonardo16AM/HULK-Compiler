import os
from termcolor import colored
import re
import sys

def clean_text(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    text = ansi_escape.sub('', text)
    text = re.sub(r'[\r\n\t]', ' ', text)
    return text

def error(type, message, code="",line="", stop=True,verbose=True,warn=False):
    if "<error>" in message:
        return ""
    
    try:
        columns, _ = os.get_terminal_size()
    except OSError:
        columns = 80  

    color="red"
    if warn: color="yellow"

    if len(code) > 40:
        code = code[:37] + '...'

    message = clean_text(message)
    code = clean_text(code)

    
    details = [
        colored(type, 'yellow', attrs=['bold']) + ": "+message
    ]
    
    if len(line) > 0:
        details.append("On line: "+line)

    if len(code) > 0:
        details.append("Details: \x1B[3m" + code + "\x1B[23m")

        

    max_width = columns - 4
    width = min(max(len(clean_text(detail)) for detail in details), max_width)

    top_left = '╔'
    top_right = '╗'
    bottom_left = '╚'
    bottom_right = '╝'
    horizontal = '═'
    vertical = '║'

    border_horizontal = top_left + (horizontal * (width + 2)) + top_right
    
    to_print=''
    to_print+=colored(border_horizontal, color)+'\n'

    for detail in details:
        clean_detail = clean_text(detail)
        if len(clean_detail) > width:
            detail = detail[:width - 3] + '...'

        to_print+=colored(vertical + ' ', color)
        to_print+=detail.ljust(width + len(detail) - len(clean_detail))
        to_print+=colored(' ' + vertical, color)+'\n'

    border_horizontal = bottom_left + (horizontal * (width + 2)) + bottom_right
    to_print+=colored(border_horizontal, color)

    if verbose:
        print(to_print)
    else:
        return to_print

    if stop:
        sys.exit(1)
