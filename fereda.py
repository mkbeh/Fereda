# -*- coding: utf-8 -*-
import os
import shutil
import argparse
import itertools as it
import collections as cs

import magic

import utils

from PIL import Image
from PIL import ImageChops


class SelfDestruction():
    pass


class DisplayInfo():
    pass


class ImagesRestore():
    def __init__(self, output_dir: str):
        self._output_dir = output_dir

        self._create_output_dir()

    def _create_output_dir(self):
        os.makedirs(self._output_dir, exist_ok=True)

    def _get_image_restore_path(self, image_obj, associated_dir_path):
        if not image_obj.path.endswith(image_obj.type):
            image_obj._replace(path=image_obj.path + image_obj.type)

        return os.path.join(
            associated_dir_path,
            image_obj.path.split('/')[-1]
        )

    def _create_associated_dir(self, associated_dir_name):
        os.makedirs(
            os.path.join(self._output_dir, associated_dir_name), 
            exist_ok=True
        )

        return os.path.join(self._output_dir, associated_dir_name)

    def restore_data(self, data_to_restore):
        print('> Restoring data...')

        for associated_dir_name, images_objs in data_to_restore.items():
            associated_dir_path = self._create_associated_dir(associated_dir_name)

            (
                shutil.move(image_obj.path, self._get_image_restore_path(image_obj, associated_dir_path))
                for image_obj in images_objs
            )   


class ImagesSearcher(ImagesRestore):
    def __init__(self, **kwargs):
        super().__init__(kwargs['output_dir'])
        self._restore_data_flag = kwargs['restore_data']
        self._default_android_point_dir = 'Android/data'

        self.default_android_data_dirs_names = (
            # Galleries parts of dirs names on various devices.
            'gallery',                                          # Samsung dir name 
            'photos',                                           # Redmi Go dir name

            # Messengers parts of dirs names.
            'telegram',
        )

        self.default_device_messengers_dirs_names = (
            'Telegram',
            'VK',
        )

        self._default_device_images_dirs = (
            'DCIM',
            'Pictures',
            'Download'
        )

        self._images_from_default_dirs = self._get_images_from_default_dirs()

    def __call__(self):
        self.search_files_handler()

    def _get_images_from_default_dirs(self):
        return it.chain(
            *(
                (file for file in self._dirs_walker(default_images_dir) if magic.from_file(file, mime=True).startswith('image'))
                for default_images_dir in self._default_device_images_dirs
            )
        )

    def _is_images_different(self, image):
        self._images_from_default_dirs, images_from_default_dirs_cp = it.tee(self._images_from_default_dirs, 2)
        image_from_filesystem = Image.open(image)

        for image_from_default_dir in images_from_default_dirs_cp:
            try:
                diff = ImageChops.difference(image_from_filesystem, Image.open(image_from_default_dir))
            except ValueError:
                continue

            if not diff.getbbox():      # Images are the same.
                return False
        else:                           # Images are different.
            return True

    def _is_images_removed(self, images):
        return [
            image for image in images if self._is_images_different(image.path)
        ]

    def _recognize_files_type(self, files):
        found_images = []
        FoundImage = cs.namedtuple('FoundImage', ['path', 'type'])

        for file in files:
            file_type = magic.from_file(file, mime=True)

            if file_type.startswith('image'):
                found_images.append(
                    FoundImage(file, file_type.split('/')[-1])
                )

        return found_images

    def _dirs_walker(self, search_directory_path):
        return (
            os.path.join(address, file)
            for address, _, files in os.walk(search_directory_path)
            for file in files
        )

    def _search_files(self, search_directory: cs.namedtuple):
        return \
        self._is_images_removed(
            self._recognize_files_type(
                self._dirs_walker(search_directory.path)
            )
        )

    def _get_default_dirs_from_device(self):
        Specific_dir = cs.namedtuple('Default_dir', ['name', 'path'])

        found_android_data_dirs = (
            Specific_dir(default_dir_name, os.path.join(self._default_android_point_dir, sub_dir))
            for sub_dir in os.listdir(self._default_android_point_dir)
            for default_dir_name in self.default_android_data_dirs_names
            if default_dir_name in sub_dir
        )

        found_device_messengers_dirs = (
            Specific_dir(default_messenger_dir, default_messenger_dir) 
            for default_messenger_dir in self.default_device_messengers_dirs_names
        )

        return it.chain(found_android_data_dirs, found_device_messengers_dirs)


    def search_files_handler(self):
        data_to_restore = filter(
            lambda x: len(*x.values()) > 0, 
            (
                {found_default_dir_from_device.name: self._search_files(found_default_dir_from_device)}
                for found_default_dir_from_device in self._get_default_dirs_from_device()
            )
        )

        if self._restore_data_flag:
            try:
                self.restore_data(
                    utils.merge_dicts_in_seq(data_to_restore)
                )
            except AttributeError:
                print('> No data to restore. Removed or hide images not found.')


def options_handler(**kwargs):
    ImagesSearcher(**kwargs)()


def cli():
    parser = argparse.ArgumentParser(prog='Fereda', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-r', '--restore-data', action='store_true')
    parser.add_argument('-s', '--self-destruction', action='store_true')
    parser.add_argument('-o', '--output-dir', default='Fereda')

    options_handler(**vars(parser.parse_args()))


if __name__ == "__main__":
    cli()
