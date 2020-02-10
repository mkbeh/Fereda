# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from fereda import __version__


setup(
    name='Fereda',
    version=__version__,
    description='Cyber security tool for Android images (removed or hide) restoring.',
    author='NoName',
    platforms='linux android',
    install_requires=[
        'python-magic==0.4.15',
        'Pillow==6.2.1',
        'ImageHash==4.0',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fereda = fereda.__main__:cli'
        ]
    }
)
