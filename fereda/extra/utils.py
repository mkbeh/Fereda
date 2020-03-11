# -*- coding: utf-8 -*-
import re

import yaml


def parse_yaml(cfg_path):
    with open(cfg_path) as f:
        return yaml.safe_load(f)


def get_compiled_regex(regexpressions: list) -> list:
    compiled_regexprs = []

    for regex in regexpressions:
        try:
            r = re.compile(rf'{regex}')
        except re.error:
            raise Exception(f'Incorrect regex "{regex}". Input correct regex.')
        else:
            compiled_regexprs.append(r)

    return compiled_regexprs
