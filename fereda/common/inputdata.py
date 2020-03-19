# -*- coding: utf-8 -*-
import os
import re

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Pattern, Generator

from fereda.extra import utils


class GenericInputData(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def generate_inputs(cls, cli_options: dict):
        pass


class AppsPathInputData(GenericInputData):
    __slots__ = ('path', )

    def __init__(self, path):
        super().__init__()
        self.path = path

    @classmethod
    def generate_inputs(cls, cli_options: dict):
        pass


@dataclass(repr=False, eq=False)
class File:
    directory_data      : list      = None
    file_name           : str       = None
    analysis_words      : list      = None
    path                : str       = None
    data                : str       = None


class FilesOptionsCheckerMixin:
    @staticmethod
    def _get_option_file_data(file: str) -> list:
        with open(file) as f:
            return [line.strip().replace('\n ', '') for line in f]

    @classmethod
    def _check_option(cls, cli_options: dict, option_name: str) -> None:
        option_value = cli_options.get(option_name)

        if not option_value:
            return

        if len(option_value) == 1 and os.path.isfile(option_value[0]):
            cli_options[option_name] = utils.get_compiled_regex(cls._get_option_file_data(option_value[0]))
        else:
            cli_options[option_name] = utils.get_compiled_regex(option_value)

    @classmethod
    def check_and_prepare_options(cls, cli_options: dict) -> dict:
        options_names = ('directories', 'files_names', 'analysis_words')
        for option_name in cli_options.keys():
            if option_name in options_names:
                cls._check_option(cli_options, option_name)

        return cli_options


class FilesPathInputData(GenericInputData, FilesOptionsCheckerMixin):
    __slots__ = ('file',)

    _cli_options = None

    def __init__(self, file: File):
        super().__init__()
        self.file = file

    @classmethod
    def _match_file_name_regex(cls, file: str) -> Pattern:
        for file_name_regex in cls._cli_options['files_names']:
            if re.search(file_name_regex, file):
                return file_name_regex

    @classmethod
    def _search_files(cls, dir_path: str, files: list, directory_regex: Pattern = None) -> File:
        for file in files:
            file_name_regex = cls._match_file_name_regex(file)
            if file_name_regex:
                try:
                    directory_data = [dir_path, directory_regex.pattern]
                except AttributeError:
                    directory_data = [dir_path]

                yield cls(
                    File(
                        directory_data=directory_data,
                        file_name=file_name_regex.pattern,
                        path=os.path.join(dir_path, file)
                    )
                )

    @classmethod
    def _search_files_by_directories(cls, dir_path: str, files: list):
        dir_name = dir_path.split('/')[-1]
        for directory_regex in cls._cli_options['directories']:
            if re.search(directory_regex, dir_name):
                yield from cls._search_files(dir_path, files, directory_regex)

    @classmethod
    def _search_files_handler(cls) -> Generator[File, None, None]:
        directories = cls._cli_options['directories']

        for dir_path, _, files in os.walk(os.getcwd()):
            if directories:
                yield from cls._search_files_by_directories(dir_path, files)
            else:
                yield from cls._search_files(dir_path, files)

    @classmethod
    def generate_inputs(cls, cli_options: dict) ->  Generator[File, None, None]:
        cls._cli_options = cls.check_and_prepare_options(cli_options)
        yield from cls._search_files_handler()

    def read_from_file(self):
        return open(
            self.file.path,
            encoding='utf-8',
            errors='ignore'
        ).read()

    def read_from_db(self):
        pass
