# -*- coding: utf-8 -*-
import re

from abc import ABCMeta, abstractmethod


class GenericWorker(metaclass=ABCMeta):
    _cli_options = None

    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    @abstractmethod
    def map(self):
        pass

    @classmethod
    def create_workers(cls, input_class, cli_options):
        if not cls._cli_options:
            cls._cli_options = cli_options

        return (
            cls(input_data) for input_data in input_class.generate_inputs(cli_options)
        )


class TextAnalysisWorker(GenericWorker):
    def map(self):
        file_obj = self.input_data.get_file_data()
        re_patterns = []
        for regex in self._cli_options.get('analysis_word'):
            if re.search(regex, file_obj.data):
                re_patterns.append(regex.pattern)

        if re_patterns:
            self.result = (file_obj.path, re_patterns)
