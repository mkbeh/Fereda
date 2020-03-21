# -*- coding: utf-8 -*-
import re

import sqlalchemy as sq

from abc import ABCMeta, abstractmethod
from typing import Generator


class GenericWorker(metaclass=ABCMeta):
    cli_options = None

    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    @abstractmethod
    def map(self):
        pass

    @classmethod
    def create_workers(cls, input_class, cli_options):
        if not cls.cli_options:
            cls.cli_options = cli_options

        return (
            cls(input_data) for input_data in input_class.generate_inputs(cli_options)
        )


class TextAnalysisWorker(GenericWorker):
    def _text_analysis(self, file: object, analysis_regexprs: Generator):
        re_patterns = [regex.pattern for regex in analysis_regexprs if re.search(regex, file.data)]

        if re_patterns:
            file.analysis_words, file.data = re_patterns, None
            self.result = self.input_data.file

    def _get_prepared_file_object(self):
        self.input_data.file.data = self.input_data.read_from_file()
        return self.input_data.file

    def map(self):
        file = self._get_prepared_file_object()
        analysis_regexprs = (re.compile(regex) for regex in self.cli_options.get('analysis_words'))
        self._text_analysis(file, analysis_regexprs)


class DatabasesAnalysisWorker(GenericWorker):
    # NOTE: exclude bytes , only strings

    def _database_analysis(self):
        pass

    def _exec_raw_sql(self, db):
        engine = sq.create_engine(f'{db.name}:///{db.path}')
        with engine.connect() as conn:
            result = conn.execute(db.raw_sql)

            if result.fetchone():
                self.input_data.file.data = (item for item in data.fetchall())
                return True

    def _handle_raw_sql(self, db):
        if not db.raw_sql:
            return

        data = self._exec_raw_sql(db)
        if data:
            return True

    def _get_prepared_database_object(self):
        database, options = self.input_data.file, self.cli_options
        database.name, database.raw_sql = options.get('db_name'), options.get('raw_sql')
        return database

    def map(self):
        database, options = self._get_prepared_database_object(), self.cli_options

        if self._handle_raw_sql(database):
            return
