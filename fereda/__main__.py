#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import enum
import shutil
import argparse
import itertools as it
import collections as cs

import magic

from dataclasses import dataclass
from hashlib import md5

from fereda import exceptions

from pprint import pprint


PREVIEW_IMG = """
                               _
         .::::::::::.        -(_)====u         .::::::::::.
       .::::''''''::::.                      .::::''''''::::.
     .:::'          `::::....          ....::::'          `:::.
    .::'             `:::::::|        |:::::::'             `::.
   .::|               |::::::|_ ___ __|::::::|               |::.
   `--'               |::::::|_()__()_|::::::|               `--'
    :::               |::-o::|        |::o-::|               :::
    `::.             .|::::::|        |::::::|.             .::'
     `:::.          .::\-----'        `-----/::.          .:::'
       `::::......::::'                      `::::......::::'
         `::::::::::'                          `::::::::::'
"""

PREVIEW_IMG = '''
`7MM"""YMM `7MM"""YMM  `7MM"""Mq.  `7MM"""YMM  `7MM"""Yb.      db      
  MM    `7   MM    `7    MM   `MM.   MM    `7    MM    `Yb.   ;MM:     
  MM   d     MM   d      MM   ,M9    MM   d      MM     `Mb  ,V^MM.    
  MM""MM     MMmmMM      MMmmdM9     MMmmMM      MM      MM ,M  `MM    
  MM   Y     MM   Y  ,   MM  YM.     MM   Y  ,   MM     ,MP AbmmmqMA   
  MM         MM     ,M   MM   `Mb.   MM     ,M   MM    ,dP'A'     VML  
.JMML.     .JMMmmmmMMM .JMML. .JMM..JMMmmmmMMM .JMMmmmdP'.AMA.   .AMMA.
'''

class SelfDestruction():
    # TODO: Написать удаление программы.
    pass


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
    author                  =   '\t\t||| CREATED BY R3N3V4L TEAM |>\n'
    start                   =   f'{templates.get("arrow")} Utility started...'
    images_searcher         =   f'{templates.get("arrow")} Running searcher of removed and hidden images...'
    remove_duplicates       =   f'{templates.get("arrow")} Removing duplicates of found images...'
    begin_restoring         =   f'{templates.get("arrow")} Running restore of found images...'
    restore_images_num      =   templates.get("arrow") + ' Summary restored' + colors.get('cyan') + ' {} ' + colors.get('green')  + 'images'
    self_destruction        =   templates.get("star_with_arrow") + ' Removing utility from device...'
    elapsed_time            =   templates.get("lattice") + ' Elapsed time: ' + colors.get('cyan') + '{}' + colors.get('reset')

    # Exceptions messages.
    no_data_to_restore      =   f'{templates.get("exception")} No data to restore. Removed or hide images not found.'

    @staticmethod
    def show_found_data_info(data):
        header = "{:>7} {:>25}".format('Name','Summary')
        print('\u001b[0m \n', ' ' * 2 + '-' * (len(header) - 3))
        print(header)
        print(' ' * 3 + '-' * (len(header) - 3))

        for name, data in data.items():
            print("   {:<18} {:>11}".format(name, len(data)))

        print(' ' * 3 + '-' * (len(header) - 3), '\n')


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
                self._move_or_copy_restored_images(image_obj.path, image_restore_path)

        print(DisplayInfo.restore_images_num.value.format(
            self._get_sum_of_restored_images(data_to_restore)
        ))


@dataclass()
class Image:
    __slots__ = ('path', 'type', 'hash')
    
    path: str
    type: str
    hash: str

    def _get_file_hash(self):
        with open(self.path, 'rb') as f:
            return md5(f.read()).hexdigest()

    def __post_init__(self):
        self.hash = self._get_file_hash()

    def __eq__(self, other):
        if isinstance(other, Image):
            return self.type == other.type and self.hash == other.hash


class ImagesSearcher(ImagesRestore, Image):
    """
    TODO: add progress bar.
    
    NOTE: сравнить производительность кучи или другой структуры данных - для замена списка
    """

    def __init__(self, **kwargs):
        super().__init__(kwargs['output_dir'], kwargs['move_files'])
        self._restore_data_flag = kwargs['restore_data']
        self._default_android_point_dir = 'Android/data'

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
            'Download'
        )

        self._images_from_default_dirs = self._get_images_from_default_dirs()

    def __call__(self):
        print(DisplayInfo.images_searcher.value)
        self.search_files_handler()

    def _get_images_from_default_dirs(self):
        return it.chain(
            *(
                self._set_info_to_images(self._dirs_walker(default_images_dir))
                for default_images_dir in self._default_device_images_dirs
            )
        )

    def _is_image_removed(self, image):
        self._images_from_default_dirs, images_from_default_dirs_cp = it.tee(self._images_from_default_dirs, 2)
        results = (image == image_from_default_dir for image_from_default_dir in images_from_default_dirs_cp)

        return False if True in results else True

        

    def _delete_non_removed_images(self, images):
        return tuple(
            image for image in images if self._is_image_removed(image)
        )

    @staticmethod
    def _remove_duplicates(folder_data):
        images_jpeg, images_png = (
            {image_obj.hash: image_obj for image_obj in folder_data if image_obj.type == ext} for ext in ('jpeg', 'png')
        )
        
        return it.chain(
            images_jpeg.values(), images_png.values()
        )

    @staticmethod
    def _set_info_to_images(files):
        found_images = []

        for file in files:
            file_type = magic.from_file(file, mime=True)

            if file_type.startswith('image'):
                found_images.append(
                    Image(path=file, type=file_type.split('/')[-1], hash='')
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

        return dir_name + ' (User)'

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

        DisplayInfo.show_found_data_info(data_to_restore)

        if self._restore_data_flag:
            print(DisplayInfo.begin_restoring.value)
            self.restore_data(data_to_restore)


def options_handler(**kwargs):
    ImagesSearcher(**kwargs)()


def cli():
    os.system('clear')

    print(DisplayInfo.preview_img.value)
    print(DisplayInfo.author.value)

    start = time.time()

    parser = argparse.ArgumentParser(prog='Fereda', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-r', '--restore-data', action='store_true')
    parser.add_argument('-s', '--self-destruction', action='store_true')
    parser.add_argument('-m', '--move-files', action='store_true')
    parser.add_argument('-o', '--output-dir', default='Fereda_Data', metavar='')

    print(parser.parse_args())      # NOTE: TO REMOVE!!!!

    try:
        args = parser.parse_args()
        print(DisplayInfo.start.value)
        options_handler(**vars(args))
    except exceptions.NoDataToRestore:
        print(DisplayInfo.no_data_to_restore.value)

    print(DisplayInfo.elapsed_time.value.format(
        float('{:.3f}'.format(time.time() - start))
        ) + 's\n')

if __name__ == "__main__":
    cli()
 