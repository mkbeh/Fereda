#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

from . import exceptions, decorators, OFF_PROGRESSBAR_FLAG
from .displayinfo import DisplayInfo
from .image import ImagesSearcher


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
