# -*- coding: utf-8 -*-
from fereda.common import File, Database
from fereda.common.pluginbase import MultiThreadingPluginBase
from fereda.common.workers import TextAnalysisWorker, DatabasesAnalysisWorker
from fereda.common.inputdata import FilesPathInputData
from fereda.common.output import OutputMixin


class TextFilesAnalysis(MultiThreadingPluginBase, OutputMixin):
    def __init__(self, **kwargs):
        kwargs['file_object'] = File
        self.cli_options = kwargs

    def run(self):
        files_objects = self.custom_map(TextAnalysisWorker, FilesPathInputData, self.cli_options)
        self.generate_output(self.cli_options, files_objects)


class DatabasesAnalysis(MultiThreadingPluginBase, OutputMixin):
    def __init__(self, **kwargs):
        kwargs['file_object'] = Database
        kwargs['files_names'] = ['.' + kwargs['db_name']]
        self.cli_options = kwargs

    def run(self):
        databases_objects = self.custom_map(DatabasesAnalysisWorker, FilesPathInputData, self.cli_options)

        from pprint import pprint
        for i in databases_objects:
            pprint(i)
            pprint(list(i.data))
            print('*' * 7)
        # self.generate_output(self.cli_options, databases_objects)
