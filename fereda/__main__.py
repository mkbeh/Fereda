#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import argparse

from fereda.plugins import SearchRemovedAndHiddenImages, TextFilesAnalysis
from fereda.extra.info import Info


# TODO: 1. send data to remote server (with custom query params and zip transfer.
#       2. output in csv, xml, html
#       3. Add only patterns of regex to File obj


class PluginsHandler:
    _plugins = {
        'search_images'            : SearchRemovedAndHiddenImages,
        'text_files_analysis'      : TextFilesAnalysis,
    }

    def __init__(self, **kwargs):
        self._plugin = self._plugins.get(kwargs.get('plugins'))
        self._plugin(**kwargs).run()


def parser_base_options(parser):
    parser.add_argument('-s', '--start-point', type=str, default=os.getcwd())


def parser_options_file_analysis(parser):
    parser_base_options(parser)
    parser.add_argument('-d', '--directories', metavar='', nargs='*')
    parser.add_argument('-f', '--files-names', metavar='', nargs='+', type=str, default=['.*'])
    parser.add_argument('-a', '--analysis-words', required=True, metavar='', nargs='*')


def parser_options_search_images(parser):
    parser_base_options(parser)
    parser.add_argument('-m', '--applications', metavar='', nargs='*')


def args_checker():
    os.system('clear')
    print(Info.preview_img.value)

    try:
        sys.argv[1]
    except IndexError:
        print(Info.plugins.value)
        sys.exit(0)


def cli():
    args_checker()
    parser = argparse.ArgumentParser(prog='Fereda')
    subparsers = parser.add_subparsers(dest='plugins')

    parser_options_search_images(subparsers.add_parser(name='search_images'))
    parser_options_file_analysis(subparsers.add_parser(name='text_files_analysis'))

    args = parser.parse_args()
    PluginsHandler(**vars(args))


if __name__ == '__main__':
    cli()
