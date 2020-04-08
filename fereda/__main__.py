#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import argparse

from fereda.plugins import SearchRemovedAndHiddenImages, TextFilesAnalysis, DatabasesAnalysis, Dump, DEFAULT_BROWSERS
from fereda.extra.info import Info


# TODO: 0. send result data to remote server (with custom query params and zip transfer(choose pack: tar, gzip, etc)).
# TODO: 2. add groups for regex (can starts with REGEXPATTERN:)
# TODO: 3. add errors logging (analysis db,) and options on/off logging.
# TODO: 4. improve typing.


class PluginsHandler:
    _plugins = {
        'search_images'            : SearchRemovedAndHiddenImages,
        'text_files_analysis'      : TextFilesAnalysis,
        'databases_analysis'       : DatabasesAnalysis,
        'dump'                     : Dump,
    }

    def __init__(self, **kwargs):
        self._plugin = self._plugins.get(kwargs.get('plugins'))
        self._plugin(**kwargs).run()


# --- BASE OPTIONS ---
def parser_base_options(parser):
    parser.add_argument('-p', '--start-point', type=str, default=os.getcwd())


# --- SEARCH IMAGES OPTIONS ---
def parser_options_search_images(parser):
    parser_base_options(parser)
    parser.add_argument('-a', '--applications', metavar='', nargs='*')


# --- ANALYSIS OPTIONS ---
def parser_base_options_analysis(parser):
    parser_base_options(parser)
    parser.add_argument('-d', '--directories', metavar='', nargs='*')

    parser.add_argument('-oJ', metavar='file name', required=False)
    parser.add_argument('-oX', metavar='file name', required=False)
    parser.add_argument('-oS', metavar='file name', required=False)      # NOTE: not tested yet.


def parser_options_files_analysis(parser):
    parser_base_options_analysis(parser)
    parser.add_argument('--files-names', metavar='', nargs='+', type=str, default=['.*'])
    parser.add_argument('--analysis-words', required=True, metavar='', nargs='*')


def parser_options_databases_analysis(parser):
    parser_base_options_analysis(parser)
    parser.add_argument('--db-name', metavar='', type=str, default='sqlite')
    parser.add_argument('--raw-sql', metavar='', type=str)

    parser.add_argument('--tables-names', metavar='', type=str, nargs='*')
    parser.add_argument('--columns-names', metavar='', type=str, nargs='*')
    parser.add_argument('--rows-limit', metavar='number', type=int, default=10)
    parser.add_argument('--fields-names', metavar='', type=str, nargs='*')
    parser.add_argument('--max-field-size', metavar='bytes', type=int, default=200)
    parser.add_argument('--skip-blob', action='store_true')
    parser.add_argument('--max-blob-size', metavar='bytes', type=int, default=5 * 10 ** 6)


# --- DUMP OPTIONS ---
def parser_options_dump(parser):
    parser_base_options(parser)
    parser.add_argument('calls', metavar='')
    parser.add_argument('messages', metavar='')
    parser.add_argument('contacts', metavar='')
    parser.add_argument('coordinates', metavar='')
    parser.add_argument('backups', metavar='')
    parser.add_argument('accounts', metavar='')     # EXPERIMENTAL

    parser.add_argument('--browser', metavar='', choices=DEFAULT_BROWSERS, default=DEFAULT_BROWSERS)
    parser.add_argument('browser_cookies', metavar='')
    parser.add_argument('browser_history', metavar='')


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
    parser_options_files_analysis(subparsers.add_parser(name='text_files_analysis'))
    parser_options_databases_analysis(subparsers.add_parser(name='databases_analysis'))
    parser_options_dump(subparsers.add_parser(name='dump'))

    args = parser.parse_args()
    PluginsHandler(**vars(args))


if __name__ == '__main__':
    cli()
