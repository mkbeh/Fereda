# -*- coding: utf-8 -*-
import sys
import re
import collections as cs

import sqlalchemy as sq

from abc import ABCMeta, abstractmethod
from typing import Generator, List, Dict, KeysView

from fereda.common import File, Database
from fereda.extra import utils


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
        not_blob_types = (str, int, bool, list, tuple, dict)
        if isinstance(val, not_blob_types):
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
        # FIXME: need to change return structure.
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
    _require_options = ('tables_names', 'columns_names', 'fields_names')
    _AnalysisData = cs.namedtuple('AnalysisData', [])

    # POTENTIAL_BUG: table may not exists columns or not exists rows.
    # NOTE: try to create class `FieldsAnalysisWorker` for use multi threading.

    @staticmethod
    def _search_matches(regexpressions: List[str], elements: KeysView):
        compiled_regexpressions = utils.get_compiled_regex(regexpressions)
        return [
            element for element in elements
            for regex in compiled_regexpressions
            if re.search(regex, element)
        ]

    @staticmethod
    def _exec_query(table, columns, connection, rows_limit):
        query = sq.select([table]).with_only_columns(columns.values()).limit(rows_limit)
        try:
            result_proxy = connection.execute(query)
        except sq.exc.OperationalError:
            return
        else:
            return result_proxy

    def _fields_analysis(self, connection, tables_with_columns: List, regexpressions: List[str], rows_limit: int):
        try:
            compiled_regexpressions = utils.get_compiled_regex(regexpressions)
        except TypeError:
            compiled_regexpressions = None

        analysis_data = []
        for table_name, table, columns in tables_with_columns:
            result_proxy = self._exec_query(table, columns, connection, rows_limit)
            if compiled_regexpressions:
                rows = [
                    row
                    for row in result_proxy
                    for regex in compiled_regexpressions
                    for field in row
                    if re.search(regex, field)
                ]
                analysis_data.append((table_name, columns.keys(), rows))
            else:
                analysis_data.append((table_name, columns.keys(), result_proxy.fetchall()))

        from pprint import pprint
        pprint(analysis_data)

    def _columns_analysis(self, tables: Dict, regexpressions: List[str]):
        tables_with_columns = []
        for table_name, table in tables.items():
            columns = {column.name: column for column in table.columns}

            if regexpressions:
                columns_matched = self._search_matches(regexpressions, columns.keys())
                columns = {column_name: column for column_name, column in columns.items() if column_name in columns_matched}

            tables_with_columns.append((table_name, table, columns))

        return tables_with_columns

    def _tables_analysis(self, metadata: sq.MetaData, regexpressions: List[str]):
        tables = metadata.tables
        if regexpressions:
            tables_matches = self._search_matches(regexpressions, tables.keys())
            tables = {table_name: table for table_name, table in tables.items() if table_name in tables_matches}

        return tables

    def _analysis_handler(self, db, options):
        tables_names_regex = options.get('tables_names')
        columns_names_regex = options.get('columns_names')
        fields_names_regex = options.get('fields_names')
        rows_limit = options.get('rows_limit')

        engine = sq.create_engine(f'{db.name}:///{db.path}')
        metadata = sq.MetaData()

        with engine.connect() as conn:
            metadata.reflect(bind=engine)

            tables = self._tables_analysis(metadata, tables_names_regex)
            if not tables:
                return

            tables_with_columns = self._columns_analysis(tables, columns_names_regex)
            result = self._fields_analysis(conn, tables_with_columns, fields_names_regex, rows_limit)

    def _is_any_require_option(self, options):
        return any(
            value for option, value in options.items() if option in self._require_options
        )

    def database_analysis(self, database, options):
        if not self._is_any_require_option(options):
            raise Exception(f'Set one of require option: {self._require_options} or use raw SQL.')

        return self._analysis_handler(database, options)


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

        self.result = self.database_analysis(database, options)
