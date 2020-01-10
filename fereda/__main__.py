#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import enum
import shutil
import argparse
import subprocess
import itertools as it
import collections as cs
import functools

import magic
import PIL
import imagehash

from dataclasses import dataclass
from hashlib import md5

from fereda import __version__, exceptions, decorators


# TODO: чекнуть будет ли как то влиять на память то , что вычисляется средний хэш и файловый дескриптор изображения
# не закрывается вручную (метод чека удалено ли изображение)

# TODO: add release to github


PREVIEW_IMG = PREVIEW_IMG = '''\u001b[0m
    -   -   -   -   -   -   -   -
 ***********************************
`*  ____ ____ ____ ____ ___  ____  *`
`*  |___ |___ |__/ |___ |  \ |__|  *`
`*  |    |___ |  \ |___ |__/ |  |  *`
`*                                 *` 
 """""""""""""""""""""""""""""""""""
 \u001b[31m||| CREATED BY EXp0s3R3b_RTH SQUAD |> v{}\u001b[0m \n
'''.format(__version__)

STDOUT = cs.deque()
OFF_PROGRESSBAR_FLAG = []


class SelfDestruction():
    # TODO: Написать удаление программы именно с телефона с компа не надо.
    _operation_system = subprocess.check_output(['uname', '-o']).decode('utf-8')
    
    def destruction(self):
        pass

    def destruction_handler(self):
        if self._operation_system != 'GNU/Linux':
            self.destruction()
            DisplayInfo.show_info(DisplayInfo.self_destruction_ok.value)


class DisplayInfo(enum.Enum):
    colors = {
        'yellow'    :   '\u001b[33m',
        'green'     :   '\u001b[32m',
        'black'     :   '\u001b[30m',
        'red'       :   '\u001b[31m',
        'blue'      :   '\u001b[34m',
        'magenta'   :   '\u001b[35m',
        'cyan'      :   '\u001b[36m',
        'white'     :   '\u001b[37m',
        'reset'     :   '\u001b[0m',
    }

    templates = {
        'arrow'                 :   f'{colors.get("yellow")}>>{colors.get("green")}',
        'lattice'               :   f'{colors.get("red")}##{colors.get("green")}',
        'star_with_arrow'       :   f'{colors.get("red")}*>{colors.get("cyan")}',
        'exception'             :   f'{colors.get("cyan")}!!{colors.get("red")}',
    }

    # Info messages.
    preview_img             =   f'{PREVIEW_IMG}'
    start                   =   f'{templates.get("arrow")} Utility started...'
    images_searcher         =   f'{templates.get("arrow")} Running searcher of removed and hidden images...'
    remove_duplicates       =   f'{templates.get("arrow")} Removing duplicates of found images...'
    begin_restoring         =   f'{templates.get("arrow")} Running restore of found images...'
    restore_images_num      =   templates.get("arrow") + ' Summary restored' + colors.get('cyan') + ' {} ' \
                                     + colors.get('green') + 'images'
    self_destruction        =   templates.get("star_with_arrow") + colors.get('yellow') + ' Removing utility from device...'
    self_destruction_ok     =   templates.get("star_with_arrow") + colors.get('yellow') + ' Utility was successfully removed from the device.'
    elapsed_time            =   templates.get("lattice") + ' Elapsed time: ' + colors.get('cyan') + '{}' \
                                     + colors.get('reset')

    # Exceptions messages.
    no_data_to_restore      =   f'{templates.get("exception")} No data to restore. Removed or hide images not found.'
    incorrect_start_dir     =   f'{templates.get("exception")} Incorrect start directory, change current' \
                                'directory to user directory.' + colors.get('reset') + '\n'

    @staticmethod
    def show_info(info=None):
        os.system('clear')

        if info:
            STDOUT.append(info)
            
        [print(msg) for msg in STDOUT]

    @staticmethod
    def add_found_data_info_to_stdout(data):
        header = "{:>7} {:>25}".format('Name','Summary')
        separator = '\u001b[0m \n' + ' ' * 3 + '-' * (len(header) - 3)
        separator1 = ' ' * 3 + '-' * (len(header) - 3)
        end_line = ' ' * 3 + '-' * (len(header) - 3) + '\n'
        
        STDOUT.append(separator)
        STDOUT.append(header)
        STDOUT.append(separator1)

        for name, data in data.items():
            STDOUT.append("   {:<18} {:>11}".format(name, len(data)))

        STDOUT.append(end_line)


class ImagesRestore():

    def __init__(self, output_dir: str, move_files_flag: str):
        self._output_dir = output_dir
        self._move_files_flag = move_files_flag

        self._create_output_dir()

    def _create_output_dir(self):
        os.makedirs(self._output_dir, exist_ok=True)

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
                    decorators.show_progress(STDOUT)
                
                self._move_or_copy_restored_images(image_obj.path, image_restore_path)

        DisplayInfo.show_info(
            DisplayInfo.restore_images_num.value.format(
                self._get_sum_of_restored_images(data_to_restore)
            )
        )


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


class ImagesSearcher(ImagesRestore, Image):

    def __init__(self, **kwargs):
        super().__init__(kwargs['output_dir'], kwargs['move_files'])
        self._restore_data_flag = kwargs['restore_data']
        self._self_destruction_flag = kwargs['self_destruction']
        self._default_android_point_dir = 'Android/data'

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
            'Avito'
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

    @decorators.progressbar(STDOUT, OFF_PROGRESSBAR_FLAG)
    def _is_image_removed(self, image):
        self._images_from_default_dirs, images_from_default_dirs_cp = it.tee(self._images_from_default_dirs, 2)

        cutoff = 5
        image_average_hash = imagehash.average_hash(PIL.Image.open(image.path))

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
            Default_dir(default_dir_name, os.path.join(self._default_android_point_dir, sub_dir))
            for sub_dir in os.listdir(self._default_android_point_dir)
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


def options_handler(**kwargs):
    OFF_PROGRESSBAR_FLAG.append(kwargs.get('off_progressbar'))
    ImagesSearcher(**kwargs)()


def cli():
    DisplayInfo.show_info(DisplayInfo.preview_img.value)

    start = time.time()

    parser = argparse.ArgumentParser(prog='Fereda', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-r', '--restore-data', action='store_true')
    parser.add_argument('-s', '--self-destruction', action='store_true')
    parser.add_argument('-m', '--move-files', action='store_true')
    parser.add_argument('-p', '--off-progressbar', action='store_true')                                     # It will improve performance
    parser.add_argument('-o', '--output-dir', default='DCIM/Fereda', metavar='')

    try:
        args = parser.parse_args()
        DisplayInfo.show_info(DisplayInfo.start.value)
        options_handler(**vars(args))
    except exceptions.NoDataToRestore:
        print(DisplayInfo.no_data_to_restore.value)

    DisplayInfo.show_info(
        DisplayInfo.elapsed_time.value.format(
            float('{:.3f}'.format(time.time() - start))
        )  + 's\n'
    )


if __name__ == "__main__":
    try:
        cli()
    # FIXME: not catch this exception and output error msg
    except FileNotFoundError:
        DisplayInfo.show_info(DisplayInfo.incorrect_start_dir.value)
 