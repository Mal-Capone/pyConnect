import colorama
from colorama import Fore as _c

yellow= _c.LIGHTYELLOW_EX
green= _c.LIGHTGREEN_EX
blue= _c.LIGHTBLUE_EX
red= _c.LIGHTRED_EX
cyan= _c.LIGHTCYAN_EX
black= _c.LIGHTBLACK_EX
RESET= _c.RESET


def info(print_message, symbol='[i]', color=yellow):
    return print(f'{color}{symbol} {print_message}{_c.RESET}')

def exc(print_message, symbol='[!]', color=red):
    return print(f'{color}{symbol} {print_message}{_c.RESET}')

def ok(print_message, symbol='[+]', color=green):
    return print(f'{color}{symbol} {print_message}{_c.RESET}')

def txt(print_message, symbol='\n\t', color=cyan):
    return print(f'{color}{symbol} {print_message}{_c.RESET}')

def cyan(print_message, symbol='[i]', color=cyan):
    return print(f'{color}{symbol} {print_message}{_c.RESET}')

def blu(print_message, symbol='[i]', color=blue):
    return print(f'{color}{symbol} {print_message}{_c.RESET}')