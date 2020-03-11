# -*- coding: utf-8 -*-
import os
import re

from abc import ABCMeta, abstractmethod
from collections import namedtuple

from fereda.extra import utils


class GenericInputData(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def generate_inputs(cls, config):
        pass


class FilesOptionsCheckerMixin:
    @staticmethod
    def _get_option_file_data(file):
        with open(file) as f:
            return [line for line in f]

    @classmethod
    def _check_option(cls, cli_options: dict, option_name: str):
        option_value = cli_options.get(option_name)

        if not option_value:
            return

        if len(option_value) == 1 and os.path.isfile(option_value[0]):
            cli_options[option_name] = utils.get_compiled_regex(cls._get_option_file_data(option_value[0]))
        else:
            cli_options[option_name] = utils.get_compiled_regex(option_value)

    @classmethod
    def check_and_prepare_options(cls, cli_options: dict):
        options_names = ('file_name', 'analysis_word', 'directories')
        for option_name in cli_options.keys():
            if option_name in options_names:
                cls._check_option(cli_options, option_name)

        return cli_options


class FilesPathInputData(GenericInputData, FilesOptionsCheckerMixin):
    __slots__ = ('path', )

    _cli_options = None

    def __init__(self, path: str):
        super().__init__()
        self.path = path

    @classmethod
    def _is_file_name_match_regex(cls, file: str) -> str:
        for file_name_regex in cls._cli_options['file_name']:
            if re.search(file_name_regex, file):
                return file

    @classmethod
    def _search_files(cls, dir_path: str, files: list):
        for file in files:
            if cls._is_file_name_match_regex(file):
                yield cls(os.path.join(dir_path, file))

    @classmethod
    def _search_files_by_directories(cls, dir_path: str, files: list):
        dir_name = dir_path.split('/')[-1]
        for directory_regex in cls._cli_options['directories']:
            if re.search(directory_regex, dir_name):
                yield from cls._search_files(dir_path, files)

    @classmethod
    def _search_files_handler(cls):
        for dir_path, _, files in os.walk(os.getcwd()):
            if cls._cli_options['directories']:
                yield from cls._search_files_by_directories(dir_path, files)
            else:
                yield from cls._search_files(dir_path, files)

    @classmethod
    def generate_inputs(cls, cli_options: dict):
        cls._cli_options = cls.check_and_prepare_options(cli_options)
        yield from cls._search_files_handler()

    def get_file_data(self):
        File = namedtuple('File', ['data', 'path'])
        return File(
            open(self.path, encoding='utf-8', errors='ignore').read(),
            self.path,
        )


class AppsPathInputData(GenericInputData):
    __slots__ = ('path', )

    def __init__(self, path):
        super().__init__()
        self.path = path

    @classmethod
    def generate_inputs(cls, cli_options: dict):
        pass
