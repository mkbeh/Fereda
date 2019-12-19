# -*- coding: utf-8 -*-
import os
import argparse
import itertools as it
import collections as cs

import magic

from PIL import Image
from PIL import ImageChops


DEFAULT_ANDROID_DATA_DIRS_NAMES = (
    # Galleries parts of dirs names on various devices.
    'gallery',                                          # Samsung dir name 
    'photos',                                           # Redmi Go dir name

    # Messengers parts of dirs names.
    'telegram',
)

DEFAULT_DEVICE_MESSENGERS_DIRS_NAMES = (
    'Telegram',
    'VK',
)


class DisplayInfo():
    pass


class FilesRestore():
    def __init__(self, output_dir: str):
        self._output_dir = output_dir

        self._create_output_dir()

    def _create_output_dir(self):
        os.makedirs(self._output_dir, exist_ok=True)

    def restore_data(self, data_to_restore):
        print('> Restoring data...')

        for data in data_to_restore:
            print(data)


class ImagesSearcher(FilesRestore):
    def __init__(self, **kwargs):
        super().__init__(kwargs['output_dir'])
        self._restore_data = kwargs['restore_data']
        self._default_android_point_dir = 'Android/data'

        self._default_images_dirs = (
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
                for default_images_dir in self._default_images_dirs
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
                    FoundImage(file, file_type)
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
            for default_dir_name in DEFAULT_ANDROID_DATA_DIRS_NAMES
            if default_dir_name in sub_dir
        )

        found_device_messengers_dirs = (
            Specific_dir(default_messenger_dir, default_messenger_dir) 
            for default_messenger_dir in DEFAULT_DEVICE_MESSENGERS_DIRS_NAMES
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

        if self._restore_data:
            self.restore_data(data_to_restore)


def options_handler(**kwargs):
    ImagesSearcher(**kwargs)()


def cli():
    parser = argparse.ArgumentParser(prog='Fereda', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-r', '--restore-data', action='store_true')
    parser.add_argument('-o', '--output-dir', default='fereda')

    options_handler(**vars(parser.parse_args()))


if __name__ == "__main__":
    cli()
