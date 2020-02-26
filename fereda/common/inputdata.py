# -*- coding: utf-8 -*-
import os
import re

from abc import ABCMeta, abstractmethod
from collections import namedtuple


class GenericInputData(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def generate_inputs(cls, config):
        pass

    @staticmethod
    def parse_options(config):
        try:
            return config['applications']
        except KeyError:
            return config.get('directories', None), config['regex']


class FilesPathInputData(GenericInputData):
    __slots__ = ('path', )

    def __init__(self, path: str):
        super().__init__()
        self.path = path

    @staticmethod
    def _is_file_match_regex(file: str, regexpressions: list) -> str:
        for regex in regexpressions:
            if re.search(regex, file):
                return file

    @classmethod
    def _search_files(cls, dir_path: str, files: list, regexpressions: list):
        for file in files:
            if cls._is_file_match_regex(file, regexpressions):
                yield cls(os.path.join(dir_path, file))

    @classmethod
    def _search_files_by_directories(cls, dir_path: str, files: list, regexpressions: list, directories: list):
        dir_name = dir_path.split('/')[-1]
        if dir_name in directories:
            yield from cls._search_files(dir_path, files, regexpressions)

    @classmethod
    def _search_files_handler(cls, regexpressions: list, directories: list):
        for dir_path, _, files in os.walk(os.getcwd()):
            if directories:
                yield from cls._search_files_by_directories(dir_path, files, regexpressions, directories)
            else:
                yield from cls._search_files(dir_path, files, regexpressions)

    @classmethod
    def generate_inputs(cls, cli_options: dict):
        directories, regexpressions = cls.parse_options(cli_options)
        yield from cls._search_files_handler(regexpressions, directories)

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
        applications = cls.parse_options(cli_options)
