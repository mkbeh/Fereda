#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import argparse

from fereda.extra.info import Info
from fereda import SearchFiles, SearchRemovedImages, SearchHiddenImages, SearchHiddenFiles, TextFileAnalysis


class PluginsHandler:
    _plugins = {
        'search_files'                  : SearchFiles,
        'search_removed_images'         : SearchRemovedImages,
        'search_hidden_images'          : SearchHiddenImages,
        'search_hidden_files'           : SearchHiddenFiles,
        'text_file_analysis'            : TextFileAnalysis,
    }

    def __init__(self, **kwargs):
        self._plugin = kwargs.get('plugins')
        self._selected_plugin = self._plugins.get(self._plugin)
        self._selected_plugin(**kwargs)


def parser_options(parser):
    parser.add_argument('-r', '--regex', metavar='')
    parser.add_argument('-d', '--directories', metavar='')


def parser_options1(parser):
    parser.add_argument('-m', '--applications', metavar='')


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

    search_files = subparsers.add_parser(name='search_files')
    parser_options(search_files)
    search_removed_images = subparsers.add_parser(name='search_removed_images')
    parser_options1(search_removed_images)
    search_hidden_images = subparsers.add_parser(name='search_hidden_images')
    parser_options1(search_hidden_images)
    search_hidden_files = subparsers.add_parser(name='search_hidden_files')
    parser_options(search_hidden_files)
    text_file_analysis = subparsers.add_parser(name='text_file_analysis')
    parser_options(text_file_analysis)

    args = parser.parse_args()
    PluginsHandler(**vars(args))


if __name__ == '__main__':
    cli()
