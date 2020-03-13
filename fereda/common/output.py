# -*- coding: utf-8 -*-
import ujson

from typing import Iterable
from xml.etree.ElementTree import Element, SubElement, ElementTree


class FormatBase:
    @staticmethod
    def check_extension(output_file_name: str, extension: str) -> str:
        if output_file_name.endswith(extension):
            return output_file_name

        return output_file_name + extension


class JSONMixin(FormatBase):
    @classmethod
    def to_json(cls, objects: Iterable, output_file_name: str):
        out_file = cls.check_extension(output_file_name, '.json')
        data = {
            f'object{index}': obj.__dict__
            for index, obj in enumerate(objects)
        }

        with open(out_file, "w") as file:
            ujson.dump(data, file, indent=4)


class XMLMixin(FormatBase):
    @classmethod
    def _indent(cls, elem: Element, level: int = 0):
        i = "\n" + level * "    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "    "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                cls._indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    @classmethod
    def to_xml(cls, objects: Iterable, output_file_name: str):
        out_file = cls.check_extension(output_file_name, '.xml')
        root = Element('data')

        for index, obj in enumerate(objects):
            sub_root_obj = SubElement(root, f'object{index}')

            for attr, value in obj.__dict__.items():
                if isinstance(value, list or tuple):
                    value = ' // '.join(map(str, value))

                sub_element = SubElement(sub_root_obj, attr)
                sub_element.text = value

        cls._indent(root)
        tree = ElementTree(root)
        tree.write(out_file, xml_declaration=True, encoding='utf-8', method="xml")


class OutputMixin(JSONMixin, XMLMixin):
    _output_options = {
        'oJ': JSONMixin.to_json,
        'oX': XMLMixin.to_xml,
    }

    def generate_output(self, cli_options: dict, objects: Iterable):
        for option_name, option_value in cli_options.items():
            if option_name in self._output_options.keys() and option_value:
                self._output_options.get(option_name)(objects, output_file_name=option_value)
