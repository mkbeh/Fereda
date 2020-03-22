# -*- coding: utf-8 -*-
import sys
import re

import sqlalchemy as sq

from abc import ABCMeta, abstractmethod
from typing import Generator, List

from fereda.common import File, Database


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
    def _text_analysis(self, file: File, analysis_regexprs: Generator) -> None:
        re_patterns = [regex.pattern for regex in analysis_regexprs if re.search(regex, file.data)]

        if re_patterns:
            file.analysis_words, file.data = re_patterns, None
            self.result = self.input_data.file

    def _get_prepared_file_object(self) -> File:
        self.input_data.file.data = self.input_data.read_from_file()
        return self.input_data.file

    def map(self):
        file = self._get_prepared_file_object()
        analysis_regexprs = (re.compile(regex) for regex in self.cli_options.get('analysis_words'))
        self._text_analysis(file, analysis_regexprs)


class RawSqlMixin:
    @staticmethod
    def _handle_field_value(val: object, options: dict, skip_blob: bool) -> object or None:
        if isinstance(val, str) or isinstance(val, int):
            if sys.getsizeof(val) <= options.get('max_field_size'):
                return val
            else:
                return None
        else:
            if skip_blob:
                return None
            elif not skip_blob and sys.getsizeof(val) <= options.get('max_blob_size'):
                return val

    def _to_dict(self, data: List[sq.engine.result.RowProxy], options: dict) -> List[dict]:
        skip_blob = options.get('skip_blob')
        return [
            {column: self._handle_field_value(value, options, skip_blob) for column, value in rowproxy.items()}
            for rowproxy in data
        ]

    def exec_raw_sql(self, db: Database, options: dict) -> Database or None:
        engine = sq.create_engine(f'{db.name}:///{db.path}')
        with engine.connect() as conn:
            try:
                resultproxy = conn.execute(db.raw_sql)
            except sq.exc.OperationalError:
                return

            db.data = self._to_dict(resultproxy.fetchall(), options)
            return db if db.data else None


class DatabaseAnalysisMixin:
    def database_analysis(self):
        pass


class DatabasesAnalysisWorker(GenericWorker, RawSqlMixin, DatabaseAnalysisMixin):
    def _get_prepared_database_object(self) -> Database:
        database, options = self.input_data.file, self.cli_options
        database.name, database.raw_sql = options.get('db_name'), options.get('raw_sql')
        return database

    def map(self):
        database, options = self._get_prepared_database_object(), self.cli_options

        if database.raw_sql:
            self.result = self.exec_raw_sql(database, options)
            return
