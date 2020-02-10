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
import enum

from fereda import __version__, STDOUT


PREVIEW_IMG = '''\u001b[0m \033[1m
  _________________________________  _______
  7     77     77  _  77     77    \ 7  _  7
  |  ___!|  ___!|    _||  ___!|  7  ||  _  |
  |  __| |  __|_|  _ \ |  __|_|  |  ||  7  |
  |  7   |     7|  7  ||     7|  !  ||  |  |
  !__!   !_____!!__!__!!_____!!_____!!__!__!

  \u001b[31m||| CREATED BY EXp0s3R3b_RTH SQUAD |> v{}\n
  With the goal of making the world better...\u001b[0m \n
'''.format(__version__)


class DisplayInfo(enum.Enum):
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

    templates = {
        'info'                 :   f'{colors.get("green")}>>{colors.get("yellow")}',
        'result'               :   f'{colors.get("yellow")}>>{colors.get("green")}',
        'lattice'              :   f'{colors.get("red")}##{colors.get("green")}',
        'star_with_arrow'      :   f'{colors.get("red")}*>{colors.get("cyan")}',
        'exception'            :   f'{colors.get("cyan")}!!{colors.get("red")}',
    }

    # Info messages.
    preview_img             =   f'{PREVIEW_IMG}'
    start                   =   f'{templates.get("info")} Utility started...'
    images_searcher         =   f'{templates.get("info")} Running searcher of removed and hidden images...'
    remove_duplicates       =   f'{templates.get("info")} Removing duplicates of found images...'
    begin_restoring         =   f'{templates.get("info")} Running restore of found images...'
    restore_images_num      =   templates.get("result") + ' Summary restored' + colors.get('cyan') + ' {} ' \
                                     + colors.get('green') + 'images'
    self_destruction        =   templates.get("star_with_arrow") + colors.get('yellow') + ' Removing utility from device...'
    self_destruction_ok     =   templates.get("star_with_arrow") + colors.get('yellow') + ' Utility was successfully removed from the device.'
    elapsed_time            =   templates.get("lattice") + ' Elapsed time: ' + colors.get('cyan') + '{}' \
                                     + colors.get('reset')

    # Exceptions messages.
    no_data_to_restore      =   f'{templates.get("exception")} No data to restore. Removed or hide images not found.'
    incorrect_start_dir     =   f'{templates.get("exception")} Incorrect start directory, change current ' \
                                'directory to Android user directory.' + colors.get('reset') + '\n'

    @staticmethod
    def show_info(info=None):
        os.system('clear')

        if info:
            STDOUT.append(info)
            
        [print(msg) for msg in STDOUT]

    @staticmethod
    def add_found_data_info_to_stdout(data):
        header = "{:>7} {:>25}".format('Name','Summary')
        separator = '\u001b[0m \n' + ' ' * 3 + '-' * (len(header) - 3)
        separator1 = ' ' * 3 + '-' * (len(header) - 3)
        end_line = ' ' * 3 + '-' * (len(header) - 3) + '\n'
        
        STDOUT.append(separator)
        STDOUT.append(header)
        STDOUT.append(separator1)

        for name, data in data.items():
            STDOUT.append("   {:<18} {:>11}".format(name, len(data)))

        STDOUT.append(end_line)
