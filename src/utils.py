# -*- coding: utf-8 -*-


def merge_dicts_in_seq(seq):
    merged_dict = None

    for i, d in enumerate(seq):
        if i == 0:
            merged_dict = d

        merged_dict.update(d)

    return merged_dict
