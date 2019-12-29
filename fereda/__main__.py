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

from hashlib import md5

from PIL import Image, ImageChops

from fereda import utils
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
    author                  =   '\t\t\t||| CREATED BY MKBEH TEAM |>\n'
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
            print("{:>11} {:>18}".format(name, len(data)))

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
        if not image_obj.path.endswith(image_obj.type):
            image_obj = image_obj._replace(path=image_obj.path + '.' + image_obj.type)

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
        for associated_dir_name, images_objs in data_to_restore.items():
            associated_dir_path = self._create_associated_dir(associated_dir_name)

            for image_obj in images_objs:
                image_restore_path = self._get_image_restore_path(image_obj, associated_dir_path)
                self._move_or_copy_restored_images(image_obj.path, image_restore_path)

        print(DisplayInfo.restore_images_num.value.format(
            self._get_sum_of_restored_images(data_to_restore)
        ))


class ImagesSearcher(ImagesRestore):
    """
    TODO: add progress bar.
    TODO: encode dirs names

    FIXME: also remove duplicates of images.
    Перед тем как проверять фото на различия - сначала требуется удалить дубликаты.

    NOTE: подумать , стоит ли определять типы файлов в данном классе , т.к. сравнение на различие не будет требовать Pillow
    """

    def __init__(self, **kwargs):
        super().__init__(kwargs['output_dir'], kwargs['move_files'])
        self._restore_data_flag = kwargs['restore_data']
        self._default_android_point_dir = 'Android/data'

        self.default_android_data_dirs_names = (
            # Galleries parts of dirs names on various devices.
            'gallery',                                          # Samsung dir name 
            'photos',                                           # Redmi Go dir 
            'camera',

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
        print(DisplayInfo.images_searcher.value)
        self.search_files_handler()

    def _get_images_from_default_dirs(self):
        return it.chain(
            *(
                (file for file in self._dirs_walker(default_images_dir) if magic.from_file(file, mime=True).startswith('image'))
                for default_images_dir in self._default_device_images_dirs
            )
        )

    # def _is_images_different(self, image):
    #     self._images_from_default_dirs, images_from_default_dirs_cp = it.tee(self._images_from_default_dirs, 2)
    #     image_from_filesystem = Image.open(image)

    #     for image_from_default_dir in images_from_default_dirs_cp:
    #         try:
    #             diff = ImageChops.difference(image_from_filesystem, Image.open(image_from_default_dir))
    #         except ValueError:
    #             continue

    #         if not diff.getbbox():      # Images are the same.
    #             return False
    #     else:                           # Images are different.
    #         return True

    def _is_images_different(self, image):
        pass

    def _is_images_removed(self, images):
        return [
            image for image in images if self._is_images_different(image.path)
        ]

    @staticmethod
    def _get_file_hash(filepath):
        with open(filepath, 'rb') as f:
            return md5(f.read()).hexdigest()

    def _remove_duplicates(self, folder_data):
        """
        TODO: 
        1. отсортировать по расширениям
        2. удалить дубли у каждой отдельной группы расширений
        3. вернуть обратно словарь
        """
        if not folder_data:
            return
        

        ######
        images_jpeg, imags_png = filter(lambda x: x.type == 'jpeg', folder_data), filter(lambda x: x.type == 'png', folder_data)

        # pprint(list(images_jpeg))
        # pprint(list(imags_png))
        
        ######
        add_hashes_to_imgs = lambda image: image._replace(hash=self._get_file_hash(image.path))
        images_jpeg_with_hashes, images_png_with_hashes = map(add_hashes_to_imgs, images_jpeg), map(add_hashes_to_imgs, imags_png)

        pprint(list(images_jpeg_with_hashes))
        pprint(list(images_png_with_hashes))


        print('////')

    def _recognize_files_type(self, files):
        found_images = []
        FoundImage = cs.namedtuple('FoundImage', ['path', 'type', 'hash'], defaults=(None,))

        for file in files:
            file_type = magic.from_file(file, mime=True)

            if file_type.startswith('image'):
                found_images.append(
                    FoundImage(file, file_type.split('/')[-1])
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
        images = self._recognize_files_type(self._dirs_walker(search_directory.path))

        new_images = self._remove_duplicates(images)

        # pprint(new_images)


        return images

        # return \
        # self._is_images_removed(
        #     self._recognize_files_type(
        #         self._dirs_walker(search_directory.path)
        #     )
        # )

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
        # NOTE: вообще вместо фильтрация полученных элементов попробовать в прыдущих вызовах вместо пустого словаря вернуть False или empty dict

        lst = []

        for found_default_dir_from_device in self._get_default_dirs_from_device():
            print('.......')
            print(found_default_dir_from_device)
            lst.append(
                {found_default_dir_from_device.name: self._search_files(found_default_dir_from_device)}
            )

        # for i in lst:
        #     pprint(i)

        # data_to_restore = filter(              
        #     lambda x: len(*x.values()) > 0, 
        #     (
        #         {found_default_dir_from_device.name: self._search_files(found_default_dir_from_device)}
        #         for found_default_dir_from_device in self._get_default_dirs_from_device()
        #     )
        # )


        # for i in data_to_restore:
        #     self._remove_duplicates(i)

        # data_to_restore = utils.merge_dicts_in_seq(data_to_restore)       # REPLACE TO CHAINMAP!!!!!!!! AND REMOVE UTIL!!!!! ?????

        # if not data_to_restore:
        #     raise exceptions.NoDataToRestore()

        # DisplayInfo.show_found_data_info(data_to_restore)

        # if self._restore_data_flag:
        #     print(DisplayInfo.begin_restoring.value)
        #     self.restore_data(data_to_restore)


def options_handler(**kwargs):
    ImagesSearcher(**kwargs)()


def cli():
    print(DisplayInfo.preview_img.value)
    print(DisplayInfo.author.value)

    start = time.time()

    parser = argparse.ArgumentParser(prog='Fereda', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-r', '--restore-data', action='store_true')
    parser.add_argument('-s', '--self-destruction', action='store_true')
    parser.add_argument('-m', '--move-files', action='store_true')
    parser.add_argument('-o', '--output-dir', default='Fereda_Data', metavar='')

    print(parser.parse_args())

    
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
 
