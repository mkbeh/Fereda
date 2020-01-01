# -*- coding: utf-8 -*-
import os

from functools import wraps


chars = '|/-\\'
last_char = None


def show_progress(stdout: list):
    global last_char

    if last_char:
        try:
            last_char = chars[chars.index(last_char) + 1]
        except IndexError:
            last_char = chars[0]
    else:
        last_char = chars[0]

    os.system('clear')
    [print(msg) for msg in stdout]
    print(f'\u001b[0m>> [\u001b[31m{last_char}\u001b[0m]')
    

def progressbar(stdout: list, off_progressbar: list):
    def decorator(func):
        wraps(func)
        def wrapper(*args):
            if not off_progressbar[0]:
                show_progress(stdout)
            return func(*args)

        return wrapper
    return decorator
