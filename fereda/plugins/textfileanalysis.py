# -*- coding: utf-8 -*-
from fereda.common.pluginbase import MultiThreadingPluginBase
from fereda.common.workers import TextAnalysisWorker
from fereda.common.inputdata import FilesPathInputData


class TextFileAnalysis(MultiThreadingPluginBase):
    def __init__(self, **kwargs):
        self.config = kwargs

    def run(self):
        # TODO: filter results
        result = self.custom_map(TextAnalysisWorker, FilesPathInputData, self.config)

        from pprint import pprint
        pprint(result)
