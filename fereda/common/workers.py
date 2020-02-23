# -*- coding: utf-8 -*-
import re

from abc import ABCMeta, abstractmethod

from fereda.additional.text_analysis_regexpressions import TEXT_ANALYSIS_REGEXPRESSIONS


class GenericWorker(metaclass=ABCMeta):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    @abstractmethod
    def map(self):
        pass

    @classmethod
    def create_workers(cls, input_class, config):
        return (
            cls(input_data) for input_data in input_class.generate_inputs(config)
        )


class TextAnalysisWorker(GenericWorker):
    # TODO: replace tuple to namedtuple
    def map(self):
        data, file_path = self.input_data.get_file_data()

        for regex in TEXT_ANALYSIS_REGEXPRESSIONS:
            if re.search(regex, data):
                self.result = (True, file_path, regex.pattern)
