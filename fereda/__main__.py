#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import argparse

from fereda.plugins import SearchRemovedAndHiddenImages, TextFilesAnalysis, DatabasesAnalysis, Dump
from fereda.extra.info import Info


# TODO: 0. send result data to remote server (with custom query params and zip transfer(choose pack: tar, gzip, etc)).
# TODO: 1. improve cli interface.
# TODO: 2. add groups for regex (can starts with REGEXPATTERN:)


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


def parser_base_options(parser):
    parser.add_argument('-s', '--start-point', type=str, default=os.getcwd())


def parser_base_options_analysis(parser):
    parser_base_options(parser)
    parser.add_argument('-d', '--directories', metavar='', nargs='*')
    parser.add_argument('-a', '--analysis-words', required=True, metavar='', nargs='*')

    parser.add_argument('-oJ', required=False)
    parser.add_argument('-oX', required=False)


def parser_options_files_analysis(parser):
    parser_base_options_analysis(parser)
    parser.add_argument('-f', '--files-names', metavar='', nargs='+', type=str, default=['.*'])


def parser_options_databases_analysis(parser):
    parser_base_options_analysis(parser)


def parser_options_search_images(parser):
    parser_base_options(parser)
    parser.add_argument('-m', '--applications', metavar='', nargs='*')


def parser_options_dump(parser):
    # TODO: also add dump for:
    #   - browsers cookies
    #   - browser history

    parser_base_options(parser)
    parser.add_argument('calls', metavar='calls')
    parser.add_argument('messages', metavar='messages')
    parser.add_argument('contacts', metavar='contacts')
    parser.add_argument('coordinates', metavar='coordinates')


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
