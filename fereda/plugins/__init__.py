# -*- coding: utf-8 -*-
from fereda.plugins.searchfiles import SearchFiles
from fereda.plugins.searchappsremovedimages import SearchRemovedImages
from fereda.plugins.searchappshiddenimages import SearchHiddenImages
from fereda.plugins.textfileanalysis import TextFileAnalysis


DEFAULT_APPLICATIONS = (
    'Gallery',
    'Telegram',
    'VK',
)

DEFAULT_REGEX = (
    '.txt',
)
