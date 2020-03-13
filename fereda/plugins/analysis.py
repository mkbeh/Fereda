# -*- coding: utf-8 -*-
from fereda.common.pluginbase import MultiThreadingPluginBase
from fereda.common.workers import TextAnalysisWorker
from fereda.common.inputdata import FilesPathInputData
from fereda.common.output import OutputMixin


class TextFilesAnalysis(MultiThreadingPluginBase, OutputMixin):
    def __init__(self, **kwargs):
        self.cli_options = kwargs

    def run(self):
        files_objects = self.custom_map(TextAnalysisWorker, FilesPathInputData, self.cli_options)
        self.generate_output(self.cli_options, files_objects)
