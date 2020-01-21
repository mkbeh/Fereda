#!/usr/bin/env python3
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


import argparse

from . import exceptions, decorators, __version__, OFF_PROGRESSBAR_FLAG
from .displayinfo import DisplayInfo
from .image import ImagesSearcher


# FIXME: bug in output statistic 


def options_handler(**kwargs):
    OFF_PROGRESSBAR_FLAG.append(kwargs.get('off_progressbar'))
    ImagesSearcher(**kwargs)()


@decorators.elapsed_time
def cli():
    DisplayInfo.show_info(DisplayInfo.preview_img.value)

    parser = argparse.ArgumentParser(prog='Fereda', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-r', '--restore-data', action='store_true')
    parser.add_argument('-s', '--self-destruction', action='store_true')
    parser.add_argument('-m', '--move-files', action='store_true')
    parser.add_argument('-p', '--off-progressbar', action='store_true')                                     
    parser.add_argument('-o', '--output-dir', default='Fereda', metavar='')

    try:
        args = parser.parse_args()
        DisplayInfo.show_info(DisplayInfo.start.value)
        options_handler(**vars(args))
    except exceptions.NoDataToRestore:
        DisplayInfo.show_info(DisplayInfo.no_data_to_restore.value)


if __name__ == "__main__":
    cli()
