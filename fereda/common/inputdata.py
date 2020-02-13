# -*- coding: utf-8 -*-
import os
import re

from abc import ABCMeta, abstractmethod


class GenericInputData(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def generate_inputs(cls, config):
        pass

    @staticmethod
    def parse_config(config):
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
    def _get_compiled_regex(cls, regexpressions: list) -> list:
        return [
            re.compile(rf'{regex}') for regex in regexpressions
        ]

    @classmethod
    def generate_inputs(cls, config: dict):
        directories, regexpressions = cls.parse_config(config)
        regexpressions = cls._get_compiled_regex(regexpressions)
        yield from cls._search_files_handler(regexpressions, directories)


class AppsPathInputData(GenericInputData):
    __slots__ = ('path', )

    def __init__(self, path):
        super().__init__()
        self.path = path

    @classmethod
    def generate_inputs(cls, config: dict):
        applications = cls.parse_config(config)