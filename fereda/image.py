# -*- coding: utf-8 -*-

# This file is part of Fereda.

# Fereda is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License 3 as published by
# the Free Software Foundation.

# Fereda is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Fereda.  If not, see <https://www.gnu.org/licenses/>.


# Copyright (c) 2020 January mkbeh


import os
import sys
import shutil
import itertools as it
import collections as cs

import magic
import PIL
import imagehash

from dataclasses import dataclass
from hashlib import md5

from . import decorators, exceptions, OFF_PROGRESSBAR_FLAG
from .displayinfo import DisplayInfo
from .destruction import SelfDestruction


@dataclass()
class Image:
    __slots__ = ('path', 'type', 'hash', 'avr_hash')
    
    path        : str
    type        : str
    hash        : str
    avr_hash    : imagehash.average_hash

    def _get_file_hash(self):
        with open(self.path, 'rb') as f:
            return md5(f.read()).hexdigest()

    def __post_init__(self):
        self.hash = self._get_file_hash()

    def __eq__(self, other):
        if isinstance(other, Image):
            return self.type == other.type and self.hash == other.hash


class ImagesRestore():

    def __init__(self, output_dir: str, move_files_flag: str):
        self._output_dir = output_dir
        self._move_files_flag = move_files_flag

        self.default_android_point_dir = 'Android/data'

        self._create_output_dir()

    def _create_output_dir(self):
        if 'Android' in os.listdir():
            os.makedirs(self._output_dir, exist_ok=True)
        else:
            DisplayInfo.show_info(DisplayInfo.incorrect_start_dir.value)
            sys.exit(0)

    @staticmethod
    def _get_sum_of_restored_images(data_to_restore):
        return sum(
            (len(value) for value in data_to_restore.values())
        )

    def _move_or_copy_restored_images(self, image_path, image_restore_path):
        if self._move_files_flag:
            shutil.move(image_path, image_restore_path)
        else:
            shutil.copy2(image_path, image_restore_path)

    @staticmethod
    def _get_image_restore_path(image_obj, associated_dir_path):
        image_name = ''

        if not image_obj.path.endswith(image_obj.type):
            image_name = image_obj.path + '.' + image_obj.type
        else:
            image_name = image_obj.path

        return os.path.join(
            associated_dir_path,
            image_name.split('/')[-1]
        )

    def _create_associated_dir(self, associated_dir_name):
        os.makedirs(
            os.path.join(self._output_dir, associated_dir_name), 
            exist_ok=True
        )

        return os.path.join(self._output_dir, associated_dir_name)

    def restore_data(self, data_to_restore):
        for associated_dir_name, images_objs in data_to_restore.items():
            associated_dir_path = self._create_associated_dir(associated_dir_name)

            for image_obj in images_objs:
                image_restore_path = self._get_image_restore_path(image_obj, associated_dir_path)
                
                if not OFF_PROGRESSBAR_FLAG[0]:
                    decorators.show_progress()
                
                self._move_or_copy_restored_images(image_obj.path, image_restore_path)

        DisplayInfo.show_info(
            DisplayInfo.restore_images_num.value.format(
                self._get_sum_of_restored_images(data_to_restore)
            )
        )


class ImagesSearcher(ImagesRestore, Image):

    def __init__(self, **kwargs):
        super().__init__(kwargs['output_dir'], kwargs['move_files'])
        self._restore_data_flag = kwargs['restore_data']
        self._self_destruction_flag = kwargs['self_destruction']

        self._utility_destruction = SelfDestruction()

        self.default_android_data_dirs_names = (
            # Galleries on various devices.
            'gallery',                                          # Samsung
            'photos',                                           # RedmiGo
            'camera',                                           # Micromax

            # Messaging (MMS)
            'messaging',

            # Messengers.
            'telegram',
            'vkontakte',
        )

        self.default_device_messengers_dirs_names = (
            'Telegram',
            'VK',
        )

        self._default_device_images_dirs = (
            'DCIM',
            'Pictures',
            'Download',
            'Avito',

            kwargs['output_dir']
        )

        self._images_from_default_dirs = self._get_images_from_default_dirs()

    def __call__(self):
        DisplayInfo.show_info(DisplayInfo.images_searcher.value)
        self.search_files_handler()

    def _get_images_from_default_dirs(self):

        def set_average_hash_info(img):
            img.avr_hash = imagehash.average_hash(PIL.Image.open(img.path))
            return img

        images = it.chain(
            *(
                self._set_info_to_images(self._dirs_walker(default_images_dir))
                for default_images_dir in self._default_device_images_dirs
            )
        )

        return (
            set_average_hash_info(image) for image in images
        )

    @decorators.progressbar(OFF_PROGRESSBAR_FLAG)
    def _is_image_removed(self, image):
        self._images_from_default_dirs, images_from_default_dirs_cp = it.tee(self._images_from_default_dirs, 2)

        cutoff = 5

        try:
            image_average_hash = imagehash.average_hash(PIL.Image.open(image.path))
        except OSError:
            return False

        for image_from_default_dir in images_from_default_dirs_cp:
            if image_average_hash - image_from_default_dir.avr_hash < cutoff:       # images are similar / not removed
                return False
        
        return True

    def _delete_non_removed_images(self, images):
        return tuple(
            image for image in images if self._is_image_removed(image)
        )

    @staticmethod
    def _remove_duplicates(folder_data):
        images_jpeg, images_png, images_gif = (
            {image_obj.hash: image_obj for image_obj in folder_data if image_obj.type == ext} for ext in ('jpeg', 'png', 'gif')
        )
        
        return it.chain(
            images_jpeg.values(), images_png.values(), images_gif.values()
        )

    @staticmethod
    def _set_info_to_images(files):
        found_images = cs.deque()

        for file in files:
            file_type = magic.from_file(file, mime=True)

            if file_type.startswith('image'):
                found_images.append(
                    Image(path=file, type=file_type.split('/')[-1], hash='', avr_hash=None)
                )

        return found_images

    @staticmethod
    def _dirs_walker(search_directory_path):
        return (
            os.path.join(address, file)
            for address, _, files in os.walk(search_directory_path)
            for file in files
        )

    def _search_files(self, search_directory: cs.namedtuple):
        return \
            self._delete_non_removed_images(
                self._remove_duplicates(
                    self._set_info_to_images(
                        self._dirs_walker(
                            search_directory.path
                        )
                    )
                )
            )

    def _get_default_dirs_from_device(self):
        Default_dir = cs.namedtuple('Default_dir', ['name', 'path'])

        found_android_data_dirs = (
            Default_dir(default_dir_name, os.path.join(self.default_android_point_dir, sub_dir))
            for sub_dir in os.listdir(self.default_android_point_dir)
            for default_dir_name in self.default_android_data_dirs_names
            if default_dir_name in sub_dir
        )

        found_device_messengers_dirs = (
            Default_dir(default_messenger_dir, default_messenger_dir) 
            for default_messenger_dir in self.default_device_messengers_dirs_names
        )

        return it.chain(found_android_data_dirs, found_device_messengers_dirs)

    @staticmethod
    def _rename_dir(dir_name):
        system_messengers_names = (
            'telegram', 
            'vkontakte',
        )
        user_messengers_names = (
            'Telegram', 
            'VK',
        )

        if dir_name in system_messengers_names:
            return dir_name.capitalize() + ' (System)'
        elif dir_name in user_messengers_names:
            return dir_name + ' (User)'
        else:
            return dir_name

    def search_files_handler(self):
        data_to_restore = filter(
            lambda x: len(*x.values()) > 0,
            (
                {self._rename_dir(found_default_dir_from_device.name): self._search_files(found_default_dir_from_device)}
                for found_default_dir_from_device in self._get_default_dirs_from_device()
            )
        )

        data_to_restore = cs.ChainMap(*data_to_restore)

        if not data_to_restore:
            raise exceptions.NoDataToRestore()
        
        DisplayInfo.add_found_data_info_to_stdout(data_to_restore)
        DisplayInfo.show_info()

        if self._restore_data_flag:
            DisplayInfo.show_info(DisplayInfo.begin_restoring.value)
            self.restore_data(data_to_restore)

        if self._self_destruction_flag:
            DisplayInfo.show_info(DisplayInfo.self_destruction.value)
            self._utility_destruction.destruction_handler()
