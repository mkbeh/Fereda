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
        file = self.input_data.file
        file.data = self.input_data.read()
        analysis_regexprs = [re.compile(regex) for regex in self._cli_options.get('analysis_words')]
        re_patterns = [regex.pattern for regex in analysis_regexprs if re.search(regex, file.data)]

        if re_patterns:
            file.analysis_words, file.data = re_patterns, None
            self.result = self.input_data.file
