# -*- coding: utf-8 -*-
from fereda.common.pluginbase import MultiThreadingPluginBase
from fereda.common.workers import TextAnalysisWorker
from fereda.common.inputdata import FilesPathInputData


# TODO: output in csv, xml, html


class TextFileAnalysis(MultiThreadingPluginBase):
    def __init__(self, **kwargs):
        self.cli_options = kwargs

    def run(self):
        raw_result = self.custom_map(TextAnalysisWorker, FilesPathInputData, self.cli_options)

        from pprint import pprint
        pprint(list(raw_result))
