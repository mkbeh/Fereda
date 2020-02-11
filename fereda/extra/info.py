# -*- coding: utf-8 -*-
import enum

from fereda.const import *


class Info(enum.Enum):

    # ---- Main.
    preview_img = PREVIEW_IMG

    # ---- Colors.
    colors = {
        'yellow'    :   '\u001b[33m',
        'green'     :   '\u001b[32m',
        'black'     :   '\u001b[30m',
        'red'       :   '\u001b[31m',
        'blue'      :   '\u001b[34m',
        'magenta'   :   '\u001b[35m',
        'cyan'      :   '\u001b[36m',
        'white'     :   '\u001b[37m',
        'reset'     :   '\u001b[0m',
    }

    # ---- Input suggestion chars.
    input_char = INPUT_SUGGESTION

    # ---- Errors.

    # ---- Messages.
    plugins = PLUGINS

    def add_color(self):
        pass
