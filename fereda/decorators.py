# -*- coding: utf-8 -*-


# This file is part of Fereda.

# Fereda is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License 3 as published by
# the Free Software Foundation.

# Fereda is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Fereda.  If not, see <https://www.gnu.org/licenses/>.


# Copyright (c) 2020 January mkbeh


import os
import time

from functools import wraps

from .displayinfo import DisplayInfo, STDOUT


chars = '|/-\\'
last_char = None


def show_progress():
    global last_char

    if last_char:
        try:
            last_char = chars[chars.index(last_char) + 1]
        except IndexError:
            last_char = chars[0]
    else:
        last_char = chars[0]

    os.system('clear')
    [print(msg) for msg in STDOUT]
    print(f'\u001b[0m>> [\u001b[31m{last_char}\u001b[0m]')
        

def progressbar(off_progressbar: list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args):
            if not off_progressbar[0]:
                show_progress()
            return func(*args)

        return wrapper
    return decorator


def elapsed_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()

        DisplayInfo.show_info(
            DisplayInfo.elapsed_time.value.format(
                float('{:.3f}'.format(end - start))
            )  + 's\n'
        )

    return wrapper
