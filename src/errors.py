import os
from termcolor import colored
import re
import sys

#region print_error
def clean_ansi(texto):
    """ Elimina los códigos ANSI de una cadena para obtener su longitud visible. """
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', texto)

def error(type, message, code,stop=False):
    try:
        columnas, _ = os.get_terminal_size()
    except OSError:
        columnas = 80 

    message = message.replace('\n', ' ')
    code = code.replace('\n', ' ')

    if len(code) > 30:
        code = code[:30] + '...'

    max_ancho = columnas - 4

    detalles = [
        colored(type, 'yellow', attrs=['bold'])+": ",
        message,
        "On: \x1B[3m" + code + "\x1B[23m"
    ]

    ancho = min(max(len(clean_ansi(linea)) for linea in detalles), max_ancho)

    esquina_sup_izq = '╔'
    esquina_sup_der = '╗'
    esquina_inf_izq = '╚'
    esquina_inf_der = '╝'
    horizontal = '═'
    vertical = '║'

    borde_horizontal = esquina_sup_izq + (horizontal * (ancho + 2)) + esquina_sup_der
    print(colored(borde_horizontal, 'red'))

    for detalle in detalles:
        texto_limpio = clean_ansi(detalle)
        if len(texto_limpio) > ancho:
            detalle = detalle[:ancho - 3] + '...'

        print(colored(vertical + ' ', 'red'), end='')
        print(detalle.ljust(ancho + len(detalle) - len(texto_limpio)), end='')
        print(colored(' ' + vertical, 'red'))

    borde_horizontal = esquina_inf_izq + (horizontal * (ancho + 2)) + esquina_inf_der
    print(colored(borde_horizontal, 'red'))

    if stop:
        sys.exit(1)


