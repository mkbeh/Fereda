# coding: utf-8 -*-
from dataclasses import dataclass


@dataclass(repr=False, eq=False)
class BaseFile:
    """
    Base class of file object.

    Contains require file data.

    Attributes:
        directory_data    (list)    : stores directory path and directory regex.
        file_name_regex   (str)     : stores file name or file  name regex.
        path              (str)     : stores absolute path to file.
        data              (str)     : stores file data.
    """
    directory_data      : list      = None
    file_name_regex     : str       = None
    path                : str       = None
    data                : str       = None


@dataclass(repr=False, eq=False)
class File(BaseFile):
    """
    Contains require file data.

    Attributes:
        analysis_words  (list)      : stores words or/and its regexpressions which will be used in text analysis.

    """
    analysis_words      : list      = None


@dataclass(repr=False, eq=False)
class Database(BaseFile):
    """
    Class of database file.

    Contains require database data.

    Attributes:
        name              (str)     : name of database (ex. sqlite, mysql, oracle, etc.)
        custom_request    (str)     : stores raw SQL request.
        table_name_regex  (str)     : stores database table name or its regexpression which will be used in analysis.
        column_name_regex (str)     : stores database column name or its regexpression which will be used in analysis.
        rows_limit        (int)     : max rows limit from query of database.
        field_name_regex  (str)     : stores database field name or its regexpression which will be used in analysis.
        max_field_size    (int)     : max number of bytes for each NOT BLOB field.
        skip_blob         (bool)    : will be skipped BLOB fields from result output.
        max_blob_size     (int)     : max number of bytes for each BLOB field.
    """

    name                : str       = None
    raw_sql             : str       = None
    table_name_regex    : str       = None
    column_name_regex   : str       = None
    rows_limit          : int       = None
    field_name_regex    : str       = None
    max_field_size      : int       = None
    skip_blob           : bool      = False
    max_blob_size       : int       = None
